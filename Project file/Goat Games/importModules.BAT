@echo off

title Importing Modules... Please Wait
py -m pip uninstall customtkinter
py -m pip install customtkinter==4.6.3
py -m pip install Pillow
py -m pip install tkinter-tooltip
py -m pip install fpdf2
py -m pip install yagmail
py -m pip install matplotlib