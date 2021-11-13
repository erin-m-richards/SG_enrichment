import numpy

"""
This library includes the following functions for image manipulation.

read_image(): To read an image file into a NumPy array.

find_object(): To detect objects in an image within a given cell_mask.

find_overlap(): To find objects that occur in two channels and threshold for
percent of overlap.

count_objects(): To count objects in an image given a lower and an upper size limit.

"""


def read_image(filename):
    """
    To detect cells in the image with CellPose.
    
    Parameters
    ----------
    filename = full path of the image file
    
    Returns
    -------
    image = NumPy array of the image
    """
    
    image = numpy.array(filename)
    
    return image


def find_object(cell_mask, channel):
    """
    To detect objects in an image within a given cell_mask.
    
    Parameters
    ----------
    cell_mask = logical NumPy array where 1 = cell, 0 = background
    
    Returns
    -------
    object_mask = logical NumPy array where 1 = object, 0 = background
    """
    
    return object_mask


def find_overlap(chA_mask, chB_mask, chA, chB, percent_overlap):
    """
    To find objects that occur in two channels and threshold for percent of overlap.
    
    Parameters
    ----------
    chA_mask = logical NumPy array where 1 = object in chA
    
    chB_mask = logical NumPy array where 1 = object in chB
    
    chA = integer for channel A
    
    chB = integer for channel B
    
    percent_overlap = float for desired amount of overlap between chA_mask and
    chB_mask, 1 = 100% overlap

    Returns
    -------
    overlap_mask = logical NumPy array where 1 = object in both channels
    """
    
    return overlap_mask


def count_objects(object_mask, lower_size_limit, upper_size_limit):
    """
    To count objects in an image given a lower and an upper size limit.
    
    Parameters
    ----------
    object_mask = logical NumPy array where 1 = object, 0 = background
    
    lower_size_limit = integer for lower limit on pixel area in an object
    
    upper_size_limit = integer for upper limit on pixel area in an object
    
    Returns
    -------
    count = integer of number of objects of a given size
    """
    
    return count


def main():
    filename = '/home/jovyan/SG_enrichment/demo/C2-onecell.npy'

if __name__ == "__main__":
    main()
