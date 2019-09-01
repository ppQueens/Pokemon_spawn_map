import requests
from bs4 import BeautifulSoup

# url = 'http://nestmigration.com/'
# html_page = requests.get(url).content
#
# soup = BeautifulSoup(html_page, 'html.parser')
soup = None
import re


def get_pokemons_names():
    scripts = soup.find('script', type='text/javascript')
    # all_pokemon_name = all_infocards.find_all('a', class_='ent-name')
    # for i in scripts:
    # print(i)
    return re.findall(r'Date\((.*)\)', scripts.text)[0].strip()


# z = get_pokemons_names()
# print(z)

from google.cloud import storage
import os


path = os.path.join('her', 'spawns_map', 'g.json')
storage_client = storage.Client.from_service_account_json(path)

bucket = storage_client.get_bucket('pokemon-xmls')
blob = bucket.blob('poke_spawn_test.xml')

fp = os.path.join('HEREWEGO.xml')
blob.download_to_filename(fp)

print("OK!")


