# Project Instruction Manual (PRISM): a step-by-step guide to run our project from scratch.

## The Setup (Computer, UR5e Robotic Arm & Transceiver TestBox)

### On your Computer:  

**Step 1:** On a *Windows 10* OS, start by checking if you have python installed. Open your cmd terminal and type:

    python --version

If you don't have Python installed in your system, you can download it [here](https://www.python.org/)

**Step 2:** Installing PIP using cURL in Python. On the cmd terminal type:

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 

followed by:

    python get-pip.py

to make sure PIP was installed correctly, you can type:

    pip --version

**Step 3:** Downloading the project onto your machine. You can visit our repository [here](https://github.com/leonardo-ra/PI) and download the project's files via ZIP on the *"< > Code"* button.
Alternatively, you can install git and later clone this repository. If you wish to do so, you can follow this [guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).


**Step 4:** Installing the required libraries. After downloading and extracting the files (or cloning the repo), open your cmd terminal and go to the project's *Setup* directory. In this directory, run the following command:   

    pip install -r requirements.txt 

:white_check_mark: The terminal setup should be good to go. :white_check_mark:

**Step 5:** Connect the UR5e's Ethernet cable to your PC's Ethernet port - it should also work on a USB port, by using an Ethernet/USB adaptor.

**Step 6:** Setting a static IP address. Got to Windows *Control Panel* > *Network and Internet* > *Network and Sharing Centre*. You should see an "Unknown" Ethernet connection. Click on the Ethernet icon. You should now see the connection status tab:

![](https://user-images.githubusercontent.com/94324481/213884196-a500d02a-3423-45db-8f46-a1f7d9e1ee33.png)

Go to *Properties* > (double-click) *Internet Protocol Version 4 (TCP/IPv4)*. You should see the IPV4 properties tab:

![](https://user-images.githubusercontent.com/94324481/213884361-1276a03f-49a7-45f3-a0d5-dd22c541e9ab.png) ![](https://user-images.githubusercontent.com/94324481/213884416-8f11dfac-319c-4e56-b34c-7608a6a7d279.png)

Tick the option "*Use the following IP address:*" and fill in the parameters with these (optional) values:

![](https://user-images.githubusercontent.com/94324481/213884549-07bafe8a-ad6b-430a-86a1-6f77f802819a.png)

***NOTE:*** The IP address should be on the same network as the UR5e i.e:
 - If you set your Robot's IP address with: 192.1.1.1 ; submask: 255.255.255.0 ; Gateway: 192.1.1.1  

 - Your machine's Ethernet connection should be something like: 192.1.1.**2** ; submask: 255.255.255.0 ; Gateway: 192.1.1.**2**

(The Robot's IP address setup will be answered further below.)

 Apply and save your changes before closing the tabs.

**Step 7:** Disabling the firewall. This step ensures that the connection is well established between the UR5e and your PC.
Go to *Control Panel* > *System and Security* > *Windows Defender Firewall*:

![](https://user-images.githubusercontent.com/94324481/213371426-ec0315e0-3648-41cb-b071-5352a083d2ca.png)

Go to *Turn Windows Defender Firewall on or off* and tick *Turn off Windows Firewall (not recommended)* on both types of network settings (Private and Public):
 
![](https://user-images.githubusercontent.com/94324481/213372114-67e5c09d-bd2f-4c0f-b7a9-f18f5a001317.png)

**Step 8:** Connect the camera to your PC via USB Type C or USB type A (using an adaptor).

**Step 9:** Connect the TestBox to your PC via USB type A. Do not turn it on yet though.

:white_check_mark: Your PC connection should be set now :white_check_mark:

### On the UR5e teach Pendant (Tablet):  

**Step 10:** Turning the Robot on. After booting up the teach Pendant, start by turning the Ur5e completely ON (releasing the brakes) by pressing the *Power off* button, on the bottom-left corner.

![](https://user-images.githubusercontent.com/94324481/213373266-7e36d5fd-c0c5-476e-bc3d-f26a0e29375f.png)

**Step 11:** In the welcome menu, press the blue *Load Program* Icon. You should see a program called **Polyscope_main.urp**, load it by opening the program.  

![](https://user-images.githubusercontent.com/94324481/213373812-064f7821-58c9-46d5-aa30-ed5cbc14d2da.png)

**Step 12:** Go to the *Dropdown menu* icon in the top-right corner of the welcome screen. Press the *Settings* tab > *Network* tab, and set the Robot's IP address, submask and gateway. You can set the remaining parameters as '0.0.0.0'. Press apply.

***NOTE:*** Make sure these three fields match the note presented in **Step 6**.

![](https://user-images.githubusercontent.com/94324481/213375458-0198e3ac-3dec-4d27-93d3-6bd40245b09c.png)

**Step 13:** Press the *Teach Pendant* icon in the top-right corner of the welcome screen - it should read *Local* by default - if it doesn't, switch to *Local Control*.

:white_check_mark: The Robot Arm is now fully setup and ready to run :white_check_mark: 

### Running the System:

**Step 14:** Booting the system - In the downloaded files/cloned repository, you should see a Python file named "**run.py**". Start by opening that program in a code editor. You should run this file using:

    python3 run.py -h

You can alter the specified information, according with the previous steps (**Step 6** and **Step 12**).


Besides this, there are a couple of lines of code in this program, that should be edited in accordance with the previous steps:

> sys.path.append('C:\\Users\\User\\Desktop\\PIC\\PIC\\Robô final\\PI\\Modules')

This path should be changed to the location of your files.

Also, the bit of code inside the *load_model* function. 

> model1 = torch.hub.load(r'C:\Users\User\Desktop\PIC\PIC\Robô final\Final2\yolov5', 'custom', path=r'C:\Users\User\Desktop\PIC\PIC\Robô final\Final2\yolov5\models\best (1).pt', source='local')

> model2 = torch.hub.load(r'C:\Users\User\Desktop\PIC\PIC\Robô final\Final2\yolov5', 'custom', path=r'C:\Users\User\Desktop\PIC\PIC\Robô final\Final2\yolov5\models\best_box2.pt', source='local')

The path to the project's files/cloned repo should be edited to their location in your computer. If you downloaded them to your Desktop, it should read something like this for example:

    model1 = torch.hub.load(r'C:\Users\Your_User\Desktop\PI\yolov5', 'custom', path=r'C:\Users\Your_User\Desktop\PI\yolov5\models\best (1).pt', source='local')`

**Step 15:** Verifying the TestBox. The system assumes it's using 'TestBox A' by default, however, before you can turn on the TestBox, make sure you check which one it is. To do this, you must edit all the occurrences of the function "getResults" inside "run.py":

> getResults(language='Portuguese',BoxCom = 'init', module='A')

The specified parameters that can be changed are: language (Portuguese or English) and module (A, B, C or D). 
The BoxCom parameter shouldn't be changed.  

After this, you can now turn the TestBox on.

**Step 16:** Starting sequence. After the previous steps were taken, your system should be fully connected, with both the UR5e and the TestBox loaded/turned on. The starting sequence is as follows:

**1** - On the UR5e teach Pendant menu, go to the top-left corner and  press the *Program* Icon. You should see the previously loaded program (Polyscope_main.urp). Press the *play* icon on the bottom of the screen and *Start from beginning*. 

![](https://user-images.githubusercontent.com/94324481/213376574-17fb8877-3ac6-4421-9348-9a875e18816a.png)


(The program should now be trying to connect via socket to your PC. You can see the highlighted blue text as it is running.)


**2** - Whilst the Polyscope_main.urp is running on the teach Pendant, you can run **run.py** on your terminal by typing this:

    python3 run.py

:white_check_mark: The program should be running! :white_check_mark:

## The Behaviour (What will the system do?)

Once the system is running, several control messages will appear on your terminal window, one of which will be this one:

> Do you wish to do Calibration? (Y/N)

Pressing Y, y or enter, will have the system calibrate itself using previously taken photos of the working surface.

Afterwards, a big TestBox Control App should pop out. This App will show you the status of the TestBox and its transceivers. This window should be put to the side or minimised, not closed!

Next, the system should print out its control/status messages in real time, without needing any further input from the user.

#### How the system works, in a nutshell -

 1) The arm moves to a top-view position, the camera takes a snapshot and sends it to the computer.

 2)  The script processes the photo using *Yolo* (You Only Look Once), finds the location of the transceiver, sends the coordinates back to the arm.

 3)  The arm moves to the appropriate location, and proceeds according to the teach Pendant instructions.

 4)  The arm goes to a front-facing view of the TestBox, the camera takes a snapshot and sends it to the computer (points (2) and (3) repeat).

 5)  The arm inserts the transceiver and their respective fibre optic cable in a previously detected port - sent by point (4).

 6)  The system repeats this from (1) to (5) until all the ports on the TextBox are filled by transceivers.

 7)  Once all the transceivers are inserted in the TestBox, as well as their respective optical fibres, a test begins. This test is run independently on the TestBox, and its status can be seen in the TestBox Control window.

***NOTE:*** Since this test is being run in parallel to the program/teach Pendant, it will keep running even if the those are halted. This is an important aspect to keep in mind when shutting down/resetting the system.

 8) Whilst the test is running in the background, the process keeps searching for more transceivers - going back to Point (1). 

 9) If a test is complete, the TestBox sends a signal and the arm proceeds to point (4) to remove all the transceivers and their cables - the teach Pendant has a different set of instructions for this phase. The arm then releases the transceiver in a specific zone, according to its respective test result (OK or Not OK).

 10) Afterwards, if all the transceivers are removed, the system loops back to point (1).


#### Some common errors/issues and troubleshooting:

- **a)** The script freezes on 
> Starting program

This issue usually occurs when the system wasn't initialised in the correct order (Pendant 1st, script 2nd), or the Ethernet cable isn't connected and the system can't perform the socket connection. **Solution** - Kill the terminal and reset the system, making sure everything is connected.

- **b)** Closing the TestBox Control App will make it impossible to communicate with it, compromising the system's functions. This window should only be closed once the system is ready to be shut down.


## Turning off/Resetting the system

### On the teach pendant:

**Step 1:** Stop the teach Pendant program by pressing the *stop* icon next to *play*.

### On your Computer:

**Step 2:** On the terminal, a message reading:

> ! Polyscope program was stopped ! Ctrl+C on the terminal, Reboot the system.

should appear. Proceed as instructed by pressing Ctrl+C, and the program should stop.

**Step 3:** 

- **a)** If the TestBox is not performing any tests, close the TestBox Control window.

- **b):** If a test is currently running on the TestBox, wait for its completion before closing the TestBox Control window.

***NOTE:*** This prevents bugs/erroneous behaviour from the system once it is rebooted. It bears mentioning as well, that although not fatal, turning the TestBox off in the middle of a test is not recommended either.

:white_check_mark: At this point the system should cease running completely :white_check_mark:

**Step 4:** Restart the system in the previously mentioned order (**Step 16:** Starting Sequence).

## Reference Material and other Manuals

**Universal Robots:** 
- [TCP/IP Connections](https://www.universal-robots.com/articles/ur/interface-communication/tcpip-socket-communication-via-urscript/)
- [User Manual (EN)](https://s3-eu-west-1.amazonaws.com/ur-support-site/40974/UR5e_User_Manual_en_US.pdf)
- [User Manual (PT)](https://s3-eu-west-1.amazonaws.com/ur-support-site/181353/99443_UR5e_User_Manual_pt_Global.pdf)
- [2FG7 OnRobot Gripper Manual (EN)](https://www.wmh-trans.co.uk/file.php?filename=ONR-106376%2FUser_Manual_For_UR_Robots_Quick_Changer_2FG7_v1.4.0_EN.pdf)
- [The URScript Programming Languange (EN)](https://www.siemens-pro.ru/docs/ur/scriptManual.pdf)

**Yolo:**
- [How to work with yolo, playlist guide](https://www.google.com/search?q=yolov5%20guide&tbm=vid&sxsrf=AJOqlzXnWTfcoxvoI_dw-P0D6z8fsZqR4Q%3A1674418098497&ei=spfNY_70HeqmkdUPjrqP8AQ&start=10&sa=N&ved=2ahUKEwj-ld2__dv8AhVqU6QEHQ7dA04Q8tMDegQIDhAE&biw=1920&bih=965&dpr=1#fpstate=ive&vld=cid:b4e9ef33,vid:rZyY2pNzypQ)
- [How to deploy YOLO, video guide](https://www.youtube.com/watch?v=KQKwXga_uTM)
- [Yolov5 GitHub](https://l.messenger.com/l.php?u=https%3A%2F%2Fgithub.com%2Fultralytics%2Fyolov5&h=AT0phyS36LDwkbLh0pNSvMVA3eeYAEQKcm_SyiWmiZQ4uGwZl53QSDWBDs2fednImFtwI1h_uiBN_epnr49gisnXlSsWN1ikJUIFtH-OwegVeoY8yeiO2XwydlNJH6ItQAiRlg)
- Instructions to transfer YOLOv5 (PT): 
- 1) Ir ao git do yolo: https://github.com/ultralytics/yolov5
- 2) Download Zip para a pasta com os restantes ficheiros (main director)
- 3) Unzipp
- 4) Change name from yolov5-master to yolov5
- 5) yolov5-> models -> copy weights files (best (1).pt, best_box2.pt)
- 6) you must have the weight files also on the main director

**Roboflow:**
- [Roboflow website](https://roboflow.com/)
- [How to create an image dataset](https://docs.roboflow.com/adding-data)
- [What is YOLOv5, a Roboflow guide](https://blog.roboflow.com/yolov5-improvements-and-evaluation/)
- [Roboflow Youtube guides](https://www.youtube.com/@Roboflow/videos)

## Contacts

Leonardo Rodrigues:
    leonardo.r@ua.pt

Vasco Fernandes:
    vasco.fernandes@ua.pt

Pedro Carvalho:
    pmdc@ua.pt

Nuno Domingues: 
    nuno.coelho@ua.pt

João Cordeiro: 
    joao.cordeiro@ua.pt

João Mendes: 
    joaomendes20@ua.pt

>This project was only possible thanks to the environment provided by the brilliant team at PICadvanced, as well as engineers: Pedro Silva, Francisco Rodrigues & Pedro Carvalho alongside Professor Mário Lima.
