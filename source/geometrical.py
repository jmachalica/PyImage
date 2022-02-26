import numpy as np
from .utils import check_2D, check_dimension

def _calc_rotation_point(x,y,angle,center):
    angle=np.radians(angle)
    cos=np.cos(angle)
    sin=np.sin(angle)
    x_diff= x-center[0 ]
    y_diff= y- center[1]

    return (cos*x_diff - sin * y_diff + center[0] ,sin*x_diff + cos * y_diff + center[1] )

def _is_in_image(image,point):
    col,row=point
    n_row,n_col=image.shape

    return row>=0 and row<n_row and col>=0 and col<n_col

def _interpolate(image,point):
    
    x_nearest= np.floor(point[0])
    x_nearest= (x_nearest, x_nearest+1)
    y_nearest= np.floor(point[1])
    y_nearest= (y_nearest, y_nearest+1)

    min=np.Infinity
    min_point=None
    point=np.asanyarray(point)
    for x in x_nearest:
        for y in y_nearest:
            point2=np.array((x,y))
            if not  _is_in_image(image,point2):
                continue
            dist=np.linalg.norm(point-point2)
            if dist< min:
                min=dist
                min_point=point2

    if min_point is None:
        return 0
    min_point=np.floor(min_point).astype(np.int0) 

    if not _is_in_image(image,min_point):
               return 0
               
    return image[min_point[1],min_point[0] ]



def rotate_image(image, angle):
    check_2D(image)
    nrow,ncol=image.shape
    center=( ncol//2,nrow//2) # x,y
    rotated=np.zeros(image.shape)

    for row_i in range(nrow):
        for col_i in range(ncol):
            input_point= _calc_rotation_point(col_i,row_i,-angle,center ) # inverse mapping
            rotated[row_i,col_i]=  _interpolate(image,input_point)
        
    return rotated


def rotate_image_90(image):
    return rotate_image(image,90)

def _padd_column(image,size):

    curr_shape=image.shape
    padding=np.zeros((curr_shape[0], abs(size)))

    if size<0:
        image=np.hstack((padding,image))
        return image
        
    else:
        image=np.hstack((image,padding))
        return image


def _padd_row(image,size):


    curr_shape=image.shape
    padding=np.zeros((abs(size), curr_shape[1]))

    if size<0:
        image=np.vstack((padding,image))
        return image
        
    else:
        image=np.vstack((image,padding))
        return image








def padd_image(image, size):
    check_dimension(image, 2)
    new_image=np.copy(image)
    curr_size = image.shape
   
    if isinstance(size, int):
        new_image=_padd_row(new_image,size)

    elif isinstance(size, tuple):
        if len(size)==2:
            new_image=_padd_column(new_image,size[1])
            new_image=_padd_row(new_image,size[0])

        else:
            raise ValueError()
    else:
        raise ValueError
    
    return new_image
