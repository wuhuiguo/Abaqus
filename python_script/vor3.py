from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random

#initial variables
point_number = 300
#rve size
size = 50
# extend size
ex = 3
#create Voronoi
points = np.array([[random.uniform(0,size*ex),random.uniform(0,size*ex),random.uniform(0,size*ex)] for i in range(point_number)])
vor = Voronoi(points)
#get attributes
vertices = vor.vertices
edges = vor.ridge_vertices

for edge in edges:
    for number in edge:
        if number !=-1 :
            for coord in vertices[number]:
                if coord >= size*4 or coord <= 0:
                    edges[edges.index(edge)].append(-1)
                    break

face_points = []
for edge in np.array(edges):
    edge = np.array(edge)
    temp = []
    if np.all(edge >= 0):
            for i in edge:
                temp.append(tuple(vertices[i]))
            temp.append(vertices[edge[0]])
    if (len(temp)>0):
        face_points.append(temp)

#
myModel = mdb.models['Model-1']
myPart = myModel.Part(name='Part-vor3', dimensionality=THREE_D, type=DEFORMABLE_BODY)

for i in range(len(face_points)):
    wire = myPart.WirePolyLine(mergeType=SEPARATE, meshable=ON, points=(face_points[i]))
    face_edge = myPart.getFeatureEdges(name=wire.name)
    myPart.CoverEdges(edgeList = face_edge, tryAnalytical=True)

faces = myPart.faces[:]
myPart.AddCells(faceList = faces)


# cut Voronoi
#create core
myPart2 = myModel.Part(name='Part-core', dimensionality=THREE_D, type=DEFORMABLE_BODY)
mySketch2 = myModel.ConstrainedSketch(name="mysketch-2",sheetSize = 200)
mySketch2.rectangle(point1=(0,0), point2=(size,size))
myPart2.BaseSolidExtrude(sketch=mySketch2, depth=size)

#create base
myPart3 = myModel.Part(name='Part-base', dimensionality=THREE_D, type=DEFORMABLE_BODY)
mySketch3 = myModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)
mySketch3.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
curve = mySketch3.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(size*10,0.0))
mySketch3.Line(point1=(0.0, 10*size), point2=(0.0, -10*size))
mySketch3.autoTrimCurve(curve1=curve, point1=(-size*10,0.0))
myPart3.BaseSolidRevolve(sketch=mySketch3, angle=360.0, flipRevolveDirection=OFF)

# instance
myAssembly = myModel.rootAssembly
myAssembly.Instance(name='Part-base-1', part=myModel.parts["Part-base"], dependent=ON)
myAssembly.Instance(name='Part-core-1', part=myModel.parts["Part-core"], dependent=ON)
myAssembly.translate(instanceList=('Part-core-1', ), vector=(size*(ex-1)/2,size*(ex-1)/2,size*(ex-1)/2))
myAssembly.InstanceFromBooleanCut(name='Part-base-cut',instanceToBeCut=myAssembly.instances['Part-base-1'],
                                  cuttingInstances=(myAssembly.instances['Part-core-1'], ), originalInstances=DELETE)

# cut voronoi
myAssembly.Instance(name='Part-cut-1', part=myModel.parts["Part-base-cut"], dependent=ON)
myAssembly.Instance(name='Part-vor3-1', part=myModel.parts["Part-vor3"], dependent=ON)
myAssembly.InstanceFromBooleanCut(name='Part-vor3-cut',instanceToBeCut=myAssembly.instances['Part-vor3-1'],
                                  cuttingInstances=(myAssembly.instances['Part-cut-1'], ), originalInstances=DELETE)

for key in myAssembly.instances.keys():
    del myAssembly.instances[key]

for key in myModel.parts.keys():
    if key != "Part-vor3-cut":
        del myModel.parts[key]






