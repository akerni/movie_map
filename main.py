"""
The module creates a web map (html page).
The web map displays information about the locations of films that were shot
in a given year. Location information is in the locations.list file.
The user indicates for the films for which year he wants to build a map and
his location as latitude and longitude (e.g. 49.83826,24.02324), and as a
result receives an HTML file.

The map has three layers (label layer, main layer).
The map should show no more than 10 labels of the nearest filming locations.
Link to github:
https://github.com/akerni/movie_map
"""

import folium
from folium import plugins
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic
from math import inf
import re
import json


def get_data(path: str) -> dict:
    """
    Function reads the ddta from the source file.
    Reads data from the locations.txt file and returns it as:
    {year: {movie_name: [(location, description, ...], ...}}
    """
    file_raw = [x.strip() for x in open('{}'.format(path), 'r', encoding='utf-8').readlines()]
    file_raw = file_raw[file_raw.index('==============') + 1:]

    file_data = {}

    for line in file_raw:
        try:
            curr_date = (re.search(r'\(\d{1,4}\)', line).group(0)[1:-1])
        except AttributeError:
            continue

        split_line = line.split("\t")
        curr_key = split_line[0].strip('# ').replace("(" + curr_date + ")", "").strip()
        curr_info = [x for x in split_line[1:] if x != '']

        if curr_date in file_data.keys():
            if curr_key in file_data[curr_date].keys():
                file_data[curr_date][curr_key].append(tuple(curr_info))
            else:
                file_data[curr_date].update({
                    curr_key: [tuple(curr_info)]
                })
        else:
            file_data.update({
                curr_date: {curr_key: [tuple(curr_info)]}
            })
    return file_data


def print_data(data: dict):
    for key, val in data.items():
        print(key, val)


def evaluate_movie(data: dict, user_year: str, user_cords: list):
    """
    The function finds the closest to the user 10 places where movies wer
    shot. Returns the movie dictionary as:
    - [(location, (length, latitude), movie_name, description), ...]
    """
    def get_cords(place: str):
        """
        The function is named location and returns a tuple with location
        coordinates. If no coordinates are found for the full name of the
        location, then there is a narrower search for it
        Example: 'Melrose Lumber, Ossining, New York, USA' - not found,
        search for 'Ossining, New York, USA'
        """
        place_location = None
        geolocator = Nominatim(user_agent="user_agent")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)
        step_indexes = [0] + [i + 1 for i, ltr in enumerate(place) if ltr == ',']

        for step in step_indexes:
            place_location = geolocator.geocode("{}".format(place))
            if not place_location:
                place = place[step:]

        if place_location is None:
            return
        return place_location.latitude, place_location.longitude

    print('Finding nearest places...')

    year_movies = data.get(user_year)
    if not year_movies:
        print('Sorry, no movies by that year was found!')
        return None

    movie_locations = []
    for movie in year_movies.keys():

        for info in year_movies[movie]:

            curr_place = info[0]
            if len(info) == 2:
                curr_description = info[1]
                location = get_cords(curr_place)
                movie_locations.append((curr_place, location, movie, curr_description))

            else:
                location = get_cords(curr_place)
                movie_locations.append((curr_place, location, movie))

            if location is None:
                continue

        min_distance = inf
        min_idx = 0
        step = 0
        while len(movie_locations) > 10:
            if step > 100:
                break
            try:
                for idx_block, block in enumerate(movie_locations):
                    if min_distance > geodesic(block[1], user_cords):
                        min_distance = geodesic(block[1], user_cords)
                        min_idx = idx_block
                movie_locations.pop(min_idx)
            except IndexError:
                break
            step += 1
    return movie_locations


def render_html(data: list, user_cords: list, user_year: str):
    """
    Function generates the HTML file with the list of the movies found.
    """
    print('Creating map...')

    def get_local(_cords: list):
        """
        The function gets the coordinates of the location and returns its
        full name.
        """
        geolocator = Nominatim(user_agent="user_agent")
        location = geolocator.reverse("{}, {}".format(_cords[0], _cords[1]))
        return location.address

    def country_count(lst: list) -> dict:
        """
        The function returns the number of locations that were captured in a
        particular country. Returns data as a dictionary, where
        {country_name: number_of_shoots, ...}
        """
        result = {}
        for tpl in lst:
            curr_country = tpl[0].split(", ")[-1]
            if curr_country in result.keys():
                result[curr_country] += 1
            else:
                result.update({
                    curr_country: 1
                })

        return result

    def update_json(dct: dict):
        """
        The function creates a new .json file with updated data on the number
        of shots in a particular country.
        """
        data_json = json.load(open('world.json', 'r', encoding='utf-8-sig'))
        check_dct = dct.copy()

        for i in range(len(data_json['features'])):
            current_country = data_json['features'][i]['properties']
            alias = " ".join((
                str(current_country['NAME']),
                str(current_country['ISO3']).replace("None", ""),
                str(current_country['FIPS']).replace("None", "")
            ))
            for country in check_dct.keys():
                if alias.find(country) != -1:
                    add_country = country
                    check_dct.pop(country)
                    break
            else:
                add_country = None

            if add_country:
                data_json['features'][i]['properties'].update({
                    'COUNT': dct[add_country]
                })
            else:
                data_json['features'][i]['properties'].update({
                    'COUNT': 0
                })

        json_object = json.dumps(data_json)
        with open('world_2.json', 'w') as outfile:
            outfile.write(json_object)

    html_map = folium.Map(location=user_cords)
    all_subs = folium.FeatureGroup(name="All info")

    counts = country_count(data)
    update_json(counts)
    fg_places = plugins.FeatureGroupSubGroup(group=all_subs, name="Places")
    for info in data:

        place = info[0]
        cords = info[1]
        movie_name = info[2]
        description = None

        if len(info) == 4:
            description = info[3]

        fg_places.add_child(folium.Marker(
            location=cords,
            popup="{}\n{}\n{}".format(movie_name, place, description).replace('None', ""),
            icon=folium.Icon()
        ))

    fg_user = plugins.FeatureGroupSubGroup(group=all_subs, name='User')
    fg_user.add_child(folium.CircleMarker(
        location=tuple(user_cords),
        radius=10,
        popup=get_local(user_cords),
        color='green',
        fill_opacity=0.5,
    ))

    fg_counts = plugins.FeatureGroupSubGroup(group=all_subs, name='Colors')

    fg_counts.add_child(folium.GeoJson(data=open('world_2.json', 'r', encoding='utf-8-sig').read(),
                                       style_function=lambda x: {
                                           'fillColor': 'white' if
                                           x['properties']['COUNT'] == 0
                                           else 'yellow' if 0 < x['properties']['COUNT'] < 3
                                           else 'green'
                                       }
                                       ))

    html_map.add_child(all_subs)
    html_map.add_child(fg_places)
    html_map.add_child(fg_user)
    html_map.add_child(fg_counts)

    folium.LayerControl(collapsed=False).add_to(html_map)

    map_name = "{}__movies_map.html".format(user_year)
    html_map.save(map_name)
    print(f'Finished. Please have a look at the map {map_name}')


def main():
    """
    The main function of the module.
    Processes the entered data: user coordinates and year.
    Throws out errors at invalid inputs.
    Invokes further leading functions of the render_html, evaluate_movie module
    """
    g_data = get_data('locations.txt')
    user_year = input('Please enter a year you would like to have a map for: ')
    if not user_year.isdigit() or int(user_year) < 1947:
        raise ValueError('Invalid year')

    cords = input('Please enter your location in latitude-longitude order '
                  '(example -> 49.83826, 24.02324): ').strip().split(", ")
    try:
        for el in cords:
            float(el)
    except ValueError:
        raise ValueError('Invalid input')

    # test_year = '1998'
    # test_cords = [49.83826, 24.02324]

    movies = evaluate_movie(g_data, user_year, cords)
    render_html(movies, cords, user_year)


if __name__ == '__main__':
    main()
