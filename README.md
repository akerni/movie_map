# General information about the module
The module creates a web map (html page).
The web map displays information about the locations of films that were shot
in a given year. Location information is in the locations.list file.
Modul reads data from the locations.txt file and returns it as:
    {year: {movie_name: [(location, description, ...], ...}}
Module finds the closest to the user 10 places where movies wer
    shot. Returns the movie dictionary as:
    - [(location, (length, latitude), movie_name, description), ...]
If no coordinates are found for the full name of the
        location, then there is a narrower search for it
        Example: 'Melrose Lumber, Ossining, New York, USA' - not found,
        search for 'Ossining, New York, USA'
Module generates the HTML file with the list of the movies found.

# What the map provide:
3 layers are created on the map, namely:
1. The main layer of the map
2. Layer of placemarks and current user position
3. Coloring layer of countries.

Tags have a movie name and a full location name.
The last layer is determined by the number of shooting locations in a particular country (0 - gray, 1-3 - yellow, more - green.)
The last layer is selective, which had to be added by a third of the task.

# Example of module processing
User should run main.py module
Then they get the message to imput year and geolocation:

Please enter a year you would like to have a map for: 2000

Please enter your location in latitude-longitude order (example -> 49.83826 24.02324): 52.494477 13.441307
Finding nearest places...
Creating map...
Finished. Please have a look at the map 2000__movies_map.html

# Structure of an html file
1) An HTML document has two main parts: the head and the body.
These tags are of the form:
<html> - appears at the beginning of your document.
</html> - appears at the end of your document.
The region associated with the BODY of a document ші declared using the following HTML tags:
<body> - appears after the </head> definition.
</body> - appears after the document's text but before the </html> tag.
2) The <meta> tag defines metadata about an HTML document:
<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
3) The <style> tag is used to define style information (CSS) for a document.
Inside the <style> element you specify how HTML elements should render in a browser.
<style>html, body {width: 100%;height: 100%;margin: 0;padding: 0;}</style>
4) Module writes script code directly into the HTML document. Script code is placed in  the document using <script> tag.
  Most of the file are java-script functions and geo coordinates.
5) The <link> tag defines the relationship between the current document and an external resources (in this case css files):
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>
  
  
