from abaqus import *
from abaqusConstants import *
import regionToolset
import random

#create model
if mdb.models.has_key('xianWei'):
    myModel = mdb.models['xianWei']
else:
    myModel = mdb.Model(name = 'xianWei')

#create sketch
mySketch = myModel.ConstrainedSketch(name='t1',sheetSize=5)
l_a = 30 #length
l_b = 10 #width
mySketch.rectangle(point1 = (0,0),point2 = (l_a,l_b))
#create Part
myPart = myModel.Part(name='P1',dimensionality = TWO_D_PLANAR,type = DEFORMABLE_BODY)
myPart.BaseShell(sketch = mySketch)
del myModel.sketches['t1']


#create xianWei
mySketch = myModel.ConstrainedSketch(name='t2',sheetSize=5)
#length and width of xianWei
length = 2
width = 0.1

ce = sqrt(length**2+width**2)

#number of xianWei
num = 200
mypoints = []
count_total = 0
signature = True

for i in range(num):
    count = 0
    while True:
        count_total = count_total + 1
        if count_total >= num*20:
            signature = False
            break
        sign = []
        
        angle = random.uniform(0,pi*2)   
        if (count==0)or(count >= 40):        
            x1 = random.uniform(ce,l_a - ce)
            y1 = random.uniform(ce,l_b - ce)
            count = 0
        
        '''
        angle = pi/4
        x1 = random.uniform(length,l_a - length)
        y1 = random.uniform(length,l_b - length)
        '''
        x2 = x1 + length*sin(angle)
        y2 = y1 + length*cos(angle)
        x3 = x2 - width*cos(angle)
        y3 = y2 + width*sin(angle)
        x4 = x1 - width*cos(angle)
        y4 = y1 + width*sin(angle)
        
        count = count + 1
        
        if(len(mypoints)==0):
            mypoints.append([x1,y1,x2,y2,x3,y3,x4,y4])
        else:
            for j in range(len(mypoints)):
            
                sign1 = True    
                x1o = mypoints[j][0]
                y1o = mypoints[j][1]
                x2o = mypoints[j][2]
                y2o = mypoints[j][3]
                x3o = mypoints[j][4]
                y3o = mypoints[j][5]
                x4o = mypoints[j][6]
                y4o = mypoints[j][7]
                
#               judge line1                
                line1_line1o_1 = ((x2-x1o)*(y2o-y1o)-(x2o-x1o)*(y2-y1o))*((x1-x1o)*(y2o-y1o)-(x2o-x1o)*(y1-y1o))
                line1_line1o_2 = ((x1o-x1)*(y2-y1)-(x2-x1)*(y1o-y1))*((x2o-x1)*(y2-y1)-(x2-x1)*(y2o-y1))
                
                line1_line2o_1 = ((x2-x2o)*(y3o-y2o)-(x3o-x2o)*(y2-y2o))*((x1-x2o)*(y3o-y2o)-(x3o-x2o)*(y1-y2o))
                line1_line2o_2 = ((x2o-x1)*(y2-y1)-(x2-x1)*(y2o-y1))*((x3o-x1)*(y2-y1)-(x2-x1)*(y3o-y1))

                line1_line3o_1 = ((x2-x3o)*(y4o-y3o)-(x4o-x3o)*(y2-y3o))*((x1-x3o)*(y4o-y3o)-(x4o-x3o)*(y1-y3o))
                line1_line3o_2 = ((x3o-x1)*(y2-y1)-(x2-x1)*(y3o-y1))*((x4o-x1)*(y2-y1)-(x2-x1)*(y4o-y1))
                
                line1_line4o_1 = ((x2-x4o)*(y1o-y4o)-(x1o-x4o)*(y2-y4o))*((x1-x4o)*(y1o-y4o)-(x1o-x4o)*(y1-y4o))
                line1_line4o_2 = ((x4o-x1)*(y2-y1)-(x2-x1)*(y4o-y1))*((x1o-x1)*(y2-y1)-(x2-x1)*(y1o-y1))

#               judge line2
                line2_line1o_1 = ((x3-x1o)*(y2o-y1o)-(x2o-x1o)*(y3-y1o))*((x2-x1o)*(y2o-y1o)-(x2o-x1o)*(y2-y1o))
                line2_line1o_2 = ((x1o-x2)*(y3-y2)-(x3-x2)*(y1o-y2))*((x2o-x2)*(y3-y2)-(x3-x2)*(y2o-y2))
                
                line2_line2o_1 = ((x3-x2o)*(y3o-y2o)-(x3o-x2o)*(y3-y2o))*((x2-x2o)*(y3o-y2o)-(x3o-x2o)*(y2-y2o))
                line2_line2o_2 = ((x2o-x2)*(y3-y2)-(x3-x2)*(y2o-y2))*((x3o-x2)*(y3-y2)-(x3-x2)*(y3o-y2))

                line2_line3o_1 = ((x3-x3o)*(y4o-y3o)-(x4o-x3o)*(y3-y3o))*((x2-x3o)*(y4o-y3o)-(x4o-x3o)*(y2-y3o))
                line2_line3o_2 = ((x3o-x2)*(y3-y2)-(x3-x2)*(y3o-y2))*((x4o-x2)*(y3-y2)-(x3-x2)*(y4o-y2))
                
                line2_line4o_1 = ((x3-x4o)*(y1o-y4o)-(x1o-x4o)*(y3-y4o))*((x2-x4o)*(y1o-y4o)-(x1o-x4o)*(y2-y4o))
                line2_line4o_2 = ((x4o-x2)*(y3-y2)-(x3-x2)*(y4o-y2))*((x1o-x2)*(y3-y2)-(x3-x2)*(y1o-y2))            
                
#               judge line3
                line3_line1o_1 = ((x4-x1o)*(y2o-y1o)-(x2o-x1o)*(y4-y1o))*((x3-x1o)*(y2o-y1o)-(x2o-x1o)*(y3-y1o))
                line3_line1o_2 = ((x1o-x3)*(y4-y3)-(x4-x3)*(y1o-y3))*((x2o-x3)*(y4-y3)-(x4-x3)*(y2o-y3))
                
                line3_line2o_1 = ((x4-x2o)*(y3o-y2o)-(x3o-x2o)*(y4-y2o))*((x3-x2o)*(y3o-y2o)-(x3o-x2o)*(y3-y2o))
                line3_line2o_2 = ((x2o-x3)*(y4-y3)-(x4-x3)*(y2o-y3))*((x3o-x3)*(y4-y3)-(x4-x3)*(y3o-y3))

                line3_line3o_1 = ((x4-x3o)*(y4o-y3o)-(x4o-x3o)*(y4-y3o))*((x3-x3o)*(y4o-y3o)-(x4o-x3o)*(y3-y3o))
                line3_line3o_2 = ((x3o-x3)*(y4-y3)-(x4-x3)*(y3o-y3))*((x4o-x3)*(y4-y3)-(x4-x3)*(y4o-y3))
                
                line3_line4o_1 = ((x4-x4o)*(y1o-y4o)-(x1o-x4o)*(y4-y4o))*((x3-x4o)*(y1o-y4o)-(x1o-x4o)*(y3-y4o))
                line3_line4o_2 = ((x4o-x3)*(y4-y3)-(x4-x3)*(y4o-y3))*((x1o-x3)*(y4-y3)-(x4-x3)*(y1o-y3))                     
                
#               judge line4
                line4_line1o_1 = ((x1-x1o)*(y2o-y1o)-(x2o-x1o)*(y1-y1o))*((x4-x1o)*(y2o-y1o)-(x2o-x1o)*(y4-y1o))
                line4_line1o_2 = ((x1o-x4)*(y1-y4)-(x1-x4)*(y1o-y4))*((x2o-x4)*(y1-y4)-(x1-x4)*(y2o-y4))
                
                line4_line2o_1 = ((x1-x2o)*(y3o-y2o)-(x3o-x2o)*(y1-y2o))*((x4-x2o)*(y3o-y2o)-(x3o-x2o)*(y4-y2o))
                line4_line2o_2 = ((x2o-x4)*(y1-y4)-(x1-x4)*(y2o-y4))*((x3o-x4)*(y1-y4)-(x1-x4)*(y3o-y4))

                line4_line3o_1 = ((x1-x3o)*(y4o-y3o)-(x4o-x3o)*(y1-y3o))*((x4-x3o)*(y4o-y3o)-(x4o-x3o)*(y4-y3o))
                line4_line3o_2 = ((x3o-x4)*(y1-y4)-(x1-x4)*(y3o-y4))*((x4o-x4)*(y1-y4)-(x1-x4)*(y4o-y4))

                line4_line4o_1 = ((x1-x4o)*(y1o-y4o)-(x1o-x4o)*(y1-y4o))*((x4-x4o)*(y1o-y4o)-(x1o-x4o)*(y4-y4o))
                line4_line4o_2 = ((x4o-x4)*(y1-y4)-(x1-x4)*(y4o-y4))*((x1o-x4)*(y1-y4)-(x1-x4)*(y1o-y4))
                if (line1_line1o_1 <= 0) and (line1_line1o_2 <= 0):
                    sign1 = False
                elif (line1_line2o_1 <= 0) and (line1_line2o_2 <= 0):
                    sign1 = False
                elif (line1_line3o_1 <= 0) and (line1_line3o_2 <= 0):   
                    sign1 = False
                elif (line1_line4o_1 <= 0) and (line1_line4o_2 <= 0):   
                    sign1 = False
                elif (line2_line1o_1 <= 0) and (line2_line1o_2 <= 0):
                    sign1 = False
                elif (line2_line2o_1 <= 0) and (line2_line2o_2 <= 0):
                    sign1 = False
                elif (line2_line3o_1 <= 0) and (line2_line3o_2 <= 0):   
                    sign1 = False
                elif (line2_line4o_1 <= 0) and (line2_line4o_2 <= 0):   
                    sign1 = False
                elif (line3_line1o_1 <= 0) and (line3_line1o_2 <= 0):
                    sign1 = False
                elif (line3_line2o_1 <= 0) and (line3_line2o_2 <= 0):
                    sign1 = False
                elif (line3_line3o_1 <= 0) and (line3_line3o_2 <= 0):   
                    sign1 = False
                elif (line3_line4o_1 <= 0) and (line3_line4o_2 <= 0):   
                    sign1 = False
                elif (line4_line1o_1 <= 0) and (line4_line1o_2 <= 0):
                    sign1 = False
                elif (line4_line2o_1 <= 0) and (line4_line2o_2 <= 0):
                    sign1 = False
                elif (line4_line3o_1 <= 0) and (line4_line3o_2 <= 0):   
                    sign1 = False
                elif (line4_line4o_1 <= 0) and (line4_line4o_2 <= 0):   
                    sign1 = False
                sign.append(sign1)
        if sign.count(True) == len(sign):
            mypoints.append([x1,y1,x2,y2,x3,y3,x4,y4])
            break
    if signature:        
        mySketch.Line(point1 = (x1,y1),point2 = (x2,y2))
        mySketch.Line(point1 = (x2,y2),point2 = (x3,y3))
        mySketch.Line(point1 = (x3,y3),point2 = (x4,y4))
        mySketch.Line(point1 = (x4,y4),point2 = (x1,y1))

myPart.PartitionFaceBySketch(faces=myPart.faces[0:1], sketch=mySketch)

#end program




