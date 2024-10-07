### Modules

#Internal

> tkinter
> os
> time
> random
> datetime
> io
> sqlite3
> functools
> sys
> traceback
> shutil

#External - must be installed

> customtkinter [MUST BE VERSION 4.6.3]		(https://pypi.org/project/customtkinter/)
> Pillow 					(https://pypi.org/project/Pillow/)
> tkinter-tooltop 				(https://pypi.org/project/tkinter-tooltip/)
> fpdf2 					(https://pypi.org/project/fpdf2/)
> yagmail 					(https://pypi.org/project/yagmail2/)
> matplotlib 					(https://pypi.org/project/matplotlib/)

the package manager pip is required for importing (https://pip.pypa.io/en/stable/)

External modules will be automatically installed on first bootup of system. 
If there are issues with this paste the following lines into command prompt one at a time:

py -m pip uninstall customtkinter
py -m pip install customtkinter==4.6.3
py -m pip install Pillow
py -m pip install tkinter-tooltip
py -m pip install fpdf2
py -m pip install yagmail
py -m pip install matplotlib




###Entry Point

To start the program run the python file "!Main"





###Access Levels

Level		Username/Email		Password

Customer	testing@gmail.com	Testing!23
Lower		laccount0003		Password!23
Upper		uaccount0002		Password!23
Admin		aaccount0001		Password!23

####IMPORTANT###
At the top of the python code "!Main" there is a variable to toggle Testing on or off. testing is currently on.
Testing mode will autofill any username or password fields throughout the system to easy testing.
It autofills the Customer and the Admin levels although this is editable at the top of the code also.
It will also reduce validation to only the necessities.




###Validation

When Testing is off:
All entry fields are validated


When Testing is on:
> Emails must include @gmail.com, at least one more character and no spaces
> Password presence check

> Game title length check
> Game description length check
> Game price type check





###Staff Extra Information

Lower Level staff are able to input images when creating or editing a game.
To do this:
1. First image should be roughly 1:1 ratio. Image will be resized to 140x140 by the system
2. Second image should be roughly 1:2 ratio. Image will be resized to 450x260 by the system
3. In order to minimize distortion, images should be as close to specified dimensions as possible (140x140 and 450x260). 
4. Images need to be in png format.
5. Images need to be renamed. The first image should be named {gameName}.png and the second should be named {gameName}Big.png 
	where {gameName} is the image name you type into the create game page.
6. Save images in Media/GameImages folder
7. Create or edit a game and input the correct image name. If the image name is correct the resized images will appear on screen.


Backups will occur on the first bootup of each day. These can be found in the Backups folder.
To restore these just delete the current database, copy and paste the desired version into the main folde and name it GoatGamesDB.




###Editors used

In the creation of this system these editors were used:

> Python IDLE 3.9.7
> DB Browser



