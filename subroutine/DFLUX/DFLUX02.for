      SUBROUTINE DFLUX(FLUX,SOL,KSTEP,KINC,TIME,NOEL,NPT,COORDS,
     1 JLTYP,TEMP,PRESS,SNAME)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION FLUX(2), TIME(2), COORDS(3)
      CHARACTER*80 SNAME
C      user coding to define FLUX(1) and FLUX(2)
C     高斯面热源模型   
C     热源参数
      real velocity
      real center_x,center_z
      real P,p1,pi,r0,h,r

C     焊接速度
      velocity = 1.2
      
C     热源中心的坐标,由于热源中心是移动的，所以z值等于焊接速度*总时间
      center_x = 35.0
      center_z = time(2)*velocity
      
C     文献里取的高斯热源参数     
      P = 2400
      p1 = 0.1
      pi = 3.14
      r0 = 4

C     节点距离热源中心的距离
      r = sqrt((coords(1)-center_x)**2+(coords(3)-center_z)**2)
      
      Flux(1) = 3*P*p1*exp(-(3*r**2)/r0**2)/(pi*r0**2)


      RETURN
      END
      
      
      
      
      
      