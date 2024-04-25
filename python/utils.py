import os
import platform
import shutil
import requests
import zipfile
import json
from urllib.parse import urlencode

def get_minecraft_directory():
    config_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    with open(os.path.join(config_dir, 'config.json')) as config:
        json_cfg = config.read()
        config = json.loads(json_cfg)
        custom_directory = config['useCustomMinecraftPath']
    if custom_directory != '':
        return custom_directory
    
    if platform.system() == 'Linux':
        mcdir = os.path.expanduser('~/.minecraft')
    elif platform.system() == 'Windows':
        mcdir = os.path.join(os.getenv('APPDATA'), '.minecraft')
    else:
        raise Exception('This platform is not supported!')
    return mcdir

def get_file_list(dir):
    current_mods = tuple(file for file in os.listdir(dir))
    return current_mods

def get_uploaded_files(resources_url, public_key, path, limit):
    mod_list_url = resources_url + urlencode(dict(public_key=public_key)) + \
        '&' + urlencode(dict(path=path))
    target_url = mod_list_url + '&' + urlencode(dict(limit=limit))
    response = requests.get(target_url)
    if response.status_code != 200:
        raise Exception(f'Failed to read files in the cloud with error {response.status_code}')
    data = json.loads(response.content)
    items = data['_embedded']['items']
    uploaded_mods = [item['name'] for item in items]
    if len(uploaded_mods) == limit:
        raise Exception(f'The amount of files on the server exceeds the given number: {limit}')
    return uploaded_mods

def backup_move_files(filedir, files_to_backup, backup_dir_name='backup'):
    backup_dir = os.path.join(filedir, backup_dir_name)
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    os.mkdir(backup_dir)
    for item in files_to_backup:
        shutil.move(os.path.join(filedir, item), os.path.join(backup_dir, item))

def remove_files(filedir, files_to_remove):
    for item in files_to_remove:
        file = os.path.join(filedir, item)
        if os.path.isfile(file):
            os.remove(os.path.join(filedir, item))
        else:
            shutil.rmtree(file)

def unzip_or_copy(src, dest, filenames):
    for filename in filenames:
        target_file = os.path.join(src, filename)
        if zipfile.is_zipfile(target_file):
            with zipfile.ZipFile(target_file, 'r') as zip_ref:
                zip_ref.extractall(dest)
            os.remove(target_file)
        else:
            shutil.move(target_file, dest)
        #os.remove(target_file)

def download_new(url, public_key, path, target_directory, files_to_download):
    for item in files_to_download:
        mod_url = url + urlencode(dict(public_key=public_key)) + \
            '&' + urlencode(dict(path=path + '/' + item))
        response = requests.get(mod_url)
        if response.status_code != 200:
            raise Exception(f'Download failed with error {response.status_code}')
        mod_download_url = response.json()['href']
        download_responce = requests.get(mod_download_url)
        with open(f'{os.path.join(target_directory, item)}', 'wb') as f:
            f.write(download_responce.content)
