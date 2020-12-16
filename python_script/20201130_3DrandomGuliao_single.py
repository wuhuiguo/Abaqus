
from abaqus import *
from abaqusConstants import *
import random

#size of guliao
diameter = 10
#number of guliao
number = 100

#size of base
length = 100
width = 100
height = 100


#create base
myModel = mdb.models["Model-1"]
mysketch_1 = myModel.ConstrainedSketch(name='mysketch_1', sheetSize=200.0)
mysketch_1.rectangle(point1=(0.0, 0.0), point2=(length, width))
myPart = myModel.Part(name='Part-Base', dimensionality=THREE_D, type=DEFORMABLE_BODY)
myPart.BaseSolidExtrude(sketch=mysketch_1, depth=height)
del mysketch_1

#create ball
partName = "Part-Ball-{}".format(diameter)
mysketch_2 = myModel.ConstrainedSketch(name='mysketch_2', sheetSize=200.0)
mysketch_2.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
curve = mysketch_2.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(diameter/2.0, 0.0))
mysketch_2.autoTrimCurve(curve1=curve, point1=(-diameter/2.0, 0.0))
mysketch_2.Line(point1=(0.0, diameter/2.0), point2=(0.0, -diameter/2.0))
myPart2 = myModel.Part(name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
myPart2.BaseSolidRevolve(sketch=mysketch_2, angle=360.0, flipRevolveDirection=OFF)
del mysketch_2

#interaction judge
def interCheck(point,center,radius1,radius2):
    sign = True
    for p in center:
        if sqrt((point[0]-p[0])**2+(point[1]-p[1])**2+(point[2]-p[2])**2) <= (radius1+radius2):
            sign = False
            break
    return sign

# caculate diameter
count = 0
center10 = []
radius = diameter/2.0

while True:
    disX = random.uniform(radius, length-radius)
    disY = random.uniform(radius, width-radius)
    disZ = random.uniform(radius, height-radius)
    if len(center10)==0:
        center10.append([disX,disY,disZ])
    else:
        if interCheck([disX,disY,disZ],center10,radius,radius):
            center10.append([disX,disY,disZ])
    count += 1
    if len(center10)==number:
        break
    elif count >= float(length*width*height)/diameter**3:
        break
    else:
        pass

#translate ball
myAssembly = myModel.rootAssembly
for index in range(len(center10)):
    myAssembly.Instance(name='Part-Ball-{}-{}'.format(diameter,index), part=myModel.parts["Part-Ball-{}".format(diameter)], dependent=ON)
    myAssembly.translate(instanceList=('Part-Ball-{}-{}'.format(diameter,index),), vector=tuple(center10[index]))


