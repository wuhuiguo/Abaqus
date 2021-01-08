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
    c = line[0]
    d = line[1]
    #
    dis = []
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
                dis.append(distance)
                if distance <= diameter:
                    sign = False
                    break
            if not sign:
                break
        if not sign:
            break
    # if sign:
    #     print(min(dis),max(dis))
    return sign

# information of solid fibre
fibre_length_solid = 5
fibre_radius_solid = 1
fibre_num_solid = 5

# create solid fibre
myPart3 = myModel.Part(name="Part-fibre-solid", dimensionality=THREE_D, type=DEFORMABLE_BODY)
mySketch3 = myModel.ConstrainedSketch(name="sketch-3", sheetSize=200)
mySketch3.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(fibre_radius_solid, 0.0))
myPart3.BaseSolidExtrude(sketch=mySketch3, depth=fibre_length_solid)

# save trans and rotate information
fibre = []
points = []
# caculate the movement and rotation of fibre
# interact of judgement
for num in range(fibre_num_solid):
    x = random.uniform(0, length)
    y = random.uniform(0, width)
    z = random.uniform(0, height)
    angle_y = random.uniform(0, 360)
    angle_z = random.uniform(0, 360)

    z2 = z + fibre_length_solid*cos(radians(angle_y))
    x2 = x + fibre_length_solid*sin(radians(angle_y))*cos(radians(angle_z))
    y2 = y + fibre_length_solid*sin(radians(angle_y))*sin(radians(angle_z))

    point = ((x,y,z), (x2,y2,z2))
    if len(points) == 0:
        points.append(point)
        fibre.append([x, y, z, angle_y, angle_z])
    elif interact_judgement(points, point, 2*fibre_radius_solid):
        points.append(point)
        fibre.append([x, y, z, angle_y, angle_z])
    else:
        pass

# create in Abaqus
myAssembly = myModel.rootAssembly
for num in range(len(fibre)):
    x = fibre[num][0]
    y = fibre[num][1]
    z = fibre[num][2]
    angle_y = fibre[num][3]
    angle_z = fibre[num][4]
    myAssembly.Instance(name='Part-fibre-solid-{}'.format(num), part=myPart3, dependent=ON)
    myAssembly.rotate(instanceList=('Part-fibre-solid-{}'.format(num),), axisPoint=(0, 0, 0), axisDirection=(0, 1, 0),
             angle = angle_y)
    myAssembly.rotate(instanceList=('Part-fibre-solid-{}'.format(num),), axisPoint=(0, 0, 0), axisDirection=(0, 0, 1),
             angle = angle_z)
    myAssembly.translate(instanceList=('Part-fibre-solid-{}'.format(num), ), vector=(x, y, z))


# merge assembly to Part
instances = []
for ins in myAssembly.instances.values():
    instances.append(ins)
myAssembly.InstanceFromBooleanMerge(name='Part-fibre-all', instances=tuple(instances), keepIntersections=ON,
    originalInstances=DELETE, domain=GEOMETRY)





