# roboPtics - Robotic arms in an Optics Production Line

> A project within the purview of University of Aveiro's course subject: Projeto Industrial.  The subject gives a group of students the oportunity to work with well established companies, within the Eletrical Engineering field. As pitched by PICadvanced S.A. at the time, the objective consisted of integrating vision in a robotic arm (an UR5e), to further increase the automation and output of their production line.
This git repository details the developments made by the team of six students who tackled this project. 

> This manual serves as a basic step-by-step guide to run the system from scratch.

# Project Instruction Manual (PRISM): 

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

**Step 6:** Setting a static IP address. Got to Windows *Control Panel* > *Network and Internet* > *Network and Sharing Center*. You should see an "Unknown" Ethernet connection. Click on the Ethernet icon. You should now see the connection status tab:

**POR IMAGEM** 

Go to *Properties* > (double-click) *Internet Protocol Version 4 (TCP/IPv4)*. You should see the IPV4 properties tab:

**POR IMAGEM**

Tick the option "*Use the following IP address:*" and fill in the parameters with these (optional) values:

 **POR IMAGEM**

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

### On the Ur5e teaching Pendant (Tablet):  

**Step 10:** Turning the Robot on. After booting up the teaching Pendant, start by turning the Ur5e completely ON (releasing the brakes) by pressing the *Power off* button, on the bottom-left corner.

![](https://user-images.githubusercontent.com/94324481/213373266-7e36d5fd-c0c5-476e-bc3d-f26a0e29375f.png)

**Step 11:** In the welcome menu, press the blue *Load Program* Icon. You should see a program called **Polyscope_main.urp**, load it by opening the program.  

![](https://user-images.githubusercontent.com/94324481/213373812-064f7821-58c9-46d5-aa30-ed5cbc14d2da.png)

**Step 12:** Go to the *Dropdown menu* icon in the top-right corner of the welcome screen. Press the *Settings* tab > *Network* tab, and set the Robot's IP address, submask and gateway. You can set the remaining parameters as '0.0.0.0'. Press apply.

***NOTE:*** Make sure thse three fields match the instructions in step 6.

![](https://user-images.githubusercontent.com/94324481/213375458-0198e3ac-3dec-4d27-93d3-6bd40245b09c.png)

**Step 13:** Press the *Teaching Pendant* icon in the top-right corner of the welcome screen - it should read *Local* by default - if it doesn't, switch to *Local Control*.

:white_check_mark: The Robot Arm is now fully setup and ready to run :white_check_mark: 

### Running the System:

**Step 14:** Booting the system - In the downloaded files/cloned repository, you should see a Python file named "**NOME DO PROGRAMA FINAL.py**". Start by opening that program in a code editor.

**POR IMAGEM do editor final**

There are two lines of code in this program, that should be edited in acordance with the previous steps:

1:
    HOST = 192.1.1.2

This line of code must match the IP chosen for your PC connection in the previous steps (6 & 12).

2:
> model = torch.hub.load(r'C:\Users\Leo\Desktop\Eu\Trabalhoua\Matricula6Ano\1Sem\PI\Final(2)\yolov5', 'custom', path=r'C:\Users\Leo\Desktop\Eu\Trabalhoua\Matricula6Ano\1Sem\PI\Final(2)\yolov5\models\best (1).pt', source='local')

This bit of code is inside the *load_model* function. The path to the project's files/cloned repo should be edited to their location in your computer. If you donwloaded them to your Desktop, it should read somethine like this for example:

    model = torch.hub.load(r'C:\Users\Your_User\Desktop\NOMEDOFILE_FINALDOGIT\yolov5', 'custom', path=r'C:\Users\Your_User\Desktop\NOMEDOFILE_FINALDOGIT\yolov5\yolov5\models\best (1).pt', source='local')`

Save the edited **NOME DO PROGRAMA FINAL.py EDITAR AS LINHA DE CIMA TAMBÉM!**.

**Step 15:** Verifying the TestBox. The system assumes its using 'TestBox A' by default, however, before you can turn on the TestBox, make sure you check which one it is.

**POR AS COISAS QUE TÊM DE MUDAR NO PROGRAMA (SE É A CAIXA 'A', 'B', 'C'...) CASO SEJA PRECISO MUDAR**

You can now turn the TestBox on.

**Step 16:** Starting sequence. After the previous steps were taken, your system should be fully connected, with both the UR5e and the TestBox loaded/turned on. The starting sequence is as follows:

**1** - On the UR5e teaching Pendant menu, go to the top-left corner and  press the *Program* Icon. You should see the previously loaded program (Polyscope_main.urp). Press the *play* icon on the bottom of the screen, and *Start from beginning*. 

![](https://user-images.githubusercontent.com/94324481/213376574-17fb8877-3ac6-4421-9348-9a875e18816a.png)


(The program should now be trying to connect via socket to your PC. You can see the higlighted blue text as it is running.)


**2** - Whilst the Polyscope_main.urp is running on the teaching Pendant, you can run **NOME DO PROGRAMA FINAL.py** on your terminal by typing this:

    python3 NOME DO PRGRAMA FINAL.py

:white_check_mark: The program should be running! :white_check_mark:

## The Behaviour (What will the system do?)

Once the system is running, several control messages will appear on your terminal window, one of which will be this one:

> Do you wish to do Calibration? (Y/N)

Pressing Y, y or enter, will have the system calibrate itself using previously taken photos of the working surface. **Acrescentar ou remover**

Afterwards, a big TestBox Control App should pop out. This App will show you the status of the TestBox and its transceivers. This window should be put to the side or minimised, not closed!

Next, the system should print out its control/status messages in real time, without needing any further input from the user.

#### How the system works, in a nutshell -

 1) The arm moves to a top-view position, the camera takes a snapshot and sends it to the computer.

 2)  The script processes the photo using *Yolo* (You Only Look Once), finds the location of the transceiver, sends the coordenates back to the arm.

 3)  The arm moves to the apropriate location, and proceeds acording to the teaching Pendant instructions.

 4)  The arm goes to a front-facing view of the TestBox, the camera takes a snapshot and sends it to the computer (points (ii) and (iii) repeat).

 5)  The arm inserts the transceiver and their respective fiber optic cable in a previously detected port - sent by point (iv).

 6)  The system repeats this from (i) to (v) until all the ports on the TextBox are filled by transceivers.

 7)  Once all the transceivers are inserted in the TestBox, as well as their respective optical fibers, a test begins. This test is run independently on the TestBox, and its status can be seen in the TestBox Controll window.

***NOTE:*** Since this test is being run in parallel to the program/teaching Pendant, it will keep running even if the those are halted. This is an important aspect to keep in mind when shutting down/reseting the system.

 8) Whilst the test is running in the background, the process keeps searching for more transceivers - going back to Point (i). 

 9) If a test is complete, the TestBox sends a signal and the arm proceeds to point (iv) to remove all the transceivers and their cables - the teaching Pendant has a different set of instructions for this phase. The arm then releases the transceiver in a specific zone, acording to its respective test result (OK or Not OK).

 10) Afterwards, if all the transceivers are removed, the system loops back to point (i).


#### Some common errors/issues and troubleshooting:

- **a)** The script freezes on 
> Starting program

This issue usually occurs when the system wasn't inicialised in the correct order (Pendant 1st, script 2nd), or the Ethernet cable isn't connected and the system can't perform the socket connection. **Solution** - Kill the terminal and reset the system, making sure everything is connected.

- **b)** **ADICIONAR O ERRO DE TCP QUANDO SE FECHA A APLICAÇÃO DA PIC** 

- **c)** **ADICIONAR O ERRO DA CÂMARA N TAR LIGADA**

- **d)** **Adicionar eventualmente mais algum erro que seja mais comum.**

## Turning off/Reseting the system

### On the teaching pendant:

**Step 1:** Stop the teaching Pendant program by pressing the *stop* icon next to *play*.

### On your Computer:

**Step 2:** On the terminal, a message reading:

> ! Polyscope program was stopped ! Ctrl+C on the terminal, Reboot the system

should appear. Proceed as instructed by pressing Ctrl+C, and the program should stop.

**Step 3:** 

- **a)** If the TestBox is not performing any tests, close the TestBox Controll window.

- **b):** If a test is currently running on the TestBox, wait for its completion before closing the TestBox Controll window.

***NOTE:*** This prevents bugs/erroneous behaviour from the system, once it is rebooted. It bears mentioning as well, that although not fatal, turning the TestBox off in the middle of a test is not recommended either.

:white_check_mark: At this point the system should cease running completely :white_check_mark:

**Step 4:** Restart the system in the aforementioned order (**Step 16:** Starting Sequence).

## Reference Material and other Manuals

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

## Contacts

Leonardo Rodrigues:
    leonardo.r@ua.pt

Vasco Fernandes:
    x

Pedro Carvalho:
    x

Nuno Domingues: 
    x

João Cordeiro: 
    x

João Esteves: 
    x

**Não sei se querem também os vossos?**

>This project was only possible thanks to the environment provided by the brilliant team at PICadvanced, as well as engineers: Pedro Silva & Francisco Rodrigues, alongside Professor Mário Lima.

**Posso tirar a quote se acharem que fica estúpido...**
