import datetime
import pathlib

def print_dictionary(dictionary):
    
    for key in dictionary:
        
        print('\t',key, dictionary[key])
        
def create_update_report(site, installed_plugins, installed_themes,
                         available_plugins, available_themes, moved_plugins,
                         moved_themes):
    
    # create timestamp for file name
    date_time = datetime.datetime.now()
    date_timestamp = date_time.strftime('%Y%m%d_%H_%M')
    
    # construct path for report
    reports_path = pathlib.Path('/var/log/wp_updates/')
    filename = site + '_report' + '_' + date_timestamp + '.log'
    out_filename_path = reports_path / filename
    
    # try to open and write report to file
    try:
        out_file = open(out_filename_path, 'w')
        
        # write a header
        header = '\t\t' + site + ' Update Report (' + date_timestamp + ')'
        out_file.write(header)
        out_file.write('\n')
        
        # previously installed
        out_file.write('\n')
        out_file.write('Version of previously installed plugins: \n')
        write_dictionary_to_file(out_file, installed_plugins)
        out_file.write('\n')
        out_file.write('Version of previously installed themes: \n')
        write_dictionary_to_file(out_file, installed_themes)
        
        # updates available
        out_file.write('\n')
        out_file.write('Plugin updates available: \n')
        write_dictionary_to_file(out_file, available_plugins)
        out_file.write('\n')
        out_file.write('Theme updates available: \n')
        write_dictionary_to_file(out_file, available_themes)
        
        #updates applied
        out_file.write('\n')
        out_file.write('Updates applied: \n')
        out_file.write('\tPlugins: \n')
        for key in moved_plugins:
            if key in available_plugins:
                out_file.write('\t\t' + key + ' ' + available_plugins[key] + 
                               '\n')
        out_file.write('\n')
        out_file.write('\tThemes: \n')
        for key in moved_themes:
            if key in available_themes:
                out_file.write('\t\t' + key + ' ' + available_themes[key] + 
                               '\n')

        out_file.close()
    
    except IOError as error:
        print('Error accessing file: ', out_filename_path)
        print('\tError: ', error)

def write_dictionary_to_file(filename, dictionary):
    
    for key in dictionary:
        
        filename.write('\t' + key + ' ' + dictionary[key] + '\n')

