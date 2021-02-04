from abaqus import *
from abaqusConstants import *
import regionToolset
from scipy.spatial import *
import numpy as np
import random

#initial variables
point_number = 250
length = 150
width = 100

# origin method
# points = np.array([[random.uniform(0,length), random.uniform(0,width)] for i in range(point_number)])

# method 1
# points = []
# x = np.sqrt(length*width/point_number)
# for i in range(int(length/x)+2):
#     for j in range(int(width/x)+2):
#         points.append([i*x, j*x])
# points = np.array(points)

# method 2
# points = []
# x = np.sqrt(2*np.sqrt(3)*length*width/point_number)
# print(x,int(length/(x/2))+2)
# for i in range(int(length/(x/2))+2):
#     for j in range(int(width/(x/np.sqrt(3)))+2):
#         if i%2 == 0:
#             points.append([i*x/2, j*x/np.sqrt(3)])
#         else:
#             points.append([i*x/2, (j+0.5)*x/np.sqrt(3)])
# points = np.array(points)

# method 3
points = []
x = np.sqrt(length*width/point_number)
for i in range(int(length/x)+2):
    for j in range(int(width/x)+2):
        px = random.uniform(i*x, (i+1)*x)
        py = random.uniform(j*x, (j+1)*x)
        points.append([px, py])
points = np.array(points)


vor = Voronoi(points) #create instance
vertices = vor.vertices
edges = vor.ridge_vertices

# create base
myModel = mdb.models["Model-1"]
mySketch1 = myModel.ConstrainedSketch(name='sketch1', sheetSize=200.0)
mySketch1.rectangle(point1=(0.0, 0.0), point2=(length, width))
myPart = myModel.Part(name='Part-voronoi', dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
myPart.BaseShell(sketch=mySketch1)

#create voronoi
mySketch2 = myModel.ConstrainedSketch(name='__profile__',sheetSize=200, gridSpacing=10)
mySketch2.CircleByCenterPerimeter(center=(-61.49, 2.795), point1=(-44.72, -8.385))

# create limited edge
for edge in np.array(edges):
    if np.all(edge>0):
        mySketch2.Line(point1=tuple(vertices[edge[0]]), point2=tuple(vertices[edge[1]]))
# create infinite edge
center = points.mean(axis=0)
for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
    simplex = np.asarray(simplex)
    if np.any(simplex < 0):
        i = simplex[simplex >= 0]
        t = points[pointidx[1]] - points[pointidx[0]]
        t = t/np.linalg.norm(t)
        n = np.array([-t[1], t[0]])
        midpoint = points[pointidx].mean(axis=0)
        far_point = vertices[i] + np.sign(np.dot(midpoint - center, n))*n*100
        mySketch2.Line(point1=tuple(vertices[i[0]]), point2=tuple(far_point[0]))

# partition face
myPart.PartitionFaceBySketch(faces=myPart.faces[:], sketch=mySketch2)






