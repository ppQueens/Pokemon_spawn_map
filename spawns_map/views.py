
from django.shortcuts import render
from .models import PokemonSpawn
from .config_parser import get_gmaps_api_key
from .kml import build_kml


def show_map(request):
    api_key = get_gmaps_api_key()
    PokemonSpawn.objects.filter(on_map=True)
    pokemon_spawns = PokemonSpawn.objects.spawns_data()
    # print(pokemon_spawns)
    if pokemon_spawns:
        path = build_kml(pokemon_spawns, 'poke_spawn_test')
        print(path)
    return render(request, template_name='map.html', context={'api_key': api_key, 'file': 'poke_spawn_test.xml'})
