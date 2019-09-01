import os
import io

from simplekml import Kml


def build_kml(data_list, file_name=None, path=None):
    kml = Kml()

    for spawn in data_list:
        # swap coordinates for google maps api
        point = kml.newpoint(name=spawn['pokemon_name'],
                             description=f'Added {spawn["created"]}\nConfirmed: {spawn["confirmed"]}',
                             coords=[spawn['coordinates'][::-1]])
        point.style.iconstyle.icon.href = \
            ''.join(('/static/pokemons_images/', spawn['pokemon_name'].lower(), '.png'))
        point.style.iconstyle.scale = 3

    if file_name:
        if __name__ == '__main__':
            file_path = os.path.join(path or 'static', f'{file_name}.xml')
        else:
            print(os.getcwd())
            file_dir = path or os.path.join('spawns_map', 'static')
            file_path = os.path.join(file_dir, f'{file_name}.xml')
        kml.save(file_path)
        return file_path

    iokml = io.BytesIO(bytes(kml.kml(), 'utf-8')).read()
    return iokml
