import numpy as np
from .utils import check_dimension, check_dtype, convert_dtype, clip_to_uint


def rgb_to_gray(image):
    check_dimension(image,3)
    shape=image.shape

    image=    image.astype(np.float64)

    applied=np.apply_along_axis(lambda x: x[0] *0.299 + x[1]*0.587 + x[2]*0.114,2,image )

    return clip_to_uint(applied)
    
    
    
