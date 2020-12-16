from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random

#initial variables
point_number = 120
length = 50
width = 50

points = np.array([[random.uniform(0,length), random.uniform(0,width)] for i in range(point_number)])

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

# asign random orientation
for i in range(len(myPart.faces)):
    # create material
    a,b,c = random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)
    myMaterial = myModel.Material(name='Material-{}'.format(i))
    myMaterial.UserMaterial(mechanicalConstants=(a,b,c ))
    # create section
    myModel.HomogeneousSolidSection(name='Section-{}'.format(i), material='Material-{}'.format(i), thickness=None)
    # asign material
    region = myPart.Set(faces = myPart.faces[i:i+1],name = "Set-{}".format(i))
    myPart.SectionAssignment(region = region, sectionName='Section-{}'.format(i), offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

