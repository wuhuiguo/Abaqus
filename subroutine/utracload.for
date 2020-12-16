      SUBROUTINE UTRACLOAD(ALPHA,T_USER,KSTEP,KINC,TIME,NOEL,NPT,
     1 COORDS,DIRCOS,JLTYP,SNAME)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION T_USER(3), TIME(2), COORDS(3), DIRCOS(3,3)
      CHARACTER*80 SNAME

      real radius,dis
c      user coding to define ALPHA and T_USER
c     受力方向
      T_USER(1) = COORDS(1) - 50.0 
      T_USER(2) = COORDS(2) - 50.0
      T_USER(3) = 0
c     受力大小
      
      radius = 50*time(1)
      dis = sqrt((coords(1)-50.0)**2+(coords(2)-50.0)**2)
      if (dis <= radius) then
          alpha = 10
      else
          alpha = 0
      end if
      
      RETURN
      END
      
      
      SUBROUTINE DLOAD(F,KSTEP,KINC,TIME,NOEL,NPT,LAYER,KSPT,
     1 COORDS,JLTYP,SNAME)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION TIME(2), COORDS (3)
      CHARACTER*80 SNAME
      parameter pi=3.1415926
      
      real dis
c      user coding to define F
      
      dis =sqrt((coords(1)-50)**2+(coords(2)-50)**2)
      if (dis<=45.and.dis>=42) then
              F = -10
      else
              F = 0    
      end if
      
      
      RETURN
      END
      
      
      
      
      
      
      
      
      
      
      
      