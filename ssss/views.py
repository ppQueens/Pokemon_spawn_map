from django.shortcuts import render

from .config_parser import get_gmaps_api_key
import os
import random
import string

def show_map(request):
    api_key = get_gmaps_api_key()
    file_dir = os.path.join('spawns_map', 'static')

    random_string = ''.join(random.choice(string.ascii_letters) for i in range(7))
    link = os.environ['LINK_TO_XML']

    return render(request, template_name='map.html', context={'api_key': api_key, 'link': link})
