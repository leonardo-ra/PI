# Project Instruction Manual (PRISM):

##### This manual serves as a basic step-by-step setup to run the UR5e Robot system, in conjunction with your PC, in order to perform the various autonomous tasks (inserting/removing, locating and testing of transceivers) required by PICadvanced.

### On your machine:  

**Step 1:** On a **Windows 10** OS, start by checking if you have python installed. Open your cmd terminal and type:

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

:white_check_mark: The terminal setup should be good to go. :white_check_mark:

**Step 5:** Connect the UR5e's Ethernet cable to your PC's Ethernet port - it should also work on a USB port, by using an Ethernet/USB adaptor.

**Step 6:** Setting a static IP address. Got to Windows *Control Panel* > *Network and Internet* > *Network and Sharing Center*.You should see an Unknown Ethernet connection. Click on the Ethernet icon. You should now see the connection status tab:

**POR IMAGEM** 

Go to *Properties* > double-click *Internet Protocol Version 4 (TCP/IPv4)*. You should see the IPV4 properties tab:

**POR IMAGEM**

Tick the option *Use the following IP address:* and fill the parameters with these (optional) numbers:

 **POR IMAGEM**

**NOTE:** The IP address should be on the same network as the Robot i.e:
 - If you set your Robot's IP address with: 192.1.1.1 ; submask: 255.255.255.0 ; Gateway: 192.1.1.1  

 - Your machine's Ethernet connection should be something like: 192.1.1.**2** ; submask: 255.255.255.0 ; Gateway: 192.1.1.**2**

 ***The Robot's IP address setup will be answered further below.***

 Apply and save your changes before closing the tabs.

**Step 7:** Disabling the firewall. This step ensures the connection is well established between the UR5e and your PC.
Go to *Control Panel* > *System and Security* > *Windows Defender Firewall*:

**POR IMAGEM**

Go to *Turn Windows Defender Firewall on or off* and tick *Turn off Windows Firewall (not recommended)* on both types of network settings (Private and Public):

**POR IMAGEM** 


**Step 8:** Connect the camera to your PC via USB Type C or USB type A (using the adaptor).

:white_check_mark: Your UR5e-PC connection should be set now :white_check_mark:

### On the Ur5e teach pendant (Tablet):  

**Step 9:** Turning the Robot on. After booting up the teach pendant, start by turning the Ur5e completely ON (releasing the brakes) by pressing the *Power Off* button, on the bottom-left corner.

![Alt text](../../../../Downloads/Step9.jpg)

**Step 10:** In the welcome menu, press the *Load Program* Icon. You should see a program called **Polyscop_main.urp**, load it by opening the program.  

**POR IMAGEM**

***If you do not manage to find this specific program, proceed with the rest of the steps normally***  

**Step 11:** Go to the *Dropdown menu* icon in the top-right corner of the welcome screen. Press the *Settings* tab -> *Network* tab, and set the Robot's IP address, submask and gateway. Press apply. ***Make sure these three fields match the instructions in step 5.***  

**Adicionar imagem**  

You can set the remaining parameters as 0.0.0.0  

**Step 12:** Finally, press the *Teaching Pendant* icon in the top-right corner of the welcome screen - it should read *Local* by default - switch to *Remote Control*.

The Robot Arm is now fully setup. :white_check_mark:

### *Send it!*

**Step 13:** After these steps, everything should be set for you to run the code on your machine remotely. Just type this in your terminal:

`python3 **nome final do programa.py**` 


**NOTA** : Este depois vai ser o README que se vê no front page do gitHub. Acho que faz sentido substituir o do progresso por este, penso eu.

**Step 9:** Connect the TestBox to your PC via USB type A. 