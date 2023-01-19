# Project Instruction Manual (PRISM):

##### This manual serves as a basic step-by-step setup to run the UR5e Robot system, in conjunction with your PC, in order to perform the various autonomous tasks (inserting/removing, locating and testing of transceivers) required by PICadvanced.

## The Setup - 

### On your machine:  

**Step 1:** On a *Windows 10* OS, start by checking if you have python installed. Open your cmd terminal and type:

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

***NOTE:*** The IP address should be on the same network as the Robot i.e:
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

**Step 9:** Connect the TestBox to your PC via USB type A. Do not turn it on yet though.

:white_check_mark: Your UR5e-PC connection should be set now :white_check_mark:

### On the Ur5e teaching Pendant (Tablet):  

**Step 10:** Turning the Robot on. After booting up the teaching Pendant, start by turning the Ur5e completely ON (releasing the brakes) by pressing the *Power off* button, on the bottom-left corner.

![](https://user-images.githubusercontent.com/94324481/213317182-5cc400c3-d07f-4835-af4f-762138f56941.jpg)


**Step 11:** In the welcome menu, press the blue *Load Program* Icon. You should see a program called **Polyscope_main.urp**, load it by opening the program.  

**POR IMAGEM**

**Step 12:** Go to the *Dropdown menu* icon in the top-right corner of the welcome screen. Press the *Settings* tab -> *Network* tab, and set the Robot's IP address, submask and gateway. Press apply.

***NOTE:*** Make sure these three fields match the instructions in step 6.  

**POR IMAGEM**  

You can set the remaining parameters as '0.0.0.0'. 

**Step 13:** Press the *Teaching Pendant* icon in the top-right corner of the welcome screen - it should read *Local* by default - if it doesn't, switch to *Local Control*.

:white_check_mark: The Robot Arm is now fully setup and ready to run :white_check_mark: 

### Running the System:

**Step 14:** Booting the system - In the downloaded files/cloned repository, you should see a Python file named "**NOME DO PROGRAMA FINAL.py**". Start by opening that program in a code editor.

**POR IMAGEM do editor**

There are two fields that should be changed in this program, in acordance with the previous steps:

> HOST = 192.1.1.2

This must match the IP chosen in the previous steps (6 & 12).

> model = torch.hub.load(r'C:\Users\Leo\Desktop\Eu\Trabalhoua\Matricula6Ano\1Sem\PI\Final(2)\yolov5', 'custom', path=r'C:\Users\Leo\Desktop\Eu\Trabalhoua\Matricula6Ano\1Sem\PI\Final(2)\yolov5\models\best (1).pt', source='local')

This bit of code is inside the *load_model* function. The path to the project files/cloned repo should be edited to their location in your PC. If you donwloaded them to your Desktop, it should read somethine like this for example:

`model = torch.hub.load(r'C:\Users\Your_User\Desktop\NOMEDOFILE_FINALDOGIT\yolov5', 'custom', path=r'C:\Users\Your_User\Desktop\NOMEDOFILE_FINALDOGIT\yolov5\yolov5\models\best (1).pt', source='local')`

Save the edited **NOME DO PROGRAMA FINAL.py VER NA LINHA DE CIMA TAMBÉM!**.

**Step 15:** Verifying the TestBox. The project was tested using 'TestBox A', however before you can turn on the TestBox, make sure you check which one it is.

**POR AS COISAS QUE TÊM DE MUDAR NO PROGRAMA (SE É A CAIXA 'A', 'B', 'C'...) CASO SEJA PRECISO MUDAR**

You can now turn the TestBox on.

**Step 16:** Booting sequence. After the previous steps were taken, your system should be fully connected, with both the UR5e and the TestBox running. The booting sequence of operations is as follows:

**1** - On the UR5e teaching Pendant menu, go to the top-left corner and  press the *Program* Icon. You should see the program loaded. Press the *play* icon on the bottom of the screen, and *Start from beginning*. 

(The program should now be trying to connect via socket to our PC)


**2** - Whilst the Polyscope_main.urp is running on the teaching Pendant, you can run **NOME DO PROGRAMA FINAL.py** on your terminal. To do so you can type this:

`python3 NOME DO PRGRAMA FINAL.py`

:white_check_mark: The program should be running! :white_check_mark:

## Behaviour - 

Once the system is running, one of several prints that will appear on your terminal will be this one:

> Do you wish to do Calibration? (Y/N)

Pressing Y,y or enter on this section, will have the system calibrate itself using previously taken photos of the working surface. **Acrescentar ou remover**

Later, a big TestBox Control App should pop out. This App will show you the status of the test box and its transceivers. This window should be put to the side/minimised (not closed!).

Afterwards, the system should print out its control/status messages in real time, without needing any further input from the user.

#### How the system works, in a nutshell -

**1** - The arm moves to a top-view position, the camera takes a snapshot and sends it to the computer.

**2** - The script processes the photo using *Yolo* (You Only Look Once), finds the location of the transceiver, sends the coordenates back to the arm.

**3** - The arm moves to the apropriate location, and proceeds acording to the teaching Pendant instructions.

**4** - The arm goes to a front-facing view of the TestBox, the camera takes a snapshot and sends it to the computer (points **2** and **3** repeat).

**5** - The arm inserts the transceiver and their respective fiber optic cable in a previously detected port - point **4**.

**6** - Repeat from **1** to **5** until all slots inserted.

**7** - Once all the transceivers are inserted in the TestBox, as well as their respective optical fibers, a test begins. This test is run independently on the TestBox and its status can be seen in the TestBox Controll window.
***NOTE:*** Since this test is being run in parallel to the program/teaching Pendant, it will keep running even if the latter ones get halted. This is an important aspect to keep in mind when shutting down/reseting the system.

**8** - Whilst the test is running in the background, the process repeats itself until it can no longer find a transceiver.

**9** - If a test is complete, the TestBox sends a signal and the arm proceeds to point **4** to remove all the transceivers and their cables - the teaching Pendant has a different set of instructions for this phase. The arm then releases the transceiver in a specific zone, acording to its respective test result.

**10** - Afterwards, the system goes back to Point **1** and repeats itself.


#### Some common errors/issues and troubleshooting:

**a)** The script freezes on *Starting program*: this issue usually occurs when the system wasn't inicialised in the correct order (Pendant 1st, script 2nd), or the Ethernet cable isn't connected and the system can't perform the socket connection. **Solution** - Kill the terminal and reset the system, making sure everything is connected.

**b)** **ADICIONAR O ERRO DE TCP QUANDO SE FECHA A APLICAÇÃO DA PIC** 

**c)** **ADICIONAR O ERRO DA CÂMARA N TAR LIGADA**

**d)** **Adicionar eventualmente mais algum erro que seja mais comum.**

## Turning off/Reseting the system -

### On the teaching pendant:

**Step 1:** Stop the teaching Pendant program by pressing the *stop* icon next to the *play* one.

**Step 2:** On the terminal, a message reading:

> ! Polyscope program was stopped ! Ctrl+C on the terminal, Reboot the system

Press Ctrl+C, and the program should stop.

**Step 3a:** If the TestBox is not performing any tests, close the TestBox Controll window.

**Step 3b:** If a test is currently running on the TestBox, wait till its completion before closing the TestBox Controll window.

**Step 4:** Restart the system in the aforementioned order (**Step 16:** Booting Sequence).

***NOTE:*** This prevents bugs/erroneous behaviour from the system, once it is rebooted. It bears mentioning as well, that although not fatal, turning the TestBox off whilst it is running a test is not recommended either.

## Reference Material and other Manuals:

**Universal Robots:** 
- [TCP/IP Connections](https://www.universal-robots.com/articles/ur/interface-communication/tcpip-socket-communication-via-urscript/)
- [User Manual (EN)](https://s3-eu-west-1.amazonaws.com/ur-support-site/40974/UR5e_User_Manual_en_US.pdf)
- [User Manual (PT)](https://s3-eu-west-1.amazonaws.com/ur-support-site/181353/99443_UR5e_User_Manual_pt_Global.pdf)
- [2FG7 OnRobot Gripper Manual (EN)](https://www.wmh-trans.co.uk/file.php?filename=ONR-106376%2FUser_Manual_For_UR_Robots_Quick_Changer_2FG7_v1.4.0_EN.pdf)
- [The URScript Programming Languange (EN)](https://www.siemens-pro.ru/docs/ur/scriptManual.pdf)

**Yolo:**
**POR OS LINKS DE TUTORIAIS OU ASSIM DE YOLO/JUPYTER AS CENAS DE VISÃO QUE SE UTILIZARAM**
- [What is Yolo?]()
- ...
- ...

**Roboflow:**
- [Roboflow web site](https://roboflow.com/)
- [How to create an image dataset](https://docs.roboflow.com/adding-data)
- ...
- ...

## Contacts:

Leonardo Rodrigues: `leonardo.r@ua.pt`
**Não sei se querem também os vossos?**
Vasco Fernandes: ``
Pedro Carvalho: ``
Nuno Domingues: ``
João Cordeiro: ``
João Esteves: ``

**Posso tirar a quote se acharem que fica estúpido...**

>This project was only possible thanks to the environment provided by the brilliant team at PICadvanced, as well as engineers: Pedro Silva, Francisco Rodrigues and Professor Mário Lima.