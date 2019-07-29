from django.shortcuts import render

from .config_parser import get_gmaps_api_key


def show_map(request):
    api_key = get_gmaps_api_key()
    return render(request, template_name='map.html', context={'api_key': api_key})
