import numpy as np
from matplotlib import image

from matplotlib import pyplot
from source.conversion import rgb_to_gray
from source.edge_detection import edge
from source.points import *
from source.geometrical import *
from source.filters import *
import source.built_in_filters as filters
from source.morphological import dilation, erosion, find_extrema, opening,closing, prune, skeleton

def show_img_effect(before,after, cmap_before=None,cmap_after=None, diff=False):

    if diff:
        fig,(ax1,ax2,ax3)=pyplot.subplots(1,3)
    else:
        fig,(ax1,ax2)=pyplot.subplots(1,2)


    ax1.imshow(before,cmap=cmap_before)
    ax2.imshow(after,cmap=cmap_after)

    if diff:
        ax3.imshow(substract_images(before,after), cmap='gray')
    pyplot.show()

def show_img_effect_gray(before,after, diff=False):

    show_img_effect(before,after,cmap_before='gray',cmap_after='gray',diff=diff)


img = image.imread("./resources/sample_images/binary_shapes.jpg")
img=rgb_to_gray(img)
img=binarize_image(img, 40)

rotated=rotate_image(img,90 )
show_img_effect_gray(img,rotated)

