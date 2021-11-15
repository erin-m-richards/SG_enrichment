import numpy
from matplotlib import pyplot

"""
This library includes the following functions for image manipulation.

mask_cell(): To read a masked image file into a NumPy array.

read_image(): To read an image file into Python as a greyscale Image.

find_object(): To detect objects in an image within a given cell_mask.

find_overlap(): To find objects that occur in two channels and threshold for
percent of overlap.

count_objects(): To count objects in an image given a lower and an upper size limit.

"""


def mask_cell(filename):
    """
    To read a masked image file into a NumPy array.
    
    Parameters
    ----------
    filename = full path of the NumPy file
    
    Returns
    -------
    image = NumPy array of the image
    """

    # Load whole file.
    data = numpy.load(filename, allow_pickle=True).item()

    # Pull out masks.
    # Note: 'outlines' is also an option.
    cell_mask = data['masks']

    # Visualize mask.
    pyplot.imshow(cell_mask)
    pyplot.show()
    
    return cell_mask


def read_image(filename):
    """
    To read an image file into Python as a greyscale Image.
    
    Parameters
    ----------
    filename = full path of the image file
    
    Returns
    -------
    image = greyscale Image of the image file
    """

    img = filename

    return img


def find_object(cell_mask, img):
    """
    To detect objects in an image within a given cell_mask.
    
    Parameters
    ----------
    cell_mask = logical NumPy array where 1 = cell, 0 = background
    
    image = 8-bit greyscale image
    
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
    filename_mask = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell_seg.npy'
    #filename_img = '/home/jovyan/SG_enrichment/demo/C3-onecell.tif'
    cell_mask = mask_cell(filename_mask)

if __name__ == "__main__":
    main()
