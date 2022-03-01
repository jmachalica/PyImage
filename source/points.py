import numpy as np
from .utils import check_2D, check_dimension, check_dtype, convert_dtype, clip_to_uint


def check_number(value):

    if not (isinstance(value, float) or isinstance(value,int) ):
        raise ValueError("Value is not a number")


def validate(image,value):
    check_dimension(image,2)
    dtype= image.dtype

    check_number(value)

    if not check_dtype(dtype):
        print("Changing dtype")
        image=convert_dtype(dtype, np.uint8)

    return image


def add(image, value):

    validate(image,value)
    image=np.copy(image)
    image=image.astype('float')
    image+=value    
    return clip_to_uint(image)


    
    
def image_multiply(image,value):

    validate(image,value)
    image=np.copy(image)
    image=image.astype('float')
    image*=value
    return clip_to_uint(image)





def substract_images(image1, image2):
    if not image1.shape == image2.shape:
        raise ValueError("Images have different shape")

    image1=image1.astype('float')
    image2=image2.astype('float')

    return clip_to_uint(image1-image2)


def gamma_correction(img,gamma):
    image=np.copy(image)
    return clip_to_uint(img**gamma)


def normalize_image(image):
    image=np.copy(image)
    min=np.min(image)
    max=np.max(image)

    image=image.astype('float')
    image=255/(max-min) * (image - min)
    return np.clip(image, 0,255)


def binarize_image(image,  threshold, btype="lower", threshold2=None, middle_value=None):
    check_dimension(image,2)

    #TODO check threshold
    image=np.copy(image)
    if btype not in ["lower","upper","both","histeresis"]:
        raise ValueError()

    if btype == "lower":
        upper_id= image>threshold
        image[upper_id]=255
        image[~upper_id]=0
        
    elif btype=='upper':
        upper_id= image<threshold
        image[upper_id]=255
        image[~upper_id]=0
    elif btype == 'both':
        #check threshold2
        upper_id= image> threshold2 
        lower_id=image< threshold 
   

        if middle_value is not None:
            middle_id= np.argwhere((image<threshold2) & (image> threshold))
            image[middle_id]=middle_value

        image[upper_id]=255
        image[lower_id]=0

    return image

        

def negate_binary(image):
    check_2D(image)
    cp=image.copy()
    indexes=image==0
    cp[indexes]=255
    cp[~indexes]=0
    return cp
