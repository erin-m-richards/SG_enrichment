'''
NOTES:
    ~this is just a brian dump of all the various functions we might need and how to pipe them into each other, could probs split functions intodifferent libraries so that there is one for file handeling, one for mask generation and manipulation, and one for data processing/ stats/ plotting
    ~will all of these funcitons are going to need to return somesort of tracking list/dict object that includes the information about what image/ cell etc they came from inorder to track all that infor in the csv?
'''

def sort_by_channels(input_dir, error_log, channel_labels = {'thing1':'C1', 'thing2':'C2', 'thing3':'C3'}, file_type= 'tif'):
    '''
    PARAMETERS
    ----------
    dir : str
        This string is the file location for the directory containing images.
    error_log : str
        This string is the filelocation and name of the error log to output what files in dir weren't sorted into a group.
    channel_labels : dict
        This dictionary contains labels for what is in each channel.
    
    RETURNS
    ----------
    cells : list
        A list of images from channel containing cell reporter
    protein_complexes : list
        A list of images from channel containing RNA-Protein complex marker.
    probe : list 
        A list of images from channel containing the probe reporter. 
        
    '''
    # seperate out images by channel
    # use os package?
    # change out put from list to actually creating sub directories and output the directory file path?
    # add initial sort to exclude files of the wrong type
    return cells, protein_complexes, probe


def for_a_dir(input_dir, function):
    # takes a directory and inputs all files in directory into the specified function. 
    # this maybe an unnecessary function, probably is
    return results_of_function


def make_mask(image_file, ROI):
    # makes mask for a given file in a particular region of interest
    # find form ROI will be in 
    # change to return multiple ROIs, one for each object (cell, granule, etc)
    return mask


def coloc(mask1, mask2):
    # determine specific regions of overlab between 2 masks (for granules and probe)
    # also output individual masks for both probe and granules to feed into enrichment functions not sure how though or if better in own function??
    return [num_granules, num_probe_coloc_gran],


def write_to_coloc_csv(csv_file, ): # there will need to be other parameters, not sure what yet
    # take info and append to csv entry in the form: 
    # image, cell number in image, total number of granules, number of granules with probe colocalized
    return None


def generate_minimum_mask(a_granule_mask, a_probe_mask):
    # generate mask that is the donut around each of them (somehow make sure it is the same one)
    return outer_mask


def find_enrichment_value(a_probe_mask, outer_mask):
    # finds averave(maybe??) value of outer_mask (minimum) and a_probe_mask (maximum) and developes enrichment value
    return [minimum, maximum, enrichment value] 


def write_to_csv_enrichment(csv_file, ): # will need other stuff
    # writes enrichment data to csv in the form: image, cell, granule location, outermask location, minimum val, max value, enrichment value 
    return None


# workflow

cells, granules, probe = sort_by_channels(directory, {}, file_type= 'tif')
for image in cells:
    cell_mask = make_mask(image)
    for cell in cell_mask:
        
    