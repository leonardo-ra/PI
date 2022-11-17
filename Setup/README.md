# Project setup  

## Here are the various steps you should take for this program to work:    

#### On your machine:  

1. On a ***Linux*** based operating system, start by installing git, running the following comand on your terminal:  

'pip install git'  

2. Copy the HTTPS of this repository and clone it to your machine. You can do so by runnign this comand as well **Adicionar imagem** :  

'git clone https://github.com/leonardo-ra/PI.git"  

3. After cloning this repo, begin by installing the required libraries for this project to work:  

'pip install -r requirements.txt'  

Your setup on the terminal side of things should be good to go.  

4. Connect the Ethernet cable tou your machine's Ethernet port - it shoud also work by using an Ethernet/USB adaptor.

5. In your network settings, make sure the Ethernet connection is setup with a ***static*** IPV4 IP address:  

**Por imagem**  

The IP adress should be on the same network as the Robot i.e:
 - If you set your Robot's IP address with: 192.1.1.1 ; submask: 255.255.255.0 ; Gateway: 192.1.1.1  

 - Your machine's ethernet connection should be something like: 192.1.1.**2** ; submask: 255.255.255.0 ; Gateway: 192.1.1.**2**  

***The Robot's IP address setup will be answered further bellow.***

6. Connect the camera to your USB port.


Your connection should be well established on your machine's side of things now.

#### On the Ur5e teach Pendant:  

7. Start by turning the Ur5e completely ON (releasing the breaks).  

8. In the welcome menu, press the *Load Program* Icon. You should see a program called **Inserir nome do programa final**, load it by opening the program.  

**Inserir imagem**

***If you do not manage to find this specific program, proceed with the rest of the steps normally***  

9. At the left-top of the welcome screen, go to the *Installation* icon. Press the *URCaps* tab. In this section you should see all the installed UrCap nodes, including the 2FG Gripper and TCP caps. Set the parameters of the External Control URCap in acordance with the previously mentioned step 5. It should be set to something like this (using the same dummy IP):  

| Remote Host's IP (your machine's connection IP) | Port (you should not have to change this field) |
| ----------- | ----------- |
| 192.1.1.**2** | 50002 |

**Por imagem da cena do URCAP External Control**  

***If you do not see an ExternalControl UrCap, then you should install [it](https://github.com/UniversalRobots/Universal_Robots_ExternalControl_URCap/releases) first. You can follow [these instructions](https://github.com/UniversalRobots/Universal_Robots_ROS_Driver/blob/master/ur_robot_driver/doc/install_urcap_e_series.md).***  

10. To confirm that this was set up properly, and to add this feature to your program, simply click the *Program* icon (the one next to *Installation*). Press the *URCap* tab, and click on *ExternalControl*:

**Adicionar imagem**  

You should see an added *ExternalControl* to your *Robot Program* dropdown view. You can confirm the IP and port chosen, by pressing it.  
The 2FG and TCP URCaps should also be added to the *Robot Program* (they are usually added by default)

***If you loaded the program in step 8 this is what you should see***

11. Go to the *Dropdown menu* icon at the top-right corner of the welcome screen. Press the *Settings* tab -> *Network* tab, and set the Robot's IP address, submask and gateway. Press apply. ***Make sure these three fields match the instructions in step 5.***  

**Adicionar imagem**  

You can set the remainding parameters as 0.0.0.0  

12. Finally, press the *Teaching Pendant* icon on the welcome screen, and choose *Remote Control*.

#### Run it!

13. After these steps, everything should be set for you to run the code on your machine remotely:

'python3 **nome final do programa.py**'