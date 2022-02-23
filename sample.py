import numpy as np
from matplotlib import image

from matplotlib import pyplot
from source.conversion import rgb_to_gray
from source.edge_detection import edge
from source.points import *
from source.geometrical import *
from source.filters import *
import source.built_in_filters as filters
from source.morphological import dilation, erosion, opening,closing
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


img = image.imread("./resources/sample_images/lena_color.tiff")



gray=rgb_to_gray(img)

# show_img_effect(img,gray,cmap_after='gray')

# img=add(gray, -200)
# show_img_effect_gray(gray,img)

# img=image_multiply(gray,2)
# print(img)
# show_img_effect_gray(gray,img,diff=True)

# gamma1=gamma_correction(gray,2)
# gamma2=gamma_correction(gray,0.25)

# show_img_effect_gray(gray,gamma1,True)
# show_img_effect_gray(gray,gamma2,True)
# bin=binarize_image(gray,120)

# show_img_effect_gray(gray,bin)
# bin=binarize_image(gray,120, btype='upper')
# show_img_effect_gray(gray,bin)



# padded=padd_image(gray,-100)
# show_img_effect_gray(gray,padded)

# padded=padd_image(gray,(100,100))
# show_img_effect_gray(gray,padded)




# img_filtered=filter_image(gray,filters.blur_box)
# show_img_effect_gray(gray,img_filtered)

# img_filtered=filter_image(gray,filters.blur_gaussian)
# show_img_effect_gray(gray,img_filtered)


# img_filtered=filter_image(gray,filters.sharpen)
# show_img_effect_gray(gray,img_filtered)


# img_filtered=filter_image(gray,filters.sobel_vertical)
# show_img_effect_gray(gray,img_filtered)



# img_filtered=edge(gray)
# show_img_effect_gray(gray,img_filtered)

img_filtered=closing(gray,size=(3,3))
show_img_effect_gray(gray,img_filtered)