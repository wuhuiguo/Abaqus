
from abaqus import *
from abaqusConstants import *
import random

width = 100
length = 200

myModel = mdb.models["Model-1"] #create model
mySketch = mdb.models['Model-1'].ConstrainedSketch(name='sketch_1', sheetSize=200.0) #create sketch
mySketch.rectangle(point1=(0,0), point2=(length, width))
myPart = myModel.Part(name='Part-1', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
myPart.BaseShell(sketch=mySketch)
del myModel.sketches['sketch_1']

mySketch = myModel.ConstrainedSketch(name='sketch_2', sheetSize=200)

def interCheck(point,center,radius1,radius2):
    sign = True
    for p in center:
        if sqrt((point[0] - p[0]) ** 2 + (point[1] - p[1]) ** 2) <= (radius1+radius2):
            sign = False
            break
    return sign
# radius = 5
count = 0
radius = 5
center = [[random.uniform(radius, length - radius), random.uniform(radius, width - radius)]]
while True:
    x = random.uniform(radius, length - radius)
    y = random.uniform(radius, width - radius)
    sign = interCheck([x,y],center,5,5)
    if sign:
        center.append([x,y])
    count += 1
    if count >= 300:
        break
for p in center:
    x,y = p[0], p[1]
    mySketch.CircleByCenterPerimeter(center=(x, y), point1=(x+radius, y))
#radius = 2
count = 0
radius = 2
center02 = []
while True:
    x = random.uniform(radius, length - radius)
    y = random.uniform(radius, width - radius)
    sign1 = interCheck([x, y], center, 5, 2)
    if sign1:
        sign2 = interCheck([x, y], center02, 2, 2)
        if sign2:
            center02.append([x, y])
    count += 1
    if count >= 500:
        break

for p in center02:
    x, y = p[0], p[1]
    mySketch.CircleByCenterPerimeter(center=(x, y), point1=(x + radius, y))
# radius = 0.5
count = 0
radius = 0.5
center03 = []
while True:
    x = random.uniform(radius, length - radius)
    y = random.uniform(radius, width - radius)
    sign1 = interCheck([x, y], center, 5, 0.5)
    if sign1:
        sign2 = interCheck([x, y], center02, 2, 0.5)
        if sign2:
            sign3 = interCheck([x, y], center03, 0.5, 0.5)
            if sign3:
                center03.append([x, y])
    count += 1
    if count >= 4000:
        break
for p in center03:
    x, y = p[0], p[1]
    mySketch.CircleByCenterPerimeter(center=(x, y), point1=(x + radius, y))
myPart.PartitionFaceBySketch(faces=myPart.faces[0:1], sketch=mySketch)
del myModel.sketches['sketch_2']
