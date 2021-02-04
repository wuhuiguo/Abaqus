from scipy.spatial import *
from random import *
import matplotlib.pyplot as plt
import numpy as np

point_number = 200
length = 200
width = 100

# 原来的解法
# points = [[uniform(0, length), uniform(0, width)] for i in range(point_number)]

# 方法一
# points = []
# x = np.sqrt(length*width/point_number)
# for i in range(int(length/x)+2):
#     for j in range(int(width/x)+2):
#         points.append([i*x, j*x])
# points = np.array(points)

# 方法二
# points = []
# x = np.sqrt(2*np.sqrt(3)*length*width/point_number)
# print(x,int(length/(x/2))+2)
# for i in range(int(length/(x/2))+2):
#     for j in range(int(width/(x/np.sqrt(3)))+2):
#         if i%2 == 0:
#             points.append([i*x/2, j*x/np.sqrt(3)])
#         else:
#             points.append([i*x/2, (j+0.5)*x/np.sqrt(3)])
# 方法三
points = []
x = np.sqrt(length*width/point_number)
for i in range(int(length/x)+2):
    for j in range(int(width/x)+2):
        px = uniform(i*x, (i+1)*x)
        py = uniform(j*x, (j+1)*x)
        points.append([px, py])

vor = Voronoi(points)
voronoi_plot_2d(vor)
plt.show()
