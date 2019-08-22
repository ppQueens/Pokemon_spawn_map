from Pokemon_spawn_map import settings
import os

from simplekml import Kml


def build_kml(data_list, file_name):
    kml = Kml()
    if __name__ == '__main__':
        file_path = os.path.join('static', f'{file_name}.xml')
    else:
        file_dir = os.path.join('spawns_map', 'static')
        # onlyfiles = [f for f in os.listdir(file_dir) if
        #              os.path.isfile(os.path.join(file_dir, f)) and f.split('.')[1] == 'xml']
        # for file in onlyfiles:
        #     print(f'deleting {file}')
        #     os.remove(os.path.join(file_dir, file))
        # for f in os.listdir(file_dir):
        #     print(f)
        # print(onlyfiles)
        # if onlyfiles:
        #     file_name = onlyfiles[0]
        file_path = os.path.join(file_dir, f'{file_name}.xml')

    for spawn in data_list:
        # swap coordinates for google maps api
        point = kml.newpoint(name=spawn['pokemon_name'], coords=[spawn['coordinates'][::-1]])
        point.style.iconstyle.icon.href = \
            ''.join(('/static/pokemons_images/', spawn['pokemon_name'].lower(), '.png'))
        point.style.iconstyle.scale = 3
    print(f"CURRENT DIRECTORY is {os.getcwd()}")
    kml.save(file_path)
    # out = kml._genkml(True)
    # f = open(os.path.join('/tmp', f'{file_name}.xml'), 'w')
    # try:
    #     f.write(out)
    # finally:
    #     f.close()
    # os.system('touch test.txt')
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
