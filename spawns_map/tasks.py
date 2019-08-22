from Pokemon_spawn_map.celery import app

#not working on heroku
def update_kml_layer():
    from .kml import build_kml
    from .models import PokemonSpawn

    pokemon_spawns = PokemonSpawn.objects.spawns_data()
    if pokemon_spawns:
        build_kml(pokemon_spawns, "poke_spawn_test")

        # r = requests.get(upload_to_aws(file_path))
        #
        # with open('spawns_map/static/poke_spawn_test.xml', 'wb') as f:
        #     f.write(r.content)

        print("poke_spawn_test has been created")
    else:
        print("poke_spawn_test has NOT been created")

@app.task
def update_pokemon_spawn_db():
    from geopy.distance import distance
    from .models import PokemonSpawn

    new_nests = PokemonSpawn.objects.filter(on_map=False, confirming_spawn=False)
    print(new_nests.query)
    print(new_nests)
    for nest in new_nests:
        pokemon = nest.pokemon
        country = nest.country
        state = nest.state
        city = nest.city

        nest_point = nest.lat, nest.lon
        nests_on_map = PokemonSpawn.objects.filter(pokemon_id=pokemon.id, country=country, state=state,
                                                   city=city, on_map=True, confirming_spawn=False)
        match = False
        print(nests_on_map)
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