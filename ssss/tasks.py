from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os

from . import s3_upload

from .models import PokemonSpawn
from .kml import build_kml


@shared_task
def update_kml_layer():
    pokemon_spawns = PokemonSpawn.objects.spawns_data()
    if pokemon_spawns:
        # file_name = ''.join(random.choice(string.ascii_letters) for i in range(14))
        file_path = build_kml(pokemon_spawns, "poke_spawn_test")
        url = s3_upload.upload_to_aws(file_path)
        if url:
            os.environ['LINK_TO_XML'] = url
        print(file_path)
        with open(file_path) as file:
            print(file.read())
        print("poke_spawn_test has been created")
    else:
        print("poke_spawn_test has NOT been created")


