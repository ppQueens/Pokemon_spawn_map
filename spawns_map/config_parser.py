from configparser import ConfigParser

__config = ConfigParser()
__config.read('spawns_map/config.ini')
if not __config.sections():
    raise FileNotFoundError('Check existence of your config file')


def get_gmaps_api_key():
    return __config['google-maps-js']['api_key']
