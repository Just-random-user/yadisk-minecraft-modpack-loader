#test
import requests
import json
import os
import utils
import platform
from urllib.parse import urlencode

def download_new(url, public_key, path, target_directory, mods_to_download):

    for item in mods_to_download:
        mod_url = url + urlencode(dict(public_key=public_key)) + \
            '&' + urlencode(dict(path=path + '/' + item))
        response = requests.get(mod_url)
        mod_download_url = response.json()['href']
        #print(response)
        download_responce = requests.get(mod_download_url)
        with open(f'{os.path.join(target_directory, item)}', 'wb') as f:
            f.write(download_responce.content)

print(utils.get_minecraft_directory())