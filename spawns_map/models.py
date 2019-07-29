from django.db import models


# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Pokemon(TimeStampedModel):
    pokemon_name = models.CharField(max_length=100)
    pokemon_image_path = models.ImageField(upload_to='pokemons')


class SpawnsDataManager(models.Manager):
    _filtered = None

    # TODO
    # посмотреть, что возвращает get_queryset после вызова стандартного filter,
    # возможно, что это queryset c УЖЕ отфильтрованными обьектами,  и следовательно
    # кастомный filter не нужен
    def filter(self, *args, **kwargs):
        filtered = super().filter(*args, **kwargs)
        return filtered

    def spawns_data(self):
        data_list = []

        spawns_objects = self._filtered if self._filtered is not None else self.get_queryset().all()
        for spawn in spawns_objects:
            spawn_data = {
                'pokemon_name': spawn.pokemon.pokemon_name,
                'coordinates': (spawn.lat, spawn.lon),
                # 'image_path': spawn.pokemon.pokemon_image_path.path
            }
            data_list.append(spawn_data)
        return data_list


class PokemonSpawn(TimeStampedModel):
    objects = SpawnsDataManager()

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    checked = models.BooleanField(default=False)
    legacy = models.BooleanField(default=False)
    migration_number = models.IntegerField()
