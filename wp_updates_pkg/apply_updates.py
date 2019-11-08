import custom_exceptions
import pathlib
import shutil
import wget
from zipfile import ZipFile
from urllib.error import HTTPError

def download_updates(updates_dictionary, flag):

    download_path = '/usr/local/python/wp_updates/wp_updates_dir/working/'

    downloads_dictionary = {}
    
    for key in updates_dictionary.copy():
        # construct download URLs
        if flag == 'p':
            url = 'https://downloads.wordpress.org/plugin/' + key + '.' \
                + updates_dictionary[key] + '.zip'
        elif flag == 't':
            url = 'https://downloads.wordpress.org/theme/' + key + '.' \
                + updates_dictionary[key] + '.zip'
        else:
            raise custom_exceptions.FlagError('Error: Invalid flag. Updates' + 
                ' not downloaded.')
        
        try:
            wget.download(url, download_path, bar=None)
            downloads_dictionary[key] = updates_dictionary[key]
        
        except HTTPError:
            print('Error:  Could not access URL:', url)
            print('\tDownload removed from list: ', key, updates_dictionary[key])
            del updates_dictionary[key]
    

    return downloads_dictionary
            
def unzip_updates(updates_dictionary):
    
    # construct working path to zip file
    working_path = '/usr/local/python/wp_updates/wp_updates_dir/working/'
    
    unzip_dictionary = {}
    
    # unzip each update
    for key in updates_dictionary.copy():
        
        filename = working_path + key + '.' + updates_dictionary[key] + '.zip'
        
        try:
            with ZipFile(filename, 'r') as zip_file:
                zip_file.extractall(working_path)
                unzip_dictionary[key] = filename
        
        except IOError:
            print(' Error: Cannot open file:', filename)
            print('\tThe following update will be removed:', key, 
                updates_dictionary[key])
            del updates_dictionary[key]
    
    return unzip_dictionary

def move_updates(updates_dictionary, directory_path):
    
    home = pathlib.Path('/usr/local/python/wp_updates/wp_updates_dir/')
    
    deleted_dictionary = {}
    moved_dictionary = {}
                              
    for key in updates_dictionary:
        
        # construct paths to work with
        install = directory_path / key
        old = home / 'old' / key
        working = home / 'working' / key
        
        # move updates into place
        if install.exists():
            
            if old.exists():
                shutil.rmtree(old)
                deleted_dictionary[key] = old
        
            install.replace(old)
        
        working.replace(install)
        moved_dictionary[key] = working
    
    return deleted_dictionary, moved_dictionary

