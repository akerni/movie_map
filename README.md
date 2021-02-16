# movie_map
3 layers are created on the map, namely:
1. The main layer of the map
2. Layer of placemarks and current user position
3. Coloring layer of countries.

Tags have a movie name and a full location name.
The last layer is determined by the number of shooting locations in a particular country (0 - gray, 1-3 - yellow, more - green.)
The last layer is selective, which had to be added by a third of the task.
# 
# example
User should run main.py module
Then they get the message to imput year and geolocation:

Please enter a year you would like to have a map for: 2000

Please enter your location in latitude-longitude order (example -> 49.83826 24.02324): 52.494477 13.441307
Finding nearest places...
Creating map...
Finished. Please have a look at the map 2000__movies_map.html
