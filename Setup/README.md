# Project Instruction Manual (PRISM):

##### This manual serves as a basic step-by-step setup to run the UR5e Robot system, in conjunction with your PC, in order to perform the various autonomous tasks (inserting/removing, locating and testing of transceivers) required by PICadvanced.

### On your machine:  

**Step 1:** On a **Windows** OS, start by checking if you have python installed. Open your cmd terminal and type:

`python --version`

If you don't have Python installed in your system, you can download it [here](https://www.python.org/)

**Step 2:** Installing PIP using cURL in Python. On the cmd terminal type:

`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` 

followed by:

`python get-pip.py`

to make sure PIP was installed correctly, you can type:

`pip --version`

**Step 3:** Downloading the project onto your machine. You can visit our repository [here](https://github.com/leonardo-ra/PI) and download the project files via ZIP on the *< > Code* button.
Alternatively, you can install git and later clone this repository. If you wish to do so, you can follow this [guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).


**Step 4:** Installing the required libraries. After downloading and extracting the files (or cloning the repo), open your cmd terminal and go to the project's *Setup* directory. Run the following command:   

`pip install -r requirements.txt` 

:white_check_mark: The setup on the terminal should be good to go. :white_check_mark:

**Step 5:** Connect the Ethernet cable on the Robot to your PC's Ethernet port - it should also work by using an Ethernet/USB adaptor.

**Step 6:** Got to *Control Panel*. In your network settings, make sure the Ethernet connection is set up with a ***static*** IPV4 IP address:  

**Por imagem**  

The IP address should be on the same network as the Robot i.e:
 - If you set your Robot's IP address with: 192.1.1.1 ; submask: 255.255.255.0 ; Gateway: 192.1.1.1  

 - Your machine's Ethernet connection should be something like: 192.1.1.**2** ; submask: 255.255.255.0 ; Gateway: 192.1.1.**2**  

***The Robot's IP address setup will be answered further below.***

**Step 6:** Connect the camera to your USB type-C port.


Your connection should be well established on your machine's side of things now. :white_check_mark:

### On the Ur5e teach Pendant:  

**Step 7:** Start by turning the Ur5e completely ON (releasing the brakes).  

**Step 8:** In the welcome menu, press the *Load Program* Icon. You should see a program called **Inserir nome do programa final**, load it by opening the program.  

**Inserir imagem**

***If you do not manage to find this specific program, proceed with the rest of the steps normally***  

**Step 9:** At the left-top of the welcome screen, go to the *Installation* icon. Press the *URCaps* tab. In this section you should see all the installed UrCap nodes, including the 2FG Gripper and TCP caps. Set the parameters of the External Control URCap in accordance with the previously mentioned step 5. It should be set to something like this (using the same dummy IP):  

| Remote Host's IP | Port (you should not have to change this field) |
| ----------- | ----------- |
| 192.1.1.**2** | 50002 |

**Por imagem da cena do URCAP External Control**  

***If you do not see an ExternalControl UrCap, then you should install [it](https://github.com/UniversalRobots/Universal_Robots_ExternalControl_URCap/releases) first. You can follow [these instructions](https://github.com/UniversalRobots/Universal_Robots_ROS_Driver/blob/master/ur_robot_driver/doc/install_urcap_e_series.md).***  

**Step 10:** To confirm that this was set up properly, and to add this feature to your program, simply click the *Program* icon (the one next to *Installation*). Press the *URCap* tab, and click on *ExternalControl*:

**Adicionar imagem**  

You should see an added *ExternalControl* to your *Robot Program* dropdown view. You can confirm the IP and port chosen, by pressing it.  
The 2FG and TCP URCaps should also be added to the *Robot Program* (they are usually added by default)

***If you loaded the program in step 8 this is what you should see***

**Step 11:** Go to the *Dropdown menu* icon in the top-right corner of the welcome screen. Press the *Settings* tab -> *Network* tab, and set the Robot's IP address, submask and gateway. Press apply. ***Make sure these three fields match the instructions in step 5.***  

**Adicionar imagem**  

You can set the remaining parameters as 0.0.0.0  

**Step 12:** Finally, press the *Teaching Pendant* icon in the top-right corner of the welcome screen - it should read *Local* by default - switch to *Remote Control*.

The Robot Arm is now fully setup. :white_check_mark:

### *Send it!*

**Step 13:** After these steps, everything should be set for you to run the code on your machine remotely. Just type this in your terminal:

`python3 **nome final do programa.py**` 


**NOTA** : Este depois vai ser o README que se vê no front page do gitHub. Acho que faz sentido substituir o do progresso por este, penso eu.
