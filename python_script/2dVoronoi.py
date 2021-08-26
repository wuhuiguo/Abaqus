from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random

# user defined variable
#initial variables
radius = 0.08
length = 1
width = 1
beta = 0.16 # range:(0,1) #0.4-90% # 0.8-80% # 0.16 95%
w = 0.013
#*******************************************

length2 = length*1.3
width2 = width*1.3
point_number = int(length2*width2/(np.pi*radius**2))
modelName = "model-1"

points = []
x = np.sqrt(length2*width2/point_number)
for i in range(-int(length*0.3/x), int(length/x)+2):
    for j in range(-int(width*0.3/x), int(width/x)+2):
        px = random.uniform(i*x, (i+1)*x)
        py = random.uniform(j*x, (j+1)*x)
        points.append([px, py])

vor = Voronoi(points)
vertices = vor.vertices
regions = vor.regions
regions2 = []
wtotal = []

for i in range(len(regions)):
    d = regions[i]
    if len(d)>0 and -1 not in d:
        temp = [vertices[index] for index in d]
        sign = True
        for point in temp:
            if (point[0] < -0.1*length or point[0]>1.2*length) or (point[1]<-0.1*length or point[1]>1.2*length):
                sign = False
                break
        if sign:
            regions2.append(temp)

for points in regions2:
    mindis = []
    for i in range(len(points)):
        a, b, c, d = points[i-3],points[i-2],points[i-1],points[i]

        ba = (a-b)/np.linalg.norm(a-b)
        bc = (c-b)/np.linalg.norm(c-b)
        l1 = ba+bc
        k1 = l1[1]/l1[0]
        cb = (b-c)/np.linalg.norm(b-c)
        cd = (d-c)/np.linalg.norm(d-c)
        l2 = cb+cd
        k2 = l2[1]/l2[0]

        x0,y0 = b[0], b[1]
        x1,y1 = c[0], c[1]

        x = (k1*x0-k2*x1+y1-y0)/(k1-k2)
        y = k1*(x-x0)+y0
        point = b-np.array([x,y])

        bc = (c-b)/np.linalg.norm(c-b)
        n = np.array([bc[1], bc[0]])
        dis = abs(np.dot(point, n))
        mindis.append(dis)
    wtotal.append(np.min(np.array(mindis)))
    # wtotal.append(mindis)

def arangePoint(p1,p2,p3,w,beta):
    l1 = p1 - p2
    l2 = p3 - p2
    l1 = l1/np.linalg.norm(l1)
    l2 = l2/np.linalg.norm(l2)
    l3 = l1 + l2
    l3 = l3/np.linalg.norm(l3)
    costheta = np.dot(l3,l2)
    sintheta = np.sqrt(1-costheta**2)
    l3 = l3*w+p2
    return l3

regionsNew = []

for index in range(len(regions2)):
    points = regions2[index]

    temp = []
    for i in range(len(points)):
        if i == 0:
            temp.append(arangePoint(points[-1], points[0], points[1], w, beta))
        elif i == len(points)-1:
            temp.append(arangePoint(points[-2], points[-1], points[0], w, beta))
        else:
            temp.append(arangePoint(points[i-1], points[i], points[i+1], w, beta))
    regionsNew.append(temp)

# create base
modelName = 'model-1'
if mdb.models.has_key(modelName):
    del mdb.models[modelName]

myModel = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)
mySketch1 = myModel.ConstrainedSketch(name='sketch1', sheetSize=200.0)
mySketch1.rectangle(point1=(0.0, 0.0), point2=(length, width))
myPart = myModel.Part(name='Part-voronoi', dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
myPart.BaseShell(sketch=mySketch1)

#create voronoi
mySketch2 = myModel.ConstrainedSketch(name='sketch-2',sheetSize=200, gridSpacing=10)
for points in regionsNew:
    for i in range(len(points)):
            mySketch2.Line(point1=tuple(points[i-1]), point2=tuple(points[i]))

sketchVoronoi = myModel.ConstrainedSketch(name='Sketch-voronoi', objectToCopy=mySketch2)


g = mySketch2.geometry
for points in regionsNew:
    for i in range(len(points)):
        if len(points) == 3:
            pass
        else:
            a, b, c, d = points[i-3],points[i-2],points[i-1],points[i]
            ad, bd, cd = a - d,b - d,c - d
            ba,ca,da = b-a,c-a,d-a
            ab,cb,db = a-b,c-b,d-b
            dc,ac,bc = d-c,a-c,b-c
            if ((max(a[0],b[0])>min(c[0],d[0])) and (max(c[0],d[0])>min(a[0],b[0])))and((max(a[1],b[1])>min(c[1],
                                                                        d[1])) and (max(c[1],d[1])>min(a[1],b[1]))):
                if np.dot(np.cross(ad, cd), np.cross(bd, cd)) < 0 and np.dot(np.cross(ca, ba), np.cross(da, ba)) < 0 and \
                        np.dot(np.cross(cb, ab), np.cross(db, ab)) < 0 and np.dot(np.cross(ac, dc), np.cross(bc, dc)) < 0:
                    mySketch2.autoTrimCurve(curve1=g.findAt(tuple((b+c)/2.)), point1=tuple((b+c)/2.))
                    mySketch2.autoTrimCurve(curve1=g.findAt(tuple((c+d)/2.)), point1=tuple(c))
                    mySketch2.autoTrimCurve(curve1=g.findAt(tuple((a+b)/2.)), point1=tuple(b))
                    if len(points)==4:
                        break

myPart.Cut(sketch=mySketch2)

area = 0
for face in mdb.models["model-1"].parts["Part-voronoi"].faces:
    area += face.getSize()


print("kongxi=",(25-area)/25.)



