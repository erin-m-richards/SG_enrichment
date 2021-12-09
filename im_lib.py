from typing import Tuple, Any
import numpy
from matplotlib import pyplot
from skimage.morphology import dilation, disk
from statistics import median
from scipy.stats import ttest_ind

"""
This library includes functions for image manipulation, including reading
images, masking images, finding objects that overlap, and displaying images.
"""


def show_moi(img1, img2, img3):
    """
    To show three "images" overlaid on top of each other.
    img1 will be red, img2 will be green, img3 will be blue.

    For comparing a mask to one image: (img*0.001, mask*0.2, img*0.001)
    img in pink/purple (white is more intense), mask in green.

    For comparing two masks to their overlap: (mask1*0.5, overlap*0.5, mask2*0.1)
    mask1 in red, mask2 in blue, overlap in yellow.

    Parameters
    ----------
    img1 = NumPy array of image1

    img2 = NumPy array of image2

    img3 = NumPy array of image3

    Returns
    -------
    None, just shows an image
    """

    # Create 3D image in order ((r, g, b)).
    overlay = numpy.dstack((img1, img2, img3))

    # Display image.
    pyplot.imshow(overlay)
    pyplot.show()

    return None


def mask_object(filename):
    """
    To read a masked image file into a NumPy array.
    
    Parameters
    ----------
    filename = full path of the NumPy file (.npy)
    
    Returns
    -------
    mask = NumPy array of the mask where int = object, 0 = background
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
    object_mask = data['masks']

    return object_mask


def read_image(filename):
    """
    To read an image file into a NumPy array.
    
    Parameters
    ----------
    filename = full path of an image file
    
    Returns
    -------
    img = NumPy array of the image
    """

    img = pyplot.imread(filename)

    return img


def mask_loc_bkgd(object_mask, radius=5):
    """
    To create a mask of the local background (the area around) the masked
    objects. The size of the local background is changed with radius.

    Parameters
    ----------
    object_mask = NumPy array where int = object, 0 = background

    radius = int for pixel radius to create loc_bkgd_mask
    The default value is 5 pixels.

    Returns
    -------
    loc_bkgd_mask = NumPy array where 1 = object, 0 = background
    """

    # Find size of mask.
    matrix_size = numpy.shape(object_mask)

    # Make dummy matrix for local background mask.
    loc_bkgd_mask = numpy.zeros(matrix_size)

    # Count number of masks in object_mask matrix.
    num_masks = int(numpy.amax(object_mask))

    # Dilate masks in object mask. Keep mask indexing from object mask.
    struct = disk(radius)  # Make disk of given radius in pixels.
    dilated_mask = dilation(object_mask, selem=struct)

    # For each mask in object mask, create a mask of the local background.
    for mask in range(1, (num_masks + 1)):
        # Find index/position of masked pixels in exp_mask.
        mask_index = numpy.where(dilated_mask == mask)
        mask_xy = list(zip(mask_index[0], mask_index[1]))
        # Makes a list of tuples with each tuple being an xy position.

        for xy in mask_xy:
            # If object mask is true, make loc_bkgd_mask = 0.
            # This carves out object from dilated mask, making a donut mask.
            if object_mask[xy[0], xy[1]] >= 1:
                loc_bkgd_mask[xy[0], xy[1]] = 0

            # If object mask is false, make loc_bkgd_mask = dilated_mask.
            # This retains the indexing in the original object mask.
            # This also works if dilated_mask = 0 (for the rest of the img).
            if object_mask[xy[0], xy[1]] == 0:
                loc_bkgd_mask[xy[0], xy[1]] = dilated_mask[xy[0], xy[1]]

    return loc_bkgd_mask


def find_object(img, exp_mask, loc_bkgd_mask):
    """
    To find objects in an image by comparing the local background mask,
    and the expected mask.

    For each mask in the expected mask, if the pixel intensity of the expected
    object is significantly higher (p = 0.05) than the pixel intensity in the
    local background by a one-tailed two-sample t-test,
    then the resulting object mask is the expected object mask.
    If this is not true, the resulting object mask shows no object at this
    position.

    Parameters
    ----------
    img = NumPy array of a one-channel image

    exp_mask = NumPy array where int = expected objects, 0 = background

    loc_bkgd_mask = NumPy array where int = local background of expected
    objects, 0 = background

    Returns
    -------
    res_mask = NumPy array where int = resulting objects, 0 = background

    object_median = int of the median value found in img under res_mask

    bkgd_median = int of the median value found in img under local_bkgd_mask
    """

    # Find size of image.
    matrix_size = numpy.shape(img)

    # Make dummy matrix for resulting mask.
    res_mask = numpy.zeros(matrix_size)

    # Make dummy list for median values.
    medians = list()

    # Count number of masks in expected mask.
    num_exp_masks = int(numpy.amax(exp_mask))

    for mask in range(1, (num_exp_masks + 1)):
        # Make dummy list for intensity values in image.
        exp_vals = list()

        # Find index/position of masked pixels in exp_mask.
        exp_index = numpy.where(exp_mask == mask)
        exp_xy = list(zip(exp_index[0], exp_index[1]))
        # Makes a list of tuples with each tuple being an xy position.

        # For each xy position in exp_mask pull the pixel value from img.
        for exy in exp_xy:
            exp_vals.append(int(img[exy[0], exy[1]]))

        # Make dummy list for intensity values in image.
        bkgd_vals = list()

        # Find index/position of masked pixels in loc_bkgd_mask.
        bkgd_index = numpy.where(loc_bkgd_mask == mask)
        bkgd_xy = list(zip(bkgd_index[0], bkgd_index[1]))
        # Makes a list of tuples with each tuple being an xy position.

        # For each xy position in loc_bkdg_mask pull the pixel value from img.
        for bxy in bkgd_xy:
            bkgd_vals.append(int(img[bxy[0], bxy[1]]))

        # See if exp_vals is significantly higher than bkgd_vals by one-tailed
        # two-sample t-test.
        (t, p) = ttest_ind(a=exp_vals, b=bkgd_vals, equal_var=True)

        # If it is significant...
        if p < 0.05:
            # Make res_mask = exp_mask for that mask.
            for xy in exp_xy:
                res_mask[xy[0], xy[1]] = exp_mask[xy[0], xy[1]]

            # Save median values of the object and of the local background.
            medians.append((mask, median(exp_vals), median(bkgd_vals)))

    return res_mask, medians


def find_overlap(ch1_mask, ch2_mask, overlap_threshold=0.9):
    """
    To find objects that occur in two channels and exceed a given percent area
    overlap.
    
    Parameters
    ----------
    ch1_mask = NumPy array where int = object in channel 1
    There should be less masked objects in channel 1 than there are in
    channel 2.
    
    ch2_mask = NumPy array where int = object in channel 2
    
    overlap_threshold = float for desired amount of overlap between ch1_mask
    and ch2_mask by pixel area, 1 = 100% overlap
    Default overlap is 0.9 or 90%.

    Returns
    -------
    overlap_mask = NumPy array where 1 = object in both channels,
    0 = background
    """

    # Count number of masks in channel 1.
    ch1_num_masks = int(numpy.amax(ch1_mask))

    # Turn ch2_mask into a simple logical mask for channel 2.
    ch2_log = numpy.where(ch2_mask > 0, True, False)

    # Get matrix size of channel 1 mask.
    matrix_size = numpy.shape(ch1_mask)

    # Make a dummy overlap mask.
    overlap_mask = numpy.zeros(matrix_size)

    # For each mask in channel 1, see if a mask in channel 2 exists.
    for mask in range(1, (ch1_num_masks + 1)):
        # Find index/position of masked pixels in channel 1.
        mask1_index = numpy.where(ch1_mask == mask)
        mask1_xy = list(zip(mask1_index[0], mask1_index[1]))
        # Makes a list of tuples with each tuple being an xy position.

        # For each xy position in ch1_mask, see if ch2_mask is true.
        for xy in mask1_xy:
            # If ch2_mask is false, make overlap_mask = 0.
            if ch2_log[xy[0], xy[1]] == False:
                overlap_mask[xy[0], xy[1]] = 0

            # If ch2_mask is true, make overlap_mask = int.
            # This retains the indexing in the original object mask.
            # This also works if ch1_mask = 0 (for the rest of the img).
            if ch2_log[xy[0], xy[1]] == True:
                overlap_mask[xy[0], xy[1]] = ch1_mask[xy[0], xy[1]]

        # Find area of mask in channel 1.
        mask1_area = len(mask1_xy)

        # Find area of overlap mask.
        overlap_index = numpy.where(overlap_mask == mask)
        overlap_xy = list(zip(overlap_index[0], overlap_index[1]))
        # Makes a list of tuples with each tuple being an xy position.
        overlap_mask_area = len(overlap_xy)

        # Find percent of area overlap.
        overlap_percent = overlap_mask_area / mask1_area

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
    filename_img_C2_one = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell.tif'
    filename_img_C3_one = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-onecell.tif'
    filename_mask_C1_one = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C1-onecell_seg.npy'
    filename_mask_C2_one = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell_seg.npy'
    filename_mask_C3_one = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-onecell_seg.npy'

    img_C2_one = read_image(filename_img_C2_one)
    img_C3_one = read_image(filename_img_C3_one)
    mask_C1_one = mask_object(filename_mask_C1_one)
    mask_C2_one = mask_object(filename_mask_C2_one)
    mask_C3_one = mask_object(filename_mask_C3_one)

    show_moi(img_C2_one*0.001, mask_C2_one*0.2, img_C2_one*0.001)
    show_moi(img_C3_one*0.001, mask_C3_one*0.2, img_C3_one*0.001)

    overlap_cells_one = find_overlap(mask_C2_one, mask_C3_one, overlap_threshold=0.9)
    show_moi(mask_C2_one*0.5, overlap_cells_one*0.5, mask_C3_one*0.1)

    bkgd_one = mask_loc_bkgd(mask_C1_one, radius=5)
    show_moi(img_C2_one*0.001, bkgd_one*0.2, img_C2_one*0.001)
    granules_C2_one = find_object(img_C2_one, mask_C1_one, bkgd_one)
    show_moi(img_C2_one*0.001, granules_C2_one*0.2, img_C2_one*0.001)

    #filename_img_C2_two = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells.tif'
    #filename_img_C3_two = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-twocells.tif'
    #filename_mask_C1_two = '/Users/Erin/PyCharmProjects/SG_enrichment/demo/C1-twocells_seg.npy'
    #filename_mask_C2_two = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells_seg.npy'
    #filename_mask_C3_two = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-twocells_seg.npy'

    #img_C2_two = read_image(filename_img_C2_two)
    #img_C3_two = read_image(filename_img_C3_two)
    #mask_C1_two = mask_object(filename_mask_C1_two)
    #mask_C2_two = mask_object(filename_mask_C2_two)
    #mask_C3_two = mask_object(filename_mask_C3_two)

    #show_moi(img_C2_two*0.001, mask_C2_two*0.2, img_C2_two*0.001)
    #show_moi(img_C3_two*0.001, mask_C3_two*0.2, img_C3_two*0.001)

    #overlap_cells_two = find_overlap(mask_C2_two, mask_C3_two, overlap_threshold=0.9)
    #show_moi(mask_C2_two*0.5, overlap_cells_two*0.5, mask_C3_two*0.1)

    #bkgd_two = mask_loc_bkgd(mask_C1_two, radius=5)
    #show_moi(img_C2_two*0.001, bkgd_two*0.2, img_C2_two*0.001)
    #granules_C2_two = find_object(img_C2_two, mask_C1_two, bkgd_two)
    #show_moi(img_C2_two*0.001, granules_C2_two*0.2, img_C2_two*0.001)


if __name__ == "__main__":
    main()
