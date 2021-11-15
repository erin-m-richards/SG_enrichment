import os, shutil
import sys
import argparse, configparser 


def input_parser():
    """
    PARAMETERS
    ----------
    None

    RETURNS
    ----------
    inputs : dict
        This dictionary contains all the inputs necessary inputs parsed from
        command line or a config file.
    """
    
    my_parser = argparse.ArgumentParser()
    
    my_parser.add_argument(
        '-c', '--config',
        type=str,
        action='store',
        help='This option is where you specify the config file.',
        required=True
    )
    
    args_parsed = my_parser.parse_args()
    
    # handle if no config file listed
    if args_parsed.config == None:
        raise TypeError\
        (f" No config file was listed. Please specify a config file using '-c'.")
        sys.exit(1)
    
    # handle if the given directory does not exist
    try:
        config_file = configparser.ConfigParser()
        config_file.read(args_parsed.config)
    except FileNotFoundError:
        print(f"The config file that you listed {args_parsed.config=} could not be found.")
        sys.exit(1)
    
    # generate dictionary with all of the necessary inputs
    inputs = {
        'image_directory' : config_file['FILE LOCATIONS']['image_directory'],
        'out_put_location' : config_file['FILE LOCATIONS']['outputs_directory'],
        'experiment_name' : config_file['EXPERIMENT INFO']['experiment_name'],
        'C1' : config_file['EXPERIMENT INFO']['C1'],
        'C2' : config_file['EXPERIMENT INFO']['C2'],
        'C3' : config_file['EXPERIMENT INFO']['C3'],
        'num_groups' : int(config_file['EXPERIMENT INFO']['num_groups']),
        'group_names' : [config_file['EXPERIMENT INFO']['group_names']]
    }
    return inputs


def sort_images(directory):
    # check that the directory exists
    try: 
        os.chdir(directory)
    except FileNotFoundError: 
        print(f'The directory given: {directory} could not be found.')
        sys.exit(1)
    
    # remove non tif files from directory
    #files = os.listdir(directory)
    files = [f for f in os.listdir(directory) if not f.startswith('.')]
    removed_files = []
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext == '.tif':
            pass
        else:
            removed_files.append(file)
    if len(removed_files)==0:
        print(f"No files were removed from this directory: {directory}")
    elif len(removed_files) != 0:
        print(f"Some of the files in this directory were removed because they were not the right file type, they can be found in the 'removed_files' folder: n/{removed_files}")
    
    #sort images by channel
    C1_images = []
    C2_images = []
    C3_images = []
    for file in files:
        if file[0:2] == 'C1':
            C1_images.append(file)
        elif file[0:2] == 'C2':
            C2_images.append(file)  
        elif file[0:2] == 'C3':
            C3_images.append(file)
        else:
            removed_files.append(file)

    # make directories for each type of image
    sub_dirs = ['C1', 'C2','C3','removed_files']
    full_paths = []
    for folder in sub_dirs:
        folder = os.path.join(directory,folder)
        os.mkdir(folder)
        full_paths.append(folder)
        
    # move all files to their respective sub folders
    for file in C1_images:
        shutil.move(os.path.join(directory, file), os.path.join(full_paths[0], file))
    for file in C2_images: 
        shutil.move(os.path.join(directory, file), os.path.join(full_paths[1], file))  
    for file in C3_images: 
        shutil.move(os.path.join(directory, file), os.path.join(full_paths[2], file))
    for file in removed_files: 
        shutil.move(os.path.join(directory, file), os.path.join(full_paths[3], file))
        
    # get full file paths to return for only C1, C2 and C3
    del full_paths[3]
    return full_paths


        
        
# testing
inputs = input_parser()
sort_images(inputs['image_directory']) 

