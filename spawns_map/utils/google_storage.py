import os
from requests.exceptions import HTTPError
from google.cloud import storage


class GoogleStorage:
    file_name = 'poke_spawn_test.xml'

    def __init__(self, file_name=None):
        if file_name:
            self.file_name = file_name
        self.client = storage.Client.from_service_account_json(os.path.join('spawns_map', 'g.json'))
        self.bucket = self.client.get_bucket('pokemon-xmls')
        self.blob = self.bucket.blob(self.file_name)

    def upload(self, iofile):
        try:
            self.blob.upload_from_string(iofile)
            print(f'UPLOADED {self.file_name} to GoogleStorage')
        except Exception as e:
            # log
            print(e)

    def download(self, name=file_name, bts=True):
        str_b = None
        try:
            if bts:
                str_b = self.blob.download_as_string()
            else:
                self.blob.download_to_filename(name)
            print(f'DOWNLOADED {name} from GoogleStorage')

        except Exception as e:
            # log
            print(f'Google.downloading error occurred: {e}')
        return str_b


def download_xml(file_name):
    response = b'''<?xml version="1.0" encoding="UTF-8"?>
                <Error>
                    <Description>smth goes wrong :(</Description>
                </Error>
            '''
    try:
        response = GoogleStorage(file_name=file_name).download() or response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return response
