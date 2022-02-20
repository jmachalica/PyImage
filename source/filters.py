import numpy as np
from pyparsing import col
from .utils import check_2D, check_dimension

def is_in_edge_range(image_shape, coords, filter_size):
    y,x= coords
    filter_size =filter_size//2

    print(x,y,filter_size)
    return (x-filter_size)<-1 or (x+filter_size) > image_shape[1] or (y-filter_size)<-1 or (y+filter_size) > image_shape[0]



def convolve(arr1, arr2):
    return np.sum(np.multiply(arr1,arr2))

def filter_image(image,filter, egde=""): # 3x3 5x5 array
    check_2D(image)

    filter_row_size, filter_col_size =filter.shape 
    row_n = image.shape[0] - filter_row_size-1
    col_n = image.shape[1] - filter_col_size-1

    filtered=np.zeros((row_n, col_n) )

    for row_i in range(row_n):
        for col_i in range(col_n):
            current_arr= image[row_i:row_i+filter_row_size,col_i:col_i+filter_col_size]
            filtered[row_i][col_i]= convolve(current_arr,filter)

    return filtered


        
def _median(arr):
    return int(np.median(arr))
    
def _min(arr):
    return np.min(arr) 
def _max(arr):
    return np.max(arr) 

def _mean(arr):
    return np.mean(arr) 

def _diff(arr):
    return _max(arr) - _min(arr)

def _filter_nonlinear(image, shape,function):
    
    check_2D(image)
    filter_row_size, filter_col_size =shape
    row_n = image.shape[0] - filter_row_size-1
    col_n = image.shape[1] - filter_col_size-1

    filtered=np.zeros((row_n, col_n) )

    for row_i in range(row_n):
        for col_i in range(col_n):
            current_arr= image[row_i:row_i+filter_row_size,col_i:col_i+filter_col_size]
            filtered[row_i][col_i]= function(current_arr)

    return filtered
    

def medfilt(image,shape):
    return _filter_nonlinear(image,shape,_median)
    


def minfilt(image,shape):
    return _filter_nonlinear(image,shape, _min)
    
def maxfilt(image,shape):
    return _filter_nonlinear(image,shape,_max)

def rangefilt(image,shape):
    return _filter_nonlinear(image,shape,_diff)

def meanfilt(image,shape):
    return _filter_nonlinear(image,shape,_mean)