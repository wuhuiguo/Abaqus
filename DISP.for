
      SUBROUTINE  DISP(U,KSTEP,KINC,TIME,NODE,NOEL,JDOF,COORDS)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION U(3),TIME(3),COORDS(3)
c      user coding to define U
      
      U(1) = 10*sin(0.05*coords(3))
      
      RETURN
      END

