import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pokemon_spawn_map.settings')

app = Celery('Pokemon_spawn_map')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_pokemon_spawn_map_over_10_minutes': {
        'task': 'spawns_map.tasks.update_kml_layer',
        'schedule': 1200,
    },
    'update_pokemon_spawn_db': {
        'task': 'spawns_map.tasks.update_pokemon_spawn_db',
        'schedule': 600,
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
