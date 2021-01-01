from abaqus import *
from abaqusConstants import *
import random

# initial variables
length = 100 # length of base
width = 50 # width of base

if mdb.models.has_key("Model-1"):
    myModel = mdb.models["Model-1"]
else:
    myModel = mdb.Model(name="Model-1",modelType=STANDARD_EXPLICIT)

mySketch = myModel.ConstrainedSketch(name="sketch-1", sheetSize=200)
myPart = myModel.Part(name="part-base", dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)

mySketch.rectangle(point1=(0, 0), point2=(length, width))
myPart.BaseShell(sketch=mySketch)

# function of interaction judgement
def interact(center, round):
    sign = True
    for each_center in center:
        if (round[0]-each_center[0])**2+(round[1]-each_center[1])**2 - (each_center[2]+round[2])**2 <= 0:
            sign = False
            break
    return sign

# random variables
mySketch2 = myModel.ConstrainedSketch(name="sketch-partition", sheetSize=200)

center = []

for i in range(10000):
    radius = random.uniform(0.5, 4) # size of guliao(aggregate)
    x = random.uniform(radius, length-radius) # x coordinate of round
    y = random.uniform(radius, width-radius) # y coordinate of round
    if len(center)==0:
        center.append([x, y, radius])
    elif interact(center, [x, y, radius]):
        center.append([x, y, radius])
    else:
        pass

for each_center in center:
    x = each_center[0]
    y = each_center[1]
    radius = each_center[2]
    mySketch2.ConstructionCircleByCenterPerimeter(center=(x, y), point1=(x+radius, y))

    edge_num = random.randint(4, 7) # edge of aggregate
    angle = [] # save points in round
    for i in range(edge_num):
        angle.append(random.uniform(2*3.1415926*i/edge_num, 2*3.1415926*(i+1)/edge_num))

    coord = [] # caculate coordinates of aggregate
    for each_angle in angle:
        px = x + radius*cos(each_angle)
        py = y + radius*sin(each_angle)
        coord.append([px, py])

    for i in range(edge_num-1): # using Line function to draw aggregate
        mySketch2.Line(point1=tuple(coord[i]), point2=tuple(coord[i+1]))
    mySketch2.Line(point1=tuple(coord[0]), point2=tuple(coord[-1]))


# partition face
myPart.PartitionFaceBySketch(faces=myPart.faces[:], sketch=mySketch2)


