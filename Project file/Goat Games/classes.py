import tkinter
import customtkinter
from functools import partial
#from datetime import datetime
#from SQLfunctions import *

frameColour = "#2A2B2A"
textColour = "#CCFCCB"
hoverColour = "#86AC94"
bgColour = "#495051"
entryColour = "#ECFEEC"
warningColour = "#B02F07"
mainFont = "Bahnschrift SemiCondensed"


def center(win):
    """
    Parameters: win - Window to be centered
    Centers a window on the users screen
    """
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = win.winfo_screenwidth() // 2 - width // 2
    y = win.winfo_screenheight() // 2 - height // 2
    win.geometry(f"{width}x{height}+{x}+{y}")
    win.deiconify()


#Entries
class CustomEntry(customtkinter.CTkEntry):
    def __init__(self,master,width,state="normal",height=35,cornerRadius=10,borderWidth=0,borderColour=entryColour,fontSize=16,show="",placeholderText=""):
        super().__init__(master=master,##
                            width=width,##
                            height=height,#35
                            corner_radius=cornerRadius,#10
                            border_width=borderWidth,#0
                            border_color=borderColour,#entryColour
                            fg_color=entryColour,
                            text_color=bgColour,
                            text_font=(mainFont, fontSize),#16
                            placeholder_text=placeholderText,#""
                            state=state,#normal
                            show=show)#""

#tkinter lables              
class CustomTkLabelEntry(tkinter.Label):
    def __init__(self,master,text):

        width = len(text)
        super().__init__(master=master,##
                         width=width,#
                         height=1,
                         text=text,##
                         fg=textColour,
                         bg=frameColour,
                         anchor="w",
                         font=(mainFont, 16))
#Buttons
class CustomButtonLight(customtkinter.CTkButton):
    def __init__(self,master,width,height,text,command=None,fontSize=16,hoverEnabled=True,borderWidth=0,borderColour=textColour):
        super().__init__(master=master,##
                         width=width,##
                         height=height,##
                         corner_radius=20,
                         fg_color=textColour,
                         hover_color=hoverColour,
                         hover=hoverEnabled,#True
                         border_width=borderWidth,#0
                         border_color=borderColour,#textColour
                         text=text,##
                         text_color=frameColour,
                         text_font=(mainFont, fontSize),#16
                         command=command)##

class CustomButtonDark(customtkinter.CTkButton):
    def __init__(self,master,width,height,text,command=None,hoverEnabled=True,borderColour=textColour,state="normal",cornerRadius=20,borderWidth=5,fgColour=frameColour,hovColour=hoverColour,fontSize=18,bgColour=bgColour):
        super().__init__(master=master,##
                         width=width,##
                         height=height,##
                         corner_radius=cornerRadius,#20
                         fg_color=fgColour,#frameColour
                         border_width=borderWidth,#5
                         border_color=borderColour,#textColour
                         hover_color=hovColour,#hoverColour
                         hover=hoverEnabled,#True
                         text=text,##
                         text_color_disabled=hoverColour,
                         text_color=textColour,
                         text_font=(mainFont,fontSize),#18
                         bg_color=bgColour,#bgColour
                         state=state,#normal
                         command=command)#

class CustomButtonText(customtkinter.CTkButton):
    def __init__(self,master,width,height,text,state="normal",command=None,cornerRadius=20,hoverEnabled=True,fontSize=18,fgColour=frameColour,txtColour=textColour):

        if width == "scale":
            numSmall = 0
            numWide = 0
            numNormal = 0
            for n in range(0,len(text)):
                if text[n:n+1] in [" ","f","i","j","t"]:
                    numSmall += 1
                elif text[n:n+1] in ["m","w"]:
                    numWide += 1
                else:
                    numNormal += 1

            width = numNormal*(fontSize*0.7)+numSmall*(fontSize*0.3)+numWide*(fontSize*0.75)
            
        super().__init__(master=master,##
                         width=width,##
                         height=height,##
                         corner_radius=cornerRadius,#20
                         fg_color=fgColour,#frameColour
                         hover_color=hoverColour,
                         hover=hoverEnabled,#True
                         text=text,##
                         text_color=txtColour,#textColour
                         text_font=(mainFont,fontSize),#18
                         command=command,#None
                         state=state,#normal
                         text_color_disabled="#43574A")
#frames
class CustomFrame(customtkinter.CTkFrame):
    def __init__(self,master,width,height,borderWidth=0,borderColour=textColour,cornerRadius=20,fgColour=frameColour):
        super().__init__(master=master,##
                         width=width,##
                         height=height,##
                         border_width=borderWidth,#0
                         border_color=borderColour,#textColour
                         corner_radius=cornerRadius,#20
                         fg_color=fgColour)#frameColour     
#subclassGameFrame
class CustomFrameGame(CustomFrame):
    def __init__(self,master):
        super().__init__(master=master,
                         width=210,
                         height=260,
                         cornerRadius=20)

class CustomFrameBestsellers(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master=master,
                         width=270,
                         height=90,
                         corner_radius=20,
                         fg_color=frameColour,
                         border_width=2,
                         border_color=textColour)

#dropdown
class CustomDropdown(customtkinter.CTkOptionMenu):
    def __init__(self,master,variable,width=450,height=35,dynamicResizing = True, command=None, cornerRadius=10,fgColour=entryColour,txtColour=bgColour,buttonColour=textColour,state="normal",
                 values=[]):
        super().__init__(master=master,##
                            values=values,#
                            variable=variable,##
                            width=width,#450
                            height=height,#35
                            corner_radius=cornerRadius,#10
                            fg_color=fgColour,#entry
                            text_color=txtColour,#bg
                            text_font=(mainFont, 16),
                            button_color=buttonColour,#txt
                            button_hover_color=hoverColour,
                            dropdown_color=bgColour,
                            dynamic_resizing=dynamicResizing,
                            dropdown_hover_color=hoverColour,
                            dropdown_text_color=textColour,
                            command=command,
                            state=state)#normal

#subtitle
class CustomSubtitle(customtkinter.CTkLabel):
    def __init__(self,master,text,fontSize=26):
        width = len(text)*15
        super().__init__(master=master,##
                        width=width,#
                        height=35,
                        fg_color=frameColour,
                        text=text,##
                        text_color=textColour,
                        text_font=(mainFont, fontSize))#
        

class CustomLabel(customtkinter.CTkLabel):
    def __init__(self,master,height,text,fontSize,bgColour="",borderWidth=0,anchor="center",fgColour=frameColour,cornerRadius=0,txtColour=textColour,wraplength=0,width=0,autoWidth=True):
        if autoWidth == True:      
            width = len(text)*(fontSize/2)
            if width > 500:
                width = 500
            if anchor != "center":
                width += fontSize*2.5
                
        super().__init__(master=master,##
                        width=width,#
                        height=height,##
                        fg_color=fgColour,
                        corner_radius=cornerRadius,
                        text=text,##
                        text_color=txtColour,
                        text_font=(mainFont, fontSize),
                        wraplength=wraplength)#0
        if anchor == "e":
            self.text_label.place(relx=1,rely=0.5,anchor=anchor)
        elif anchor == "w":
            self.text_label.place(relx=0,rely=0.5,anchor=anchor)

        if bgColour != "":
            self.configure(bg_color=bgColour)
            
            
#checkbox
class CustomCheckbox(customtkinter.CTkCheckBox):
    def __init__(self,master,text):
        super().__init__(master=master,##
                         width=20,
                         height=20,
                         corner_radius=7,
                         border_width=2,
                         fg_color = hoverColour,
                         border_color = textColour,
                         hover_color = hoverColour,
                         text_color = textColour,
                         text = text,##
                         text_font = (mainFont,16),
                         onvalue=1,
                         offvalue=0)

class CustomToggleButton(tkinter.Label):
    def __init__(self,master,width,height,image1,image2,image3,bgColour=frameColour,command=None):
        self.unclickedImage = image1##
        self.clickedImage = image2##
        self.hoverImage = image3##
        self.command = command
    
        super().__init__(master,##
                         width=width,##
                         height=height,##
                         text="",
                         bg = bgColour,
                         fg = frameColour,
                         image = self.unclickedImage) 
        
        self.toggleState = 1

        self.bind("<Button-1>", self.clickFunction)
        self.bind("<Button-1>", command, add="+")
        
        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)

    def clickFunction(self,event=None):
        """
        Configures image when clicked to the opposite of its current image
        """
        self.toggleState *= -1
        if self.toggleState == -1:
            self.config(image = self.clickedImage)
        else:
            self.config(image = self.unclickedImage)
        
    def enter(self, event):
        """
        Configures to hover image when mouse is over it
        """
        self.config(image = self.hoverImage)

    def leave(self, event):
        """
        Configures to the image it was previously when mouse exits it
        """
        if self.toggleState == -1:
            self.config(image = self.clickedImage)
        else:
            self.config(image = self.unclickedImage)
     
    def refresh(self,event=None):
        """
        Refreshes the buttons command
        """
        self.bind("<Button-1>", self.clickFunction)
        self.bind("<Button-1>", self.command, add="+")

class CustomHoverButton(tkinter.Label):
    def __init__(self,master,width,height,image1,image2,bgColour=frameColour,command=None):
        self.normalImage = image1##
        self.hoverImage = image2##
        self.command = command
    
        super().__init__(master,##
                         width=width,##
                         height=height,##
                         text="",
                         bg = bgColour,
                         fg = frameColour,
                         image = self.normalImage) 

        self.bind("<Button-1>", command)
        
        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)
        
    def enter(self, event):
        """
        Configures to hover image when mouse is over it
        """
        self.config(image = self.hoverImage)

    def leave(self, event):
        """
        Configures to normal image when mouse exits it
        """
        self.config(image = self.normalImage)


class customRatingSystem(customtkinter.CTkFrame):
    def __init__(self,master,image1,image2,image3,fgColour=frameColour,command=None):
        global button1,button2,button3,button4,button5
        self.normalImage = image1##
        self.hoverImage = image2##
        self.fullImage = image3##
        self.command = command
    
        super().__init__(master,##
                         width=180,
                         height=40,
                         fg_color=fgColour)#

        
        self.button1=customtkinter.CTkButton(master=self,
                                      width=34,
                                      height=40,
                                      image=self.normalImage,
                                      fg_color=fgColour,
                                      corner_radius=0,
                                      border_width=0,
                                      hover=False,
                                      command=partial(self.clickFunction,num=1))
        self.button1.place(x=0,y=0)
        self.button2=customtkinter.CTkButton(master=self,
                                      width=34,
                                      height=40,
                                      image=self.normalImage,
                                      fg_color=fgColour,
                                      corner_radius=0,
                                      border_width=0,
                                      hover=False,
                                      command=partial(self.clickFunction,num=2))
        self.button2.place(x=36,y=0)
        self.button3=customtkinter.CTkButton(master=self,
                                      width=34,
                                      height=40,
                                      image=self.normalImage,
                                      fg_color=fgColour,
                                      corner_radius=0,
                                      border_width=0,
                                      hover=False,
                                      command=partial(self.clickFunction,num=3))
        self.button3.place(x=72,y=0)
        self.button4=customtkinter.CTkButton(master=self,
                                      width=34,
                                      height=40,
                                      image=self.normalImage,
                                      fg_color=fgColour,
                                      corner_radius=0,
                                      border_width=0,
                                      hover=False,
                                      command=partial(self.clickFunction,num=4))
        self.button4.place(x=108,y=0)
        self.button5=customtkinter.CTkButton(master=self,
                                      width=34,
                                      height=40,
                                      image=self.normalImage,
                                      fg_color=fgColour,
                                      corner_radius=0,
                                      border_width=0,
                                      hover=False,
                                      command=partial(self.clickFunction,num=5))
        self.button5.place(x=144,y=0)

        
        self.button1.bind('<Enter>', partial(self.enter,num=1))
        self.button1.bind('<Leave>', partial(self.leave,num=1))

        self.button2.bind('<Enter>', partial(self.enter,num=2))
        self.button2.bind('<Leave>', partial(self.leave,num=2))

        self.button3.bind('<Enter>', partial(self.enter,num=3))
        self.button3.bind('<Leave>', partial(self.leave,num=3))

        self.button4.bind('<Enter>', partial(self.enter,num=4))
        self.button4.bind('<Leave>', partial(self.leave,num=4))

        self.button5.bind('<Enter>', partial(self.enter,num=5))
        self.button5.bind('<Leave>', partial(self.leave,num=5))

        self.toggleState = -1
        self.lastNum=0
        self.rating=0
        self.game=-1
        self.command=None
        
    def enter(self,event,num):
        """
        Parameters: num - number that is being hovered over
        Configures stars below num to the hover image and starts above num to normal image when widget is hovered over
        """
        if num > 0:
            self.button1.configure(image = self.hoverImage)
        if num > 1:
            self.button2.configure(image = self.hoverImage)
        if num > 2:
            self.button3.configure(image = self.hoverImage)
        if num > 3:
            self.button4.configure(image = self.hoverImage)
        if num > 4:
            self.button5.configure(image = self.hoverImage)

        if num < 2:
            self.button2.configure(image = self.normalImage)
        if num < 3:
            self.button3.configure(image = self.normalImage)
        if num < 4:
            self.button4.configure(image = self.normalImage)
        if num < 5:
            self.button5.configure(image = self.normalImage)

    
    def leave(self,event,num):
        """
        Parameters: num - number that was being hovered over
        Configures stars to their previous images when exiting widget
        """
        if self.toggleState == -1:
            if num > 0 and self.rating < 1:
                self.button1.configure(image = self.normalImage)
            if num > 1 and self.rating < 2:
                self.button2.configure(image = self.normalImage)
            if num > 2 and self.rating < 3:
                self.button3.configure(image = self.normalImage)
            if num > 3 and self.rating < 4:
                self.button4.configure(image = self.normalImage)
            if num > 4 and self.rating < 5:
                self.button5.configure(image = self.normalImage)
        else:
            if self.rating < 1:
                self.button1.configure(image = self.normalImage)
            else:
                self.button1.configure(image = self.fullImage)

            if self.rating < 2:
                self.button2.configure(image = self.normalImage)
            else:
                self.button2.configure(image = self.fullImage)

            if self.rating < 3:
                self.button3.configure(image = self.normalImage)
            else:
                self.button3.configure(image = self.fullImage)

            if self.rating < 4:
                self.button4.configure(image = self.normalImage)
            else:
                self.button4.configure(image = self.fullImage)

            if self.rating < 5:
                self.button5.configure(image = self.normalImage)
            else:
                self.button5.configure(image = self.fullImage)
        

    def clickFunction(self,event=None,num=5,setUp=False):
        """
        Parameters: num - number star that was clicked. Default is 5
                    setUp - If True images are changed but no command is called
        Changes the images to match with the number clicked updates self.rating and then calls command of widget
        """
        if self.lastNum == num or self.toggleState==-1:
            self.toggleState *= -1
        if self.toggleState == 1 or self.lastNum != num:
            self.rating=num
            
            if self.lastNum > num:
                self.button1.configure(image=self.normalImage)
                self.button2.configure(image=self.normalImage)
                self.button3.configure(image=self.normalImage)
                self.button4.configure(image=self.normalImage)
                self.button5.configure(image=self.normalImage)
                                  
            if num > 0:
                self.button1.configure(image = self.fullImage)
            if num > 1:
                self.button2.configure(image = self.fullImage)
            if num > 2:
                self.button3.configure(image = self.fullImage)
            if num > 3:
                self.button4.configure(image = self.fullImage)
            if num > 4:
                self.button5.configure(image = self.fullImage)
            
        if self.toggleState == -1 and self.lastNum == num :
            self.rating=0
            if self.lastNum <= num:
                if num > 0:
                    self.button1.configure(image = self.normalImage)
                if num > 1:
                    self.button2.configure(image = self.normalImage)
                if num > 2:
                    self.button3.configure(image = self.normalImage)
                if num > 3:
                    self.button4.configure(image = self.normalImage)
                if num > 4:
                    self.button5.configure(image = self.normalImage)
            if self.lastNum > num:
                self.button1.configure(image=self.normalImage)
                self.button2.configure(image=self.normalImage)
                self.button3.configure(image=self.normalImage)
                self.button4.configure(image=self.normalImage)
                self.button5.configure(image=self.normalImage)
        self.lastNum = num
        if setUp == False:
            self.command()


class errorMessage(tkinter.Toplevel):
    def __init__(self,master,title,message,command=None,button="Close",extraCommand=None,extraButton=None):

        height= 360+message.count("\n")*18
    
        super().__init__(master,
                         bg=frameColour)
        self.title=("Error")
        self.resizable(False, False)
        self.geometry(f"530x{height}")

        center(self)

        self.frameMain = CustomFrame(master=self,
                                width=500,
                                height=height-30,
                                cornerRadius=0,
                                fgColour=bgColour)
        self.frameMain.place(x=15,y=15)
        self.frameTitle = CustomFrame(master=self.frameMain,
                                   width=460,
                                   height=50,
                                   fgColour=frameColour)
        self.frameTitle.place(x=20,y=20)
        self.frameText = CustomFrame(master=self.frameMain,
                                  width=460,
                                  height=height-140,
                                  fgColour=frameColour)
        self.frameText.place(x=20,y=90)

        self.labelTitle = CustomLabel(master=self.frameTitle,
                                      height=30,
                                   fgColour=frameColour,
                                   text="An Error Occurred",
                                   fontSize=20)
        self.labelTitle.place(x=15,y=5)

        self.labelSubtitle = tkinter.Label(master=self.frameText,
                                   fg=textColour,
                                   bg=frameColour,
                                   text=title,
                                   font=(mainFont,18))
        self.labelSubtitle.place(relx=0.5,y=30,anchor="center")

        self.labelInfo = tkinter.Label(master=self.frameText,
                                   fg=textColour,
                                   bg=frameColour,
                                   text=message,
                                   font=(mainFont,16),
                                   anchor="w",
                                   justify=tkinter.LEFT)
        self.labelInfo.place(x=15,y=60)
        
        self.buttonClose = CustomButtonDark(master=self.frameText,
                                     width=50,
                                     height=20,
                                     text=button,
                                     fgColour=bgColour,
                                     borderWidth=2,
                                     cornerRadius=10,
                                     bgColour=frameColour,
                                     fontSize=16,
                                    command=command)
        if button == "Close":
            self.buttonClose.place(x=375,y=height-190)
        if button == "Continue":
            self.buttonClose.place(x=350,y=height-190)

        if extraButton != None:
            self.extraButton = CustomButtonDark(master=self.frameText,
                                     width=50,
                                     height=20,
                                     text=extraButton,
                                     fgColour=warningColour,
                                     hovColour="#2A2B2A",
                                     borderWidth=2,
                                     cornerRadius=10,
                                     bgColour=frameColour,
                                     fontSize=16,
                                    command=extraCommand)
            self.extraButton.place(x=15,y=height-190)

        #while self.winfo_exists() == True:
            #raise SystemExit

