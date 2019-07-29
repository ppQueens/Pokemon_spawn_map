from Pokemon_spawn_map import settings
import os

from simplekml import Kml


def build_kml(data_list, file_name):
    kml = Kml()
    if __name__ == '__main__':
        file_path = os.path.join('static', f'{file_name}.xml')
    else:
        file_path = os.path.join('spawns_map', 'static', f'{file_name}.xml')

    for spawn in data_list:
        # swap coordinates for google maps api
        point = kml.newpoint(name=spawn['pokemon_name'], coords=[spawn['coordinates'][::-1]])
        point.style.iconstyle.icon.href = \
            ''.join((f'http://{settings.HOST}:{settings.PORT}', '/static/pokemons_images/', spawn['pokemon_name'], '.png'))
        point.style.iconstyle.scale = 3
    kml.save(file_path)
    return file_path


#
# data_list = [
#     {
#         'pokemon_name': 'Bulbasaur',
#         'coordinates': (46.850011, 35.376347),
#     },
#     {
#         'pokemon_name': 'Charmander',
#         'coordinates': (46.270011, 35.176347),
#     },
#     {
#         'pokemon_name': 'Pikachu',
#         'coordinates': (46.450011, 35.876347),
#     }
# ]

# build_kml(data_list, 'test')
