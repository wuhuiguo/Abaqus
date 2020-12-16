
from abaqus import *
from abaqusConstants import *
import random

myModel = mdb.models["Model-1"]
mysketch_1 = myModel.ConstrainedSketch(name='mysketch_1', sheetSize=200.0)
mysketch_1.rectangle(point1=(0.0, 0.0), point2=(100.0, 100.0))
myPart = myModel.Part(name='Part-Base', dimensionality=THREE_D, type=DEFORMABLE_BODY)
myPart.BaseSolidExtrude(sketch=mysketch_1, depth=100.0)
del mysketch_1

#create ball
for diameter in [1, 4, 10]:
    partName = "Part-Ball-{}".format(diameter)
    mysketch_2 = myModel.ConstrainedSketch(name='mysketch_2', sheetSize=200.0)
    mysketch_2.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    curve = mysketch_2.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(diameter/2.0, 0.0))
    mysketch_2.autoTrimCurve(curve1=curve, point1=(-diameter/2.0, 0.0))
    mysketch_2.Line(point1=(0.0, diameter/2.0), point2=(0.0, -diameter/2.0))
    myPart2 = myModel.Part(name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    myPart2.BaseSolidRevolve(sketch=mysketch_2, angle=360.0, flipRevolveDirection=OFF)
    del mysketch_2


#Assembly
myAssembly = myModel.rootAssembly
myAssembly.Instance(name='Part-Base', part = myModel.parts["Part-Base"], dependent=ON) #base

def interCheck(point,center,radius1,radius2):
    sign = True
    for p in center:
        if sqrt((point[0]-p[0])**2+(point[1]-p[1])**2+(point[2]-p[2])**2) <= (radius1+radius2):
            sign = False
            break
    return sign

# caculate diameter of 10mm
count = 0
center10 = []
radius = 5
while True:
    disX = random.uniform(radius, 100-radius)
    disY = random.uniform(radius, 100-radius)
    disZ = random.uniform(radius, 100-radius)
    if len(center10)==0:
        center10.append([disX,disY,disZ])
    else:
        if interCheck([disX,disY,disZ],center10,5,5):
            center10.append([disX,disY,disZ])
    count += 1
    if count >= 100:
        break

# caculate diameter of 4mm
count = 0
center4 = []
radius = 2
while True:
    disX = random.uniform(radius, 100-radius)
    disY = random.uniform(radius, 100-radius)
    disZ = random.uniform(radius, 100-radius)
    if len(center4) == 0:
        center4.append([disX,disY,disZ])
    else:
        if interCheck([disX,disY,disZ],center4, 2, 2):
            if interCheck([disX,disY,disZ],center10,2,5):
                center4.append([disX,disY,disZ])
    count += 1
    if count >= 200:
        break
# caculate diameter of 1mm
count = 0
center1 = []
radius = 0.5
while True:
    disX = random.uniform(radius, 100-radius)
    disY = random.uniform(radius, 100-radius)
    disZ = random.uniform(radius, 100-radius)
    if len(center1) == 0:
        center1.append([disX,disY,disZ])
    else:
        if interCheck([disX,disY,disZ],center1,0.5,0.5):
            if interCheck([disX,disY,disZ],center4, 0.5, 2):
                if interCheck([disX,disY,disZ],center10,0.5,5):
                    center1.append([disX,disY,disZ])
    count += 1
    if count >= 400:
        break

for index in range(len(center10)):
    myAssembly.Instance(name='Part-Ball-10-{}'.format(index), part=myModel.parts["Part-Ball-10"], dependent=ON)
    myAssembly.translate(instanceList=('Part-Ball-10-{}'.format(index),), vector=tuple(center10[index]))
for index in range(len(center4)):
    myAssembly.Instance(name='Part-Ball-4-{}'.format(index), part=myModel.parts["Part-Ball-4"], dependent=ON)
    myAssembly.translate(instanceList=('Part-Ball-4-{}'.format(index),), vector=tuple(center4[index]))
for index in range(len(center1)):
    myAssembly.Instance(name='Part-Ball-1-{}'.format(index), part=myModel.parts["Part-Ball-1"], dependent=ON)
    myAssembly.translate(instanceList=('Part-Ball-1-{}'.format(index),), vector=tuple(center1[index]))


