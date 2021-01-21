from abaqus import *
from abaqusConstants import *
import random

if mdb.models.has_key("Model-1"):
    myModel = mdb.models["Model-1"]
else:
    myModel = mdb.Model(name="Model-1",modelType=STANDARD_EXPLICIT)

# initial variables
length = 100
width = 50
height = 40

# create part
myPart = myModel.Part(name="Part-aggregate",dimensionality=THREE_D,type=DEFORMABLE_BODY)

# information of aggregate
number = 1000

def interact(points, center):
    sign = True
    for point in points:
        if sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2 + (point[2] - center[2])**2) < (center[3]+point[3]):
            sign = False
            break
    return sign

centers = []
for num in range(number):
    radius = random.uniform(2,10)
    center = [random.uniform(radius,length-radius),random.uniform(radius,width-radius),random.uniform(radius,height-radius),radius]
    if len(centers) == 0:
        centers.append(center)
    else:
        if interact(centers,center):
            centers.append(center)

print len(centers)

for center in centers:
    points = []
    for i in range(4):
        angle = random.uniform(0+1.57*i, 1.57*(i+1))
        x = center[0] + radius*sin(angle)
        y = center[1] + radius*cos(angle)
        z = center[2]
        points.append((x,y,z))
    points.append(points[0])

    for index in [1, -1]:
        angle2 = random.uniform(0, 2*3.1415926)
        angle3 = random.uniform(0, 0.785)
        x = center[0] + radius*sin(angle3)*cos(angle2)
        y = center[1] + radius*sin(angle3)*cos(angle2)
        z = center[2] + index*radius*cos(angle3)
        for i in range(4):
            wire = myPart.WirePolyLine(mergeType = SEPARATE,meshable = ON,points = (points[i],points[i+1],(x,y,z),points[i]))
            edges = myPart.getFeatureEdges(name=wire.name)
            myPart.CoverEdges(edgeList=edges, tryAnalytical=True)



