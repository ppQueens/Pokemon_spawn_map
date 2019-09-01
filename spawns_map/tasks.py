from Pokemon_spawn_map.celery import app
from celery.signals import task_success


@app.task
def update_kml_layer():
    from .utils.kml import build_kml
    from .models import PokemonSpawn
    from .utils.google_storage import GoogleStorage
    pokemon_spawns = PokemonSpawn.objects.spawns_data()
    if pokemon_spawns:
        GoogleStorage().upload(build_kml(pokemon_spawns))

        print("poke_spawn_test has been created")
    else:
        print("poke_spawn_test has NOT been created")


@app.task
def update_pokemon_spawn_db():
    from geopy.distance import distance
    from .models import PokemonSpawn

    new_nests = PokemonSpawn.objects.filter(on_map=False, confirming_spawn=False)
    for nest in new_nests:
        pokemon = nest.pokemon
        country = nest.country
        state = nest.state
        city = nest.city

        nest_point = nest.lat, nest.lon
        nests_on_map = PokemonSpawn.objects.filter(pokemon_id=pokemon.id, country=country, state=state,
                                                   city=city, on_map=True, confirming_spawn=False)
        match = False
        for n_m in nests_on_map:
            n_m_point = n_m.lat, n_m.lon

            if distance(nest_point, n_m_point).meters <= 15:
                n_m.confirmed += 1
                n_m.save()
                nest.confirming_spawn = True
                nest.save()
                match = True
                break

        if not match:
            nest.on_map = True
            nest.save()
    print('Everthing is ok!')


@app.task
def update_migration_date():
    import requests
    import re
    from bs4 import BeautifulSoup
    from datetime import datetime
    from .models import NestMigrations

    url = 'http://nestmigration.com/'
    response = requests.get(url)
    script = BeautifulSoup(response.content, 'html.parser').find('script', type='text/javascript')

    res = re.findall(r'Date\((.*)\)', (lambda: script and script.text)() or '')
    if res:
        dt = datetime.strptime(res[0].strip("'"), "%Y-%m-%dT%H:%M:%SZ")
        NestMigrations.objects.create(next_m_date=dt)

    else:
        return
    return dt


@task_success.connect(sender=update_migration_date)
@app.task
def countdown(sender=None, result=None, conf=None, **kwargs):
    from .models import NestMigrations
    from django.utils import timezone

    next_migration_date = NestMigrations.objects.get_last_datetime()
    if not next_migration_date:
        next_migration_date = update_migration_date.run()

    if next_migration_date:
        total_seconds = (next_migration_date - timezone.now()).total_seconds() + 60
        update_migration_date.apply_async(countdown=total_seconds)
    else:
        return False
    return True


# @worker_ready.connect
# def f(sender=None, conf=None, **kwargs):
    # countdown.run()

