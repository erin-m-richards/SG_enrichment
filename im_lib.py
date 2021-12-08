from typing import Tuple, Any

import numpy
from matplotlib import pyplot
from skimage.morphology import binary_dilation, disk

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

    # Segmenting C2 for cells based on 6xA_004, 005, 006, 008:
    # radius = 250 pixels
    # model = cyto2
    # Note: Segments cells from background and from each other well.
    # USE THIS CHANNEL TO DEFINE CELL OUTLINES.

    # Segmenting C3 based on 6xA_004, 005, 006, 008:
    # radius = 300 pixels
    # model = cyto
    # Note: Segments cells from background but not from each other.

    # Segmenting C1 for granules based on 6xA_004, 005, 006, 008:
    # radius = 15 pixels
    # model = cyto
    # Note: Segments most granules from the background.
    # USE THIS CHANNEL TO DEFINE GRANULE OUTLINES.

    # From command line for C2 for cells:
    # python -m cellpose --dir ~/images/ --pretrained_model cyto2 --diameter 250

    # From command line for C3 for cells:
    # python -m cellpose --dir ~/images/ --pretrained_model cyto --diameter 300

    # From command line for C1 for granules:
    # python -m cellpose --dir ~/images/ --pretrained_model cyto --diameter 15

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


def find_object(chB_img, chA_mask):
    """
    To find objects in channelB image using channelA mask.
    chA_mask will be used to make a local background mask loc_bkgd_mask.
    Pixel intensity in chB_img inside chA_mask will be compared to pixel
    intensity in the loc_bkgd_mask for this image.
    For each mask in chA_mask, if intensity is significantly higher than
    intensity in loc_bkgd_mask, a mask in chB_mask will be created.

    Parameters
    ----------
    chB_img = NumPy array of a channelB

    chA_mask = NumPy array of channelA where int = object, 0 = background

    Returns
    -------
    object_mask = NumPy array where 1 = object, 0 = background
    """

    # Find size of channelB image.
    img_size = numpy.shape(chB_img)
    num_rows = int(img_size[0])
    num_cols = int(img_size[1])

    # Make dummy matrix for channelB object mask.
    chB_mask = numpy.zeros(img_size)

    # Count number of masks in channelA.
    chA_num_masks = int(numpy.amax(chA_mask))

    # Turn channelA mask into simple logical mask for dilation.
    chA_log = numpy.where(chA_mask > 0, True, False)

    # Dilate masks in chA_mask.
    struct = disk(5)  # Make disk of radius = 5 pixels.
    chA_dilated = binary_dilation(chA_log, selem=struct)
    loc_bkgd_mask = chA_dilated

    # Make local background mask.
    for row in range(1, num_rows):
        for col in range(1, num_cols):
            if chA_log[row, col]:
                loc_bkgd_mask[row, col] = False

    #for mask in range(1, chA_num_masks):  # Start indexing at 1 for mask 1.
        # Find index/position of masked pixels in channelA.
        #maskA_index = numpy.where(chA_mask == mask)
        #maskA_xy = list(zip(maskA_index[0], maskA_index[1]))
        # Makes a list of tuples with each tuple being an xy position.

    # Make object_mask true where image pixel is greater than or equal to
    # threshold intensity.
    #for row in range(1, num_rows):
        #for col in range(1, num_cols):
            #if img[row, col] >= thresholds[1]:
                #object_mask[row, col] = 1

    return chA_log, chA_dilated


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
    chB_log = numpy.where(chB_mask > 0, True, False)

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
            if chB_log[xy[0], xy[1]] == False:
                overlap_mask[xy[0], xy[1]] = 0

            # If chB_mask is true at xy, make overlap_mask = int at xy.
            # Will work if chA_mask is false at this point, too.
            if chB_log[xy[0], xy[1]] == True:
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
    #filename_maskA = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells_seg.npy'
    #filename_maskB = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-twocells_seg.npy'
    filename_maskC = '/Users/Erin/PyCharmProjects/SG_enrichment/demo/C1-onecell_seg.npy'
    #filename_imgA = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells.tif'
    filename_imgB = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell.tif'

    #maskA = mask_cell(filename_maskA)
    #maskB = mask_cell(filename_maskB)
    maskC = mask_cell(filename_maskC)

    img = read_image(filename_imgB)
    #show_moi(img*0.001, maskA*0.2, img*0.001)

    #overlap = find_overlap(maskA, maskB, 0.9)
    #show_moi(maskA*0.5, overlap*0.5, maskB*0.1)

    log, dilated = find_object(img, maskC)
    show_moi(log*0.9, log*0.001, dilated*0.9)
    #show_moi(img*0.001, granule_mask*0.2, img*0.001)


if __name__ == "__main__":
    main()
