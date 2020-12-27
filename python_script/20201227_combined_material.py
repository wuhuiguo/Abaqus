# session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

from abaqus import *
from abaqusConstants import *
import regionToolset

# 1
# initialize
length = 20
width = 10
height = 4

# define of layer
layer = 20
height_layer = height/float(layer)

# 2
# Base_create
myModel = mdb.models["Model-1"]
mySketch = myModel.ConstrainedSketch(name='sketch-1',sheetSize=200)
mySketch.rectangle(point1=(0,0), point2=(length, width))

myPart = myModel.Part(name = "Part-base", dimensionality=THREE_D, type=DEFORMABLE_BODY)
myPart.BaseSolidExtrude(sketch=mySketch, depth=height_layer)

# 3
# assembly
myAssembly = myModel.rootAssembly
totalInstance = []
for num in range(layer):
    insName = 'Part-base-{}'.format(num)
    distance = height_layer*num
    myAssembly.Instance(name = insName, part=myPart, dependent = ON)
    myAssembly.translate(instanceList=(insName,),vector=(0, 0, distance))
    totalInstance.append(myAssembly.instances[insName])

# 4
myAssembly.InstanceFromBooleanMerge(name="Part-total", instances=tuple(totalInstance), keepIntersections=ON,
                                    originalInstances = DELETE, domain=GEOMETRY)

# 5
# create material
for mat in range(layer):
    myMaterial = myModel.Material(name="Material-{}".format(mat))
    myMaterial.Elastic(table=((2.1e5, 0.3),))
    myModel.HomogeneousSolidSection(name='Section-{}'.format(mat),material='Material-{}'.format(mat),
                                    thickness=None)

# 6
# assign material
totalPart = myModel.parts["Part-total"]
for num in range(layer):
    cell = totalPart.cells.findAt(((0, 0, height_layer/2.0 + height_layer*num),),)
    region = regionToolset.Region(cells=cell[:])
    totalPart.SectionAssignment(region = region,sectionName='Section-{}'.format(num), offset=0.0,offsetType=MIDDLE_SURFACE,
                             offsetField='',thicknessAssignment=FROM_SECTION)
