import unittest
from unittest import mock
from unittest.mock import patch
from source import utils
import numpy as np


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.img=np.ones((10,10))
        self.img2= np.ones((11,11))
        self.array1= np.ones(1)
        self.array3d= np.ones((5,5,5))

    
   
    def test_check_dimension(self):

    
        with self.assertRaises(ValueError) as context:
            utils.check_dimension(self.img, 3)
        self.assertTrue("Array ndim: 2 isn't equal to 3" in str(context.exception))

        with self.assertRaises(ValueError) as context:
            utils.check_dimension(self.img, -1)
        self.assertTrue("Array ndim: 2 isn't equal to -1" in str(context.exception))

        try: 
            utils.check_dimension(self.img, 2)
        except ValueError:
            self.fail("Points.check_dimension raised exception on valid dimensions")

        try: 
            utils.check_dimension(self.array3d, 3)
        except ValueError:
            self.fail("Points.check_dimension raised exception on valid dimensions")


    def test_check_2D(self):

        try: 
            utils.check_2D(self.img)
        except ValueError:
            self.fail("Points.check_2D raised exception on valid dimensions")
        
        
        with self.assertRaises(ValueError) as context:
            utils.check_2D(self.array3d)
        self.assertTrue("Array ndim: 3 isn't equal to 2" in str(context.exception))

        with self.assertRaises(ValueError) as context:
            utils.check_2D(self.array1d)
        self.assertTrue("Array ndim: 1 isn't equal to 2" in str(context.exception))


        types=[2,None, (0,), [10],]
        for type in types:
            with self.assertRaises(TypeError) as context:
                utils.check_2D(type)
            self.assertTrue("Passed array is not a numpy ndarray" in str(context.exception))

    def test_clip_to_uint(self):
        pass


