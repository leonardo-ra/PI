

while ROBOT Program:
   
    resets variables
    
    while connection_with_computer == False:
        try_to_connect
       
    sends trigger
    test = communicate_with_test_box()
    
    if any test ended:

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


    if no test ended:

        go to XFP board fixed position 

        sends trigger
        Position_of_XFP, Side_of_XFP = input_from_computer(find_xfp)

        get close to Position_of_XFP
        
        confirm position??

        if Side_of_XFP == front:
            grab XFP

        if Side_of_XFP == back:
            adjust XFP 
            grab XFP

        if Side_of_XFP == side:
            adjust XFP 
            grab XFP

        go to test box fixed position 

        sends trigger
        Location_of_port = input_from_computer(find_free_port)

        go to Location_of_port

        insert XFP
        lock removal mechanism
        adds optic fiber

    reset_conection_with_coputer




