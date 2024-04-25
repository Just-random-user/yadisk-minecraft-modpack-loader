import os
import platform
import utils
import sys

def find_diff(curr_mods, needed_mods):
    curr_mods_namesonly = [''.join([char for char in item.split('.')[0] if char.isalpha()]) for item in curr_mods]
    curr_mods_dict = dict(zip(curr_mods_namesonly, curr_mods))
    
    mod_difference = []
    for item in needed_mods:
        if item not in curr_mods:
            item_name = item.split('.')[0]
            item_name = ''.join(char for char in item_name if char.isalpha())
            if item_name in curr_mods_dict.keys():
                mod_difference.append((item, curr_mods_dict[item_name]))
            else:
                mod_difference.append((item, None))
    return mod_difference

def _main(yadisk_key, yadisk_mod_path, mod_amount_limit=300):
    if platform.system() == 'Linux':
        mcdir = os.path.expanduser('~/.minecraft')
    elif platform.system() == 'Windows':
        mcdir = os.path.join(os.getenv('APPDATA'), '.minecraft')
    else:
        print('This platform is not supported!')
        return
    
    moddir = os.path.join(mcdir, 'mods')    
    resources_url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
    download_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    if 'http' not in yadisk_key:
        public_key = 'https://disk.yandex.ru/d/' + yadisk_key
    else:
        public_key = yadisk_key

    try:
        curr_mods = utils.get_file_list(moddir)
        needed_mods = utils.get_uploaded_files(resources_url, public_key, yadisk_mod_path, mod_amount_limit)
    except Exception as e:
        print(e)
        return

    mod_difference = find_diff(curr_mods, needed_mods)
    if mod_difference:
        mods_to_update = tuple(item[1] for item in mod_difference if item[1])
        mods_to_install = tuple(item[0] for item in mod_difference if item[1] == None)
        if mods_to_update:
            print(f'These mods have new version available and will be replaced: \
{mods_to_update}')
        if mods_to_install:
            print(f'These mods are not installed and will be downloaded: \
{mods_to_install}')
        answer = input("Do you wish to proceed? [y/N]")
        if answer in 'YyДд':
            mods_to_update = tuple(item[1] for item in mod_difference if item[1])
            try:
                if mods_to_update:
                    utils.backup_move_files(moddir, mods_to_update, 'jaru_update_program_outdated')
                utils.download_new(download_url, public_key, yadisk_mod_path, moddir, tuple(item[0] for item in mod_difference))
            except Exception as e:
                print(e)
                return
            print('The mods are successfully updated')
    else:
        print('All mods are up to date!')

_main(sys.argv[1], sys.argv[2])