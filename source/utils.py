
import numpy as np

VALID_DTYPES= (np.uint8, np.float64)

def check_dimension(array,ndim):


    array=np.asanyarray(array)

    if isinstance(ndim,int):
        ndim=[ndim]
    if array.size == 0:
        raise ValueError()
    if array.ndim not in ndim:
        raise ValueError()


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
        raise ValueError()
    
 
def clip_to_uint(array):
    clipped=np.clip(array,0,255)
    return clipped.astype(np.uint8)

    

