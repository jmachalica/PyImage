import unittest
from unittest import mock
from unittest.mock import patch
from source import points
import numpy as np
class TestPoints(unittest.TestCase):


    def setUp(self) -> None:
        super().setUp()
        self.img=np.ones((10,10))
        self.img2= np.ones((11,11))

    
   
    def test_check_number(self):
        
        with self.assertRaises(ValueError) as context:
            points.check_number('1')
        self.assertTrue('Value is not a number' in str(context.exception))

        with self.assertRaises(ValueError) as context:
            points.check_number((1,))
        self.assertTrue('Value is not a number' in str(context.exception))

        try: 
            points.check_number(1)
        except ValueError:
            self.fail("Points.check_number raised exception on int")

        try: 
            points.check_number(10.5)
        except ValueError:
            self.fail("Points.check_number raised exception on float")


    def test_validate(self):
       
        value=2


    def test_add(self):
    
        self.assertEqual( (points.add(self.img,10) == self.img+10).all()   ,True  ) 

    def test_multiply(self):
        result=points.image_multiply(self.img, 20)
        self.assertEqual( ( result != self.img *20 ).all()   , True )

        result=points.image_multiply(self.img, -20)
 
        self.assertEqual( (result==0).all() , False )

    def test_substract_images(self):
        
        img3= self.img.copy()

        try: 
            result=points.substract_images(self.img, img3)
        except ValueError:
            self.fail("Exception raised on same shape")

        

        self.assertEqual( (result==0).all()   ,True  )
        self.assertEqual( result.shape,img3.shape )
        self.assertEqual( result.shape,self.img.shape )

        with self.assertRaises(ValueError) as context:
            points.substract_images(self.img, self.img2)
        self.assertTrue('Images have different shape' in str(context.exception))

    
    def test_gamma_correction(self):
        result=points.gamma_correction(self.img,1)   
        self.assertEqual(( result ==1).all(), True )


        result=points.gamma_correction(self.img,-1)
        self.assertEqual(( result ==1).all(), True )


        image=self.img.copy()*2
        result=points.gamma_correction(image,2)
        self.assertEqual(( result ==4).all(), True )

        result=points.gamma_correction(image,2)
        self.assertEqual(( result ==4).all(), True )

        
        result=points.gamma_correction(image,1/2)
        self.assertEqual( (result == 1).all(), True )

        image=self.img*255
        result=points.gamma_correction(image,1/2)
        self.assertEqual( (result == 15).all(), True )

    def test_binarize_image_exceptions(self): 
       
        image=self.img.copy()
        image[:,:]=128


        # check valid
        valid= ["lower","upper","both","histeresis"]
        for method in valid:
            try: 
                points.binarize_image(image,10 , btype = method)
            except ValueError:
                self.fail(f"Exception raised on valid method {method}")
        
        try: 
            points.binarize_image(image,20.7 , btype = method)
        except ValueError:
            self.fail(f"Exception raised on valid threshold")
        

        with self.assertRaises(ValueError) as context:
            points.binarize_image(image,None)
            
        self.assertTrue('Value is not a number' in str(context.exception))


        with self.assertRaises(ValueError) as context:
            points.binarize_image(image,'a')
            
        self.assertTrue('Value is not a number' in str(context.exception))
        
    


    def test_binarize_image_lower(self):
        image=self.img.copy()
        image[:,:]=128

       
        result=points.binarize_image(image,129)
        self.assertTrue( (result==0).all())
       
        result=points.binarize_image(image,128)
        self.assertTrue( (result==0).all())

        result=points.binarize_image(image,127)
        self.assertTrue( (result==1).all())


        image[:5,:5]=128
        result=points.binarize_image(image,129)
        self.assertEqual( np.count_nonzero(result !=0 ), 0)

        image[:5,:5]=128
        result=points.binarize_image(image,128)
        self.assertEqual( np.count_nonzero(result !=0 ), 100)

        image[:5,:5]=128
        result=points.binarize_image(image,127)
        self.assertEqual( np.count_nonzero(result !=0 ), 25)

    def test_binarize_image_upper(self):
        image=self.img.copy()
        image[:,:]=128

       
        result=points.binarize_image(image,129, btype='upper')
        self.assertTrue( (result==0).all())
       
        result=points.binarize_image(image,128)
        self.assertTrue( (result==0).all())

        result=points.binarize_image(image,127)
        self.assertTrue( (result==1).all())


        image[:5,:5]=128
        result=points.binarize_image(image,129)
        self.assertEqual( np.count_nonzero(result !=0 ), 0)

        image[:5,:5]=128
        result=points.binarize_image(image,128)
        self.assertEqual( np.count_nonzero(result !=0 ), 100)

        image[:5,:5]=128
        result=points.binarize_image(image,127)
        self.assertEqual( np.count_nonzero(result !=0 ), 25)




if __name__=='__main__':
    unittest.main()