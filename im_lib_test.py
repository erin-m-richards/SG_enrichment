import unittest
import im_lib
    

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
        
    def test_mc_oneCell(self):
        filename = '/home/jovyan/SG_enrichment/demo/C2-onecell.npy'
        cell_mask = im_lib.mask_cell(filename)
        res = str(type(cell_mask))
        exp = "<class 'numpy.ndarray'>"
        self.assertEqual(res, exp)
    
    def test_mc_twoCells(self):
        filename = '/home/jovyan/SG_enrichment/demo/C2-twocells.npy'
        cell_mask = im_lib.mask_cell(filename)
        res = str(type(cell_mask))
        exp = "<class 'numpy.ndarray'>"
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
        
    def test_ri_oneCell(self):
        filename = '/home/jovyan/SG_enrichment/demo/C3-onecell.tif'
        image = im_lib.read_image(filename)
        print(type(image))
        res = str(type(image))
        exp = "<class 'PIL.TiffImagePlugin.TiffImageFile'>"
        self.assertEqual(res, exp)
    
    def test_ri_twoCells(self):
        filename = '/home/jovyan/SG_enrichment/demo/C3-twocells.tif'
        image = im_lib.read_image(filename)
        res = str(type(image))
        exp = "<class 'PIL.TiffImagePlugin.TiffImageFile'>"
        self.assertEqual(res, exp)
    
    
class FindObjectsTest(unittest.TestCase):

    @classmethod
    def setUpClass(clc):
        print("\nRunning FindObjects class setUp...")

    @classmethod
    def tearDownClass(clc):
        print("\nRunning FindObjects class tearDown...")

    def setUp(self):
        print("\nRunning setUp...")

    def tearDown(self):
        print("\nRunning tearDown...")
        
    #def test_fobj_oneCell(self):
        #filename = '/home/jovyan/SG_enrichment/demo/C2-onecell.npy'
        #image = im_lib.read_image(filename)
        #res = im_lib.find_object(image)
        

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
        
    #def test_foverlap(self):
    

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
