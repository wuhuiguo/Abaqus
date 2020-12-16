from abaqus import *
from abaqusConstants import *
import random

myModel = mdb.models["Model-1"]

for number in range(1, 11):
    materialName = "Material-{}".format(number)
    sectionName = "Section-{}".format(number)
    myModel.Material(name=materialName)
    myModel.materials[materialName].Elastic(table=((70000.0-100*number, 0.3), ))
    myModel.materials[materialName].Density(table=((2.7e-09, ), ))
    myModel.HomogeneousSolidSection(name=sectionName, material=materialName, thickness=None)


myPart = myModel.parts['Part-1']
myElement = myPart.elements
for iter in range(len(myElement)):
    randNum = random.randint(1, 10)
    setName = 'Set-{}'.format(iter)
    myPart.Set(elements=myElement[iter:iter+1], name=setName)
    myPart.SectionAssignment(region=myPart.sets[setName], sectionName='Section-{}'.format(randNum), offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)










