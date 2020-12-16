      SUBROUTINE DLOAD(F,KSTEP,KINC,TIME,NOEL,NPT,LAYER,KSPT,
     1 COORDS,JLTYP,SNAME)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION TIME(2), COORDS (3)
      CHARACTER*80 SNAME

      real x,z,velocity
      real move
      
      velocity = 400
      
      x = coords(1)
      z = coords(3)
      
      move = velocity*time(2)
      
      if((x>=17.5.and.x<=22.5).or.(x>=57.5.and.x<=62.5))then
          if (z <= move .and. z >= move-15)then
              F = 10
          elseif(z <= move-45 .and. z >= move-60)then
              F = 10
          else
              F = 0
          end if
      else
          F = 0
      end if

      
      
      RETURN
      END
      