from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .models import PokemonSpawn
from .kml import build_kml


@shared_task
def update_kml_layer():
    pokemon_spawns = PokemonSpawn.objects.spawns_data()
    if pokemon_spawns:
        build_kml(pokemon_spawns, 'poke_spawn_test')
        print("poke_spawn_test has been created")
    else:
        print("poke_spawn_test has NOT been created")


