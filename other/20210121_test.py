from abaqus import *
from abaqusConstants import *
import numpy as np
from random import *

# function of interact judgement
def interact(points, center, radius):
    sign = True
    for point in points:
        if sqrt((point[0]-center[0])**2+(point[1]-center[1])**2+(point[2]-center[2])**2) <= 2*radius:
            sign = False
    return sign

def CCD(modelName, partName, setName, radius, type, angler=None):
    '''
    :param modelName: name of model
    :param partName:  name of part
    :param setname:   name of set
    :param radius:    radius of aggregate
    :param type:      type of aggregate, round or polygon
    :param angle:     angle of dotted line
    :return:          None
    '''
    if type == "round":
        myModel = mdb.models[modelName]
        myPart = myModel.parts[partName]
        mySet = myPart.sets[setName]
        x = []
        y = []
        for ver in myPart.vertices:
            x.append(ver.pointOn[0][0])
            y.append(ver.pointOn[0][1])
        length = max(x) - min(x)
        width = max(y) - min(y)
        num = int(length*width/radius)
        points = []
        for i in range(num):
            center = (uniform(radius, length - radius), uniform(radius, width - radius), 0)
            sign = True
            for i in np.linspace(0,2*np.pi,10):
                ptemp = (center[0]+radius*cos(i),center[1]+radius*sin(i),center[2])
                if myPart.faces.findAt((ptemp,), ) != mySet.faces:
                    sign = False
                    break
            if sign:
                if len(points) == 0:
                    points.append(center)
                elif interact(points, center, radius):
                    points.append(center)
                else:
                    pass
        # sketch
        mySketch = myModel.ConstrainedSketch(name="sketch-1", sheetSize=2)
        for point in points:
            mySketch.CircleByCenterPerimeter(center=(point[0], point[1]), point1=(point[0] + radius, point[1]))
            if angler is not None:
                angle = angler
            else:
                angle = uniform(0, 2 * np.pi)
            point1 = (point[0] + radius * cos(angle), point[1] + radius * sin(angle))
            point4 = (point[0] - radius * cos(angle), point[1] - radius * sin(angle))
            mySketch.ConstructionLine(point1=point1, point2=point4)
            # create ploy line
            angle2 = angle - radians(40)
            l = 0.3
            point2 = (point[0] + l * radius * cos(angle2), point[1] + l * radius * sin(angle2))
            point3 = (point[0] - l * radius * cos(angle2), point[1] - l * radius * sin(angle2))
            mySketch.Line(point1=point1, point2=point2)
            mySketch.Line(point1=point2, point2=point3)
            mySketch.Line(point1=point3, point2=point4)
        myPart.PartitionFaceBySketch(faces=mySet.faces[:], sketch=mySketch)
    elif type == "polygon":
        pass
    else:
        pass



## example
## CCD("Model-1","Part-1","Set-1",1,"round")















