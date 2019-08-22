from django.db import models
from pytz import timezone

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

    def filter(self, *args, **kwargs):
        self._filtered = super().filter(*args, **kwargs)
        return self._filtered

    def spawns_data(self):
        data_list = []

        spawns_objects = self._filtered if self._filtered is not None else self.get_queryset().all()
        for spawn in spawns_objects:
            dt = spawn.created
            tz = timezone(spawn.time_zone)
            spawn_data = {
                'pokemon_name': spawn.pokemon.pokemon_name,
                'coordinates': (spawn.lat, spawn.lon),
                'created': '{} {}'.format(dt.astimezone(tz).strftime("%d/%m/%Y, %H:%M:%S"), spawn.time_zone),
                'confirmed': spawn.confirmed
                # 'image_path': spawn.pokemon.pokemon_image_path.path
            }
            data_list.append(spawn_data)
        return data_list


class PokemonSpawn(TimeStampedModel):
    objects = SpawnsDataManager()

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    checked = models.BooleanField(default=False, null=True)
    legacy = models.BooleanField(default=False, null=True)
    migration_number = models.IntegerField(default=0, null=True)
    time_zone = models.CharField(max_length=100, default='UTC')
    confirming_spawn = models.BooleanField(default=False)
    confirmed = models.IntegerField(default=0)
    on_map = models.BooleanField(default=False)
    country = models.CharField(max_length=300, default='')
    state = models.CharField(max_length=300, default='')
    city = models.CharField(max_length=300, default='')