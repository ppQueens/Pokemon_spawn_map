from django.shortcuts import render, HttpResponse
from .models import PokemonSpawn, NestMigrations

from .config_parser import get_gmaps_api_key
from .tasks import update_migration_date
from .utils.google_storage import download_xml


def show_map(request):
    nxt = NestMigrations.objects.get_last_datetime()
    if not nxt:
        nxt = update_migration_date()

    api_key = get_gmaps_api_key()
    PokemonSpawn.objects.filter(on_map=True)
    return render(request, template_name='map.html', context={'api_key': api_key,
                                                              'file': 'poke_spawn_test.xml',
                                                              'next_migration_date': nxt.strftime(
                                                                  "%Y-%m-%dT%H:%M:%SZ")})


def proxy(request):
    xml = download_xml(request.GET['url'])
    return HttpResponse(xml, content_type='text/xml')
