from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random

#initial variables
point_number = 250
length = 250
width = 50

points = np.array([[random.uniform(0,length*1.2), random.uniform(0,width*1.2)] for i in range(point_number)])

vor = Voronoi(points)#create instance
vertices = vor.vertices
edges = vor.ridge_vertices

# create base
myModel = mdb.models["Model-1"]
mySketch1 = myModel.ConstrainedSketch(name='sketch1', sheetSize=200.0)
mySketch1.rectangle(point1=(0.0, 0.0), point2=(length, width))
myPart = myModel.Part(name='Part-voronoi', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY )
myPart2 = myModel.Part(name="Part-analys", dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY )
myPart.BaseShell(sketch=mySketch1)
myPart2.BaseShell(sketch=mySketch1)

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


# getArea
myFaces = myPart.faces
area = []
for i in range(len(myFaces)):
    area_size = myFaces[i].getSize()
    area.append([i,area_size])
area = np.array(area)
sort = np.lexsort(area.T)[::-1]

face1 = []
face2 = []
face3 = []
total_area = 0
#create Set
for i in sort:
    total_area += area[i,1]
    if total_area <= 0.2*length*width:
        face1.append(i)
    elif total_area <= 0.5*length*width:
        face2.append(i)
    else:
        face3.append(i)

for faces in [face1,face2,face3]:
    set_name = "Set-{}".format([face1,face2,face3].index(faces))
    for i in faces:
        if faces.index(i)==0:
            face = myFaces[i:i+1]
        else:
            face += myFaces[i:i+1]
    myPart.Set(faces = face,name=set_name)

