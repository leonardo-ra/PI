while ROBOT Program:
   
   ✓ #resets variables
   ✓ Loop(1) 
   ✓ #conn=false, xfp, etc... ✓
    
   ✓ #Confirms communication with computer
   ✓ while connection_with_computer == False:
   ✓     try_to_connect 
   ✓ sends trigger #"test done?"
    
   ✓ loop test_done[0] = 0
   ✓  waits for reply from trigger
    
   ✓ #"In case a test has finished" 
   ✓ if test_done = 1:
      ✓ MoveJ
      ✓   Waypoint_TestBoxPOV
      ✓ Release(37mm) #Make sure the grip is open
      ✓ socket_send_string("test position")
      ✓ loop test_data[0] = 0
      ✓  test_data = socket_read_ascii_float(3)
      ✓ test_pos = poseTrans(TestBox_Plane, p[test_data[1]/1000, test_data[2]/1000, -5/1000, 0, 0, 0]
      ✓ MoveJ
      ✓   test_pos
      ✓ Subprogram(removeFiber) #Removes optic fiber from XFP slot.
      ✓ Subprogram(unlockXFP) #Unlocks XFP leaver and removes XFP from the testbox
        
      ✓ if test_data[4] == 1: #1 means XFP is OK 
      ✓     MoveJ
      ✓        Waypoint_OK
      ✓ else
      ✓     MoveJ
      ✓        Waypoint_NOK
      ✓ Release(37mm)
     
   ✓ else:  #test_done = 0
    ✓ subprogram(go_to_xfp_position)
      {
      ✓ go to default initial position to read XFP #WapointX (substituir com o número do waypoint final)
      ✓ sends trigger "take xfp photo"
     ✘✓ xfp_data = data_from_foto_taken # PolyscopeVar, X, Y, Alpha, Side, !!!!!!!Push!!!!!!!
      ✓                                 # xfp_data[0], xfp_data[1], xfp_data[2], xfp_data[3], xfp_data[4], xfp_data[5] - order of variables received
      ✓ 
      ✓ xfp_position = poseTrans(plane_camera, p[xfp_data[1]/1000, xfp_data[2]/1000, -0.01, 0, 0, xfp_data[3]]) #0,0 represent the Rx, Ry. The -0.01 lets the arm hover above the XFP.
      ✓   moveJ
      ✓    xfp_position #moves the arm to the translated pose
      ✓    
      ✓ xfp_side = xfp_data[4]
      } 
      
     ✓ if xfp_side == 3: # if Side = 3, meaning the XFP is on its side
        ✓ if xfp_data[5]==1 #must adjust in X axis
          ✓  xfp_position = poseTrans(plane_camera, p[(xfp_data[1]/1000 + 0.05), xfp_data[2]/1000, -0.01, 0, 0, xfp_data[3]]) #0,0 represent the Rx, Ry. The -0.01 lets the arm hover above the XFP.
         
        ✓ elif xfp_data[5]==2 #must adjust in Y axis
        ✓    xfp_position = poseTrans(plane_camera, p[(xfp_data[1]/1000), (xfp_data[2]/1000 + 0.05), -0.01, 0, 0, xfp_data[3]]) #0,0 represent the Rx, Ry. The -0.01 lets the arm hover above the XFP.
        ✓ moveJ
         ✓   xfp_position
     ✓ else
       ✓ Grip_Release(37)  #to make sure its open
       ✓ xfp_position = poseTrans(plane_camera, p[xfp_data[1]/1000, xfp_data[2]/1000, 0, 0, 0, xfp_data[3]]) #lowers the arm to be within reach of the XFP
        ✓    moveJ
         ✓     xfp_position  #moves the arm to the translated pose
       ✓ Grip(0)
       ✓ xfp_position = poseTrans(plane_camera, p[xfp_data[1]/1000, xfp_data[2]/1000, -0.19, 0, 0, xfp_data[3]]) #raises the arm from the place where the xpf was
       ✓  moveJ
        ✓    #Waypoint_levantado
        ✓    #Waypoint_suporte para pousar o xfp ## MAY REQUIRE ADJUSTMENTS
        ✓ Release(37mm)
        ✓ if(xfp_side == 1){ # Meaning XFP is 'front'
           ✓ subprogram(Grab_XFP_To_testbox) #Subprogram grabs XFP from the rear, without turning it, and moves to Waypoint_TestBoxPOV
           }
        ✓ elif(xfp_side == 2){ # Meaning XFP is 'back'
           ✘✓ subprogram(TurnXFP) #Subprogram grabs XFP from the rear, turns it upside down, and moves Waypoint_TestBoxPOV
               # nao esta a funcionar bem, estamos a usar uma versao mais beta
           }
       ✓ send_trigger("find_free_port") #Takes photo of the box and calulates free port position
       ✓ free_port_data = [PolyscopeVar, X, Y] #X and Y come from computer processed photo.
       ✓ free_port_pos = poseTrans(TestBox_Plane, p[free_port_data[1]/1000,free_port_data[2]/1000, -100/1000, 0, 0, 0]) #VERIFICAR MEDIDAS E  SE É PRECISO ALPHA OU NÃO!!!!!
       ✓ moveJ 
       ✓    free_port_pos #moves to free port position, just a few centimeters from the port.
       ✓ free_port_pos = poseTrans(TestBox_Plane, p[free_port_data[1]/1000,free_port_data[2]/1000, -30/1000, 0, 0, 0]) #VERIFICAR  MEDIDAS E SE É PRECISO ALPHA OU NÃO!!!!!
       ✓ moveJ   
       ✓    free_port_pos # moves the remaining distance to insert the XFP into the port.
       ✓ Release(37 mm) # releases the inserted XFP
       ✓ Subprogram(insertFiber); #insert the fiber into the XFP slot
     
 ✓ reset_conection_with_coputer
