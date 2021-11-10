import os
import sys
import argparser, configparser 


def sort_images(directory, C1_id='', C2_id='', C3_id=''):
    # check that the directory exists
    try os.chdir(directory):
        if FileNotFoundError: 
            print(f'The directory given: {directory} could not be found.')
            sys.exit(1)
        else:
            pass
    
    # remove non tif files from directory
    files = os.listdir(directory)
    removed_files = []
    for file in files:
        if file[:4] == '.tif':
            pass
        else:
            removed_files.append(files.pop(file))
    if len(removed_files)=0:
        print("No files were removed from this directory.")
    elif len(removed_files =! 0:
        print(f"Some of the files in this directory were removed because they were not the right file type: n/{removed_files}")
    
    #sort images by channel
    C1_images = []
    C2_images = []
    C3_images = []
    not_added = []
    for file in files:
        if file[0:1] == 'C1':
            C1_images.append(files.pop(file)
        elif file[0:1] == 'C2':
            C2_images.append(files.pop(file)       
        elif file[0:1] == 'C3':
            C3_images.append(files.pop(file)
        else:
            not_added.append(files.pop(file)
                             
    os.mkdir(C1, C2, C3) # make directories
    
    