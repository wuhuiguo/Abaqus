import odbAccess
from abaqusConstants import *
import os, sys

myOdb = odbAccess.openOdb(path=r"D:\temp\Job-2.odb", readOnly=False)
instance1 = myOdb.rootAssembly.instances["PART-1-1"]
elements = instance1.elements
for frame in myOdb.steps["Step-1"].frames:
    test = frame.FieldOutput(name="test", description="peeq*2 test", type=SCALAR)
    data = frame.fieldOutputs["PEEQ"]
    for ele in elements:
        temp = data.getSubset(region=ele).values[0].data
        test.addData(position=CENTROID, instance=instance1, labels=[ele.label, ], data=((temp, ),))

