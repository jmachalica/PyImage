
import numpy as np
from .utils import check_2D, check_dimension, check_dtype, clip_to_uint, convert_dtype

def _check_origin_range(origin, structure_shape):
    for i in range(len(origin)):
        if origin[i] <0 or origin >= structure_shape[i]:
            raise ValueError()
    
def _min_max_filter(image,structure,origin, min):
    
    d_row_p=structure.shape[0]-origin[0]-1
    d_row_n= structure.shape[0]- d_row_p -1
    d_col_p=structure.shape[1]-origin[1]-1
    d_col_n= structure.shape[1]- d_col_p-1

    padded=np.pad(image, ((d_row_n, d_row_p),(d_col_n,d_col_p)), mode='reflect' )
    padded=padded.astype('float32')

    filtered=np.zeros( image.shape,dtype='float32')
    
    row_n = padded.shape[0] 
    col_n = padded.shape[1] 

    for row_i in range(d_row_n,row_n-d_row_p):
        for col_i in range(d_col_n,col_n-d_col_p):

            image_curr= padded[row_i- d_row_n:row_i+d_row_p+1 , col_i-d_col_n: col_i+d_col_p+1]
         
            if min:
                function=np.min
            else :
                function=np.max

            filtered[row_i- d_row_n, col_i- d_col_n]=function(image_curr-structure)
        
    return clip_to_uint(filtered) 
          



def validate_morphological(func):
    def wrapper(image, size= None,structure=None,origin=None):
        if size is None and structure is None:
            raise ValueError()

        elif size is not None and structure is not None:
            raise ValueError
        check_2D(image)

        if structure is not None:
            structure = np.asarray(structure)
        else:
            structure= np.zeros( size )
        
        image=np.asarray(image)



        if origin is not None:
            _check_origin_range(origin,structure.shape)
        else: 
            origin = (structure.shape[0]//2, structure.shape[1]//2)

        return func(image,size,structure,origin)

    
    return wrapper


def _erosion(image, size,structure,origin):
    
    return _min_max_filter(image,structure, origin, min=True)
    


def _dilation(image, size,structure,origin):

    return _min_max_filter(image,structure, origin, min=False)
    

@validate_morphological
def erosion(image, size= None,structure=None,origin=None):
    return _erosion(image,size,structure,origin)

@validate_morphological
def dilation(image, size= None,structure=None,origin=None):
    return _dilation(image,size,structure,origin)


@validate_morphological
def opening(image, size= None,structure=None,origin=None):
     eroded=_erosion(image,size,structure,origin)
     return _dilation(eroded,size,structure,origin)

 
@validate_morphological
def closing(image, size= None,structure=None,origin=None):
     dilated=_dilation(image,size,structure,origin)
     return _erosion(dilated,size,structure,origin)

