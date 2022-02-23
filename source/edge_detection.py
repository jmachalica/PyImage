
import numpy as np

from source.points import binarize_image
from .filters import *
from .built_in_filters import sobel_horizontal, sobel_vertical
# The process of Canny edge detection algorithm can be broken down to five different steps:

#     Apply Gaussian filter to smooth the image in order to remove the noise
#     Find the intensity gradients of the image
#     Apply gradient magnitude thresholding or lower bound cut-off suppression to get rid of spurious response to edge detection
#     Apply double threshold to determine potential edges
#     Track edge by hysteresis: Finalize the detection of edges by suppressing all the other edges that are weak and not connected to strong edges.

# Edges correspond to a change of pixels’ intensity. To detect it, the easiest way is to apply filters that highlight this intensity change in both directions: horizontal (x) and vertical (y) 


def get_neighbors_in_direction(image,i,j,direction):
                #angle 0
    try:
        if (0 <= direction  < 22.5) or (157.5 <= direction <= 180):
            n1= image[i, j+1]
            n2= image[i, j-1]
        #angle 45
        elif (22.5 <= direction < 67.5):
            n1 = image[i+1, j-1]
            n2 = image[i-1, j+1]
        #angle 90
        elif (67.5 <= direction < 112.5):
            n1 = image[i+1, j]
            n2 = image[i-1, j]
        #angle 135
        elif (112.5 <= direction < 157.5):
            n1 = image[i-1, j-1]
            n2 = image[i+1, j+1]
            
        return (n1,n2)

    except IndexError:
        raise IndexError

def non_max_supression(image,directions_radians):
    n_row,n_col=image.shape
    directions= np.degrees(directions_radians)
    directions[directions<0]+=180
    output= np.zeros(image.shape)

    for i in range(1,n_row-1): 
        for j in range(1, n_col-1):
            try:
                angle=directions[i,j]
                n1,n2=get_neighbors_in_direction(image,i,j,angle)
                value=image[i,j]

                if value>=n1 and value>= n2:
                    output[i][j]=value

            except IndexError:
                print("error")

    return output




def hysteresis(image,weak_value,strong_value):
    
    n_row,n_col=image.shape
    for i in range(n_row):
        for j in range(n_col):

            if image[i][j] == weak_value:
                strong_found=False
                for il in range(-1,2):
                    if not strong_found:

                        for jl in range(-1,2):
                            if il ==0 and jl ==0:
                                pass
                            try:
                                value = image[i+il][j+jl]
                                if value ==strong_value:
                                    strong_found=True
                                    break

                            except IndexError:
                                continue
                if strong_found:
                    image[i][j]=strong_value
                else:
                    image[i][j]=0


def edge(image,method='canny'):
    
    sobel_v=filter_image(image,sobel_vertical)
    sobel_h=filter_image(image, sobel_horizontal)

    G=np.hypot(sobel_h,sobel_v)
    G=G/ G.max() * 255 # normalization
    angles=np.arctan2(sobel_v,sobel_h)
    

    edges=non_max_supression(G,angles)


    high_thresh=0.1 * edges.max()
    low_thresh=0.05 *high_thresh

    binarized=binarize_image(edges,low_thresh,btype='both',threshold2= high_thresh, middle_value=30)
    hysteresis(binarized, 30,255)

    return binarized
    

def canny():
    pass