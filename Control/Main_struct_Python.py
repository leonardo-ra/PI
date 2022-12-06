

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
    elif s == k:
        #verifies if a test ended
        communicate_with_test_box()
    else:
        continue


# How many inputs and outputs the functions have
find_port_of_test()
    input: photo
    output: 3. x.y and alpha

find_xfp()
    input: photo
    output: 3. x.y and alpha
    
    We may need to define a new label as the back of the xfp, to grab it by there

find_free_port()
    input: photo
    output: 3. x.y and alpha

communicate_with_test_box()
    input: 0
    output: 2 whitch return the last test that ended and the result
