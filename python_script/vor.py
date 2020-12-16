
from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random

#initial variables
point_number = 420
length = 200
width = 100

points = [[random.uniform(0,length*1.3),random.uniform(0,width*1.3)] for i in range(point_number)]
vor = Voronoi(points)#create instance
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

for edge in np.array(edges):
    if np.all(edge>0):
        mySketch2.Line(point1=tuple(vertices[edge[0]]), point2=tuple(vertices[edge[1]]))

myPart.PartitionFaceBySketch(faces=myPart.faces[:], sketch=mySketch2)
















