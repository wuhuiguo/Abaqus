def CTS( Modelname, Partname, Acoordinates, Bcoordinates, Ccoordinates, m, n, Orientation ):
	"""create a transition sketch"""
	import math
	import part
	import sketch
	
	Acoordinates=[float(i) for i in Acoordinates]
	Bcoordinates=[float(i) for i in Bcoordinates]
		
	dx=Bcoordinates[0]-Acoordinates[0]
	dy=Acoordinates[1]-Bcoordinates[1]
	
	if m%2==0:
		if dx>0 and dy>0:
			if dx>dy:
				Nmax = dx
			else:
				Nmax = dy
		
			if Orientation=='HD' or Orientation=='HU': CTSH( Modelname, Partname, Acoordinates, Bcoordinates, Ccoordinates, m, n, dx, dy, Nmax, Orientation )
			elif Orientation=='VR' or Orientation=='VL': CTSV( Modelname, Partname, Acoordinates, Bcoordinates, Ccoordinates, m, n, dx, dy, Nmax, Orientation )
			else: print ('\nOrientation you inputted is wrong! Orientation must be \'HD\', \'HU\', \'VR\' or \'VL\'.')
		else: print ('\nAcoordinates and Bcoordinates you inputted is wrong! you should locate A point at top left corner and B point at bottom right corner.')
	else: print ('\nm you inputted is wrong, m must be multiple of 2.')
	
def CTSH( Modelname, Partname, Acoordinates, Bcoordinates, Ccoordinates, m, n, dx, dy, Nmax, Orientation ):		
	
	XX=[]
	counter=n		
	while counter>=0:
		i=0
		Temp=[]
		times=pow(2,counter)
		while i<times*m:
			x=Acoordinates[0]+i*dx/times/m
			Temp.append(x)
			i+=1
		Temp.append(Bcoordinates[0])
		XX.append(Temp)
		counter-=1
	
	if Orientation=='HD':
		YY=[]
		yy=0
		i=0
		counter=n
		YY.append(Bcoordinates[1])
		IniTerm=dy/(pow(2,n)-1)
		while i<counter:
			yy=yy+IniTerm*pow(2,i)
			y=Bcoordinates[1]+yy
			YY.append(y)
			i+=1
	else: 
		YY=[]
		yy=0
		i=0
		counter=n
		YY.append(Acoordinates[1])
		IniTerm=dy/(pow(2,n)-1)
		while i<counter:
			yy=yy+IniTerm*pow(2,i)
			y=Acoordinates[1]-yy
			YY.append(y)
			i+=1
		
	MyPart = mdb.models[Modelname].parts[Partname]
	MyFace = MyPart.faces.findAt(Ccoordinates)
	t = MyPart.MakeSketchTransform(sketchPlane=MyFace)
	MySketch = mdb.models[Modelname].ConstrainedSketch(name='temp', 
		sheetSize=3*Nmax, transform=t)
	MyPart.projectReferencesOntoSketch(sketch=MySketch)

	i=0
	while i<=n:
		MySketch.Line(point1=(Acoordinates[0], YY[i]), point2=(Bcoordinates[0], YY[i]))
		i+=1
    		
	i=0
	while i<=m:
		MySketch.Line(point1=(XX[n][i], Acoordinates[1]), point2=(XX[n][i], Bcoordinates[1]))
		i+=1
    
	i=0
	h=0.5
	counter=n-1
	while i<n:
		j=0
		times=pow(2,counter)
		while j<times*m/2:
			k=4*j
			MySketch.Line(point1=(XX[i][k], YY[i+1]), point2=(XX[i][k+1], h*(YY[i+1]-YY[i])+YY[i]))
			MySketch.Line(point1=(XX[i][k+1], h*(YY[i+1]-YY[i])+YY[i]), point2=(XX[i][k+3], h*(YY[i+1]-YY[i])+YY[i]))
			MySketch.Line(point1=(XX[i][k+3], h*(YY[i+1]-YY[i])+YY[i]), point2=(XX[i][k+4], YY[i+1]))
			MySketch.Line(point1=(XX[i][k+1], h*(YY[i+1]-YY[i])+YY[i]), point2=(XX[i][k+1], YY[0]))
			MySketch.Line(point1=(XX[i][k+3], h*(YY[i+1]-YY[i])+YY[i]), point2=(XX[i][k+3], YY[0]))
			j+=1
		counter-=1
		i+=1

	MyPart.PartitionFaceBySketch(faces=MyFace, sketch=MySketch) 
	del mdb.models[Modelname].sketches['temp']
	
def CTSV( Modelname, Partname, Acoordinates, Bcoordinates, Ccoordinates, m, n, dx, dy, Nmax, Orientation ):		
	
	XX=[]
	counter=n		
	while counter>=0:
		i=0
		Temp=[]
		times=pow(2,counter)
		while i<times*m:
			x=Bcoordinates[1]+i*dy/times/m
			Temp.append(x)
			i+=1
		Temp.append(Acoordinates[1])
		XX.append(Temp)
		counter-=1

	if Orientation=='VR':
		YY=[]
		yy=0
		i=0
		counter=n
		YY.append(Bcoordinates[0])
		IniTerm=dx/(pow(2,n)-1)
		while i<counter:
			yy=yy+IniTerm*pow(2,i)
			y=Bcoordinates[0]-yy
			YY.append(y)
			i+=1
	else:
		YY=[]
		yy=0
		i=0
		counter=n
		YY.append(Acoordinates[0])
		IniTerm=dx/(pow(2,n)-1)
		while i<counter:
			yy=yy+IniTerm*pow(2,i)
			y=Acoordinates[0]+yy
			YY.append(y)
			i+=1		
	
	MyPart = mdb.models[Modelname].parts[Partname]
	MyFace = MyPart.faces.findAt(Ccoordinates)
	t = MyPart.MakeSketchTransform(sketchPlane=MyFace)
	MySketch = mdb.models[Modelname].ConstrainedSketch(name='temp', 
		sheetSize=3*Nmax, transform=t)
	MyPart.projectReferencesOntoSketch(sketch=MySketch)

	i=0
	while i<=n:
		MySketch.Line(point1=(YY[i], Acoordinates[1]), point2=(YY[i], Bcoordinates[1]))
		i+=1
    		
	i=0
	while i<=m:
		MySketch.Line(point1=(Acoordinates[0], XX[n][i]), point2=(Bcoordinates[0], XX[n][i]))
		i+=1
    
	i=0
	h=0.5
	counter=n-1
	while i<n:
		j=0
		times=pow(2,counter)
		while j<times*m/2:
			k=4*j
			MySketch.Line(point1=(YY[i+1], XX[i][k]), point2=(h*(YY[i+1]-YY[i])+YY[i], XX[i][k+1]))
			MySketch.Line(point1=(h*(YY[i+1]-YY[i])+YY[i], XX[i][k+1]), point2=(h*(YY[i+1]-YY[i])+YY[i], XX[i][k+3]))
			MySketch.Line(point1=(h*(YY[i+1]-YY[i])+YY[i], XX[i][k+3]), point2=(YY[i+1], XX[i][k+4]))
			MySketch.Line(point1=(h*(YY[i+1]-YY[i])+YY[i], XX[i][k+1]), point2=(YY[0], XX[i][k+1]))
			MySketch.Line(point1=(h*(YY[i+1]-YY[i])+YY[i], XX[i][k+3]), point2=(YY[0], XX[i][k+3]))
			j+=1
		counter-=1
		i+=1

	MyPart.PartitionFaceBySketch(faces=MyFace, sketch=MySketch) 
	del mdb.models[Modelname].sketches['temp'] 
