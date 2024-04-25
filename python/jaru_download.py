import os
import platform
import utils
import shutil
import sys

def analyze(curr_files, needed_files):
    already_exist = []
    for item in needed_files:
        if item in curr_files:
            already_exist.append(item)
    return already_exist

def _main(yadisk_key, yadisk_main_path, mod_amount_limit=300):
    if platform.system() == 'Linux':
        mcdir = os.path.expanduser('~/.minecraft')
    elif platform.system() == 'Windows':
        mcdir = os.path.join(os.getenv('APPDATA'), '.minecraft')
    else:
        print('This platform is not supported!')
        return

    temp_directory = os.path.join(mcdir, 'jaru_temp_dir')
    resources_url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
    download_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    if 'http' not in yadisk_key:
        public_key = 'https://disk.yandex.ru/d/' + yadisk_key
    else:
        public_key = yadisk_key

    try:
        curr_files = utils.get_file_list(mcdir)
        needed_files = utils.get_uploaded_files(resources_url, public_key, yadisk_main_path, mod_amount_limit)
    except Exception as e:
        print(e)
        return

    existing_files = analyze(curr_files, needed_files)
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)
    os.mkdir(temp_directory)

    if existing_files:
        print(f'These existing dirs/files present in the modpack: \
{existing_files}')
        print('Possible operations: ')
        print('1. Exit')
        print('2. Backup and proceed')
        print('3. Delete and proceed')
        answer = input("Your choice: ")
        try:
            if answer == '2':
                pass
                utils.backup_move_files(mcdir, existing_files, 'jaru_backup')
            elif answer == '3':
                pass
                utils.remove_files(mcdir, existing_files)
            else:
                print('Exiting')
                return
            utils.download_new(download_url, public_key, yadisk_main_path, temp_directory, needed_files)
        except Exception as e:
            print(e)
            return
        print('The modpack has been successfully installed')
    else:
        utils.download_new(download_url, public_key, yadisk_main_path, temp_directory, needed_files)
    
    try:
        utils.unzip_or_copy(temp_directory, mcdir, needed_files)
        shutil.rmtree(temp_directory)
    except Exception as e:
        print(e)

_main(sys.argv[1], sys.argv[2])