

while True:

    #checks to see if theres been any message from polyscope

    s = socket.socket()
    
    s.listen()
    

    if s == x: 
        find_port_of_test()
        
    elif s ==y:
        find_xfp()

    elif s == w:
        find_free_port()
    elif s == w:
        #verifies if a test ended
        communicate_with_test_box()
    else:
        continue


# How many inputs and outputs the functions have
find_port_of_test()
    input: photo
    output: 6 - center of port defined by - XYZ and each rotation

find_xfp()
    input: photo
    output: 6 - center of xfp defined by - XYZ and each rotation
    
    We may need to define a new label as the back of the xfp, to grab it by there

find_free_port()
    input: photo
    output:

communicate_with_test_box()
    input: 0
    output: 1 whitch return the last test that ended