import numpy as np

identity=np.ones((3,3))
ridge1=np.array([[0, -1, 0], [-1, 4, -1],[0,-1,0]])
ridge2=np.array([[-1, -1, -1], [-1, 8, -1],[-1,-1,-1]])
sharpen=np.array([[0, -1, 0], [-1, 5, -1],[0,-1,0]])
blur_box=identity/sum(identity)
blur_gaussian=np.array([[1, 2, 1], [2, 4, 2],[1,2,1]])/ 16
previtt_horizontal=np.array([[1, 1, 1], [0, 0, 0],[-1,-1,-1]])


previtt_vertical=np.tile (np.array([1, 0, -1]), (3,1) )
sobel_horizontal=  np.array([[1, 2, 1], [0, 0, 0],[-1,-2,-1]])
sobel_vertical=  np.array([[1, 0, -1], [2, 0, -2],[1,0,-1]])


skeleton= np. array([[np.nan,0,np.nan],[np.nan, 1,np.nan],np.ones(3) ])

#  np.array([[-1, -1, -1], [-1, 8, -1],[-1,-1,-1]])
#  np.array([[-1, -1, -1], [-1, 8, -1],[-1,-1,-1]])