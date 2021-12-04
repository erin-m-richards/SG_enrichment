from typing import Tuple, Any

import numpy
from matplotlib import pyplot

"""
This library includes functions for image manipulation.
"""


def show_moi(img1, img2, img3):
    """
    To show a mask overlaid on an image.

    For comparing a mask to an image: (image*0.001, mask*0.2, image*0.001)
    image in pink (white is more intense), mask in green.

    For comparing masks to overlap mask: (maskA*0.5, overlap*0.5, maskB*0.1)
    maskB in blue, maskA in red, overlap in yellow.

    Parameters
    ----------
    image = background image as a NumPy array that will be shown at 100%
    intensity

    mask = mask as a NumPy array that will be shown at 50% intensity

    Returns
    -------
    None, just shows an image
    """

    overlay = numpy.dstack((img1, img2, img3))
    pyplot.imshow(overlay)
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


def find_overlap(chA_mask, chB_mask, overlap_threshold):
    """
    To find objects that occur in two channels and threshold for percent of
    overlap.
    
    Parameters
    ----------
    chA_mask = NumPy array where non-zero integer = object in channelA
    There should be less masked objects in channelA than there are in channelB.
    
    chB_mask = NumPy array where non-zero integer = object in channelB
    
    percent_overlap = float for desired amount of overlap between chA_mask and
    chB_mask, 1 = 100% overlap

    Returns
    -------
    overlap_mask = logical NumPy array where 1 = object in both channels
    """

    # Count number of masks in channelA.
    chA_num_masks = int(numpy.amax(chA_mask))

    # Turn channelB mask into a simple logical mask.
    chB_log = numpy.where(chB_mask > 0, 1, 0)

    # Get matrix size of channelA mask.
    matrix_size = numpy.shape(chA_mask)

    # Make a dummy overlap mask the same size as channelA mask.
    overlap_mask = numpy.zeros(matrix_size)

    for mask in range(chA_num_masks):
        # Find index/position of masked pixels in channelA.
        maskA_index = numpy.where(chA_mask == (mask + 1))  # Because indexing starts at 0.
        maskA_xy = list(zip(maskA_index[0], maskA_index[1]))
        # Makes a list of tuples with each tuple being an xy position.

        # For each xy position in chA_mask, see if chB_mask is true.
        for xy in maskA_xy:  # xy is a tuple.

            # If chB_mask is false at xy, make overlap_mask false at xy.
            if chB_log[xy[0], xy[1]] == 0:
                overlap_mask[xy[0], xy[1]] = 0

            # If chB_mask is true at xy, make overlap_mask = int at xy.
            # Will work if chA_mask is false at this point, too.
            if chB_log[xy[0], xy[1]] == 1:
                overlap_mask[xy[0], xy[1]] = chA_mask[xy[0], xy[1]]  # To keep masks separate.

        # Filter overlap masks for percent of overlap with maskA.
        maskA_area = len(maskA_xy)  # Find number of pixels in maskA.

        overlap_index = numpy.where(overlap_mask == (mask + 1))  # Because indexing starts at 0.
        overlap_xy = list(zip(overlap_index[0], overlap_index[1]))
        # Makes a list of tuples with each tuple being an xy position.
        overlap_mask_size = len(overlap_xy)  # Find number of pixels in overlap_mask.

        # Find percent of area overlap.
        overlap_percent = overlap_mask_size / maskA_area

        # If percent overlap is less than threshold, remove the mask.
        if overlap_percent < overlap_threshold:
            for xy in overlap_xy:
                overlap_mask[xy[0], xy[1]] = 0

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
    filename_maskA = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells_seg.npy'
    filename_maskB = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-twocells_seg.npy'
    filename_img = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells.tif'

    maskA = mask_cell(filename_maskA)
    maskB = mask_cell(filename_maskB)

    img = read_image(filename_img)
    show_moi(img*0.001, maskA*0.2, img*0.001)

    overlap = find_overlap(maskA, maskB, 1.0)
    show_moi(maskA*0.5, overlap*0.5, maskB*0.1)


if __name__ == "__main__":
    main()
