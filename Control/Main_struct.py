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

        go to test box fixed position 

        sends trigger
        Position_of_port,Result_of_test = input_from_computer(find_port_of_test)

        get closer to Position_of_port

        sends trigger
        confirm position??
        
        removes optic fiber

        unlock removal mechanism
        remove XFP

        if Result_of_test == ok:
            Drop_in_fixed point
        if Result_of_test == nok:
            Drop_in_fixed point


    ✓ if test_done = 0:
     subprogram(go_to_xfp_position)
     {
     ✓ go to default initial position to read XFP #WapointX (substituir com o número do waypoint final)
     ✓ sends trigger "take xfp photo"
     ✓ xfp_data = data_from_foto_taken # PolyscopeVar, X, Y, Alpha, Side, !!!!!!!Push!!!!!!!
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
        ✓ if(xfp_side == 1) # Meaning XFP is 'front'
           ✓ subprogram(Grab_XFP_To_testbox)x
        ✓ elif(xfp_side == 2) # Meaning XFP is 'back'
           ✓ subprogram(TurnXFP) #Subprogram grabs XFP from the rear, and moves Waypoint_TestBoxPOV
               # nao esta a funcionar bem, estamos a usar uma versao mais beta
        
         send_trigger("Find_Free_Port") #Takes photo of the box and calulates free port
         Location_of_port = input_from_computer(find_free_port)

         go to Location_of_port

         insert XFP
         lock removal mechanism
         adds optic fiber       
 }
   ✓ reset_conection_with_coputer
