from abaqus import *
from abaqusConstants import *
import random

# create model
if mdb.models.has_key("Model-1"):
    myModel = mdb.models["Model-1"]
else:
    myModel = mdb.Model(name="Model-1", modelType=STANDARD_EXPLICIT)

# initial variable
# information of base
length = 100
width = 50
height = 20

# create base
myPart = myModel.Part(name="Part-base",dimensionality=THREE_D, type=DEFORMABLE_BODY)
mySketch = myModel.ConstrainedSketch(name="sketch-1", sheetSize=200)

mySketch.rectangle(point1=(0, 0), point2=(length, width))
myPart.BaseSolidExtrude(sketch=mySketch, depth=height)

# define interact of 
def interact_judgement(points, line, diameter):
    #
    c = line[0]
    d = line[1]
    #
    num = 50
    sign = True
    for point in points:
        a = point[0]
        b = point[1]
        #
        for i in range(num+1):
            mx = c[0] + (d[0] - c[0]) * i * (1. / num)
            my = c[1] + (d[1] - c[1]) * i * (1. / num)
            mz = c[2] + (d[2] - c[2]) * i * (1. / num)
            for j in range(num+1):
                nx = a[0] + (b[0] - a[0]) * j * (1. / num)
                ny = a[1] + (b[1] - a[1]) * j * (1. / num)
                nz = a[2] + (b[2] - a[2]) * j * (1. / num)
                # distance calculate
                distance = sqrt((mx-nx)**2+(my-ny)**2+(mz-nz)**2)
                if distance < diameter:
                    sign = False
                    break
            if not sign:
                break
        if not sign:
            break
    return sign

# information of fibre(xianwei)
fibre_length = 10
fibre_diameter = 1
fibre_num = 100
# create fibre
myPart2 = myModel.Part(name="Part-fibre", dimensionality=THREE_D, type=DEFORMABLE_BODY)


points = []
for i in range(fibre_num):
    # first point of fibre
    x = random.uniform(fibre_length, length-fibre_length)
    y = random.uniform(fibre_length, width-fibre_length)
    z = random.uniform(fibre_length, height-fibre_length)
    # angle of fibre
    angle_x = random.uniform(0, 2*3.1415926)
    angle_z = random.uniform(0, 2*3.1415926)
    # caculate the second point of fibre
    z2 = z + fibre_length*sin(angle_z)
    x2 = x + fibre_length*cos(angle_z)*cos(angle_x)
    y2 = y + fibre_length*cos(angle_z)*sin(angle_x)
    # interact judgement
    point = ((x,y,z), (x2,y2,z2))
    if len(points)==0:
        points.append(point)
    elif interact_judgement(points, point, fibre_diameter):
        points.append(point)
    else:
        pass

# create wire
for point in points:
    myPart2.WirePolyLine(points=(point, ), mergeType=IMPRINT, meshable = ON)



