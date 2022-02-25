

from matplotlib import transforms
import numpy as np
from source.geometrical import rotate_image

from source.points import binarize_image, substract_images
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



def find_extrema(image,threshold, min=True, size=None, structure=None,origin=None):
    
    if min:
        transformed= opening(image,size,structure,origin)
    else:
        transformed= closing(image,size,structure,origin)

    transformed=substract_images(image,transformed)


    return binarize_image(transformed,threshold, btype="lower" )


def calc_padding(structure,origin):
    row,col= structure.shape

    row_origin, col_orogin=origin

    d_row_p=structure.shape[0]-origin[0]-1
    d_row_n= structure.shape[0]- d_row_p -1
    d_col_p=structure.shape[1]-origin[1]-1
    d_col_n= structure.shape[1]- d_col_p-1

    return (d_row_p, d_row_n, d_col_p,d_col_n)


def structure_fit(structure,image_slice, background_level):
    structure=structure.flatten()
    image_slice=image_slice.flatten()

    stacked=np.column_stack((structure,image_slice))

    for struct_el,img_el in stacked:
        if struct_el == np.nan:
            continue
        elif struct_el ==1:
            if (struct_el > background_level) != (img_el>background_level):
                return False
        else:
            if (struct_el < background_level) != (img_el<background_level):
                return False
         
        
    return True
        
def imageChanged(image,image2):

    return True

def prune(image,structure,rotate,origin, iterations=None,stop=False,padding_mode='reflect',background=None):

    check_2D(image)
    if iterations == None:
        iterations=1
    
    d_row_p,d_row_n, d_col_n,d_col_p=calc_padding(structure,origin)

    padded=np.pad(image, ((d_row_n, d_row_p),(d_col_n,d_col_p)), mode=padding_mode )
    padded=padded.astype('float32')
    
    row_n = padded.shape[0] 
    col_n = padded.shape[1] 

    previous=padded

    for i in range(iterations):

        curr_image=previous.copy()

        for row_i in range(d_row_n,row_n-d_row_p):
            for col_i in range(d_col_n,col_n-d_col_p):
         

                image_slice= curr_image[row_i- d_row_n:row_i+d_row_p+1 , col_i-d_col_n: col_i+d_col_p+1]
                
                if background==None:
                    background=np.mean(previous)

                if structure_fit(structure, image_slice,background):
            
                    curr_image[row_i][col_i]=0

                    

     
        if not imageChanged(curr_image,previous): 
            if(i< iterations-1):
                print(f"Prunning stopped early in iteration: {i}")
            break
            
        if rotate:
            structure=rotate_image(structure,90)

    
    return clip_to_uint(curr_image)
