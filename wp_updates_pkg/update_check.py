import custom_exceptions
import os
import urllib.request
from urllib.error import URLError

def create_directory_list(directory_path):
    
    # list the directories at the path
    dirs = os.listdir(directory_path)
    
    # remove hello.php from list if it exists
    i = 0
    while i < len(dirs):
        if dirs[i] == 'hello.php':
            del dirs[i] 
        i += 1
    
    # remove index.php from directory list
    dirs.remove('index.php')
    
    # return list of installed plugins or themes
    return dirs

def create_installed_dictionary(directory_path, installs_list, flag):
    
    # create a dictionary to store plugin name and version
    installed_dictionary = {}
    
    # construct dictionary from list
    for install in installs_list:

        # deal with plugins
        if flag == 'p':
            filename = construct_plugin_filename(install)
        
        # deal with themes
        elif flag == 't':
            filename = 'style.css'
        
        else:
            raise custom_exceptions.FlagError('Error: Invalid flag. Installed' +
                ' name and version dictionary' + ' not constructed.')
        
        # construct full path to file
        install_path = directory_path / install / filename
        
        # create a dictionary of the name and version of the install
        try:
            version = get_installed_version(install_path)
            if (version !=''):
                installed_dictionary[install] = version
            
        except IOError:
            print('Error: Cannot open file:', install_path)
        
    return installed_dictionary;

def construct_plugin_filename(plugin):
    
    if plugin == 'ldap-login-password-and-role-manager':
        filename = 'ldap_login_password_and_role_manager.php'
    else:
        filename = plugin + '.php'
        
    return filename

def get_installed_version(filename):
    
    version = ''
        
    # construct dictionary with name and version of install
    with open (filename, 'r') as file:
        
        for line in file:
                
            if 'Version:' in line:
                version += (line.split(': '))[1]
                break
                           
        if (version !=''):
            # strip version of leading and ending characters
            version = version.strip()
    
    return version

def get_available_dictionary(installs_list, flag):
    
    #create empty dictionary
    available_dictionary = {}
    
    # construct dictionary of plugin and currently avaiable version
    for install in installs_list:
        
        version = ''
        
        # construct URLs
        url = construct_url(install, flag)
        
        try:
            # get content from URL
            html = urllib.request.urlopen(url)
            
            for line in html:
                
                string_line = line.decode().strip()
                
                if flag == 'p':
                    
                    if 'softwareVersion' in string_line:
                        version = (string_line.split(':'))[1]
                        version = version.strip('" ,')
                        break
                    
                elif flag == 't':
                    
                    if 'Version' in string_line:
                        version = (string_line.split(':'))[1]
                        version = find_theme_version(string_line)
                        break
                
                else:
                    raise custom_exceptions.FlagError('Error: Invalid flag.' + 
                                                      ' Current version' + 
                                                      ' dictionary not' + 
                                                      ' constructed.')
               
            if (version != ''):
                available_dictionary[install] = version
            
        except URLError:
            print('Error: Unable to access URL:', url)
    
    return available_dictionary

def construct_url(install, flag):
    
    if flag == 'p':
        url = 'https://wordpress.org/plugins/' + install
    elif flag == 't':
        url = 'https://wordpress.org/themes/' + install
    else:
        raise custom_exceptions.FlagError('Error:  Invalid flag. URL to ' +
                                          ' get current version not' + 
                                          ' constructed. \n\tInstall ' 
                                          + 'failed on: ' + install)
    return url

def find_theme_version(line):
    
    # find the beginning of the version number
    i = line.find('<strong>')
    i += 8
    # find the end of the version number
    j = line.find('</strong>')
    
    # return the substring version number
    return line[i:j]

def compare_dictionaries(installed, available):
    
    updates_dictionary = {}
    
    for key in installed:
        
        if key in available:
            
            if installed[key] != available[key]:
                updates_dictionary[key] = available[key]
    
    return updates_dictionary
