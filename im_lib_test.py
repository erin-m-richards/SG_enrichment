import unittest
import im_lib
import numpy


class MaskCellTest(unittest.TestCase):

    @classmethod
    def setUpClass(clc):
        print("\nRunning MaskCell class setUp...")

    @classmethod
    def tearDownClass(clc):
        print("\nRunning MaskCell class tearDown...")

    def setUp(self):
        print("\nRunning setUp...")

    def tearDown(self):
        print("\nRunning tearDown...")
        
    def test_mc_oneCellType(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell_seg.npy'
        cell_mask = im_lib.mask_cell(filename)
        res = str(type(cell_mask))
        exp = "<class 'numpy.ndarray'>"
        self.assertEqual(res, exp)
    
    def test_mc_twoCellsType(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells_seg.npy'
        cell_mask = im_lib.mask_cell(filename)
        res = str(type(cell_mask))
        exp = "<class 'numpy.ndarray'>"
        self.assertEqual(res, exp)

    def test_mc_oneCellMask(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell_seg.npy'
        cell_mask = im_lib.mask_cell(filename)
        res = numpy.amax(cell_mask)
        exp = 1
        self.assertEqual(res, exp)

    def test_mc_twoCellsMask(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells_seg.npy'
        cell_mask = im_lib.mask_cell(filename)
        res = numpy.amax(cell_mask)
        exp = 2
        self.assertEqual(res, exp)


class ReadImageTest(unittest.TestCase):

    @classmethod
    def setUpClass(clc):
        print("\nRunning ReadImage class setUp...")

    @classmethod
    def tearDownClass(clc):
        print("\nRunning ReadImage class tearDown...")

    def setUp(self):
        print("\nRunning setUp...")

    def tearDown(self):
        print("\nRunning tearDown...")
        
    def test_ri_oneCellType(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell.tif'
        image = im_lib.read_image(filename)
        res = str(type(image))
        exp = "<class 'numpy.ndarray'>"
        self.assertEqual(res, exp)
    
    def test_ri_twoCellsType(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells.tif'
        image = im_lib.read_image(filename)
        res = str(type(image))
        exp = "<class 'numpy.ndarray'>"
        self.assertEqual(res, exp)


class MaskLocalBackground(unittest.TestCase):

    @classmethod
    def setUpClass(clc):
        print("\nRunning MaskLocalBackground class setUp...")

    @classmethod
    def tearDownClass(clc):
        print("\nRunning MaskLocalBackground class tearDown...")

    def setUp(self):
        print("\nRunning setUp...")

    def tearDown(self):
        print("\nRunning tearDown...")

    def test_mlb_oneCell(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C1-onecell_seg.npy'
        mask = im_lib.mask_cell(filename)
        exp = numpy.amax(mask)
        loc_mask = im_lib.mask_loc_bkgd(mask, radius=5)
        res = numpy.amax(loc_mask)
        self.assertEqual(res, exp)

    def test_mlb_noRadiusGiven(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C1-onecell_seg.npy'
        mask = im_lib.mask_cell(filename)
        exp = numpy.amax(mask)
        loc_mask = im_lib.mask_loc_bkgd(mask)
        res = numpy.amax(loc_mask)
        self.assertEqual(res, exp)

    def test_mlb_diffRadiusGiven(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C1-onecell_seg.npy'
        mask = im_lib.mask_cell(filename)
        exp = numpy.amax(mask)
        loc_mask = im_lib.mask_loc_bkgd(mask, radius=3)
        res = numpy.amax(loc_mask)
        self.assertEqual(res, exp)

    def test_mlb_twoCells(self):
        filename = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C1-twocells_seg.npy'
        mask = im_lib.mask_cell(filename)
        exp = numpy.amax(mask)
        loc_mask = im_lib.mask_loc_bkgd(mask, radius=5)
        res = numpy.amax(loc_mask)
        self.assertEqual(res, exp)


class FindObject(unittest.TestCase):

    @classmethod
    def setUpClass(clc):
        print("\nRunning FindObject class setUp...")

    @classmethod
    def tearDownClass(clc):
        print("\nRunning FindObject class tearDown...")

    def setUp(self):
        print("\nRunning setUp...")

    def tearDown(self):
        print("\nRunning tearDown...")

    def test_fob_oneCell(self):
        filename_mask_C1 = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C1-onecell_seg.npy'
        filename_img_C2 = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell.tif'
        mask_C1 = im_lib.mask_cell(filename_mask_C1)
        max = int(numpy.amax(mask_C1))
        img_C2 = im_lib.read_image(filename_img_C2)
        mask_bkgd = im_lib.mask_loc_bkgd(mask_C1, radius=5)
        mask_C2, medians = im_lib.find_object(img_C2, mask_C1, mask_bkgd)
        res = int(numpy.amax(mask_C2))
        self.assertFalse(res > max)

    def test_fob_twoCells(self):
        filename_mask_C1 = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C1-twocells_seg.npy'
        filename_img_C2 = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells.tif'
        mask_C1 = im_lib.mask_cell(filename_mask_C1)
        max = int(numpy.amax(mask_C1))
        img_C2 = im_lib.read_image(filename_img_C2)
        mask_bkgd = im_lib.mask_loc_bkgd(mask_C1, radius=5)
        mask_C2, medians = im_lib.find_object(img_C2, mask_C1, mask_bkgd)
        res = int(numpy.amax(mask_C2))
        self.assertFalse(res > max)


class FindOverlapTest(unittest.TestCase):

    @classmethod
    def setUpClass(clc):
        print("\nRunning FindOverlap class setUp...")

    @classmethod
    def tearDownClass(clc):
        print("\nRunning FindOverlap class tearDown...")

    def setUp(self):
        print("\nRunning setUp...")

    def tearDown(self):
        print("\nRunning tearDown...")
        
    def test_fov_oneCell(self):
        filename_maskA = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-onecell_seg.npy'
        filename_maskB = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-onecell_seg.npy'
        maskA = im_lib.mask_cell(filename_maskA)
        exp = numpy.amax(maskA)
        maskB = im_lib.mask_cell(filename_maskB)
        overlap = im_lib.find_overlap(maskA, maskB, 0.9)
        res = numpy.amax(overlap)
        self.assertEqual(res, exp)

    def test_fov_twoCells(self):
        filename_maskA = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells_seg.npy'
        filename_maskB = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-twocells_seg.npy'
        maskA = im_lib.mask_cell(filename_maskA)
        exp = numpy.amax(maskA)
        maskB = im_lib.mask_cell(filename_maskB)
        overlap = im_lib.find_overlap(maskA, maskB, 0.9)
        res = numpy.amax(overlap)
        self.assertEqual(res, exp)

    def test_fov_twoCells_highPercent(self):
        filename_maskA = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C2-twocells_seg.npy'
        filename_maskB = '/Users/Erin/PycharmProjects/SG_enrichment/demo/C3-twocells_seg.npy'
        maskA = im_lib.mask_cell(filename_maskA)
        exp = 0
        maskB = im_lib.mask_cell(filename_maskB)
        overlap = im_lib.find_overlap(maskA, maskB, 1.0)
        res = numpy.amax(overlap)
        self.assertEqual(res, exp)

class CountObjectsTest(unittest.TestCase):

    @classmethod
    def setUpClass(clc):
        print("\nRunning CountObjects class setUp...")

    @classmethod
    def tearDownClass(clc):
        print("\nRunning CountObjects class tearDown...")

    def setUp(self):
        print("\nRunning setUp...")

    def tearDown(self):
        print("\nRunning tearDown...")
        
    #def test_co(self):


if __name__ == "__main__":
    unittest.main()
