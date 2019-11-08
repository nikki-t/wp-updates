#!/usr/local/python/wp_updates/wp_updates_env/bin/python3

import apply_updates
import custom_exceptions
import getopt
import maintenance_cleanup
import pathlib
import print_reports
import sys
import update_check
from urllib.error import URLError

def main(argv):
    
    # determine site
    try:
        opts, args = getopt.getopt(argv, 'hs:', ['site='])
    
    except getopt.GetoptError as error:
        print('wp_updates.py -s <site>')
        sys.exit(2)
    
    for opt, arg in opts:
        
        if opt == '-h':
            print('wp_updates.py -s <site>')
            sys.exit(0)
            
        elif opt in ('-s', '--site'):
            site = arg 
    
    try:
        # construct paths
        site_path = pathlib.Path('/var/www/') / site / 'wp-content'
        plugins_path = site_path / 'plugins'
        themes_path = site_path / 'themes'
        
        #### CHECK FOR UPDATES ####
        print()
        print('Checking for updates...')
        print()
        
        # create a list of installed plugins
        plugins_list = update_check.create_directory_list(plugins_path)
        themes_list = update_check.create_directory_list(themes_path)
            
        # create dictionaries with the name and version
        installed_plugins_dict = update_check.create_installed_dictionary(plugins_path, 
            plugins_list, 'p')
        installed_themes_dict = update_check.create_installed_dictionary(themes_path, 
            themes_list, 't')
         
        # create a dictionary with the name and current version available for 
        # each plugin and theme
        available_plugins_dict = update_check.get_available_dictionary(plugins_list, 'p')
        available_themes_dict = update_check.get_available_dictionary(themes_list, 't')
          
        # compare both dictionaries to determine if there are updates
        plugin_updates_dict = update_check.compare_dictionaries(installed_plugins_dict, 
            available_plugins_dict)
        theme_updates_dict = update_check.compare_dictionaries(installed_themes_dict, 
            available_themes_dict)
        
        # check if there are any updates available and if so ask to install
        if plugin_updates_dict or theme_updates_dict:
            # ask if use would like to download and install updates
            # print available updates
            print('The following updates are available:')
            print('Plugins:')
            print_reports.print_dictionary(plugin_updates_dict)
            print()
            print('Themes:')
            print_reports.print_dictionary(theme_updates_dict)
            print()
            install_prompt = input('Would you like to download and install these' + 
                                  ' updates? \n\tEnter \'y\' for yes: ')
            if install_prompt == 'y':
            
                #### APPLY UPDATES ####
                
                # download updates to working directory
                plugin_downloads = apply_updates.download_updates(plugin_updates_dict, 'p')
                theme_downloads = apply_updates.download_updates(theme_updates_dict, 't')
                
                # print updates downloaded
                print()
                print('Plugin Updates Downloaded:')
                print_reports.print_dictionary(plugin_downloads)
                print()
                print('Theme Updates Downloaded:')
                print_reports.print_dictionary(theme_downloads)
                
                
                # unzip downloaded updates
                unzipped_plugins = apply_updates.unzip_updates(plugin_updates_dict)
                unzipped_themes = apply_updates.unzip_updates(theme_updates_dict)
                
                # print unzipped updates
                print()
                print('Unzipped Plugins: ')
                print_reports.print_dictionary(unzipped_plugins)
                print()
                print('Unzipped Themes:')
                print_reports.print_dictionary(unzipped_themes)
                
                # move updates into place
                deleted_plugins, moved_plugins = apply_updates.move_updates(plugin_updates_dict, plugins_path)
                deleted_themes, moved_themes = apply_updates.move_updates(theme_updates_dict, themes_path)
                
                print()
                print('Updates complete.')
                print('The following updates were moved to production:')
                print_reports.print_dictionary(moved_plugins)
                print_reports.print_dictionary(moved_themes)
                if deleted_plugins:
                    print()
                    print('The following old plugins were deleted:')
                    print_reports.print_dictionary(deleted_plugins)
                if deleted_themes:
                    print()
                    print('The following old themes were deleted:')
                    print_reports.print_dictionary(deleted_themes)
                
                #### MAINTENANCE AND CLEANUP ####
                
                # cleanup zip files
                maintenance_cleanup.cleanup_zip_files(plugin_updates_dict, 'p')
                maintenance_cleanup.cleanup_zip_files(theme_updates_dict, 't')
                print()
                print('Updates cleaned up and organized.')
                
                # check if website is still available
                status = maintenance_cleanup.check_host(site)
                if status != 200:
                    print('Checked site availability. Site is unavailable:\n' + 
                          'Status code: ', status)
                else:   
                    #### PRINT AND REPORT ON UPDATES APPLIED ####
                    print()
                    print('The following updates were applied:')
                    print()
                    print('Plugins:')
                    for key in moved_plugins:
                        if key in plugin_updates_dict:
                            print('\t' + key + ' ' + plugin_updates_dict[key])
                    print()
                    print('Themes:')
                    for key in moved_themes:
                        if key in theme_updates_dict:
                            print('\t' + key + ' ' + theme_updates_dict[key])
                    
                    print_reports.create_update_report(site, installed_plugins_dict, 
                                         installed_themes_dict, 
                                         plugin_updates_dict, 
                                         theme_updates_dict, moved_plugins, 
                                         moved_themes)
                    print()
                    print('Update report written for site:', site)
                    print()
                        
            else:
                print()
                print('Quitting program. Updates will not be installed for:', site)
                print()
        
        else:
            print('No updates available for:', site)
            print()
        
    
    except custom_exceptions.FlagError as error:
        print(error)
        print('Program exit for site:', site)
        print()
    
    except URLError as error:
        print()
        print('Error accessing site after updates. Site:', site)
        print('\tError: ', error)
        print()
    
main(sys.argv[1:])
