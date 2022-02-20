
import numpy as np

from .utils import check_dimension, check_dtype, convert_dtype


def rotate(image, angle):
    pass

def _padd_column(image,size):



    curr_shape=image.shape
    padding=np.zeros((curr_shape[0], abs(size)))

    if size<0:
        image=np.hstack((padding,image))
        return image
        
    else:
        image=np.hstack((image,padding))
        return image


def _padd_row(image,size):


    curr_shape=image.shape
    padding=np.zeros((abs(size), curr_shape[1]))

    if size<0:
        image=np.vstack((padding,image))
        return image
        
    else:
        image=np.vstack((image,padding))
        return image








def padd_image(image, size):
    check_dimension(image, 2)
    new_image=np.copy(image)
    curr_size = image.shape
   
    if isinstance(size, int):
        new_image=_padd_row(new_image,size)

    elif isinstance(size, tuple):
        if len(size)==2:
            new_image=_padd_column(new_image,size[1])
            new_image=_padd_row(new_image,size[0])

        else:
            raise ValueError()
    else:
        raise ValueError
    
    return new_image
