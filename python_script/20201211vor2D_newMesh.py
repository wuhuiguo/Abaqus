from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random

#initial variables
point_number = 150
length = 50
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


# mesh analysis Part

myPart2.seedPart(size=min(length,width)/100.0, deviationFactor=0.1, minSizeFactor=0.1)
myPart2.generateMesh()

myFaces = myPart.faces
myNodes = myPart2.nodes
myElement = myPart2.elements

# create void list
element_number = []
for i in range(len(myFaces)):
    element_number.append([])

for element in myElement:
    points = []
    for index in element.connectivity:
        points.append(list(myNodes[index].coordinates))
    center = np.array(points).mean(axis=0)
    index = myFaces.findAt(center, ).index
    for i in range(len(myFaces)):
        if index == i:
            element_number[i].append(element.label-1)

# create element set
for set_element in element_number:
    element = myElement[set_element[0]:set_element[0]+1]
    for i in range(1, len(set_element)):
        element += myElement[set_element[i]:set_element[i]+1]
    myPart2.Set(elements=element, name="Set-{}".format(element_number.index(set_element)))



