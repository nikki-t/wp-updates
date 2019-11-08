import custom_exceptions
import pathlib
import urllib.request

def cleanup_zip_files(updates_dictionary, flag):
    
    home_path = pathlib.Path('/usr/local/python/wp_updates/wp_updates_dir/')
    
    for key in updates_dictionary:
        
        filename = key + '.' + updates_dictionary[key] + '.zip'
        
        working_file = home_path / 'working' / filename
    
        if flag == 'p':
            working_file.replace(home_path / 'plugins' / filename)
            
        elif flag == 't':
            working_file.replace(home_path / 'themes' / filename)
            
        else:
            raise custom_exceptions.FlagError('Error: Invalid flag. Zip files' +
                ' not cleaned up.')

def check_host(site):
    
    if site == 'btp':
        url = 'https://btp.umass.edu'
    else:
        url = 'https://' + site + '.chem.umass.edu'
    
    return (urllib.request.urlopen(url).getcode())

