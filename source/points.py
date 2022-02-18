import numpy as np
from .utils import check_dimension, check_dtype, convert_dtype


def check_number(value):

    if not (isinstance(value, float) or isinstance(value,int) ):
        raise ValueError()


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
    image=np.clip(image,0,255)
    return image.astype('uint8')

    
    
def image_multiply(image,value):

    validate(image,value)
    image=np.copy(image)
    image=image.astype('float')
    image*=value
    image=np.clip(image,0,255)
    return image.astype('uint8')






def substract_images(image1, image2):
    if not image1.shape == image2.shape:
        raise ValueError()
    image1=image1.astype('float')
    image2=image2.astype('float')

    return np.clip(image1 - image2, 0,255)


def gamma_correction(img,gamma):
    image=np.copy(image)
    return img**gamma


def normalize_image(image):
    image=np.copy(image)
    min=np.min(image)
    max=np.max(image)

    image=image.astype('float')
    image=255/(max-min) * (image - min)
    return np.clip(image, 0,255)


def binarize_image(image,  threshold, btype="lower", threshold2=None):
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
        middle_id= np.argwhere(image<threshold2 and image> threshold)
        image[upper_id]=255
        image[lower_id]=0

    return image

        

