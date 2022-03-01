

from matplotlib import transforms
import numpy as np
from source.geometrical import rotate_image,padd_image, rotate_image_90
from source.points import binarize_image, substract_images
from .utils import check_2D, check_dimension, check_dtype, clip_to_uint, convert_dtype
import source.built_in_filters as built_in_filters



def _check_origin_range(origin, structure_shape):
    for i in range(len(origin)):
        if origin[i] < 0 or origin >= structure_shape[i]:
            raise ValueError()


def calc_padding(structure, origin):

    d_row_p = structure.shape[0]-origin[0]-1
    d_row_n = structure.shape[0] - d_row_p - 1
    d_col_p = structure.shape[1]-origin[1]-1
    d_col_n = structure.shape[1] - d_col_p-1

    return (d_row_p, d_row_n, d_col_p, d_col_n)

def padd_image_to_structure(image,structure,origin,padding_mode='reflect',padding=False):
    d_row_p, d_row_n, d_col_n, d_col_p = calc_padding(structure, origin)
    if padding:

        return padd_image(image, ((d_row_n, d_row_p),
                        (d_col_n, d_col_p)), mode=padding_mode), (d_row_p, d_row_n, d_col_n, d_col_p)
    else:
        return padd_image(image, ((d_row_n, d_row_p),
                        (d_col_n, d_col_p)), mode=padding_mode)


def _min_max_filter(image, structure, origin,function):

    padded, padding=padd_image_to_structure(image,structure[0],origin,padding=True)

    padded = padded.astype('float32')
    filtered = np.zeros(image.shape, dtype='float32')

    row_n = padded.shape[0]
    col_n = padded.shape[1]



    for row_i in range(padding[0], row_n-padding[1]):
        for col_i in range(padding[2], col_n-padding[3]):

            image_slice = padded[row_i - padding[0]:row_i +
                                padding[1]+1, col_i-padding[2]: col_i+padding[3]+1]

            if min:
                function = np.min
            else:
                function = np.max

            filtered[row_i - padding[0],col_i-padding[2]]= function(image_slice-structure)

    return clip_to_uint(filtered)


def validate_morphological(func):
    def wrapper(image, size=None, structure=None, origin=None):
        if size is None and structure is None:
            raise ValueError()

        elif size is not None and structure is not None:
            raise ValueError
        check_2D(image)

        if structure is not None:
            structure = np.asarray(structure)
        else:
            structure = np.zeros(size)

        image = np.asarray(image)

        if origin is not None:
            _check_origin_range(origin, structure.shape)
        else:
            origin = (structure.shape[0]//2, structure.shape[1]//2)

        return func(image, size, structure, origin)

    return wrapper


def _erosion(image,structure, origin):

    return _min_max_filter(image, structure, origin, min=True)


def _dilation(image,  structure, origin):

    return _min_max_filter(image, structure, origin, min=False)


@validate_morphological
def erosion(image, size=None, structure=None, origin=None):
    return _erosion(image, size, structure, origin)


@validate_morphological
def dilation(image, size=None, structure=None, origin=None):
    return _dilation(image, size, structure, origin)


@validate_morphological
def opening(image, size=None, structure=None, origin=None):
    eroded = _erosion(image, size, structure, origin)
    return _dilation(eroded, size, structure, origin)


@validate_morphological
def closing(image, size=None, structure=None, origin=None):
    dilated = _dilation(image, size, structure, origin)
    return _erosion(dilated, size, structure, origin)


def find_extrema(image, threshold, min=True, size=None, structure=None, origin=None):

    if min:
        transformed = opening(image, size, structure, origin)
    else:
        transformed = closing(image, size, structure, origin)

    transformed = substract_images(image, transformed)

    return binarize_image(transformed, threshold, btype="lower")




def structure_fit(structure, image_slice, background_level):
    structure = structure.flatten()
    image_slice = image_slice.flatten()

    stacked = np.column_stack((structure, image_slice))

    for struct_el, img_el in stacked:

        if np.isnan(struct_el):
            continue

        elif (struct_el == 1) != (img_el > background_level):
            return False

    return True


def imageChanged(image, image2):
    return np.any(image!=image2)
    
def _validate_structures_same_shape(structures):

    shape= structures[0].shape
    for structure in structures:
        if structure.shape != shape:
            raise ValueError()

def _convert_to_list(object):

    try:
        iter(object)
        return list(object)
    except TypeError:
        return [object]


def prune(image, structures, rotate, origin, iterations=1, stop=False, padding_mode='reflect', background=None):

    check_2D(image)
    structures=_convert_to_list(structures)
    _validate_structures_same_shape(structures)
  
    padded, padding=padd_image_to_structure(image,structure[0],origin,padding_mode,padding=True)


    padded = padded.astype('float32')
    row_n = padded.shape[0]
    col_n = padded.shape[1]
    previous = padded

    for i in range(iterations):

        for structure in structures:

            curr_image = previous.copy()

            for row_i in range(padding[0], row_n-padding[1]):
                for col_i in range(padding[2], col_n-padding[3]):

                    image_slice = previous[row_i - padding[0]:row_i +
                                        padding[1]+1, col_i-padding[2]: col_i+padding[3]+1]

                    if background == None:
                        background = np.mean(curr_image)
                        print(background)

                    if structure_fit(structure, image_slice, background):
                        curr_image[row_i][col_i] = 0
                    
            previous = curr_image

        if rotate:
            structure = [rotate_image_90(structure) for structure in structures ]
        if stop:
            if not imageChanged(curr_image, previous):
                if(i < iterations-1):
                    print(f"Prunning stopped early in iteration: {i}")
                break

       
    return clip_to_uint(curr_image)


def skeleton(image, structures=(built_in_filters.skeleton,), rotate=False, origin=(1, 1), iterations=1, stop=False, padding_mode='reflect', background_level=None):

    return prune(image, structures, rotate=rotate, origin=origin, iterations=iterations, stop=stop, padding_mode=padding_mode, background=background_level)
