import numpy
from matplotlib import pyplot
import cv2

"""
This library includes functions for image manipulation.
"""


def show_moi(image, mask):
    """
    To show a mask overlaid on an image.

    Parameters
    ----------
    image = background image as a NumPy array that will be shown at 100%
    intensity

    mask = mask as a NumPy array that will be shown at 50% intensity

    Returns
    -------
    None, just shows an image
    """

    overlay = cv2.addWeighted(image, 0.03, mask, 1.0, 0)
    pyplot.imshow(overlay, cmap='gray')
    pyplot.show()

    return None


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

    # Segmenting C2 based on 6xA_004, 005, 006, 008:
    # radius = 250 pixels
    # model = cyto2
    # Note: Segments cells from background and from each other well.
    # USE THIS CHANNEL TO DEFINE CELL OUTLINES.

    # Segmenting C3 based on 6xA_004, 005, 006, 008:
    # radius = 300 pixels
    # model = cyto
    # Note: Segments cells from background but not from each other.

    # From command line for C2:
    # python -m cellpose --dir ~/images/ --pretrained_model cyto2 --diameter 250

    # From command line for C3:
    # python -m cellpose --dir ~/images/ --pretrained_model cyto --diameter 300

    # Load whole file.
    data = numpy.load(filename, allow_pickle=True).item()

    # Pull out masks.
    # Note: 'outlines' is also an option.
    cell_mask = data['masks']

    return cell_mask


def read_image(filename):
    """
    To read an image file into Python as a greyscale Image.
    
    Parameters
    ----------
    filename = full path of the image file
    
    Returns
    -------
    image = NumPy array of the image
    """

    img = pyplot.imread(filename)

    return img


def find_object(maskA):
    """
    To detect objects in an image where two masks overlap.
    
    Parameters
    ----------
    maskA = NumPy array where integer = cell, 0 = background

    maskB = NumPy array where integer = cell, 0 = background
    
    Returns
    -------
    object_mask = logical NumPy array where 1 = object, 0 = background
    """

    # Turn masks into simple logical masks, 1 = cell, 0 = background.
    maskA_log = numpy.where(maskA > 0, 1, 0)
    pyplot.imshow(maskA_log)
    pyplot.show()

    return maskA_log


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
    filename_mask = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-twocells_seg.npy'
    filename_img = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-twocells.tif'
    cell_mask = mask_cell(filename_mask)
    img = read_image(filename_img)
    show_moi(img, cell_mask)
    mask = find_object(cell_mask)

if __name__ == "__main__":
    main()
