import odbAccess
import numpy as np

myOdb = odbAccess.openOdb(r"D:\temp\Job-1.odb", readOnly=False)
myFrames = myOdb.steps["Step-1"].frames
time = []
data = []
for i in range(len(myFrames)):
    myField = myFrames[i].fieldOutputs
    tempField = [myFrames[i].frameValue,]
    for key in ["E","S"]:
        myValues = myField[key].values
        temp = []
        for value in myValues:
            if value.mises is not None:
                temp.append(value.mises)
        tempField.append(np.mean(np.array(temp)))
    data.append(tempField)

data = np.array(data)
np.savetxt(r"D:\temp\20210126.txt", data,fmt="%.10f")

