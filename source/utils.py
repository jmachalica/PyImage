
import numpy as np

VALID_DTYPES= (np.uint8, np.float64)

def check_dimension(array,ndim):

    if not isinstance(array,np.ndarray):
        raise TypeError("Passed array is not a numpy ndarray")

    if array.ndim != ndim:
        raise ValueError("Array ndim: {array.ndim} isn't equal to {ndim}")


def check_2D(array):
    return check_dimension(array,2)

def check_dtype(dtype):
    if dtype not in VALID_DTYPES:
        return False
    return True
    

def convert_dtype(image, new_dtype):
        
    dtype=image.dtype

    if dtype == new_dtype:
        return image

    if check_dtype(new_dtype):
        return image.astype(new_dtype)

    else:
        raise ValueError("Invalid new dtype")
    
 
def clip_to_uint(array):
    clipped=np.clip(array,0,255)
    return clipped.astype(np.uint8)

    

