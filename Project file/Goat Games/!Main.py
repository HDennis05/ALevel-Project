"""
When testing = False the system will operate as normal
When testing = True the system will reduce validation to only what is completely necessary
    it will also auto fill login and password fields to aid testing.
"""
testing = True #change to True to enter testing mode
if testing == True:
    testEmail="testing@gmail.com" #Change accounts that will auto fill here
    testPassword="Testing!23"
    
    staffTestEmail="aaccount0001" #This is the admin account to change levels change to 'laccount0003' for lower or 'uaccount0002' for upper.
    staffTestPassword="Password!23"
    

#Define colours and font
frameColour = "#2A2B2A"
textColour = "#CCFCCB"
hoverColour = "#86AC94"
bgColour = "#495051"
entryColour = "#ECFEEC"
warningColour = "#B02F07"
mainFont = "Bahnschrift SemiCondensed"

#Import built in libraries
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import os
import time
import random
from datetime import datetime
import io
import sqlite3
from functools import partial
import sys, traceback
import shutil


def center(win):
    """
    Parameters: win - window to be centered
    Centers window to the middle of the users screen
    """
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = win.winfo_screenwidth() // 2 - width // 2
    y = win.winfo_screenheight() // 2 - height // 2
    win.geometry(f"{width}x{height}+{x}+{y}")
    win.deiconify()

def close():
    """
    Closes any top levels and main window
    """
    for widget in window.winfo_children():
        if isinstance(widget,tkinter.Toplevel):
            widget.destroy()
    window.destroy()
    exit()


setup = False
count = 0
while setup == False:
    try:
        #Try to import libraries from installed modules
        import customtkinter
        from tktooltip import ToolTip
        from PIL import ImageTk, Image, ImageDraw, ImageFont
        import matplotlib.pyplot as plt
        setup = True
    except:
        #Runs a batch file to import the necessary modules. Attempts this 3 times 
        os.system("importModules.BAT")
        count += 1
        if count > 2:
            #Displays error message
            window = tkinter.Tk()
            window.geometry("600x480")
            window.title("Goat Games")
            window.resizable(False, False)
            window.configure(bg="#2a2b2a")
            try:
                window.iconbitmap("Media/Icons/GIcon.ico")
            except:
                pass

            def close():
                window.destroy()
                
            center(window)

            frameMain = tkinter.Frame(master=window,
                                    width=530,
                                    height=410,
                                    bg=bgColour)
            frameMain.place(x=35,y=35)
            frameTitle = tkinter.Frame(master=frameMain,
                                       width=490,
                                       height=50,
                                       bg=frameColour)
            frameTitle.place(x=20,y=20)
            frameText = tkinter.Frame(master=frameMain,
                                      width=490,
                                      height=290,
                                      bg=frameColour)
            frameText.place(x=20,y=100)

            labelTitle = tkinter.Label(master=frameTitle,
                                       fg=textColour,
                                       bg=frameColour,
                                       text="An Error Occurred",
                                       font=(mainFont,20))
            labelTitle.place(x=15,y=5)

            labelSubtitle = tkinter.Label(master=frameText,
                                       fg=textColour,
                                       bg=frameColour,
                                       text="Could not import necessary modules",
                                       font=(mainFont,18))
            labelSubtitle.place(relx=0.5,y=30,anchor="center")
            labelInfo = tkinter.Label(master=frameText,
                                       fg=textColour,
                                       bg=frameColour,
                                       text="Please ensure the following:\n>Pip package manager is installed\n>Your Pip version corresponds to your Python version\n>Pip is saved in the correct directory\n>Your system permissions allow importing",
                                       font=(mainFont,16),
                                       anchor="w",
                                      justify=tkinter.LEFT)
            labelInfo.place(x=15,y=70)
            labelREADME = tkinter.Label(master=frameText,
                                        fg=textColour,
                                        bg=frameColour,
                                        text="For more help refer to the README",
                                        font=(mainFont,14),
                                        anchor="w")
            labelREADME.place(x=15,y=250)

            button_border = tkinter.Frame(frameText, highlightbackground = textColour, 
                                     highlightthickness = 2, bd=0)
            button_border.place(x=380,y=225)
            buttonClose = tkinter.Button(master=button_border,
                                         width=8,
                                         height=1,
                                         text="Close",
                                         fg=textColour,
                                         
                                         bg=warningColour,
                                         activebackground="#EC805F",
                                         font=(mainFont,16),
                                         command=close)
            buttonClose.pack()
                                         

            while window.winfo_exists() == True:
                raise SystemExit


#Create Window
window = tkinter.Tk()
window.geometry("1000x740")
window.title("Goat Games")
window.resizable(False, False)
window.configure(bg="#495051")

center(window)

try:
    #Import user defiend libraries
    from classes import *
    from SQLfunctions import *
    from analyticgraph import *
    from sendreceipts import *
    from imagemanipulation import *
    import sort
    import validation
    import encryption
except:
    #if not found display error message
    window.withdraw()
    pauseVar = tkinter.StringVar()
    try:
        topError = errorMessage(window,"Modules not Found",
                                "Possible reasons include:\n> Modules have been deleted\n> Modules have been moved\n\n\
Modules should be placed in the same folder as the\nMain file",
                                command=close)
    except:
        print("file 'classes.py' not found")
        
    window.wait_variable(pauseVar)   


conn = sqlite3.connect("GoatGamesDB.db")#Connect to database
cur = conn.cursor()

#Check necessary tables exist
tables=["basket","customer","game","gameOrder","gameTransaction","ratings","staff","wishlist"]
tableExists=True
for n in range(0,7):
    try:
        searchTable("*",tables[n],"")
    except sqlite3.OperationalError:
        tableExists=False

def create():
    """
    Creates new table and starts program
    """
    createTable()
    pauseVar.set(2)
    window.deiconify()
    return
        
if tableExists==False:
    #Display error message asking if the user would like to create a new database
    window.withdraw()
    pauseVar = tkinter.StringVar()
    topError = errorMessage(window,"Database not Found",
                            "Database was not found, possible reasons include:\n> Database has been deleted\n> Database has been moved\n\
Old backups can be found in the 'Backups' Folder\n\nContinuing will create a NEW database\nThis will ONLY contain an Admin Account.",
                            command=close,extraButton="Continue and Create",extraCommand=create)
    window.wait_variable(pauseVar)    


todaysDate = datetime.today()
datestr = todaysDate.strftime("%d-%m-%Y")

#If a backup for todays doesn't exist, create one        
exists = os.path.exists(f'Backups/GoatGamesDB-Backup-{datestr}.db')
if exists == False:
    shutil.copy('GoatGamesDB.db', "Backups/")
    shutil.move('Backups/GoatGamesDB.db', f'Backups/GoatGamesDB-Backup-{datestr}.db')


try:
    window.iconbitmap("Media/Icons/GIcon.ico")
except:
    pass


def openImage(folder,imageName,w=None,h=None,message="Image Not\n    Found"):
    """
    Parameters: folder - Folder that the desired image is located in
                imageName - name of image to open
                w - width of image. Default is None
                h - height of image. Default is None
    Attempts to open the image and if the file is not found creates a placeholder image
    Returns correct or placeholder image
    """
    try:
        if w==None and h==None:
            image = ImageTk.PhotoImage(Image.open(f"Media/{folder}/{imageName}.png"),master=window)
        else:
            image = ImageTk.PhotoImage(Image.open(f"Media/{folder}/{imageName}.png"),size=(w,h),master=window)
    except :
        img = Image.new("RGBA",(w%2304, h%1408),(0,0,0,0))
        
        fontSize=16
        pos = ((w/2-35),(h/2-25))
        if w < 140:
            fontSize=8
            pos = ((w/2-17),(h/2-15))
        if w < 40:
            fontSize=16
            pos = ((w*2),(h*2))
            
        fnt = ImageFont.truetype("Font/Saira.ttf", fontSize)
        draw = ImageDraw.Draw(img)
        if w > 130:
            draw.text(pos,message, font=fnt, fill=(204,252,203))
            draw.rounded_rectangle([(7,7),(w-7,h-7)],radius=20,outline=(204,252,203),width=3)
            draw.rounded_rectangle([(14,14),(w-14,h-14)],radius=13,outline=(204,252,203),width=1)
        else:
            draw.rounded_rectangle([(7,7),(w-7,h-7)],radius=2,outline=(204,252,203),width=1)
            if w > 40:
                draw.text(pos, message, font=fnt, fill=(204,252,203))

        image = ImageTk.PhotoImage(image=img)
    return image

#Open all icon images 
logoLong1 = openImage("Icons","LogoLong1",178,88)
logoLong2 = openImage("Icons","LogoLong2",120,70)
logoBig = openImage("Icons","logoBig",370,340)
logoSmall = openImage("Icons","logoSmall",250,210)
bigGoat = openImage("Icons","bigGoat",250,210)

profileIcon = openImage("Icons","profileIcon",65,65)
profileHover = openImage("Icons","profileHover",65,65)
searchIcon = openImage("Icons","searchIcon",20,20)
homeIcon = openImage("Icons","homeIcon",65,65)
homeHover = openImage("Icons","homeHover",65,65)
basketIcon = openImage("Icons","basketIcon",65,65)
basketHover = openImage("Icons","basketHover",65,65)
wishlistIcon = openImage("Icons","wishlistIcon",65,65)
wishlistHover = openImage("Icons","wishlistHover",65,65)
plusIcon = openImage("Icons","plusIcon",36,36)
plusHover = openImage("Icons","plusHover",36,36)

backIcon = openImage("Icons","backIcon",55,50)
backHover = openImage("Icons","backHover",55,50)

hollowHeart = openImage("Icons","hollowHeart",40,35)
hoverHeart = openImage("Icons","hoverHeart",40,35)
fullHeart = openImage("Icons","fullHeart",40,35)

hollowStar = openImage("Icons","hollowStar",34,35)
hoverStar = openImage("Icons","hoverStar",34,35)
fullStar = openImage("Icons","fullStar",34,35)

XIcon = openImage("Icons","XIcon",30,30)
XHover = openImage("Icons","XHover",30,30)
XIconMini = openImage("Icons","XIconMini",15,15)
XHoverMini = openImage("Icons","XHoverMini",15,15)

lockedIcon = openImage("Icons","lockedIcon",60,80)

downloadIcon = openImage("Icons","downloadIcon",40,39)
downloadHover = openImage("Icons","downloadHover",40,39)

       

def Analytics(frameMain,frameSide,analyticType):
    """
    Parameters: frameMain - main frame of staff area
                frameSide - side frame of staff area holding the traversal buttons
                analyticType - the version of analytics the user wants to view, eg. "Customers" or "Staff"
    Displays a Graph depending on the version chosen
    Displays all items in the chosen category
    These items can be sorted and searched.
    Allows staff to download a summary report on the chosen version of analytics.
    """
    global analyticGraph
    def downloadPopup(event=None):
        """
        Creates a toplevel screen to inform the user that the download is happening,
        automatically moves onto a confirmation message once summary report is downloaded.
        User can close the window once download has taken place
        """
        def download():
            #downloads report
            downloadReport(analyticType[:-1])

            labelTitle.configure(text="Done!",width=20)

            for widget in frameInput.winfo_children():
                widget.configure(text=f"{analyticType[:-1]} Analytics Summary in\nyour Downloads folder")
                widget.place(relx=0.5,rely=0.45,anchor="center")
                
            buttonClose = CustomButtonDark(master=frameInput,
                                           height=20,
                                           width=50,
                                           text="Close",
                                           borderWidth=2,
                                           bgColour=frameColour,
                                           command=partial(cancel))
            buttonClose.place(x=380,y=115)
            
        def cancel():
            """
            Closes popup 
            """
            popup.destroy()

        popup = tkinter.Toplevel(window)   
        popup.geometry("600x370")
        popup.title("Download")
        popup.resizable(False, False)
        popup.configure(bg=frameColour)

        center(popup)

        framePopup = CustomFrame(master=popup,
                                 width=530,
                                 height=300,
                                 fgColour=bgColour,
                                 cornerRadius=0)
        framePopup.place(x=35, y=35)

        frameTitle = CustomFrame(master=framePopup,
                                width=490,
                                height=70)
        frameTitle.place(x=20, y=20)

        labelLogoSmall = customtkinter.CTkLabel(master=frameTitle,
                                                width=120,
                                                height=70,
                                                image=logoLong2)
        labelLogoSmall.place(x=355, y=0)

        labelTitle = CustomSubtitle(master=frameTitle,
                                    text="Downloading...")
        labelTitle.place(x=20, y=10)

        frameInput = CustomFrame(master=framePopup,
                                width=490,
                                height=170)
        frameInput.place(x=20, y=110)
        
        labelSubtitle = CustomLabel(master=frameInput,
                                        height=60,
                                        autoWidth=False,
                                        width=490,
                                       text="Downloading...\nPlease Wait",
                                       fontSize=20)
        labelSubtitle.place(relx=0.5,rely=0.5,anchor="center")

        #Loads next function and will stay on screen until fucntion is complete
        popup.after(1000,download)
        
    def fillAnalyticFrames(displayList,firstItem,lastItem):
        """
        Parameters: displayList - List of items to be displayed
                    firstItem - index of the first item from the display list to be displayed
                    lastItem - index of the last item from the display list to be displayed
        Fills analytics frames with the appropriate results displaying information about their analytics and their rank number
        """
        #clear frames
        for n in range(0,len(frames)):
            for widget in frames[n].winfo_children():
                widget.destroy()

        #get analytics information
        if analyticType == "Games":
            titles=[]
            amounts=[]
            revenues=[]
            wishlists=[]
            baskets=[]
            ratings=[]
            for n in range(firstItem,lastItem):
                currentRecord = searchTable("title,numberBought,price","game","WHERE gameID = "+str(displayList[n]))
                titles.append(currentRecord[0][0])
                amounts.append(currentRecord[0][1])
                getRevenue = currentRecord[0][2]*currentRecord[0][1]
                revenue = round(getRevenue,2)
                if revenue == 0.0 or revenue == 0.00:
                    revenues.append("£0.00")
                else:
                    if len(str(revenue).rsplit('.')[-1]) == 2:
                        revenues.append("£"+str(revenue))
                    else:
                        revenues.append("£"+str(revenue)+"0")

                getWishlists = searchTable("*","wishlist","WHERE gameID = "+str(displayList[n]))
                numWishlists = 0
                for m in range(0,len(getWishlists)):
                    numWishlists += 1
                wishlists.append(numWishlists)

                getBaskets = searchTable("*","basket","WHERE gameID = "+str(displayList[n]))
                numBaskets = 0
                for m in range(0,len(getBaskets)):
                    numBaskets += 1
                baskets.append(numBaskets)

                getRatings = searchTable("rating","ratings","WHERE gameID = "+str(displayList[n]))
                gameRating = 0
                count = 0
                for m in range(0,len(getRatings)):
                    gameRating += getRatings[m][0]
                    count += 1
                if count != 0:
                    actualRating = int(round(gameRating/count,0))
                    rating = actualRating*"★"+(5-actualRating)*"☆"
                else:
                    rating = "not rated" 
                    
                ratings.append(rating)
                
        if analyticType == "Genres":
            titles=[]
            amounts=[]
            revenues=[]
            favourites=[]
            for n in range(firstItem,lastItem):
                titles.append(displayList[n])
                
                getGames = searchTable("gameID","game","WHERE genre = '"+displayList[n]+"'")
                getRevenue = 0
                amount = 0
                for m in range(0,len(getGames)):
                    currentRecord = searchTable("numberBought,price","game","WHERE gameID = "+str(getGames[m][0]))
                    getRevenue += (currentRecord[0][0]*currentRecord[0][1])
                    amount += currentRecord[0][0]
                    
                amounts.append(amount)
                revenue = round(getRevenue,2)
                if revenue == 0.0 or revenue == 0.00:
                    revenues.append("£0.00")
                else:
                    if len(str(revenue).rsplit('.')[-1]) == 2:
                        revenues.append("£"+str(revenue))
                    else:
                        revenues.append("£"+str(revenue)+"0")

                getFavourites = searchTable("*","customer","WHERE favGenre = '"+displayList[n]+"'")
                numFavs = 0
                for m in range(0,len(getFavourites)):
                    numFavs += 1
                favourites.append(numFavs)

                

        if analyticType == "Developers":
            titles=[]
            amounts=[]
            revenues=[]
            wishlists=[]
            baskets=[]
            for n in range(firstItem,lastItem):
                title = displayList[n]
                titles.append(title)

                getGames = searchTable("gameID","game","WHERE dev = '"+title+"'")
                getRevenue = 0
                amount = 0
                numWishlists = 0
                numBaskets = 0
                for m in range(0,len(getGames)):
                    currentRecord = searchTable("numberBought,price","game","WHERE gameID = "+str(getGames[m][0]))
                    getRevenue += (currentRecord[0][0]*currentRecord[0][1])
                    amount += currentRecord[0][0]
                                       
                    getWishlists = searchTable("*","wishlist","WHERE gameID = "+str(getGames[m][0]))
                    for i in range(0,len(getWishlists)):
                        numWishlists += 1

                    getBaskets = searchTable("*","basket","WHERE gameID = "+str(getGames[m][0]))
                    for i in range(0,len(getBaskets)):
                        numBaskets += 1
                    
                amounts.append(amount)
                revenue = round(getRevenue,2)
                if revenue == 0.0 or revenue == 0.00:
                    revenues.append("£0.00")
                else:
                    if len(str(revenue).rsplit('.')[-1]) == 2:
                        revenues.append("£"+str(revenue))
                    else:
                        revenues.append("£"+str(revenue)+"0")

                wishlists.append(numWishlists)
                baskets.append(numBaskets)


        dif = lastItem-firstItem
        if dif !=0:
            #Get the rank number of current item by getting a list of all items in order and then finding its index in this list 
            #If searching the rank will be relative to the sort type
            for n in range(0,dif):
                sortType = sortVar.get()
                if sortType == "Number Sold":
                    if analyticType == "Games":
                        array = searchTable("gameID,numberBought","game","ORDER BY numberBought DESC")
                    
                    if analyticType == "Genres":
                        getGenres = searchTable("genre","game","")    
                        array=[]
                        for p in range(0,len(getGenres)):
                            if not any(getGenres[p][0] in i for i in array):
                                array.append([getGenres[p][0]])

                        for p in range(0,len(array)):
                            amount = 0
                            currentRecord = searchTable("numberBought","game","WHERE genre = '"+array[p][0]+"'")
                            for q in range(0,len(currentRecord)):
                                amount += currentRecord[q][0]   
                            array[p].append(amount)
                            
                        array.sort(key=lambda x:x[1],reverse=True)

                    if analyticType == "Developers":
                        getDevs = searchTable("dev","game","")    
                        array=[]
                        for p in range(0,len(getDevs)):
                            if not any(getDevs[p][0] in i for i in array):
                                array.append([getDevs[p][0]])

                        for p in range(0,len(array)):
                            amount = 0
                            currentRecord = searchTable("numberBought","game","WHERE dev = '"+array[p][0]+"'")
                            for q in range(0,len(currentRecord)):
                                amount += currentRecord[q][0]   
                            array[p].append(amount)
                            
                        array.sort(key=lambda x:x[1],reverse=True)
                    
                if sortType == "Revenue Made":
                    if analyticType == "Games":
                        getGames = searchTable("gameID,price,numberBought","game","")
                        array=[]
                        for p in range(0,len(getGames)):
                            array.append((getGames[p][0],(getGames[p][1]*getGames[p][2])))
                        
                    if analyticType == "Genres":
                        getGenres = searchTable("genre","game","")    
                        array=[]
                        for p in range(0,len(getGenres)):
                            if not any(getGenres[p][0] in i for i in array):
                                array.append([getGenres[p][0]])

                        for p in range(0,len(array)):
                            revenue = 0
                            currentRecord = searchTable("numberBought,price","game","WHERE genre = '"+array[p][0]+"'")
                            for q in range(0,len(currentRecord)):
                                revenue += currentRecord[q][0]*currentRecord[q][1]  
                            array[p].append(revenue)
                            
                    if analyticType == "Developers":
                        getDevs = searchTable("dev","game","")    
                        array=[]
                        for p in range(0,len(getDevs)):
                            if not any(getDevs[p][0] in i for i in array):
                                array.append([getDevs[p][0]])

                        for p in range(0,len(array)):
                            revenue = 0
                            currentRecord = searchTable("numberBought,price","game","WHERE dev = '"+array[p][0]+"'")
                            for q in range(0,len(currentRecord)):
                                revenue += currentRecord[q][0]*currentRecord[q][1]  
                            array[p].append(revenue)
                            
                    array.sort(key=lambda x:x[1],reverse=True)
                            
                if sortType == "Wishlists":
                    if analyticType == "Games":
                        getGames = searchTable("gameID,price,numberBought","game","")
                        array=[]
                        for p in range(0,len(getGames)):
                            getWishlists = searchTable("*","wishlist","WHERE gameID = "+str(getGames[p][0]))
                            numWishlists = 0
                            for q in range(0,len(getWishlists)):
                                numWishlists += 1
                            array.append((getGames[p][0],numWishlists))


                    if analyticType == "Developers":
                        getDevs = searchTable("dev","game","")    
                        array=[]
                        names=[]
                        for p in range(0,len(getDevs)):
                            if getDevs[p][0] not in names:
                                names.append(getDevs[p][0])
                                getGames = searchTable("gameID","game","WHERE dev = '"+getDevs[p][0]+"'")
                                numWishlists=0
                                for q in range(0,len(getGames)):                                       
                                    getWishlists = searchTable("*","wishlist","WHERE gameID = "+str(getGames[q][0]))
                                    for i in range(0,len(getWishlists)):
                                        numWishlists += 1
                                array.append([getDevs[p][0],numWishlists])

                        
                    array.sort(key=lambda x:x[1],reverse=True)

                if sortType == "Baskets":
                    if analyticType == "Games":
                        getGames = searchTable("gameID,price,numberBought","game","")
                        array=[]
                        for p in range(0,len(getGames)):
                            getBaskets = searchTable("*","basket","WHERE gameID = "+str(getGames[p][0]))
                            numBaskets = 0
                            for q in range(0,len(getBaskets)):
                                numBaskets += 1
                            array.append((getGames[p][0],numBaskets))

                    if analyticType == "Developers":
                        getDevs = searchTable("dev","game","")
                        array=[]
                        names=[]
                        for p in range(0,len(getDevs)):
                            if getDevs[p][0] not in names:
                                names.append(getDevs[p][0])
                                getGames = searchTable("gameID","game","WHERE dev = '"+getDevs[p][0]+"'")
                                numBaskets=0
                                for q in range(0,len(getGames)):                                       
                                    getBaskets = searchTable("*","basket","WHERE gameID = "+str(getGames[q][0]))
                                    for i in range(0,len(getBaskets)):
                                        numBaskets += 1
                                array.append([getDevs[p][0],numBaskets])

                    array.sort(key=lambda x:x[1],reverse=True)

                if sortType == "Favourites":
                    getGenres = searchTable("genre","game","")    
                    array=[]
                    for p in range(0,len(getGenres)):
                        if not any(getGenres[p][0] in i for i in array):
                            array.append([getGenres[p][0]])
                                
                    for p in range(0,len(array)):
                        getFavourites = searchTable("*","customer","WHERE favGenre = '"+array[p][0]+"'")
                        numFavourites = 0
                        for q in range(0,len(getFavourites)):
                            numFavourites += 1
                        array[p].append(numFavourites)
                        
                    array.sort(key=lambda x:x[1],reverse=True)
          
                for m in range(0,len(array)):
                    if array[m][0] == displayList[firstItem+n]:
                        number = m + 1

                


                #Display information
                labelNum = CustomLabel(master=frames[n],
                                       height=30,
                                       text=str(number),
                                       fontSize=34,
                                       autoWidth=False,
                                       width=30)
                labelNum.place(x=15,y=15)
                
                labelTitle = CustomLabel(master=frames[n],
                                         height=36,
                                         text=titles[n],
                                         fontSize=22,
                                         anchor="w")
                labelTitle.place(x=60,y=10)
                if analyticType == "Games":
                    window.update()
                    xcoord = ((len(titles[n])*11)+(11*2.5))+65
                    labelRating = CustomLabel(master=frames[n],
                                             height=36,
                                             autoWidth=False,
                                             width=120,
                                             txtColour="#FFD557",
                                             text=f"[{ratings[n]}]",
                                             fontSize=16,
                                             anchor="e")
                    labelRating.place(x=xcoord,y=10)    
                
                labelSold = CustomLabel(master=frames[n],
                                        height=30,
                                        text=str(amounts[n])+" Sold",
                                        fontSize=14,
                                        autoWidth=False,
                                        width=70,
                                       anchor="w")
                labelSold.place(x=60,y=50)

                
                labelLine1 = CustomLabel(master=frames[n],
                                        height=30,
                                        text="|",
                                        fontSize=16)
                labelLine1.place(x=131,y=50)
                
                labelRevenue = CustomLabel(master=frames[n],
                                        height=30,
                                        text=str(revenues[n])+" Revenue",
                                        fontSize=14,
                                        autoWidth=False,
                                        width=150)
                labelRevenue.place(x=140,y=50)

                
                labelLine2 = CustomLabel(master=frames[n],
                                        height=30,
                                        text="|",
                                        fontSize=16)
                labelLine2.place(x=291,y=50)

                if analyticType == "Games" or analyticType == "Developers":
                    labelWishlists = CustomLabel(master=frames[n],
                                            height=30,
                                            text="In "+str(wishlists[n])+" Wishlists",
                                            fontSize=14,
                                            autoWidth=False,
                                            width=130)
                    labelWishlists.place(x=300,y=50)

                    
                    labelLine3 = CustomLabel(master=frames[n],
                                            height=30,
                                            text="|",
                                            fontSize=16)
                    labelLine3.place(x=431,y=50)

                    labelBaskets = CustomLabel(master=frames[n],
                                            height=30,
                                            text="In "+str(baskets[n])+" Baskets",
                                            fontSize=14,
                                            autoWidth=False,
                                            width=110,
                                            anchor="e")
                    labelBaskets.place(x=440,y=50)
                    
                if analyticType == "Genres":
                    labelSold.configure(font=(mainFont,16), width=120)
                    labelLine1.configure(font=(mainFont,20))
                    labelRevenue.configure(font=(mainFont,16), width=210)
                    labelLine2.configure(font=(mainFont,20))
                    labelLine1.place(x=181,y=47)
                    labelRevenue.place(x=190,y=50)
                    labelLine2.place(x=391,y=47)
                    
                    labelFavourites = CustomLabel(master=frames[n],
                                            height=30,
                                            text=str(favourites[n])+" Favourites",
                                            fontSize=16,
                                            autoWidth=False,
                                            width=150,
                                            anchor="e")
                    labelFavourites.place(x=400,y=50)
        else:
            #if no matches found display message
            labelNone = CustomLabel(master=frame1,
                                         height=36,
                                         text="No Matches Found",
                                         fontSize=18,
                                         anchor="w")
            labelNone.place(relx=0.5,rely=0.5,anchor="center")
        
    def sortBy(choice):
        """
        Parameters: choice - chosen dropdown option
        Sorts the results in the chosen way and calls fillAnalyticFrames to display them
        """
        if choice == "Number Sold":
            if analyticType == "Games":
                array = searchTable("gameID,numberBought","game","ORDER BY numberBought DESC")
                
            if analyticType == "Genres":
                #gets number sold for each game in that genre and adds them up
                getGenres = searchTable("genre","game","")    
                array=[]
                for n in range(0,len(getGenres)):
                    if not any(getGenres[n][0] in i for i in array):
                        array.append([getGenres[n][0]])

                for n in range(0,len(array)):
                    amount = 0
                    currentRecord = searchTable("numberBought","game","WHERE genre = '"+array[n][0]+"'")
                    for m in range(0,len(currentRecord)):
                        amount += currentRecord[m][0]   
                    array[n].append(amount)

                #sorts array in descending order    
                array.sort(key=lambda x:x[1],reverse=True)

            if analyticType == "Developers":
                #gets number sold for each game by that developer and adds them up
                getDevs = searchTable("dev","game","")    
                array=[]
                for n in range(0,len(getDevs)):
                    if not any(getDevs[n][0] in i for i in array):
                        array.append([getDevs[n][0]])

                for n in range(0,len(array)):
                    amount = 0
                    currentRecord = searchTable("numberBought","game","WHERE dev = '"+array[n][0]+"'")
                    for m in range(0,len(currentRecord)):
                        amount += currentRecord[m][0]   
                    array[n].append(amount)

                #sorts array in descending order    
                array.sort(key=lambda x:x[1],reverse=True)
                
            
        if choice == "Revenue Made":
            if analyticType == "Games":
                #gets price and number bought of each game to work out its revenue
                getGames = searchTable("gameID,price,numberBought","game","")
                array=[]
                for n in range(0,len(getGames)):
                    array.append((getGames[n][0],(getGames[n][1]*getGames[n][2])))
                
            if analyticType == "Genres":
                #gets price and number bought of each game in the genre to work out its revenue
                getGenres = searchTable("genre","game","")    
                array=[]
                for n in range(0,len(getGenres)):
                    if not any(getGenres[n][0] in i for i in array):
                        array.append([getGenres[n][0]])

                for n in range(0,len(array)):
                    revenue = 0
                    currentRecord = searchTable("numberBought,price","game","WHERE genre = '"+array[n][0]+"'")
                    for m in range(0,len(currentRecord)):
                        revenue += currentRecord[m][0]*currentRecord[m][1]  
                    array[n].append(revenue)
                    
            if analyticType == "Developers":
                #gets price and number bought of each game by the developer to work out its revenue
                getDevs = searchTable("dev","game","")    
                array=[]
                for n in range(0,len(getDevs)):
                    if not any(getDevs[n][0] in i for i in array):
                        array.append([getDevs[n][0]])

                for n in range(0,len(array)):
                    revenue = 0
                    currentRecord = searchTable("numberBought,price","game","WHERE dev = '"+array[n][0]+"'")
                    for m in range(0,len(currentRecord)):
                        revenue += currentRecord[m][0]*currentRecord[m][1]  
                    array[n].append(revenue)

            #sorts array in descending order          
            array.sort(key=lambda x:x[1],reverse=True)
                
        if choice == "Wishlists":
            if analyticType == "Games":
                #Gets a list of all the wshlists game is in and the number is the length of the list
                getGames = searchTable("gameID","game","")
                array=[]
                for n in range(0,len(getGames)):
                    wishlists = searchTable("*","wishlist","WHERE gameID = "+str(getGames[n][0]))
                    numWishlists = 0
                    for m in range(0,len(wishlists)):
                        numWishlists += 1
                    array.append((getGames[n][0],numWishlists))

            if analyticType == "Developers":
                #Gets a list of all the wishlists games by the developer are in and the number is the lengths of the lists added up
                getDevs = searchTable("dev","game","")    
                array=[]
                names=[]
                for n in range(0,len(getDevs)):
                    if getDevs[n][0] not in names:
                        names.append(getDevs[n][0])
                        getGames = searchTable("gameID","game","WHERE dev = '"+getDevs[n][0]+"'")
                        numWishlists=0
                        for m in range(0,len(getGames)):                                       
                            getWishlists = searchTable("*","wishlist","WHERE gameID = "+str(getGames[m][0]))
                            for i in range(0,len(getWishlists)):
                                numWishlists += 1
                        array.append([getDevs[n][0],numWishlists])

            #sorts array in descending order    
            array.sort(key=lambda x:x[1],reverse=True)
                
        if choice == "Baskets":
            if analyticType == "Games":
                ##Gets a list of all the baskets game is in and the number is the length of the list
                getGames = searchTable("gameID","game","")
                array=[]
                for n in range(0,len(getGames)):
                    baskets = searchTable("*","basket","WHERE gameID = "+str(getGames[n][0]))
                    numBaskets = 0
                    for m in range(0,len(baskets)):
                        numBaskets += 1
                    array.append((getGames[n][0],numBaskets))
            
            if analyticType == "Developers":
                #Gets a list of all the baskets games by the developer are in and the number is the lengths of the lists added up
                getDevs = searchTable("dev","game","")
                array=[]
                names=[]
                for n in range(0,len(getDevs)):
                    if getDevs[n][0] not in names:
                        names.append(getDevs[n][0])
                        getGames = searchTable("gameID","game","WHERE dev = '"+getDevs[n][0]+"'")
                        numBaskets=0
                        for m in range(0,len(getGames)):                                       
                            getBaskets = searchTable("*","basket","WHERE gameID = "+str(getGames[m][0]))
                            for i in range(0,len(getBaskets)):
                                numBaskets += 1
                        array.append([getDevs[n][0],numBaskets])

            #sorts array in descending order    
            array.sort(key=lambda x:x[1],reverse=True)

        if choice == "Favourites":
            #gets a list of how many people have this genre as their favourite and the number is the length of the list
            getGenres = searchTable("genre","game","")    
            array=[]
            for n in range(0,len(getGenres)):
                if not any(getGenres[n][0] in i for i in array):
                    array.append([getGenres[n][0]])
                        
            for n in range(0,len(array)):
                favourites = searchTable("*","customer","WHERE favGenre = '"+array[n][0]+"'")
                numFavourites = 0
                for m in range(0,len(favourites)):
                    numFavourites += 1
                array[n].append(numFavourites)

            #sorts array in descending order    
            array.sort(key=lambda x:x[1],reverse=True)

            
        if searchBar.get() != "":
            #if user was searching when sorted, continue searching by results are now ordered in the chosen way
            search()
        else:
            displayList=[]
            for n in range(0,len(array)):
                displayList.append(array[n][0])
            nextPage(0,-3,0,displayList)
        
        
    def search(event=None):
        """
        Searches all items and finds matches
        These matches are then sorted by relevence
        fillAnalyticsFrame is then called to display the results
        """
        def backSearch():
            """
            Removes all labels and buttons from searching
            Returns the user to the normal viewing mode
            """
            searchBar.delete(0,'end')
            frame1.focus_set()
            buttonX.place_forget()
            try: labelNone.destroy()
            except: pass
            
            sortBy(sortVar.get())


        buttonX.place_forget()
        try: labelNone.destroy()
        except: pass
            
        searchTerm=(searchBar.get()).lower()
        searchResults=[]

        #if searchTerm is not present return to normal viewing mode
        if searchTerm == "" or searchTerm == " ":
            return
        
        if analyticType == "Games":
            getGames = searchTable("title,gameID","game","")
            IDs=[]
            array=[]
            for n in range(0,len(getGames)):
                array.append(getGames[n][0])
                IDs.append(getGames[n][1])
            
        if analyticType == "Genres":
            getGenres = searchTable("genre","game","")    
            array=[]
            for n in range(0,len(getGenres)):
                if not any(getGenres[n][0] in i for i in array):
                    array.append(getGenres[n][0])

        if analyticType == "Developers":
            getDevs = searchTable("dev","game","")
            array=[]
            for n in range(0,len(getDevs)):
                if getDevs[n][0] not in array:
                    array.append(getDevs[n][0])

        sortMatches = sort.searchSort(array,searchTerm)

        searchResults=[]
        for n in range(0, len(sortMatches)):
            for m in range(0,len(array)):
                if sortMatches[n] == array[m].lower():
                    if analyticType == "Games":
                        searchResults.append(IDs[m])
                    else:
                        searchResults.append(array[m])

        #place clear button  
        buttonX.place(x=540,y=317)
        buttonX.configure(command=backSearch)

        #display results
        nextPage(0,-3,0,searchResults)
        

    #Clear main frame
    for widget in frameMain.winfo_children():
        widget.destroy()

    #remove all extra frames of toplevels
    for count,widget in enumerate(window.winfo_children()):
        if count == 2:
            widget.destroy()
        if isinstance(widget,tkinter.Toplevel):
            widget.destroy()

    #reset all widgets in side frame                 
    for count,widget in enumerate(frameSide.winfo_children()):
        if count < 2:
            widget.configure(border_width=1)
            for button in widget.winfo_children():
                    button.configure(text_color = textColour,
                                        fg_color = frameColour,
                                        bg_color = frameColour)
        if count == 2:
            widget.place(x=25,y=320)
        if count == 3:
            widget.place_forget()
        if count == 4:
             widget.configure(fg_color=textColour,
                              text_color=frameColour)

    #configure button that was pressed and its frame to be highlighted
    for count,frame in enumerate(frameSide.winfo_children()):
       if count == 0:
            frame.configure(border_width=5)
            for button in frame.winfo_children():
                if button.text == analyticType:
                    button.configure(text_color = frameColour,
                                     fg_color = textColour,
                                     bg_color = textColour)

    #create pie or bar chart and open the image
    if analyticType == "Genres":
        imageName = ""
        #try:
        createPie("Genre")
        imageName ="genrePie"
        #except: pass
        analyticGraph = openImage("Analytics", imageName,500,280,"Analytics not found")
    else:
        imageName = ""
        try:
            createBar(analyticType)
            if analyticType == "Games":
                imageName = "gameBar"
            if analyticType == "Developers":
                imageName = "devBar"
        except: pass
        analyticGraph = openImage("Analytics",imageName,500,280,"Analytics not found")


    #Screen formatting
            
    labelGraph = customtkinter.CTkLabel(master=frameMain,
                                   height=250,
                                   width=595,
                                   image = analyticGraph)
    labelGraph.place(x=20,y=10)

    frameDownload = CustomFrame(master=frameMain,
                                width=55,
                                height=54,
                                cornerRadius=0,
                                borderWidth=2)
    frameDownload.place(x=580,y=0)
    buttonDownload = CustomHoverButton(master=frameMain,
                                       width=40,
                                       height=39,
                                       image1=downloadIcon,
                                       image2=downloadHover,
                                       command=downloadPopup)
    buttonDownload.place(x=585,y=5)

    line = ttk.Separator(frameMain, orient="horizontal")
    line.place(x=0, y=300, relwidth=1, relheight=0.00005)

    sortVar = customtkinter.StringVar(value="Number Sold")
    
    #changes what is sorted by depending on type of analytics
    if analyticType == "Genres":
        values = ["Number Sold","Revenue Made","Favourites"]
    else:
        values = ["Number Sold","Revenue Made","Wishlists","Baskets"]
        
    dropdownSortType = customtkinter.CTkOptionMenu(master=frameMain,
                                                   width=205,
                                                   height=40,
                                                   corner_radius=0,
                                                   fg_color=frameColour,
                                                   button_color=frameColour,
                                                   button_hover_color=hoverColour,
                                                   dropdown_color=bgColour,
                                                   dropdown_hover_color=hoverColour,
                                                   dropdown_text_color=textColour,
                                                   text_color=textColour,
                                                   text_font=(mainFont,20),
                                                   variable=sortVar,
                                                   dynamic_resizing=False,
                                                   command=sortBy,
                                                   values=values)
    dropdownSortType.place(x=25,y=310)                                              

    placeholderText = "Search "+analyticType
    searchBar = CustomEntry(master=frameMain,
                            width=180,
                            height=35,
                            cornerRadius=20,
                            borderWidth=1,
                            fontSize=14,
                            placeholderText=placeholderText)
    searchBar.place(x=390, y=315)
    buttonSearch = customtkinter.CTkButton(master=frameMain,
                                           width=40,
                                           height=40,
                                           text="",
                                           corner_radius=30,
                                           hover_color=hoverColour,
                                           fg_color=frameColour,
                                           image=searchIcon,
                                           command=search)
    buttonSearch.place(x=570, y=312)
    searchBar.bind("<Return>",search)

    buttonX = CustomButtonText(master=frameMain,
                           height=5,
                           width=1,
                           text="x",
                           fontSize=14,
                           txtColour=frameColour,
                           fgColour=entryColour,
                           cornerRadius=0)

    #create frames
    frame1 = CustomFrame(master=frameMain,
                         height=90,
                         width=585,
                         borderWidth=1)
    frame1.place(x=25,y=365)
    frame2 = CustomFrame(master=frameMain,
                         height=90,
                         width=585,
                         borderWidth=1)
    frame2.place(x=25,y=465)
    frame3 = CustomFrame(master=frameMain,
                         height=90,
                         width=585,
                         borderWidth=1)
    frame3.place(x=25,y=565)
    frames=[frame1,frame2,frame3]

    #get original displayList
    if analyticType == "Games":
        getGames = searchTable("gameID","game","ORDER BY numberBought DESC")
        displayList=[]
        for n in range(0,len(getGames)):
            displayList.append(getGames[n][0])
            
    if analyticType == "Genres":
        getGenres = searchTable("genre","game","")    
        array=[]
        for n in range(0,len(getGenres)):
            if not any(getGenres[n][0] in i for i in array):
                array.append([getGenres[n][0]])

        for n in range(0,len(array)):
            amount = 0
            currentRecord = searchTable("numberBought","game","WHERE genre = '"+array[n][0]+"'")
            for m in range(0,len(currentRecord)):
                amount += currentRecord[m][0]   
            array[n].append(amount)
            
        array.sort(key=lambda x:x[1],reverse=True)
        displayList=[]
        for n in range(0,len(array)):
            displayList.append(array[n][0])

    if analyticType == "Developers":
        getDevs = searchTable("dev","game","")    
        array=[]
        for n in range(0,len(getDevs)):
            if not any(getDevs[n][0] in i for i in array):
                array.append([getDevs[n][0]])

        for n in range(0,len(array)):
            amount = 0
            currentRecord = searchTable("numberBought","game","WHERE dev = '"+array[n][0]+"'")
            for m in range(0,len(currentRecord)):
                amount += currentRecord[m][0]   
            array[n].append(amount)
            
        array.sort(key=lambda x:x[1],reverse=True)
        displayList=[]
        for n in range(0,len(array)):
            displayList.append(array[n][0])

    #navigation
    def nextPage(pageNo,firstItem,lastItem,displayList):
        """
        Parameters: pageNo - page number
                    firstItem - first item that is displayed
                    lastItem - last item that is displayed
                    displayList - list of items to display
        Goes forwards one page
        """
        pageNo += 1

        numGames = len(displayList)
        numPages = numGames//3
        numExtra = numGames%3
        if numExtra != 0:
            numPages += 1
            
        firstItem += 3

        if numGames != 0:
            if pageNo == 1:
                #revert everything to normal
                buttonBack.configure(state="disabled")
                buttonNext.configure(state="normal")
                frame2.place(x=25,y=465)
                frame3.place(x=25,y=565)

            if pageNo != numPages:
                lastItem += 3
            else:
                if numExtra != 0:
                    lastItem += numExtra
                    for n in range(numExtra,3):#remove all unused frames
                        frames[n].place_forget()
                else:
                    lastItem += 3
                buttonNext.configure(state="disabled")
            if pageNo == 2:
                buttonBack.configure(state="normal")
                

            labelPageNo.configure(text="Page "+str(pageNo))
            buttonNext.configure(command=partial(nextPage,pageNo,firstItem,lastItem,displayList))
            buttonBack.configure(command=partial(backPage,pageNo,firstItem,lastItem,displayList))

            fillAnalyticFrames(displayList,firstItem,lastItem)

        else:
            for n in range(1,3):
                frames[n].place_forget()
            buttonBack.configure(state="disabled")
            buttonNext.configure(state="disabled")
            fillAnalyticFrames([],0,0)
            
    def backPage(pageNo,firstItem,lastItem,displayList):
        """
        Parameters: page - the current page number
                    firstItem - the index of the first item being displayed
                    lastItem - the index of the last item being displayed
                    displayList - list of items to display
        Moves backwards one page
        """
        pageNo -= 1

        numGames = len(displayList)
        numPages = numGames//3
        numExtra = numGames%3
        if numExtra != 0:
            numPages += 1

        firstItem -= 3
        if pageNo != numPages-1:
            lastItem -= 3
        else:
            if numExtra != 0:
                #revert frames back to normal
                lastItem -= numExtra
                frame2.place(x=25,y=465)
                frame3.place(x=25,y=565)
            else:
                lastItem -= 3
            buttonNext.configure(state="normal")
            
        if pageNo == 1:
            buttonBack.configure(state="disabled")

        labelPageNo.configure(text="Page "+str(pageNo))
        buttonNext.configure(command=partial(nextPage,pageNo,firstItem,lastItem,displayList))
        buttonBack.configure(command=partial(backPage,pageNo,firstItem,lastItem,displayList))

        fillAnalyticFrames(displayList,firstItem,lastItem)

    numGames = len(displayList)
    numPages = numGames//3
    numExtra = numGames%3
    if numExtra != 0:
        numPages += 1
    pageNo = 0
    firstItem = -3
    lastItem = 0

    if numPages > 1:
        labelPageNo = CustomLabel(master=frameMain,
                                    autoWidth=False,
                                    width=50,
                                    height=15,
                                    text="Page "+str(pageNo),
                                    fontSize=14)
        labelPageNo.place(x=290,y=665)
        buttonBack =  CustomButtonText(master=frameMain,
                                     width=20,
                                     height=15,
                                     text="<",
                                     state="disabled",
                                     cornerRadius=0,
                                     fontSize=14,
                                     hoverEnabled=False,
                                     command=partial(backPage,pageNo,firstItem,lastItem,displayList))
        buttonBack.place(x=265, y=664)
        buttonNext = CustomButtonText(master=frameMain,
                                     width=20,
                                     height=15,
                                     text=">",
                                     cornerRadius=0,
                                     fontSize=14,
                                     hoverEnabled=False,
                                     command=partial(nextPage,pageNo,firstItem,lastItem,displayList))
        buttonNext.place(x=345, y=664)

        nextPage(0,firstItem,lastItem,displayList)
        
def Profiles(view,frameMain,frameSide,profileType):
    """
    Parameters: view - staff members access levels
                frameMain - main frame of staff area
                frameSide - side frame of staff area holding the traversal buttons
                profileType - the version of profiles the user wants to view, eg. "Customers" or "Staff"
    Displays a Treeview of all the accounts of the chosen category
    Allows the staff member to select, search, edit or delete records
    Also allows staff to add a new record
    """
    def fixedMap(option):
        """
        fixes styling of treeview
        """
        return[elm for elm in s.map("Treeview", query_opt=option) if elm[:2] !=("!disabled","!selected")]

    def fillTree():
        """
        Fills the treeview widget with the correct records
        If not admin account, admin's account will be uneditable and some details will be obscured
        """
        if profileType == "Customers":
            profileInfo=searchTable("customerID,emailAddress,password,customerForename,customerSurname,customerDOB,favGenre",
                                     "customer","")

        if profileType == "Staff":
            profileInfo=searchTable("staffID,username,password,staffForename,staffSurname,jobTitle",
                                     "staff","")
   
        records=[]
        for n in range(0, len(profileInfo)):
            
            getID = str(profileInfo[n][0])
            ID = ((4-len(getID))*"0")+getID
            if ID == "0001" and profileType == "Staff" and view != "Admin":
                password = "\t-"
                username = "\t-"
            else:
                password = profileInfo[n][2]
                password=encryption.XOR(password)
            forename = profileInfo[n][3].capitalize()
            surname = profileInfo[n][4].capitalize()
                
            if profileType == "Customers":
                email = profileInfo[n][1]
                DOB = profileInfo[n][5]
                favGenre = profileInfo[n][6]
                records.append((ID, email, password, forename, surname, DOB, favGenre))
                
            if profileType == "Staff":
                if ID != "0001" or view == "Admin":
                    username = profileInfo[n][1]
                jobTitle = profileInfo[n][5]
                records.append((ID, username, password, forename, surname, jobTitle))

        for record in records:
            tree.insert('', tkinter.END, values=record)
        
                
    def search(event=None):
        """
        Searches records and sorts the results by most relevent
        """
        def searchRecord(ID):
            """
            Searches through fields and adds results to an array
            """
            if profileType == "Customers":
                 record = (searchTable("*","customer","WHERE customerID = "+str(ID)))
                 record = record[0]
                 numZeros = 4 - len(str(record[0]))
                 if str(searchTerm) in (numZeros*"0"+(str(record[0]))):
                     results.append((str(ID),"ID"))
                 if searchTerm in record[4]:
                     results.append((str(ID),"Email"))
                 if str(searchBar.get()) in encryption.XOR(record[5]):
                     results.append((str(ID),"Password"))
                 if searchTerm in record[1]:
                     results.append((str(ID),"Forename"))
                 if searchTerm in record[2]:
                     results.append((str(ID),"Surname"))
                 if str(searchTerm) in record[3]:
                     results.append((str(ID),"Date"))
                 if searchTerm in record[6].lower():
                     results.append((str(ID),"Fav"))
            if profileType == "Staff":
                 record = (searchTable("*","staff","WHERE staffID = "+str(ID)))
                 record = record[0]
                 numZeros = 4 - len(str(record[0]))
                 if str(searchTerm) in (numZeros*"0"+(str(record[0]))):
                     results.append((str(ID),"ID"))
                 if str(searchTerm) in record[3]:
                     results.append((str(ID),"Username"))
                 if searchTerm in record[1]:
                     results.append((str(ID),"Forename"))
                 if searchTerm in record[2]:
                     results.append((str(ID),"Surname"))
                 if str(searchTerm) in record[5].lower():
                     results.append((str(ID),"Job"))
                 if str(searchBar.get()) in record[4]:
                     results.append((str(ID),"Password"))
                     
        def backSearch():
            """
            Stops searching and returns staff to normal viewing mode
            """
            for count,widget in enumerate(frameSearch.winfo_children()):
                if count > 3:
                    widget.destroy()

            tree.configure(selectmode="browse")

            searchBar.delete(0,'end')
            buttonSave.focus_set()

            for item in tree.selection():
               tree.selection_remove(item)

            buttonDeselect.configure(command=deselect)
                
            for n in range(0,len(entries)):
                if n == 0:
                    if profileType == "Staff":
                        IDVar.set("")
                    if profileType == "Customers":
                        entries[n].configure(text="")
                    highlightID.configure(fg_color=frameColour)
                    entryID.configure(height=35,width=285)
                    entryID.place(x=0, y=0)
                    entryID.text_label.place(x=10,y=3)
                elif n == 1 and profileType == "Staff":
                    entries[n].configure(text="")
                    highlightUsername.configure(fg_color=frameColour)
                    entryUsername.configure(height=35,width=285)
                    entryUsername.place(x=0, y=0)
                    entryUsername.text_label.place(x=10,y=3)
                elif n == 6 and profileType == "Customers":
                    entries[n].set("-")
                    entries[n].configure(state="disabled")
                    highlightGenre.configure(fg_color=frameColour)
                    entryGenre.configure(height=35,width=285)
                    entryGenre.place(x=0, y=0)
                elif n == 4 and profileType == "Staff":
                    entries[n].set("-")
                    entries[n].configure(state="disabled")
                    highlightJobTitle.configure(fg_color=frameColour)
                    entryJobTitle.configure(height=35,width=285)
                    entryJobTitle.place(x=0, y=0) 
                else:
                    entries[n].delete(0,'end')
                    entries[n].configure(state="disabled",border_color = entryColour)

            buttonSave.configure(text="Save Changes",command=addCustomer)

            buttonSave.configure(state="disabled",border_color=hoverColour)
            buttonDelete.configure(state="disabled",border_color=hoverColour)
            buttonDeselect.configure(state="disabled",border_color=hoverColour)     

        def resultDisplay(page):
            """
            Displays the results one at a time highlighting the area the match is found
            """
            for count,entry in enumerate(entries):
                if count == 0:
                    highlightID.configure(fg_color=frameColour)
                    entryID.configure(height=35,width=285)
                    entryID.place(x=0, y=0)
                    entryID.text_label.place(x=10,y=3)
                elif count == 1 and profileType == "Staff":
                    highlightUsername.configure(fg_color=frameColour)
                    entryUsername.configure(height=35,width=285)
                    entryUsername.place(x=0, y=0)
                    entryUsername.text_label.place(x=10,y=3) 
                elif count == 6 and profileType == "Customers":
                    highlightGenre.configure(fg_color=frameColour)
                    entryGenre.configure(height=35,width=285)
                    entryGenre.place(x=0, y=0)
                elif count == 4 and profileType == "Staff":
                    highlightJobTitle.configure(fg_color=frameColour)
                    entryJobTitle.configure(height=35,width=285)
                    entryJobTitle.place(x=0, y=0)
                else:
                    entry.configure(border_color = entryColour)

            tree.configure(selectmode="none")
                    
            result=results[page-1]
            if profileType == "Customers":
                IDs = searchTable("customerID","customer","")
            if profileType == "Staff":
                IDs = searchTable("staffID","staff","")
            for n in range(0,len(IDs)):
                if IDs[n][0] == int(result[0]):
                    index=n
                    
            rowID = tree.get_children()[index]
            tree.focus(rowID)
            tree.selection_set(rowID)

            item_selected(search=True)

            if str(result[1])=="ID":
                highlightID.configure(fg_color=warningColour)
                entryID.configure(height=29,width=279)
                entryID.place(x=3, y=3)
                entryID.text_label.place(x=7,y=0)
            if str(result[1])=="Username":
                highlightUsername.configure(fg_color=warningColour)
                entryUsername.configure(height=29,width=279)
                entryUsername.place(x=3, y=3)
                entryUsername.text_label.place(x=7,y=0)
            if str(result[1])=="Email":
                entryEmail.configure(border_color = warningColour)
                entryEmail.focus_set()
            if str(result[1])=="Password":
                entryPassword.configure(border_color = warningColour)
                entryPassword.focus_set()
            if str(result[1])=="Forename":
                entryForename.configure(border_color = warningColour)
                entryForename.focus_set()
            if str(result[1])=="Surname":
                entrySurname.configure(border_color = warningColour)
                entrySurname.focus_set()
            if str(result[1])=="Date":
                entryDOB.configure(border_color = warningColour)
                entryDOB.focus_set()
            if str(result[1])=="Fav":
                highlightGenre.configure(fg_color=warningColour)
                entryGenre.configure(height=33,width=279)
                entryGenre.place(x=3, y=3)
            if str(result[1])=="Job":
                highlightJobTitle.configure(fg_color=warningColour)
                entryJobTitle.configure(height=33,width=279)
                entryJobTitle.place(x=3, y=3)

        def nextResult(page):
            """
            Parameters: page - current page number
            Moves to next result
            """
            page += 1
            labelNum.configure(text=f"{page} of {len(results)}"),
            if page == 10:
                buttonNext.place(x=325,y=10)
                labelNum.configure(width=60)
            if page == 2:
                buttonLast.configure(state="normal")
            if page == len(results): 
                buttonNext.configure(state="disabled")
            resultDisplay(page)

            buttonNext.configure(command=partial(nextResult,page))
            buttonLast.configure(command=partial(lastResult,page))
            
        def lastResult(page):
            """
            Parameters: page - current page number
            Moves to previous result
            """
            page -= 1
            labelNum.configure(text=f"{page} of {len(results)}")
            if page == 9:
                buttonNext.place(x=312,y=10)
                labelNum.configure(width=50)
            if page == 1:
                buttonLast.configure(state="disabled")
            if page == (len(results)-1):
                buttonNext.configure(state="normal")
            resultDisplay(page)

            buttonNext.configure(command=partial(nextResult,page))
            buttonLast.configure(command=partial(lastResult,page))
            
            
        searchTerm=(searchBar.get()).lower()

        results=[]
        for count,widget in enumerate(frameSearch.winfo_children()):
            if count > 3:
                widget.destroy()

            
        if searchTerm == "":
            return
        else:
            if profileType == "Customers":
                IDs = searchTable("customerID","customer","")
            if profileType == "Staff":
                IDs = searchTable("staffID","staff","")
            for n in range(0,len(IDs)):
                searchRecord(IDs[n][0])        

        for item in tree.selection():
           tree.selection_remove(item)

        buttonDeselect.configure(command=backSearch)

        buttonX = CustomButtonText(master=frameSearch,
                                   height=5,
                                   width=1,
                                   text="x",
                                   fontSize=14,
                                   txtColour=frameColour,
                                   fgColour=entryColour,
                                   cornerRadius=0,
                                   command=backSearch)
        buttonX.place(x=175,y=10)

        if len(results)==0:
            labelNone = CustomLabel(master=frameSearch,
                               height=20,
                               text="No Matches",
                               fontSize=14)
            labelNone.place(x=250,y=13)
            deselect()
                                       
        else:
            labelNum = CustomLabel(master=frameSearch,
                                   autoWidth=False,
                                   width=50,
                               height=20,
                               text=f"0 of {len(results)}",
                               fontSize=14,
                                   anchor="e")
            labelNum.place(x=260,y=13)
            if len(results) > 1:
                page=0
                buttonLast = CustomButtonText(master=frameSearch,
                                              width=10,
                                              height=1,
                                              text="<",
                                              state="disabled",
                                              cornerRadius=0,
                                              fontSize=14,
                                              command=partial(lastResult,page))
                buttonLast.place(x=245,y=10)
                buttonNext = CustomButtonText(master=frameSearch,
                                              width=10,
                                              height=1,
                                              text=">",
                                              state="normal",
                                              cornerRadius=0,
                                              fontSize=14,
                                              command=partial(nextResult,page))
                if len(results) < 10:
                    buttonNext.place(x=305,y=10)
                    labelNum.configure(width=43)
                else:
                    buttonNext.place(x=312,y=10)

                nextResult(page)
            else:
                page=1
                labelNum.configure(text=f"{page} of {len(results)}",
                                   width=40)
                labelNum.place(x=250,y=13)
                resultDisplay(page)
                

            if profileType == "Customers":
                num=16
                height=9
            if profileType == "Staff":
                num=14
                height=11

            #Moves all widgets back to where they should be if they had previously been pushed up by an error message
            message=False
            for count, widget in enumerate(frameMain.winfo_children()):
                if count >= num+3:
                    widget.destroy()
                    message=True
                    
            if message == True:
                for count,widget in enumerate(frameMain.winfo_children()):
                    if count == 0:
                        for subcount,subwidget in enumerate(widget.winfo_children()):
                            if subcount == 0:
                                subwidget.configure(height=height)
                    if count != 0 and count < num:
                        oldy = widget.winfo_y()
                        oldx = widget.winfo_x()
                        newy = oldy+55
                        widget.place(x=oldx,y=newy)

                
    def back(buttonBack):
        """
        Parameters: buttonBack - back button from add record
        When in add record
        Returns staff to normal viewing mode
        """
        buttonBack.destroy()
        if profileType == "Customers":
            labelAdd.place(x=388, y=8)
        if profileType == "Staff":
            labelAdd.place(x=343, y=8)
        buttonAdd.place(x=555,y=13)
        searchBar.place(x=20, y=10)
        buttonSearch.place(x=200, y=5)
        buttonDelete.place(x=220,y=645)
        buttonDeselect.place(x=455,y=645)

        searchBar.delete(0,'end')
        buttonSave.focus_set()

        tree.configure(selectmode="browse")

        for n in range(0,len(entries)):
            if n == 0 and profileType == "Customers":
                entries[n].configure(text="")
            elif (n == 0 or n == 1) and profileType == "Staff":
                IDVar.set("")
            if (n > 0 and profileType == "Customers") or (n > 1 and profileType == "Staff"):
                if (n < 6 and profileType == "Customers") or ((n < 4 or n > 4) and profileType == "Staff"):
                    entries[n].delete(0,'end')
                    entries[n].configure(state="disabled")
                else:
                    entries[n].set("-")
                    entries[n].configure(state="disabled")

        buttonSave.configure(text="Save Changes",command=saveChanges)

        buttonSave.configure(state="disabled",border_color=hoverColour)
        buttonDelete.configure(state="disabled",border_color=hoverColour)
        buttonDeselect.configure(state="disabled",border_color=hoverColour)

        if profileType == "Customers":
            num=16
            height=9
        if profileType == "Staff":
            num=14
            height=11
            
        message=False
        for count, widget in enumerate(frameMain.winfo_children()):
            if count >= num+3:
                widget.destroy()
                message=True
                
        if message == True:
            for count,widget in enumerate(frameMain.winfo_children()):
                if count == 0:
                    for subcount,subwidget in enumerate(widget.winfo_children()):
                        if subcount == 0:
                            subwidget.configure(height=height)
                if count != 0 and count < num:
                    oldy = widget.winfo_y()
                    oldx = widget.winfo_x()
                    newy = oldy+55
                    widget.place(x=oldx,y=newy)

        
    def addCustomer():
        """
        Validates user inputs
        If valid creates new record and wipe entry widgets
        If not valid calls messageBox to display error 
        """
        email = str(entries[1].get()).lower()
        validEmail = validation.emailCheck(email,extra="an")
        if validEmail != True:
            messageBox(validEmail)
            return

        getEmails = searchTable("emailAddress","customer","")
        emails = []
        for field in getEmails:
            emails.append(field[0])
                
        if email in emails:
            messageBox("Email address is taken")
            return

        password = entries[2].get()
        
        forename = (entries[3].get()).lower()
        surname = (entries[4].get()).lower()

        DOB = entries[5].get()

        favourite = genreVar.get()

        if testing == False:
            validPassword = validation.passwordCheck(password)
            if validPassword != True:
                messageBox(validPassword)
                return
            
            validForename = validation.nameCheck(forename,"forename",extra="a")
            if validForename != True:
                messageBox(validForename)
                return
            
            validSurname = validation.nameCheck(surname,"surname",extra="a")
            if validSurname != True:
                messageBox(validSurname)
                return
                
            validDOB = validation.dateCheck(DOB,extra="a")
            if validDOB != True:
                messageBox(validDOB)
                return
            
            if favourite == "-":
                messageBox("Please select a favourite genre")
                return
        else:
            if password == "":
                messageBox("Please enter a Password")

            
        password=encryption.XOR(password)

        insertCustomer(email=email,
                       password=password,
                       forename=forename,
                       surname=surname,
                       DOB=DOB,
                       favGenre=favourite)

        tree.delete(*tree.get_children())
        fillTree()
        newCustomer()
        
    def addStaff():
        """
        Validates user inputs
        If valid creates new record and wipe entry widgets
        If not valid calls messageBox to display error 
        """
        staffID=int(IDVar.get())
        username = (entries[1].text).lower()

        forename = (entries[2].get()).lower()
        surname = (entries[3].get()).lower()

        if testing == False:
            validForename = validation.nameCheck(forename,"forename",extra="a")
            if validForename != True:
                messageBox(validForename)
                return
            
            validSurname = validation.nameCheck(surname,"surname",extra="a")
            if validSurname != True:
                messageBox(validSurname)
                return
        
        jobTitle = jobVar.get()
        if jobTitle == "-":
            messageBox("Please enter a Job Title")
            return

        password = entries[5].get()

        if testing == False:
            validPassword = validation.passwordCheck(password)
            if validPassword != True:
                messageBox(validPassword)
                return
        else:
            if password == "":
                messageBox("Please enter a Password")
                return
            
        password=encryption.XOR(password)

        insertStaff(forename=forename,
                    surname=surname,
                    username=username,
                    jobTitle=jobTitle,
                    password=password)

        tree.delete(*tree.get_children())
        fillTree()
        newStaff()
        

    def newCustomer(event=None):
        """
        Activates all entry widgets to allow staff to create a customer record
        """
        for widget in frameSearch.winfo_children():
            widget.place_forget()

        buttonDelete.place_forget()
        buttonDeselect.place_forget()
        buttonSave.configure(text="Add Customer",
                             command=addCustomer,
                             border_color=textColour,
                             state="normal")

        tree.configure(selectmode="none")
        
        IDs = searchTable("customerID","customer","")
        if len(IDs) == 0:
            getNewID = "1"
        else:
            #get last ID and increment by 1
            getNewID = str((IDs[-1][0])+1)
        newID = ((4-len(getNewID))*"0")+getNewID
        for n in range(0,len(entries)):
            if n == 0:
                entries[n].configure(text=newID)            
                highlightID.configure(fg_color=frameColour)
                entryID.configure(height=35,width=285)
                entryID.place(x=0, y=0)
                entryID.text_label.place(x=10,y=3)
            else:
                if n < 6:
                    entries[n].delete(0,'end')
                    entries[n].configure(state="normal",border_color=entryColour)
                else:
                    entries[n].configure(state="normal")
                    entries[n].set("-")
                    highlightGenre.configure(fg_color=frameColour)
                    entryGenre.configure(height=35,width=285)
                    entryGenre.place(x=0, y=0)

        for item in tree.selection():
           tree.selection_remove(item)
           
        buttonBack = CustomButtonText(master=frameSearch,
                                      width=20,
                                      height=30,
                                      text="Back",
                                      cornerRadius=5)
        buttonBack.place(x=505,y=8)
        buttonBack.configure(command=partial(back,buttonBack))

        message=False
        for count, widget in enumerate(frameMain.winfo_children()):
            if count >= 19:
                widget.destroy()
                message=True
        if message == True:
            for count,widget in enumerate(frameMain.winfo_children()):
                if count == 0:
                    for subcount,subwidget in enumerate(widget.winfo_children()):
                        if subcount == 0:
                            subwidget.configure(height=9)
                if count != 0 and count < 16:
                    oldy = widget.winfo_y()
                    oldx = widget.winfo_x()
                    newy = oldy+55
                    widget.place(x=oldx,y=newy)
        
    def newStaff(event=None):
        """
        Activates all entry widgets to allow staff to create a staff record
        """
        for widget in frameSearch.winfo_children():
            widget.place_forget()

        buttonDelete.place_forget()
        buttonDeselect.place_forget()
        buttonSave.configure(text="Add Staff Member",
                             command=addStaff,
                             border_color=textColour,
                             state="normal")

        tree.configure(selectmode="none")

        IDs = searchTable("staffID","staff","")

        if len(IDs) == 0:
            getNewID = "1"
        else:
            #get last ID and increment by 1
            getNewID = str((IDs[-1][0])+1)
        newID = ((4-len(getNewID))*"0")+getNewID
        IDVar.set(newID)
        
        for n in range(0,len(entries)):
            if n == 0:          
                highlightID.configure(fg_color=frameColour)
                entryID.configure(height=35,width=285)
                entryID.place(x=0, y=0)
                entryID.text_label.place(x=10,y=3)
            elif n == 1:
                highlightUsername.configure(fg_color=frameColour)
                entryUsername.configure(height=35,width=285)
                entryUsername.place(x=0, y=0)
                entryUsername.text_label.place(x=10,y=3)
            elif n == 4:
                entries[n].configure(state="normal")
                entries[n].set("-")
                highlightJobTitle.configure(fg_color=frameColour)
                entryJobTitle.configure(height=35,width=285)
                entryJobTitle.place(x=0, y=0)
            else:
                entries[n].delete(0,'end')
                entries[n].configure(state="normal", border_color=entryColour)

        for item in tree.selection():
           tree.selection_remove(item)
           
        buttonBack = CustomButtonText(master=frameSearch,
                                      width=20,
                                      height=30,
                                      text="Back",
                                      cornerRadius=5)
        buttonBack.place(x=505,y=8)
        buttonBack.configure(command=partial(back,buttonBack))


        #returns widgets to their normal positions
        message=False
        for count, widget in enumerate(frameMain.winfo_children()):
            if count >= 17:
                widget.destroy()
                message=True
        if message == True:
            for count,widget in enumerate(frameMain.winfo_children()):
                if count == 0:
                    for subcount,subwidget in enumerate(widget.winfo_children()):
                        if subcount == 0:
                            subwidget.configure(height=11)
                if count != 0 and count < 14:
                    oldy = widget.winfo_y()
                    oldx = widget.winfo_x()
                    newy = oldy+55
                    widget.place(x=oldx,y=newy)
        
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """
        if profileType == "Customers":
            alreadyThere=False
            for count, widget in enumerate(frameMain.winfo_children()):
                if count >= 19:
                    widget.destroy()
                    alreadyThere=True

            num=16
            height=7
                    
        if profileType == "Staff":
            alreadyThere=False
            for count, widget in enumerate(frameMain.winfo_children()):
                if count >= 17:
                    widget.destroy()
                    alreadyThere=True
                    
            num=14
            height=9
            

        fontsize=16
        if len(message) > 50:
            fontsize=14
            
        if message == " Password too weak\n [must contain a capital, number and special character]":
            message = "Password too weak [must contain a capital, number and special character]"
            
        if alreadyThere == False:  
            for count,widget in enumerate(frameMain.winfo_children()):
                if count == 0:
                    for subcount,subwidget in enumerate(widget.winfo_children()):
                        if subcount == 0:
                            subwidget.configure(height=height)
                if count != 0 and count < num:
                    oldy = widget.winfo_y()
                    oldx = widget.winfo_x()
                    newy = oldy-55
                    widget.place(x=oldx,y=newy)

        frameMessage = CustomFrame(frameMain,
                                 width=605,
                                 height=45,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=15, y=585)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=False,
                                   width=525,
                                   height=30,
                                   text=message,
                                   fontSize=fontsize,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")
            
    def saveChanges():
        """
        Validates user entries
        If valid updates record and refreshes treeview
        If not valid calls messageBox to display appropriate error
        """
        if profileType == "Customers":
            
            email = str(entries[1].get()).lower()
            validEmail = validation.emailCheck(email)
            if validEmail != True:
                messageBox(validEmail)
                return

            password = entries[2].get()
            forename = (entries[3].get()).lower()
            surname = (entries[4].get()).lower()
            DOB = entries[5].get()
            favourite = genreVar.get()

            if testing == False:
                validPassword = validation.passwordCheck(password)
                if validPassword != True:
                    messageBox(validPassword)
                    return
                
                validForename = validation.nameCheck(forename,"forename")
                if validForename != True:
                    messageBox(validForename)
                    return
                
                validSurname = validation.nameCheck(surname,"surname")
                if validSurname != True:
                    messageBox(validSurname)
                    return
                
                validDOB = validation.dateCheck(DOB)
                if validDOB != True:
                    messageBox(validDOB)
                    return
                
                if favourite == "-":
                    messageBox("Please select your favourite genre")
                    return

            else:
                if password == "":
                    messageBox("Please enter a password")

                    
            password=encryption.XOR(password)
            
            customerID=int(entries[0].text)

            updateCustomerUser(customerID=customerID,
                               email=email,
                               password=password,
                               forename=forename,
                               surname=surname,
                               DOB=DOB,
                               favourite=favourite)

            ID = customerID
            IDs = searchTable("customerID","customer","")

            message=False
            for count, widget in enumerate(frameMain.winfo_children()):
                if count >= 19:
                    widget.destroy()
                    message=True
            if message == True:
                num=16
                height=9
                

        if profileType == "Staff":
            
            staffID=int(IDVar.get())
            username = (entries[1].text).lower()

            forename = (entries[2].get()).lower()
            surname = (entries[3].get()).lower()
            jobTitle = jobVar.get()
            password = entries[5].get()

            if testing == False:
                validForename = validation.nameCheck(forename,"forename",extra="a")
                if validForename != True:
                    messageBox(validForename)
                    return
            
                validSurname = validation.nameCheck(surname,"surname",extra="a")
                if validSurname != True:
                    messageBox(validSurname)
                    return
                
                if jobTitle == "-":
                    messageBox("Please enter a Job Title")
                    return
                
                validPassword = validation.passwordCheck(password)
                if validPassword != True:
                    messageBox(validPassword)
                    return

            else:
                if password == "":
                     messageBox("Please enter a password")
                     
            password = encryption.XOR(password)

            updateStaff(staffID=staffID,
                           username=username,
                           forename=forename,
                           surname=surname,
                           jobTitle=jobTitle,
                           password=password)

            ID = staffID
            IDs = searchTable("staffID","staff","")

            message=False
            for count, widget in enumerate(frameMain.winfo_children()):
                if count >= 17:
                    widget.destroy()
                    message=True
            if message == True:
                num=14
                height=11

        if message == True:
            for count,widget in enumerate(frameMain.winfo_children()):
                if count == 0:
                    for subcount,subwidget in enumerate(widget.winfo_children()):
                        if subcount == 0:
                            subwidget.configure(height=height)
                if count != 0 and count < num:
                    oldy = widget.winfo_y()
                    oldx = widget.winfo_x()
                    newy = oldy+55
                    widget.place(x=oldx,y=newy)

        #refreshes Treeview              
        tree.delete(*tree.get_children())
        fillTree()
        for n in range(0,len(IDs)):
            if IDs[n][0] == ID:
                index=n
        rowID = tree.get_children()[index]
        tree.focus(rowID)
        tree.selection_set(rowID)


                
    def deleteUser():
        """
        Creates a toplevel widget to confirm the staff member wants to delete the record
        Deletes user record and all associated records so as to not leave any orphan foreign keys
        """
        def cancel():
            """
            Destroy delete toplevel
            """
            delete.destroy()
            
        def deleteCustomer():
            """
            Deletes Customer record and all associated records
            """
            delete.destroy()
            customerID=int(entries[0].text)

            deleteRecord("customer","customerID",str(customerID))
            transactions=searchTable("transactionID","gameTransaction","WHERE userID = "+str(currentUserID))
            deleteRecord("gameTransaction", "userID", str(currentUserID))
            for n in range(0,len(transactions)):
                deleteRecord("gameOrder", "transactionID", str(transactions[n][0]))
                
            deleteRecord("wishlist", "userID", str(currentUserID))
            deleteRecord("basket", "userID", str(currentUserID))
            deleteRecord("ratings", "userID", str(currentUserID))

            tree.delete(*tree.get_children())
            fillTree()

            for n in range(0,len(entries)):
                if n == 0:
                    entries[n].configure(text="")
                if n > 0:
                    if n < 6:
                        entries[n].delete(0,'end')
                        entries[n].configure(state="disabled")
                    else:
                        entries[n].set("-")
                        entries[n].configure(state="disabled")
        
            buttonSave.configure(state="disabled",border_color=hoverColour)
            buttonDelete.configure(state="disabled",border_color=hoverColour)
            buttonDeselect.configure(state="disabled",border_color=hoverColour)

            message=False
            for count, widget in enumerate(frameMain.winfo_children()):
                if count >= 19:
                    widget.destroy()
                    message=True
            if message == True:
                for count,widget in enumerate(frameMain.winfo_children()):
                    if count == 0:
                        for subcount,subwidget in enumerate(widget.winfo_children()):
                            if subcount == 0:
                                subwidget.configure(height=9)
                    if count != 0 and count < 16:
                        oldy = widget.winfo_y()
                        oldx = widget.winfo_x()
                        newy = oldy+55
                        widget.place(x=oldx,y=newy)
                            
        def deleteStaff():
            """
            Deletes Staff record and all associated records
            """
            delete.destroy()
            staffID=int(IDVar.get())

            deleteRecord("staff","staffID",str(staffID))
            
            tree.delete(*tree.get_children())
            fillTree()

            for n in range(0,len(entries)):
                if n == 0:
                    IDVar.set("")
                if n > 1:
                    if n == 4:
                        entries[n].set("-")
                        entries[n].configure(state="disabled")
                    else:
                        entries[n].delete(0,'end')
                        entries[n].configure(state="disabled")
    
        
            buttonSave.configure(state="disabled",border_color=hoverColour)
            buttonDelete.configure(state="disabled",border_color=hoverColour)
            buttonDeselect.configure(state="disabled",border_color=hoverColour)

            message=False
            for count, widget in enumerate(frameMain.winfo_children()):
                if count >= 17:
                    widget.destroy()
                    message=True
            if message == True:
                for count,widget in enumerate(frameMain.winfo_children()):
                    if count == 0:
                        for subcount,subwidget in enumerate(widget.winfo_children()):
                            if subcount == 0:
                                subwidget.configure(height=11)
                    if count != 0 and count < 14:
                        oldy = widget.winfo_y()
                        oldx = widget.winfo_x()
                        newy = oldy+55
                        widget.place(x=oldx,y=newy)

            
        delete = tkinter.Toplevel(window)   
        delete.geometry("600x370")
        delete.title("Security Check")
        delete.resizable(False, False)
        delete.configure(bg=frameColour)

        center(delete)

        frameDelete = CustomFrame(master=delete,
                                 width=530,
                                 height=300,
                                 fgColour=bgColour,
                                 cornerRadius=0)
        frameDelete.place(x=35, y=35)

        frameTitle = CustomFrame(master=frameDelete,
                                width=490,
                                height=70)
        frameTitle.place(x=20, y=20)

        labelLogoSmall = customtkinter.CTkLabel(master=frameTitle,
                                                width=120,
                                                height=70,
                                                image=logoLong2)
        labelLogoSmall.place(x=355, y=0)

        labelTitle = CustomSubtitle(master=frameTitle,
                                    text="Security Check")
        labelTitle.place(x=20, y=10)

        frameInput = CustomFrame(master=frameDelete,
                                width=490,
                                height=170)
        frameInput.place(x=20, y=110)

        labelSubtitle = CustomSubtitle(master=frameInput,
                                       text="Are You Sure?",
                                       fontSize=22)
        labelSubtitle.place(x=145, y=20)

        buttonConfirm = CustomButtonDark(master=frameInput,
                                       width=100,
                                       height=50,
                                       fgColour=warningColour,
                                       bgColour=frameColour,
                                       borderWidth=2,
                                       text="Delete",
                                       hovColour="#EC805F")
        buttonConfirm.place(x=120, y=90)
        if profileType == "Customers":
            buttonConfirm.configure(command=deleteCustomer)
        if profileType == "Staff":
            buttonConfirm.configure(command=deleteStaff)

        buttonCancel = CustomButtonDark(master=frameInput,
                                       width=100,
                                       height=50,
                                       fgColour=frameColour,
                                       bgColour=frameColour,
                                       borderWidth=2,
                                       text="Cancel",
                                       command=cancel)
        buttonCancel.place(x=270, y=90)
        

    def deselect():
        """
        Deselects the chosen record and returns the staff member to normal viewing mode
        """
        for item in tree.selection():
           tree.selection_remove(item)

        for n in range(0,len(entries)):
            if n == 0 and profileType == "Customers":
                entries[n].configure(text="")
            elif (n == 0 or n == 1) and profileType == "Staff":
                IDVar.set("")
            else:
                if (n==6 and profileType == "Customers") or (n==4 and profileType == "Staff"):
                    entries[n].set("-")
                    entries[n].configure(state="disabled")
                else:
                    entries[n].delete(0,'end')
                    entries[n].configure(state="disabled")

        buttonSave.configure(state="disabled",border_color=hoverColour)
        buttonDelete.configure(state="disabled",border_color=hoverColour)
        buttonDeselect.configure(state="disabled",border_color=hoverColour)

        if profileType == "Customers":
            num=16
            height=9
        if profileType == "Staff":
            num=14
            height=11
            
        message=False
        for count, widget in enumerate(frameMain.winfo_children()):
            if count >= num+3:
                widget.destroy()
                message=True
                
        if message == True:
            for count,widget in enumerate(frameMain.winfo_children()):
                if count == 0:
                    for subcount,subwidget in enumerate(widget.winfo_children()):
                        if subcount == 0:
                            subwidget.configure(height=height)
                if count != 0 and count < num:
                    oldy = widget.winfo_y()
                    oldx = widget.winfo_x()
                    newy = oldy+55
                    widget.place(x=oldx,y=newy)

    def item_selected(event=None,search=False):
        """
        When a record is selected
        Retrieves information about the chosen record
        This information is filled into the entry widgets so the user can edit them
        Entry widgets are buttons are activated
        """

        buttonSave.configure(command=saveChanges)
                             
        for selected_item in tree.selection():
            
            if profileType == "Customers":
                num=16
                height=9
            if profileType == "Staff":
                num=14
                height=11
                
            message=False
            for count, widget in enumerate(frameMain.winfo_children()):
                if count >= num+3:
                    widget.destroy()
                    message=True
                    
            if message == True:
                for count,widget in enumerate(frameMain.winfo_children()):
                    if count == 0:
                        for subcount,subwidget in enumerate(widget.winfo_children()):
                            if subcount == 0:
                                subwidget.configure(height=height)
                    if count != 0 and count < num:
                        oldy = widget.winfo_y()
                        oldx = widget.winfo_x()
                        newy = oldy+55
                        widget.place(x=oldx,y=newy)


                            
            item = tree.item(selected_item)
            values = item["values"]
            
            #rowID = tree.get_children()[int(selected_item)]
            #tree.focus(selected_item)
            #tree.selection_set(selected_item)
            
            if profileType == "Staff":
                values = [values[0],values[1],values[3],values[4],values[5],values[2]]
                if values[4] == "Admin" and view != "Admin":
                    #flash locked icon the the screen 
                    labelLock = customtkinter.CTkLabel(master=frameTreeview,
                                                       width=60,
                                                       height=80,
                                                       image=lockedIcon)
                    labelLock.place(relx=0.5,rely=0.5,anchor="center")
                    window.update()
                    
                    time.sleep(0.5)
                    labelLock.place_forget()
                    window.update()
                    
                    time.sleep(0.2)
                    labelLock.place(relx=0.5,rely=0.5,anchor="center")
                    window.update()
                    
                    time.sleep(0.35)
                    labelLock.place_forget()
                    window.update()
                    
                    time.sleep(0.2)
                    labelLock.place(relx=0.5,rely=0.5,anchor="center")
                    window.update()
                    
                    time.sleep(0.30)
                    labelLock.place_forget()
                    window.update()
                    
                    deselect()
                    return
                
            if profileType == "Staff":
                entries[4].configure(state="disabled")
                buttonDelete.configure(state="disabled",border_color=hoverColour)
                
                
            for n in range(0,len(values)):
                if n == 0:
                    if profileType == "Customers":
                        entries[n].configure(text=(4-len(str(values[n])))*"0"+str(values[n]))
                    if profileType == "Staff":
                        IDVar.set((4-len(str(values[n])))*"0"+str(values[n]))
                elif (n == 6 and profileType == "Customers") or (n == 4 and profileType == "Staff"):
                    entries[n].set(values[n])
                    if values[4] != "Admin":
                        entries[n].configure(state="normal")
                else:
                    if (profileType == "Customers") or (profileType == "Staff" and n != 1):
                        entries[n].configure(state="normal")
                        entries[n].delete(0,'end')
                        entries[n].insert(0, values[n])

        if len(tree.selection()) != 0:
            buttonSave.configure(state="normal",border_color=textColour)
            if values[4] != "Admin":
                buttonDelete.configure(state="normal",border_color=textColour)
            buttonDeselect.configure(state="normal",border_color=textColour)

    def editUsername(*args):
        """
        If in staff profiles
        Username is auto made using staff members first initial, surname and ID number
        When any of these fields are updated the username label is updated too to match
        """
        username = ""
        if forenameVar.get() != "":
            username = ((forenameVar.get())[:1].upper())
        if surnameVar.get() != "":
            username = ((forenameVar.get())[:1].upper())+(surnameVar.get()).capitalize()+ IDVar.get()
            
        entryUsername.configure(text = username)
        

    #clear main frame
    for widget in frameMain.winfo_children():
        widget.destroy()


    for count,widget in enumerate(window.winfo_children()):
        if count == 2:
            widget.destroy()
        if isinstance(widget,tkinter.Toplevel):
            widget.destroy()

    #reset all widgets in sideframe             
    for count,widget in enumerate(frameSide.winfo_children()):
        if count < 2:
            widget.configure(border_width=1)
            for button in widget.winfo_children():
                    button.configure(text_color = textColour,
                                        fg_color = frameColour,
                                        bg_color = frameColour)
        if count == 2:
            widget.place(x=25,y=320)
        if count == 3:
            widget.place_forget()
        if count == 4:
             widget.configure(fg_color=textColour,
                              text_color=frameColour)

    #configure pressed button and frame to be highlighted          
    for count,frame in enumerate(frameSide.winfo_children()):
        if count ==1:
            frame.configure(border_width=5)
            for button in frame.winfo_children():
                if button.text == profileType:
                    button.configure(text_color = frameColour,
                                     fg_color = textColour,
                                     bg_color = textColour)

    frameTreeview = CustomFrame(master=frameMain,
                                width=100,
                                height=100,
                                borderWidth=2,
                                cornerRadius=0)
    frameTreeview.place(x=20,y=20)

    #Treeview widget restyle
    s = ttk.Style()
    s.theme_use('default')
    s.map("Treeview", foreground = fixedMap("foreground"),background=fixedMap("background"))
    s.configure("Treeview",background=frameColour,foreground=entryColour,fieldbackground=frameColour,rowheight=28)
    s.configure("Treeview.Heading", background=textColour)
    s.map("Treeview",background=[("selected",hoverColour)],foreground=[("selected",frameColour)])
    s.map("Treeview.Heading",background=[("selected",textColour)])

    s.configure("Vertical.TScrollbar", background=textColour,arrowcolor=frameColour)

    #Create Treeview
    if profileType == "Customers":
        columns=("ID","Email Address","Password","Forename","Surname","Date of Birth","Favourite Genre")
        widths=(35,89,89,89,89,89,90)
    if profileType == "Staff":
        columns=("ID","Username","Password","Forename","Surname","Job Title")
        widths=(35,120,110,100,100,105)

    if profileType == "Customers":
        height = 9
    if profileType == "Staff":
        height = 11
        
    tree= ttk.Treeview(frameTreeview, column=columns, show= 'headings', height=height, selectmode="browse")
    for n in range(0,len(columns)):
        tree.column(columns[n],anchor="w", width=widths[n])
        tree.heading(columns[n],text=columns[n])

    tree.grid(padx=(3,0),pady=(3,4),row=0, column=0, sticky="nsew")
    tree.bind('<<TreeviewSelect>>', item_selected)

    fillTree()

    scrollbar = ttk.Scrollbar(frameTreeview,
                              orient=tkinter.VERTICAL,
                              command=tree.yview)
    
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(padx=(0,4),pady=(3,4),row=0, column=1, sticky="ns")

    #Search Frame
    frameSearch = CustomFrame(master=frameMain,
                              width=595,
                              height=50,
                              cornerRadius=0,
                              borderWidth=2)
    if profileType == "Customers":
        frameSearch.place(x=20,y=295)
    if profileType == "Staff":
        frameSearch.place(x=20,y=352)

    placeholderText = "Search "+profileType
    searchBar = CustomEntry(master=frameSearch,
                            width=180,
                            height=30,
                            cornerRadius=20,
                            borderWidth=1,
                            fontSize=12,
                            placeholderText=placeholderText)
    searchBar.place(x=20, y=10)
    buttonSearch = customtkinter.CTkButton(master=frameSearch,
                                           width=40,
                                           height=40,
                                           text="",
                                           corner_radius=30,
                                           hover_color=hoverColour,
                                           fg_color=frameColour,
                                           image=searchIcon,
                                           command=search)
    buttonSearch.place(x=200, y=5)
    searchBar.bind("<Return>",search)

    if profileType == "Customers":
        labelText = "Add Customers"
        labelWidth = 50
        labelx = 383
    if profileType == "Staff":
        labelText = "Add Staff Members"
        labelWidth = 60
        labelx = 343
    labelAdd = CustomButtonText(master=frameSearch,
                                width=labelWidth,
                               height=30,
                               text=labelText,
                               fontSize=18,
                                hoverEnabled=False)
    labelAdd.place(x=labelx, y=7)
    buttonAdd = CustomHoverButton(master=frameSearch,
                                  width=20,
                                  height=20,
                                  image1=plusIcon,
                                  image2=plusHover)
    buttonAdd.place(x=555,y=13)
    if profileType == "Customers":
        labelAdd.configure(command=newCustomer)
        buttonAdd.bind("<Button-1>",newCustomer)
    if profileType == "Staff":
        labelAdd.configure(command=newStaff)
        buttonAdd.bind("<Button-1>",newStaff)
    
            
    #Entry widgets
    if profileType == "Customers":
        IDText = "UserID:"
    if profileType == "Staff":
        IDText = "StaffID:"

    labelID = CustomTkLabelEntry(master=frameMain,
                                     text=IDText)
    highlightID = CustomFrame(master=frameMain,
                                  width=285,
                                  height=35,
                                  fgColour=frameColour,
                                  cornerRadius=10)
    entryID = CustomLabel(master=highlightID,
                         autoWidth=False,
                         width=285,
                         height=35,
                         cornerRadius=10,
                         fgColour=bgColour,
                         text="",
                         fontSize=16)
    entryID.place(x=0,y=0)
    entryID.text_label.place(x=10,y=3)

    labelPassword = CustomTkLabelEntry(master=frameMain,
                                     text="Password:")
    entryPassword = CustomEntry(master=frameMain,
                                width=285,
                         borderWidth=3,
                           state="disabled")

    labelForename = CustomTkLabelEntry(master=frameMain,
                                     text="Forename:")
    entryForename = CustomEntry(master=frameMain,
                                width=285,
                                borderWidth=3,
                                state="disabled")

    labelSurname = CustomTkLabelEntry(master=frameMain,
                                     text="Surname:")
    entrySurname = CustomEntry(master=frameMain,
                               width=285,
                               borderWidth=3,
                               state="disabled")
    

    if profileType == "Customers":
        labelID.place(x=25,y=365)
        highlightID.place(x=20,y=395)

        labelEmail = CustomTkLabelEntry(master=frameMain,
                                         text="Email Address:")
        labelEmail.place(x=25,y=430)
        entryEmail = CustomEntry(master=frameMain,
                                    width=285,
                             borderWidth=3,
                               state="disabled")
        entryEmail.place(x=20,y=460)

        labelPassword.place(x=335,y=430)
        entryPassword.place(x=330,y=460)

        labelForename.place(x=25,y=495)
        entryForename.place(x=20, y=525)

        labelSurname.place(x=335,y=495)
        entrySurname.place(x=330,y=525)

        labelDOB = CustomTkLabelEntry(master=frameMain,
                                      text="Date of Birth:")
        labelDOB.place(x=25,y=560)
        entryDOB = CustomEntry(master=frameMain,
                               width=285,
                             borderWidth=3,
                               state="disabled")
        entryDOB.place(x=20,y=590)

        labelGenre = CustomTkLabelEntry(master=frameMain,
                                         text="Favourite Genre:")
        labelGenre.place(x=335,y=560)

        getInfo = searchTable("genre","game","")        
        getGenres = []
        for n in range(0, len(getInfo)):
            if getInfo[n][0] not in getGenres:
                getGenres.append(getInfo[n][0])
        getGenres = sorted(getGenres)
            
        favourite="-"
        
        highlightGenre = CustomFrame(master=frameMain,
                                      width=285,
                                      height=38,
                                      fgColour=frameColour,
                                      cornerRadius=10)
        highlightGenre.place(x=330,y=590)
        genreVar = customtkinter.StringVar(value=favourite)
        entryGenre = CustomDropdown(master=highlightGenre,
                                    variable=genreVar,
                                    width=285,
                                    values=getGenres,
                                    state="disabled")
        entryGenre.place(x=0,y=0)
    
        entries = [entryID,entryEmail,entryPassword,entryForename,entrySurname,entryDOB,entryGenre]


    if profileType == "Staff":
        IDVar = tkinter.StringVar()
        IDVar.trace('w', editUsername)
        forenameVar = tkinter.StringVar()
        forenameVar.trace('w', editUsername)
        surnameVar = tkinter.StringVar()
        surnameVar.trace('w', editUsername)
        
        labelID.place(x=25,y=430)
        highlightID.place(x=20,y=460)
        entryID.configure(textvariable = IDVar)

        labelUsername = CustomTkLabelEntry(master=frameMain,
                                            text="Username:")
        labelUsername.place(x=335,y=430)
        highlightUsername = CustomFrame(master=frameMain,
                                  width=285,
                                  height=35,
                                  fgColour=frameColour,
                                  cornerRadius=10)
        highlightUsername.place(x=330,y=460)
        entryUsername = CustomLabel(master=highlightUsername,
                             autoWidth=False,
                             width=285,
                             height=35,
                             cornerRadius=10,
                             fgColour=bgColour,
                            text="",
                             fontSize=16)
        entryUsername.place(x=0,y=0)
        entryUsername.text_label.place(x=10,y=3)

        labelForename.place(x=25,y=495)
        entryForename.place(x=20, y=525)
        entryForename.configure(textvariable = forenameVar)

        labelSurname.place(x=335,y=495)
        entrySurname.place(x=330,y=525)
        entrySurname.configure(textvariable = surnameVar)

        labelJobTitle = CustomTkLabelEntry(master=frameMain,
                                         text="Job Title:")
        labelJobTitle.place(x=25,y=560)
        job="-"
        highlightJobTitle = CustomFrame(master=frameMain,
                                      width=285,
                                      height=38,
                                      fgColour=frameColour,
                                      cornerRadius=10)
        highlightJobTitle.place(x=20,y=590)
        jobVar = customtkinter.StringVar(value=job)
        entryJobTitle = CustomDropdown(master=highlightJobTitle,
                                       values=["-",
                                               "Upper",
                                               "Lower"],
                                    variable=jobVar,
                                    width=285,
                                    state="disabled")
        entryJobTitle.place(x=0,y=0)      

        labelPassword.place(x=335,y=560)
        entryPassword.place(x=330,y=590)
 
        entries = [entryID,entryUsername,entryForename,entrySurname,entryJobTitle,entryPassword]

        

    buttonSave = CustomButtonDark(master=frameMain,
                                  height=35,
                                  width=160,
                                  text="Save Changes",
                                  fgColour=bgColour,
                                  bgColour=frameColour,
                                  borderWidth=2,
                                  borderColour=hoverColour,
                                  fontSize=14,
                                  state="disabled",
                                  command=saveChanges)
    buttonSave.place(x=20,y=645)

    if profileType == "Customers":
        deleteText = "Delete Customer"
    if profileType == "Staff":
        deleteText = "Delete Staff Member"
    buttonDelete = CustomButtonDark(master=frameMain,
                                    height=35,
                                    width=200,
                                    text=deleteText,
                                    fgColour=warningColour,
                                    bgColour=frameColour,
                                    borderWidth=2,
                                    borderColour=hoverColour,
                                    fontSize=14,
                                    state="disabled",
                                    command=deleteUser)
    buttonDelete.place(x=220,y=645)

    buttonDeselect = CustomButtonDark(master=frameMain,
                                  height=35,
                                  width=160,
                                  text="Deselect",
                                  fgColour=bgColour,
                                  bgColour=frameColour,
                                  borderWidth=2,
                                  borderColour=hoverColour,
                                  fontSize=14,
                                  state="disabled",
                                  command=deselect)
    buttonDeselect.place(x=455,y=645)


def StaffOrders(frameMain,frameSide):
    """
    Parameters: frameMain - main frame of staff area
                frameSide - side frame of staff area holding the traversal buttons
    Displays all orders to the staff
    Orders are displayed most recent first
    Can be searched by many attributes such as orderID or User ID etc.
    Staff can click into the orders for more details
    """
    def details(transactionID):
        """
        Parameters: transactionID - ID of transaction to display details of
        Displays a recreation of order receipt on the screen
        Includes all games in the order and their price
        """
        def fillReceipt(pageNo):
            """
            Parameters: pageNo - receipt page number
            fill receipt with the game names and prices from the order depending on the page number
            """
            #clear receipt
            for count,widget in enumerate(frameReceipt.winfo_children()):
                if count > 4:
                    widget.destroy()
                
            n=pageNo-1
            for m in range(0,len(titlesSplit[n])):
                ycoord=9+30*m
                labelTitle = CustomLabel(master=frameGames,
                                         autoWidth=False,
                                         width=180,
                                         height=30,
                                         fgColour=bgColour,
                                         text=titlesSplit[n][m],
                                         fontSize=16,
                                         anchor="w")
                labelTitle.place(x=25,y=ycoord)
                labelPrice = CustomLabel(master=frameGames,
                                         autoWidth=False,
                                         width=170,
                                         height=30,
                                         fgColour=bgColour,   
                                         text=pricesSplit[n][m],
                                         fontSize=16,
                                         anchor="e")
                labelPrice.place(x=390,y=ycoord)


        def backPage(pageNo):
            """
            Parameters: pageNo - receipt page number
            Goes backwards one page on the receipt
            """
            pageNo -= 1
            buttonNext.configure(command=partial(nextPage,pageNo))
            buttonBack.configure(command=partial(backPage,pageNo))

            labelPageNo.configure(text="Page "+str(pageNo))
            
            if pageNo == 1:
                buttonBack.configure(state="disabled")

            buttonNext.configure(state="normal")
            fillReceipt(pageNo)
            
        def nextPage(pageNo):
            """
            Parameters: pageNo - receipt page number
            Goes forwards one page on the receipt
            """
            pageNo += 1
            buttonNext.configure(command=partial(nextPage,pageNo))
            buttonBack.configure(command=partial(backPage,pageNo))

            labelPageNo.configure(text="Page "+str(pageNo))

            if pageNo == numPages:
                buttonNext.configure(state="disabled")

            if pageNo == 2:
                buttonBack.configure(state="normal")
                
            fillReceipt(pageNo)

        def destroy(event=None):
            """
            Destroy more details frame 
            Return user to view orders page
            """
            frameDetails.destroy()

        
        frameDetails = CustomFrame(master=window,
                            width=635,
                            height=700)
        frameDetails.place(x=345,y=20)
        buttonBack = CustomHoverButton(master=frameDetails,
                                         width=45,
                                         height=40,
                                         image1=backIcon,
                                        image2=backHover,
                                        command=destroy)
        buttonBack.place(x=10, y=10)
        
        transactionInfo = searchTable("total,date,userID","gameTransaction","WHERE transactionID = "+str(transactionID))
        customerInfo = searchTable("customerForename,customerSurname,cardNumber","customer","WHERE customerID = "+str(transactionInfo[0][2]))

        numZeros = 4-len(str(transactionID))
        orderNum = "Order Number: "+"0"*numZeros+ str(transactionID)
        
        date = str(transactionInfo[0][1])
        
        total=transactionInfo[0][0]
        if total == 0.0:
            totalStr="Total: £0.00 GBP"
        else:
            if len(str(total).rsplit('.')[-1]) == 2:
                totalStr = "Total: £"+str(total)+" GBP"
            elif len(str(total).rsplit('.')[-1]) == 1:
                totalStr = "Total: £"+str(total)+"0 GBP"
            if len(str(total).rsplit('.')[-1]) > 2:
                numExtra = len(str(total).rsplit('.')[-1]) - 2
                totalStr = "Total: £"+str(total)[:-numExtra]+" GBP"
                
        name = customerInfo[0][0].capitalize()+" "+customerInfo[0][1].capitalize()
        
        numZeros2 = 4-len(str(transactionInfo[0][2]))
        userID = "User ID: "+"0"*numZeros2+ str(transactionInfo[0][2])
        
        labelOrderNum = CustomLabel(master=frameDetails,
                                    height=50,
                                    text=orderNum,
                                    anchor="w",
                                    fontSize=22)
        labelOrderNum.place(x=35,y=60)
        labelDate = CustomLabel(master=frameDetails,
                                    height=50,
                                    anchor="w",
                                    text=date,
                                    fontSize=20)
        labelDate.place(x=35,y=100)

        labelName = CustomLabel(master=frameDetails,
                                height=50,
                                    text=name,
                                    anchor="e",
                                    fontSize=22)
        labelName.place(x=600,y=60,anchor="ne")
        labelUserID = CustomLabel(master=frameDetails,
                                    height=40,
                                  autoWidth=False,
                                  width=210,
                                  anchor="e",
                                    text=userID,
                                    fontSize=20)
        labelUserID.place(x=390,y=103)
        
        frameReceipt = CustomFrame(master=frameDetails,
                                    width=585,
                                    fgColour=bgColour,
                                    height=505)
        frameReceipt.place(x=25,y=170)
        frameTitles = CustomFrame(master=frameReceipt,
                                    width=534,
                                    fgColour=bgColour,
                                    height=44)
        frameTitles.place(x=25,y=0)
        frameExtra = CustomFrame(master=frameReceipt,
                                    width=534,
                                    fgColour=bgColour,
                                    height=44)
        frameExtra.place(x=25,y=456)
        
        labelTitle = CustomLabel(master=frameTitles,
                                    height=40,
                                    text="Title",
                                    fgColour=bgColour,
                                    fontSize=20)
        labelTitle.place(x=0,y=5)
        labelSubtotal = CustomLabel(master=frameTitles,
                                    fgColour=bgColour,
                                    height=40,
                                    text="Subtotal",
                                    fontSize=20)
        labelSubtotal.place(x=445,y=5)
        
        line1 = ttk.Separator(frameReceipt, orient="horizontal")
        line1.place(x=25, y=45, relwidth=0.9145, relheight=0.00005)


        frameGames = CustomFrame(master=frameReceipt,
                                   width=584,
                                   height=408,
                                   fgColour=bgColour,
                                   cornerRadius=0)
        frameGames.place(x=0,y=46)
        
        line2 = ttk.Separator(frameReceipt, orient="horizontal")
        line2.place(x=25, y=455, relwidth=0.9145, relheight=0.00005)

        
        labelTotal = CustomLabel(master=frameExtra,
                                 autoWidth=False,
                                 width=190,
                                 anchor="e",
                                    fgColour=bgColour,
                                    height=35,
                                    text=totalStr,
                                    fontSize=18)
        labelTotal.place(x=345,y=0)

        
        gameDetails = searchTable("gameID","gameOrder","WHERE transactionID = "+str(transactionID))
        
        titles=[]
        prices=[]
        numGames=len(gameDetails)
        numPages = numGames//13
        numExtra = numGames%13
        pageNo=0
        
        if numExtra!=0:
            numPages+=1
        
        for n in range(0,numGames):
                currentRecord=searchTable("title,price","game","WHERE forSale = 1 AND gameID = "+str(gameDetails[n][0]))
                titles.append(currentRecord[0][0])
                getPrice=currentRecord[0][1]
                if getPrice == 0.0 or getPrice == 0.00:
                    currentPrice="£0.00"
                else:
                    if len(str(getPrice).rsplit('.')[-1]) == 2:
                        currentPrice = "£"+str(getPrice)
                    else:
                        currentPrice = "£"+str(getPrice)+"0"
                prices.append(currentPrice)


        #split titles into lists of 13 because 13 can fit on one page
        start = 0
        end = len(titles)
        step = 13
        titlesSplit=[]
        pricesSplit=[]
        for i in range(start, end, step):
            x = i
            titlesSplit.append(titles[x:x+step])
            pricesSplit.append(prices[x:x+step])

        if numPages > 1:
            labelPageNo = CustomLabel(master=frameGames,
                                      autoWidth=False,
                                      width=50,
                                      height=15,
                                      fgColour=bgColour,
                                      text="Page "+str(pageNo),
                                      fontSize=14)
            labelPageNo.place(x=270,y=375)
            buttonBack =  CustomButtonText(master=frameGames,
                                         width=20,
                                         height=15,
                                         fgColour=bgColour,
                                         text="<",
                                         state="disabled",
                                         cornerRadius=0,
                                           fontSize=14,
                                         hoverEnabled=False,
                                           command=partial(nextPage,pageNo))
            buttonBack.place(x=245, y=372)
            buttonNext = CustomButtonText(master=frameGames,
                                         width=20,
                                         height=15,
                                         fgColour=bgColour,
                                         text=">",
                                         cornerRadius=0,
                                          fontSize=14,
                                         hoverEnabled=False,
                                          command=partial(backPage,pageNo))
            buttonNext.place(x=325, y=372)
            nextPage(pageNo)
        else:
            fillReceipt(1)
            
    def fillOrderFrames(firstTransaction,lastTransaction,displayList):
        """
        Parameters: firstTransaction - index of first transaction to be displayed from displayList
                    lastTransaction - index of last transaction to be displayed from displayList
                    displayList - array of transactions to be displayed
        Fills all order frames with the information: Date, Order Number, User ID, Total
        Frames contain a button to view more details
        """
        global gameImage1,gameImage2,gameImage3,gameImage4,gameImage5,gameImage6,gameImage7,gameImage8,gameImage9,gameImage10,gameImage11,gameImage12

        dif=lastTransaction-firstTransaction

        dates=[]
        orderNums=[]
        userIDs=[]
        totals=[]
        imageNames=[]
        for n in range(firstTransaction,lastTransaction):
            currentTransaction = str(displayList[n])
            transactionInfo = searchTable("userID,date,total","gameTransaction","WHERE transactionID = "+currentTransaction)
            
            orderZeros = 4-len(currentTransaction)
            orderNums.append(orderZeros*"0"+currentTransaction)
            
            userZeros = 4-len(str(transactionInfo[0][0]))
            userIDs.append(userZeros*"0"+str(transactionInfo[0][0]))

            dates.append(transactionInfo[0][1])

            total = transactionInfo[0][2]
            if total == 0.0:
                totalStr="£00.00"
            else:
                if len(str(total).rsplit('.')[-1]) == 2:
                    totalStr = "£"+str(total)
                elif len(str(total).rsplit('.')[-1]) == 1:
                    totalStr = "£"+str(total)+"0"
                if len(str(total).rsplit('.')[-1]) > 2:
                    numExtra = len(str(total).rsplit('.')[-1]) - 2
                    totalStr = "£"+str(total)[:-numExtra]
            totals.append(totalStr)

            getGames = searchTable("gameID","gameOrder","WHERE transactionID = "+currentTransaction)
            namesList=[]
            for m in range(0, len(getGames)):
                imageName= searchTable("imageName","game","WHERE forSale = 1 AND gameID = "+str(getGames[m][0]))
                namesList.append(imageName[0][0]+"Mini")
            imageNames.append(namesList)


        #There is a possibility of 12 images being on this screen they must all be defined seperately:
        images = [[],[],[]]
        if len(imageNames[0]) == 1:
            gameImage1= openImage("GameImages",(imageNames[0][0])[:-4],140,140)
            images[0].append(gameImage1)
        if len(imageNames[0]) > 0 and len(imageNames[0]) != 1:
            gameImage1= openImage("GameImages",imageNames[0][0],70,70)
            images[0].append(gameImage1)
        if len(imageNames[0]) > 1:
            gameImage2= openImage("GameImages",imageNames[0][1],70,70)
            images[0].append(gameImage2)
        if len(imageNames[0]) > 2:  
            gameImage3= openImage("GameImages",imageNames[0][2],70,70)
            images[0].append(gameImage3)
        if len(imageNames[0]) == 4:  
            gameImage4= openImage("GameImages",imageNames[0][3],70,70)
            images[0].append(gameImage4)
            
        if len(imageNames) > 1:
            if len(imageNames[1]) == 1:
                gameImage5= openImage("GameImages",(imageNames[1][0][:-4]),140,140)
                images[1].append(gameImage5)
            if len(imageNames[1]) > 0 and len(imageNames[1]) != 1:
                gameImage5= openImage("GameImages",imageNames[1][0],70,70)
                images[1].append(gameImage5)
            if len(imageNames[1]) > 1:
                gameImage6= openImage("GameImages",imageNames[1][1],70,70)
                images[1].append(gameImage6)
            if len(imageNames[1]) > 2:
                gameImage7= openImage("GameImages",imageNames[1][2],70,70)
                images[1].append(gameImage7)
            if len(imageNames[1]) == 4:
                gameImage8= openImage("GameImages",imageNames[1][3],70,70)
                images[1].append(gameImage8)

        if len(imageNames) > 2:
            if len(imageNames[2]) == 1:
                gameImage9= openImage("GameImages",(imageNames[2][0])[:-4]+"",140,140)
                images[2].append(gameImage9)
            if len(imageNames[2]) > 0 and len(imageNames[2]) != 1:
                gameImage9= openImage("GameImages",imageNames[2][0],70,70)
                images[2].append(gameImage9)
            if len(imageNames[2]) > 1:
                gameImage10= openImage("GameImages",imageNames[2][1],70,70)
                images[2].append(gameImage10)
            if len(imageNames[2]) > 2:
                gameImage11= openImage("GameImages",imageNames[2][2],70,70)
                images[2].append(gameImage11)
            if len(imageNames[2]) == 4:
                gameImage12= openImage("GameImages",imageNames[2][3],70,70)
                images[2].append(gameImage12)

            
        for n in range(0,dif):
            for widget in frames[n].winfo_children():
                widget.destroy()
                
            currentImages = images[n]

            if len(imageNames[n]) == 1:
                thumbnail1= customtkinter.CTkLabel(master=frames[n],
                                                   width=140,
                                                   height=140,
                                                   image=currentImages[0])
                thumbnail1.place(x=10,y=10)
            if len(imageNames[n]) > 0 and len(imageNames[n]) != 1:
                thumbnail1= customtkinter.CTkLabel(master=frames[n],
                                                   width=70,
                                                   height=70,
                                                   image=currentImages[0])
                thumbnail1.place(x=10,y=10)
            if len(imageNames[n]) > 1:
                thumbnail2= customtkinter.CTkLabel(master=frames[n],
                                                   width=70,
                                                   height=70,
                                                   image=currentImages[1])
                thumbnail2.place(x=81,y=10)
            if len(imageNames[n]) > 2:
                thumbnail3= customtkinter.CTkLabel(master=frames[n],
                                                   width=70,
                                                   height=70,
                                                   image=currentImages[2])
                thumbnail3.place(x=10,y=81)
            if len(imageNames[n]) == 4:
                gameImage4= openImage("GameImages",imageNames[n][3],70,70)
                thumbnail4= customtkinter.CTkLabel(master=frames[n],
                                                   width=70,
                                                   height=70,
                                                   image=currentImages[3])
                thumbnail4.place(x=81,y=81)
            if len(imageNames[n]) > 3 and len(imageNames[n]) != 4:
                labelMore = CustomLabel(master=frames[n],
                                        height=70,
                                        autoWidth=False,
                                        width=70,
                                        cornerRadius=10,
                                        fontSize=22,
                                        fgColour=textColour,
                                        txtColour=frameColour,
                                        text="+"+str(len(imageNames[n])-3))
                labelMore.place(x=81,y=81)


            labelDate = CustomLabel(master=frames[n],
                                    height=25,
                                    anchor="w",
                                    fgColour=bgColour,
                                    fontSize=18,
                                    text=dates[n])
            labelDate.place(x=170,y=10)
            labelOrderNum = CustomLabel(master=frames[n],
                                    height=25,
                                    anchor="w",
                                    fgColour=bgColour,
                                    fontSize=18,
                                    text="Order Number: "+orderNums[n])
            labelOrderNum.place(x=170,y=55)
            labelUser = CustomLabel(master=frames[n],
                                    height=25,
                                    anchor="w",
                                    fgColour=bgColour,
                                    fontSize=18,
                                    text="User ID: "+userIDs[n])
            labelUser.place(x=170,y=80)
            labelTotal = CustomLabel(master=frames[n],
                                    height=25,
                                    anchor="w",
                                    fgColour=bgColour,
                                    fontSize=18,
                                    text="Total: "+totals[n])
            labelTotal.place(x=170,y=125)

            buttonMore = CustomButtonLight(master=frames[n],
                                           width=120,
                                           height=50,
                                           fontSize=16,
                                           text="More Details",
                                           command=partial(details,int(orderNums[n])))
            buttonMore.place(x=410,y=100)
                                    
    def searchOrders(event=None):
        """
        Searches through orders based on the dropdown option that was selected
        sorts results by most relevent
        calls fillOrderFrames to display games
        """
        def backSearch():
            """
            Removes extra buttons and labels from searching
            Returns user to normal viewing mode
            """
            buttonX.place_forget()
            searchBar.delete(0,tkinter.END)
            frame1.focus_set()
            labelMatches.configure(text="")
            
            getTransactions = searchTable("transactionID","gameTransaction","")
            getTransactions.reverse()
            transactions=[]
            for n in range(0,len(getTransactions)):
                transactions.append(getTransactions[n][0])
                
            nextPage(0,-3,0,transactions)

        buttonX.place_forget()
        
        buttonX.place(x=225,y=40)
        buttonX.configure(command=backSearch)
        
        sortType = searchVar.get()
        searchTerm = searchBar.get()
        
        if searchTerm == "":
            backSearch()
            return

        getOrders = searchTable("transactionID,userID,date","gameTransaction","")
        getOrders.reverse()
        
        if sortType == "Order No.":
            orders=[]
            for n in range(0,len(getOrders)):
                zeros = 4-len(str(getOrders[n][0]))
                orders.append(zeros*"0"+str(getOrders[n][0]))
        
            sortedList = sort.searchSort(orders,searchTerm)
            searchResults=[]
            for n in range(0,len(sortedList)):
                searchResults.append(int(sortedList[n]))


        if sortType == "User ID":
            IDs=[]
            for n in range(0,len(getOrders)):
                zeros = 4-len(str(getOrders[n][1]))
                if zeros*"0"+str(getOrders[n][1]) not in IDs:
                    IDs.append(zeros*"0"+str(getOrders[n][1]))
                
            sortedList = sort.searchSort(IDs,searchTerm)
            searchResults=[]
            for n in range(0,len(sortedList)):
                for m in range(0,len(getOrders)):
                    if int(sortedList[n]) == getOrders[m][1]:
                        searchResults.append(getOrders[m][0])


        if sortType == "Date":
            dates=[]
            for n in range(0,len(getOrders)):
                if getOrders[n][2] not in dates:
                    dates.append(getOrders[n][2])
                
            sortedList = sort.searchSort(dates,searchTerm)
            searchResults=[]
            for n in range(0,len(sortedList)):
                for m in range(0,len(getOrders)):
                    if sortedList[n] == getOrders[m][2]:
                        searchResults.append(getOrders[m][0])


        if len(searchResults) != 0:
            labelMatches.configure(text= f"[{len(searchResults)} Results]")
            nextPage(0,-3,0,searchResults)
        else:
            labelMatches.configure(text="[No Matches]")

    #clear main frame   
    for widget in frameMain.winfo_children():
        widget.destroy()

    #reset all button formatting
    for count,widget in enumerate(window.winfo_children()):
        if count == 2:
            widget.destroy()
        if isinstance(widget,tkinter.Toplevel):
            widget.destroy()

    #change button pressed to be highlighted      
    for count,widget in enumerate(frameSide.winfo_children()):
        if count < 2:
            widget.configure(border_width=1)
            for button in widget.winfo_children():
                    button.configure(text_color = textColour,
                                        fg_color = frameColour,
                                        bg_color = frameColour)
        if count == 2:
            widget.place_forget()
        if count == 3:
            widget.place(x=25,y=320)
        if count == 4:
             widget.configure(fg_color=textColour,
                              text_color=frameColour)
             

    labelSearch = CustomLabel(master=frameMain,
                                 height=20,
                                 text="Search",
                                 fontSize=16)
    labelSearch.place(x=34,y=10)
    searchVar = customtkinter.StringVar(value="Order No.")
    dropdownSearch = CustomDropdown(master=frameMain,
                                    variable=searchVar,
                                    width=10,
                                    height=20,
                                    cornerRadius=5,
                                    fgColour=frameColour,
                                    txtColour=textColour,
                                    buttonColour=frameColour,
                                    command=searchOrders,
                                    values=["Order No.","User ID","Date"])
    dropdownSearch.place(x=92,y=8)
    
    searchBar = CustomEntry(master=frameMain,
                            width=220,
                            height=30,
                            cornerRadius=20,
                            fontSize=16,
                            borderWidth=1)
    searchBar.place(x=30, y=40)

    buttonX = CustomButtonText(master=frameMain,
                           height=5,
                           width=1,
                           text="x",
                           fontSize=14,
                           txtColour=frameColour,
                           fgColour=entryColour,
                           cornerRadius=0)
    labelMatches= CustomLabel(master=frameMain,
                              height=30,
                              fontSize=16,
                              text="")
    labelMatches.place(x=295,y=40)
                              

    buttonSearch = customtkinter.CTkButton(master=frameMain,
                                           width=40,
                                           height=40,
                                           corner_radius=30,
                                           text="",
                                           hover_color=hoverColour,
                                           fg_color=frameColour,
                                           image=searchIcon,
                                           command=searchOrders)
    buttonSearch.place(x=250, y=35)
    searchBar.bind("<Return>",searchOrders)



    line = ttk.Separator(frameMain, orient="horizontal")
    line.place(x=0, y=85, relwidth=1, relheight=0.00005)


    getTransactions = searchTable("transactionID","gameTransaction","")
    getTransactions.reverse()
    transactions=[]
    for n in range(0,len(getTransactions)):
        transactions.append(getTransactions[n][0])
    
    numTransactions = len(getTransactions)
    numPages = numTransactions//3
    numExtra = numTransactions%3
    firstTransaction = -3
    lastTransaction = 0
    page=0

    frame1 = CustomFrame(master=frameMain,
                             width=575,
                             height=160,
                             fgColour=bgColour)
    frame1.place(x=30,y=115)
    if numTransactions == 0:
        labelNone = CustomLabel(master=frame1,
                                height=60,
                                fgColour=bgColour,
                                text="No orders have been made yet",
                                fontSize=26)
        labelNone.place(relx=0.5,rely=0.5,anchor="center")
        frames=[]
    else:
        frame2 = CustomFrame(master=frameMain,
                             width=575,
                             height=160,
                             fgColour=bgColour)
        frame2.place(x=30,y=295)
        frame3 = CustomFrame(master=frameMain,
                             width=575,
                             height=160,
                             fgColour=bgColour)
        frame3.place(x=30,y=475)
        frames=[frame1,frame2,frame3]
        

    #navigation
    def nextPage(pageNo,firstTransaction,lastTransaction,displayList):
        """
        Parameters: pageNo - the current page number
                    firstTransaction - the index of the first transaction being displayed
                    lastTransaction - the index of the last transaction being displayed
                    displayList - array of transactions to be displayed 
        Moves forwards one page
        """
        pageNo += 1
        numTransactions = len(displayList)
        numPages = numTransactions//3
        numExtra = numTransactions%3
        if numExtra != 0:
            numPages += 1
            
        firstTransaction += 3

        if numTransactions != 0:
            if pageNo == 1:
                buttonBack.configure(state="disabled")
                buttonNext.configure(state="normal")
                frame2.place(x=30,y=295)
                frame3.place(x=30,y=475)

            if pageNo != numPages:
                lastTransaction += 3
            else:
                if numExtra != 0:
                    lastTransaction += numExtra
                    for n in range(numExtra,3):
                        frames[n].place_forget()
                else:
                    lastTransaction += 3
                buttonNext.configure(state="disabled")
            if pageNo == 2:
                buttonBack.configure(state="normal")
                

            labelPageNo.configure(text="Page "+str(pageNo))
            buttonNext.configure(command=partial(nextPage,pageNo,firstTransaction,lastTransaction,displayList))
            buttonBack.configure(command=partial(backPage,pageNo,firstTransaction,lastTransaction,displayList))

            fillOrderFrames(firstTransaction,lastTransaction,displayList)

        else:
            for n in range(1,3):
                frames[n].place_forget()
            buttonBack.configure(state="disabled")
            buttonNext.configure(state="disabled")
            fillOrderFrames(0,0,[])
            
    def backPage(pageNo,firstTransaction,lastTransaction,displayList):
        """
        Parameters: pageNo - the current page number
                    firstTransaction - the index of the first transaction being displayed
                    lastTransaction - the index of the last transaction being displayed
                    displayList - array of transactions to be displayed 
        Moves backwards one page
        """
        pageNo -= 1

        numTransactions = len(displayList)
        numPages = numTransactions//3
        numExtra = numTransactions%3
        if numExtra != 0:
            numPages += 1

        firstTransaction -= 3
        if pageNo != numPages-1:
            lastTransaction -= 3
        else:
            if numExtra != 0:
                lastTransaction -= numExtra
                frame2.place(x=30,y=295)
                frame3.place(x=30,y=475)
            else:
                lastTransaction -= 3
            buttonNext.configure(state="normal")
            
        if pageNo == 1:
            buttonBack.configure(state="disabled")

        labelPageNo.configure(text="Page "+str(pageNo))
        buttonNext.configure(command=partial(nextPage,pageNo,firstTransaction,lastTransaction,displayList))
        buttonBack.configure(command=partial(backPage,pageNo,firstTransaction,lastTransaction,displayList))

        fillOrderFrames(firstTransaction,lastTransaction,displayList)

    if len(frames) != 0:
        framePages = CustomFrame(master=frameMain,
                                width=160,
                                height=30, 
                                cornerRadius=10)
        framePages.place(x=235, y=650)

        pageNo = "Page", page

        labelPageNo = CustomLabel(master=framePages,
                                 height=20,
                                 text=pageNo,
                                 fontSize=12)
        labelPageNo.place(x=55, y=4)

        buttonNext = CustomButtonText(framePages,
                                        width=20,
                                        height=20,
                                        cornerRadius=0,
                                        text=">",
                                        fontSize=12,
                                        state="normal",
                                        command=partial(nextPage,page,firstTransaction,lastTransaction))
        buttonNext.place(x=105, y=2)

        buttonBack = CustomButtonText(framePages,
                                    width=20,
                                    height=20,
                                    cornerRadius=0,
                                    text="<",
                                    fontSize=12,
                                    state="disabled",
                                    command=partial(backPage,page,firstTransaction,lastTransaction))
        buttonBack.place(x=30, y=2)
        
        nextPage(page,firstTransaction,lastTransaction,transactions)


def MassEmail(frameMain,frameSide):
    """
    Parameters: frameMain - main frame of staff area
                frameSide - side frame of staff area holding the traversal buttons
    Allows upper staff members to email all customer at once
    Displays Email Screen including an entry for subject and message
    """
    def sendConfirm():
        """
        Creates a toplevel to ensure the staff memeber understand what they are doing
        """
        def sendEmail():
            """
            Sends email to all customers
            """
            mailer=yagmail.SMTP(user="goatgamescompany@gmail.com", password="xnzrrgtqfbsuodil")

            subject=entrySubject.get()
            contents=[textMessage.get(1.0,tkinter.END)]

            try:
                getEmails = searchTable("emailAddress","customer","")
                for n in range(0,len(getEmails)):
                    recipient = getEmails[n][0]
                    mailer.send(to=recipient, subject=subject, contents=contents)
                for widget in frameInput.winfo_children():
                    widget.configure(text="Emails Sent!")
                    buttonClose = CustomButtonDark(master=frameInput,
                                                   height=20,
                                                   width=50,
                                                   text="close",
                                                   borderWidth=2,
                                                   bgColour=frameColour,
                                                   command=partial(cancel,True))
                    buttonClose.place(x=380,y=115)
            except:
                def closeTopError():
                    """
                    Closes error topLevel
                    """
                    for count,widget in enumerate(window.winfo_children()):
                        if isinstance(widget,tkinter.Toplevel):
                            widget.destroy()
                            
                confirm.destroy()
                pauseVar = tkinter.StringVar()
                topError = errorMessage(window,"Email could not send",
                                        "Possible reasons include:\n> No Internet Connection\n> Email blocked by System Settings\n> An email was invalid\n> Email request timed out\n> Company Gmail account may not be authorised\n   for sending emails",
                                        command=closeTopError)
                window.wait_variable(pauseVar)    
                    
                    


            
        def cancel(afterSent=False):
            """
            Close confirmation topLevel
            """
            #if closed once sent, clear entry fields
            if afterSent==True:
                textMessage.delete(0.1,tkinter.END)
                entrySubject.delete(0,tkinter.END)
            confirm.destroy()

        def sending():
            """
            Loading screen for sending an email
            Will automatically move on once emails are sent
            """
            for widget in frameInput.winfo_children():
                widget.destroy()

            labelSubtitle = CustomLabel(master=frameInput,
                                        height=60,
                                        autoWidth=False,
                                        width=490,
                                       text="Sending Emails...\nPlease Wait",
                                       fontSize=20)
            labelSubtitle.place(relx=0.5,rely=0.5,anchor="center")

            confirm.after(1000,sendEmail)
        
        confirm = tkinter.Toplevel(window)   
        confirm.geometry("600x370")
        confirm.title("Email")
        confirm.resizable(False, False)
        confirm.configure(bg=frameColour)

        center(confirm)

        frameConfirm = CustomFrame(master=confirm,
                                 width=530,
                                 height=300,
                                 fgColour=bgColour,
                                 cornerRadius=0)
        frameConfirm.place(x=35, y=35)

        frameTitle = CustomFrame(master=frameConfirm,
                                width=490,
                                height=70)
        frameTitle.place(x=20, y=20)

        labelLogoSmall = customtkinter.CTkLabel(master=frameTitle,
                                                width=120,
                                                height=70,
                                                image=logoLong2)
        labelLogoSmall.place(x=355, y=0)

        labelTitle = CustomSubtitle(master=frameTitle,
                                    text="Send Email")
        labelTitle.place(x=20, y=10)

        frameInput = CustomFrame(master=frameConfirm,
                                width=490,
                                height=170)
        frameInput.place(x=20, y=110)

        labelSubtitle = CustomLabel(master=frameInput,
                                    height=60,
                                    autoWidth=False,
                                    width=490,
                                       text="This Email will be sent to all Goat Games customers.\nDo you want to send it?",
                                       fontSize=16)
        labelSubtitle.place(x=0, y=20)

        buttonCancel = CustomButtonDark(master=frameInput,
                                       width=100,
                                       height=50,
                                       fgColour=frameColour,
                                       bgColour=frameColour,
                                       borderWidth=2,
                                       text="Cancel",
                                       command=cancel)
        buttonCancel.place(x=120, y=95)

        buttonSend = CustomButtonDark(master=frameInput,
                                       width=100,
                                       height=50,
                                       fgColour=warningColour,
                                       bgColour=frameColour,
                                       hovColour="#EC805F",
                                       borderWidth=2,
                                       text="Send",
                                       command=sending)
        buttonSend.place(x=270, y=95)



    #clear main frame  
    for widget in frameMain.winfo_children():
        widget.destroy()

    #reset contents of side frame
    for count,widget in enumerate(window.winfo_children()):
        if count == 2:
            widget.destroy()
        if isinstance(widget,tkinter.Toplevel):
            widget.destroy()

    #configure button pressed and frame to be highlighted         
    for count,widget in enumerate(frameSide.winfo_children()):
        if count < 2:
            widget.configure(border_width=1)
            for button in widget.winfo_children():
                    button.configure(text_color = textColour,
                                        fg_color = frameColour,
                                        bg_color = frameColour)
        if count == 2:
            widget.place(x=25,y=320)
        if count == 3:
            widget.place_forget()
        if count == 4:
            widget.configure(fg_color=frameColour,
                             text_color=textColour)
            

    frameSubject = CustomFrame(master=frameMain,
                               width=565,
                               height=120,
                               fgColour=bgColour)
    frameSubject.place(x=35,y=35)

    labelTo = CustomLabel(master=frameSubject,
                          height=40,
                          text="To: All Customers",
                          fontSize=18,
                          fgColour=bgColour)
    labelTo.place(x=20,y=12)
    
    line = ttk.Separator(frameSubject, orient="horizontal")
    line.place(x=0, y=60, relwidth=1, relheight=0.00005)

    labelSubject = CustomLabel(master=frameSubject,
                          height=40,
                          text="Subject:",
                          fontSize=18,
                          fgColour=bgColour)
    labelSubject.place(x=20,y=70)

    entrySubject = CustomEntry(master=frameSubject,
                               width=435,
                               height=40,
                               cornerRadius=0)
    entrySubject.place(x=115,y=70)
    
    frameMessage = CustomFrame(master=frameMain,
                               width=565,
                               height=425,
                               fgColour=bgColour)
    frameMessage.place(x=35,y=180)

    labelMessage = CustomLabel(master=frameMessage,
                          height=40,
                          text="Message:",
                          fontSize=18,
                          fgColour=bgColour)
    labelMessage.place(x=20,y=7)

        
    textMessage = scrolledtext.ScrolledText(master=frameMessage,
                                            wrap=tkinter.WORD,
                                            width=56,
                                            height=15,
                                            font=(mainFont,14),
                                            bg=entryColour,
                                            fg=frameColour,
                                            selectbackground=hoverColour)
    textMessage.place(x=20,y=45)
    
    buttonSend = CustomButtonLight(master=frameMain,
                                   width=150,
                                   height=50,
                                   text="Send",
                                   command=sendConfirm)
    buttonSend.place(x=450,y=625)

def individualGame(frameMain,frameSide,game=-1,forSale=True):
    """
    Parameters: frameMain - main frame of staff area
                frameSide - side frame of staff area holding the traversal buttons
                game - if applicable, ID of game to be edited. Default is -1
                forSale - an indicator of whether the game is forSale or not. Defauslt is True
    Individulal Game page for creating or editing games
    Allows the entry of all aspects of the game
    Includes options to unlist and delete games 
    """
    def errors(messageList):
        """
        Parameters: messageList - array of errors that were experienced when attemption to save details
        creates error popup to display all error that occured in the creation of a game or saving of game details
        """
        def close():
            """
            Closes error popup
            """
            messageBox.destroy()

        try:
            messageBox.destroy()
        except:pass

        #scale height of error message
        height= 300+len(messageList)*18

        #Create string of all the issues
        messageStr="Issue(s):"
        for n in range(0,len(messageList)):
            messageStr = messageStr+"\n>"+messageList[n]
            
        messageBox = tkinter.Toplevel(window)   

        messageBox.title("Email")
        messageBox.resizable(False, False)
        messageBox.configure(bg=frameColour)

        messageBox.geometry(f"530x{height}")

        center(messageBox)

        frameMain = CustomFrame(master=messageBox,
                                width=500,
                                height=height-30,
                                cornerRadius=0,
                                fgColour=bgColour)
        frameMain.place(x=15,y=15)
        frameTitle = CustomFrame(master=frameMain,
                                   width=460,
                                   height=50,
                                   fgColour=frameColour)
        frameTitle.place(x=20,y=20)
        frameText = CustomFrame(master=frameMain,
                                  width=460,
                                  height=height-140,
                                  fgColour=frameColour)
        frameText.place(x=20,y=90)

        labelTitle = CustomLabel(master=frameTitle,
                                 height=30,
                                   fgColour=frameColour,
                                   text="Game Cannot be Created",
                                   fontSize=20)
        labelTitle.place(x=15,y=5)

        if game != -1:
            labelTitle.configure(text="Game Cannot be Updated")

        labelInfo = tkinter.Label(master=frameText,
                                       fg=textColour,
                                       bg=frameColour,
                                       text=messageStr,
                                      font=(mainFont,16),
                                       anchor="w",
                                      justify=tkinter.LEFT)
        labelInfo.place(x=15,y=15)
        
        buttonClose = CustomButtonDark(master=frameText,
                                     width=50,
                                     height=20,
                                     text="Close",
                                     fgColour=bgColour,
                                       borderWidth=2,
                                       cornerRadius=10,
                                       bgColour=frameColour,
                                     fontSize=16,
                                     command=close)
        buttonClose.place(x=375,y=height-190)
        
    def destroy(event=None):
        """
        Destroys individual game page and returns user to the view games section
        """
        frameIndividual.destroy()
        try:
            messageBox.destroy()
        except:pass

        for count,widget in enumerate(frameMain.winfo_children()):
            if count == 0:
                choice = widget.get()

        #if they just listed the last unlisted game then return them to Most Popular instead of not for sale
        if choice == "Not for Sale":
            getGames = searchTable("gameID","game","WHERE forSale = 0")
            if len(getGames) == 0:
                choice = "Most Popular"
                
        Games(frameMain,frameSide,sortType=choice)

    def delete():
        """
        Delete All Traces of Game
        """
        deleteRecord("game","gameID",str(game))
        deleteRecord("basket","gameID",str(game))
        deleteRecord("wishlist","gameID",str(game))
        deleteRecord("ratings","gameID",str(game))
        deleteRecord("gameOrder","gameID",str(game))
        destroy()

        
    def unlist():
        """
        Remove Game from being viewable by customer.
        Game is removed from wishlists, baskets, browsing and searching
        Its data is kept in its own table, orders and transactions
        """
        unlistGame(str(game))
        deleteRecord("basket","gameID",str(game))
        deleteRecord("wishlist","gameID",str(game))
        
        buttonSave.place_forget()
        buttonRevert.place_forget()
        
        buttonListing.configure(text="Put up for Sale",
                                    command=reinstate)
        
        buttonDelete.place(x=260,y=645)

        #deactivate all widgets except reinstate button
        for count,widget in enumerate(frameIndividual.winfo_children()):
            if count == 2:
                widget.configure(text_color="#C1C0BF")
            if count == 4 or count == 10 or count == 15 or count == 18 or count == 22:
                for subcount,subwidget in enumerate(widget.winfo_children()):
                    if count == 22 and subcount == 0:
                        subwidget.configure(fg="#C1C0BF")
                        subwidget.configure(state="disabled")
                    elif subcount == 0:
                        subwidget.configure(state="disabled")
                    if count != 22:
                        subwidget.configure(text_color="#C1C0BF")
            elif count > 0 and count < 5 or count > 6 and count < 22:
                widget.configure(state="disabled")

        

    def reinstate():
        """
        Puts game back up for sale
        It is then editable, viewable and buyable
        """
        listGame(str(game))
        buttonListing.configure(text="Unlist Game",
                                    command=unlist)

        buttonDelete.place_forget()
        buttonRevert.place(x=25,y=645)
        buttonSave.place(x=195,y=645)

        for count,widget in enumerate(frameIndividual.winfo_children()):
            if count == 2:
                widget.configure(text_color=bgColour)
            if count == 4 or count == 10 or count == 15 or count == 18 or count == 22:
                for subcount,subwidget in enumerate(widget.winfo_children()):
                    if count == 22 and subcount == 0:
                        subwidget.configure(fg=bgColour)
                        subwidget.configure(state="normal")
                    elif subcount == 0:
                        subwidget.configure(state="normal")
                    if count != 22:
                        subwidget.configure(text_color=bgColour)
            elif count > 0 and count < 5 or count > 6 and count < 22:
                widget.configure(state="normal")
                
            
        
    def save(saveType=""):
        """
        Parameters: saveType - the type of saving, eg. "create" or "edit"
        Validates all entries
        If not valid calls errors to display error message
        If valid:
        formats and saves images
        updates game details 
        """
        messageList = []

        title = str.title(entryName.get())
        if title == "":
            messageList.append("Please enter a Title")
        else:
            if not validation.lengthCheck(title,21):
                messageList.append("Title cannot be longer than 20 Characters")


        image = entryImageName.get()

        genre = genreVar.get()
        dev = devVar.get()
                    
        if testing == False:
            getImageNames = searchTable("imageName","game","")
            imageNames=[]
            if game != -1:
                gameImage = (searchTable("imageName","game","WHERE gameID = "+str(game)))[0][0]
                for n in range(0,len(getImageNames)):
                    if getImageNames[n][0].lower() != gameImage.lower():
                        imageNames.append(getImageNames[n][0].lower())
            else:
                for n in range(0,len(getImageNames)):
                    imageNames.append(getImageNames[n][0].lower())
                
            if image != "":
                if image.lower() in imageNames:
                    messageList.append("Cannot use another game's Images")
                else:
                    try:
                        img = Image.open(f"Media/GameImages/{image}.png")
                    except:
                        messageList.append(f"No Image found with name '{image}.png'\n   -Ensure images are saved in 'Media/GameImages'")
            else:
                messageList.append("Please enter an Image Name")
        
            if genre == "Other":
                genre = (entryGenreOther.get()).capitalize()
                if genre == "":
                    messageList.append("Please enter a Genre")
                else:
                    if not validation.lengthCheck(genre,21):
                        messageList.append("Genre cannot be longer than 20 Characters")
            else:
                if genre == "-":
                    messageList.append("Please choose a Genre")
        
            if dev == "Other":
                dev = entryDevOther.get()
                if dev == "":
                    messageList.append("Please enter a Developer")
                else:
                    if not validation.lengthCheck(dev,21):
                        messageList.append("Developer name cannot be longer than 20 Chars")
            else:
                if dev == "-":
                    messageList.append("Please choose a Developer")

                    
        else:
            if image != "":
                try:
                    img = Image.open(f"Media/GameImages/{image}.png")
                except:
                    messageList.append(f"No Image found with name '{image}.png'\n   -Ensure images are saved in 'Media/GameImages'")
            else:
                messageList.append("Please enter an Image Name")
                            
            if genre == "Other":
                genre = (entryGenreOther.get()).capitalize()
                if genre == "":
                    messageList.append("Please enter a Genre")
        
            if dev == "Other":
                dev = (entryDevOther.get()).capitalize()
                if dev == "":
                    messageList.append("Please enter a Genre")
                    
            
            
        todaysDate = datetime.today()
        creationDate = todaysDate.strftime("%d/%m/%Y")


        price = entryPrice.get()
        if price == "":
            messageList.append("Please enter a Price [0.0 if it's free]")
        else:
            if not validation.typeCheck(price,"flt"):
                messageList.append("Price must be a number")

        description = entryDescription.get(1.0,tkinter.END)
        if len(description) == 0:
            description= "This game doesnt have a description :( \n I guess you''ll just have to play it to find out!"
        else:
            validDescription = validation.descriptionCheck(description)
            if validDescription != True:
                messageList.append(validDescription)
   
        multi = multiVar.get()
        if multi == "-":
            messageList.append("Please indicate if the game is multiplayer")
        else:
            if multi == "Yes":
                multi = 1
            else:
                multi = 0

        if messageList != []:
            errors(messageList)
            return

        #format images
        imgBig = Image.open(f"Media/GameImages/{image}Big.png")
        resizedBig = imgBig.resize((450,260))
        cornersBig = curveCorners(resizedBig,"big")
        cornersBig.save(f"Media/GameImages/{image}Big.png")

        img = Image.open(f"Media/GameImages/{image}.png")
        resized = img.resize((140,140))
        corners = curveCorners(resized,"normal")
        corners.save(f"Media/GameImages/{image}.png")

        resizedMini = corners.resize((70,70))
        resizedMini.save(f"Media/GameImages/{image}Mini.png")
            
        moreInfo = moreInfoColour(imgBig)
        

        if saveType == "create":
            insertGame(title, dev, creationDate, genre, price, image, moreInfo, description, multi)
            word="Created"
        else:
            updateGame(game, title, dev, genre, price, image, moreInfo, description, multi)
            word="Saved"

        #flash up word for 0.7 seconds 
        frameDone = CustomFrame(master=frameIndividual,
                                width=170,
                                height=80,
                                cornerRadius=0,
                                borderWidth=4)
        frameDone.place(relx=0.5,rely=0.5,anchor="center")
        frameBorder = CustomFrame(master=frameDone,
                                width=155,
                                height=65,
                                cornerRadius=5,
                                borderWidth=2)
        frameBorder.place(x=7,y=7)
        labelDone = CustomLabel(master=frameDone,
                                 text=word,
                                autoWidth=False,
                                width=120,
                                 height=50,
                                 fontSize=30)
        labelDone.place(relx=0.5,rely=0.5,anchor="center")

        if saveType == "create":
            #clear all entry fields
            entryName.delete(0,tkinter.END)
            entryImageName.delete(0,tkinter.END)
            genreVar.set("-")
            frameGenreOther.place(x=100,y=390)
            entryGenreOther.place_forget()
            entryGenreOther.delete(0,tkinter.END)
            devVar.set("-")
            frameDevOther.place(x=420,y=390)
            entryDevOther.place_forget()
            entryDevOther.delete(0,tkinter.END)
            entryPrice.delete(0,tkinter.END)
            multiVar.set("-")
            entryDescription.delete(1.0,tkinter.END)
            
        window.update()
        
        time.sleep(0.7)
        
        frameDone.destroy()
        window.update()
        
    def fillInfo():
        """
        Fills entry widgets with games information
        """
        info = searchTable("*","game","WHERE gameID = "+str(game))
        entryName.delete(0,tkinter.END)
        entryName.insert(0,str(info[0][1]))
        entryImageName.delete(0,tkinter.END)
        entryImageName.insert(0,str(info[0][7]))
        genreVar.set(info[0][4])
        devVar.set(info[0][2])
        entryPrice.delete(0,tkinter.END)
        price = f"{info[0][5]:.2f}"
        entryPrice.insert(0,price)
        if info[0][10] == 0:
            multiVar.set("No")
        else:
            multiVar.set("Yes")
        entryDescription.delete(1.0,tkinter.END)
        entryDescription.insert(1.0,str(info[0][9]))
        
    def imageName(*args):
        """
        When imageName field is edited
        Checks if any files in the gameImages folder match the entry and if they do displays them on the screen
        If doesnt match, screen displays placeholder images
        """
        global imageBig, image
        imageName = imageVar.get()

        if "big"  in imageName.lower() or "mini"  in imageName.lower():
            imageName=""
            
        try:
            imgBig = Image.open(f"Media/GameImages/{imageName}Big.png")
            image = imgBig.resize((450,260))
            corners = curveCorners(image,"big")
            resized = corners.resize((338,195))
            imageBig = ImageTk.PhotoImage(image=resized,master=window)
            labelImageBig.configure(image=imageBig)
            
        except FileNotFoundError or OSError or PIL.UnidentifiedImageError:
            img = Image.new("RGBA",(331, 188),(0,0,0,0))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle([(7,7),(331,188)],radius=20,outline=(204,252,203),width=3)
            draw.rounded_rectangle([(14,14),(324,181)],radius=13,outline=(204,252,203),width=1)
            fnt = ImageFont.truetype("Font/Saira.ttf", 16)
            draw.text((253,160), "450x260", font=fnt, fill=(204,252,203))

            imageBig = ImageTk.PhotoImage(image=img,master=window)
            labelImageBig.configure(image=imageBig)

        try:
            img = Image.open(f"Media/GameImages/{imageName}.png")
            resized = img.resize((140,140))
            corners = curveCorners(resized,"normal")
            image = ImageTk.PhotoImage(image=resized,master=window)
            labelImageSmall.configure(image=image)
        except FileNotFoundError or OSError or PIL.UnidentifiedImageError:
            img = Image.new("RGBA",(140, 140),(0,0,0,0))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle([(7,7),(133,133)],radius=20,outline=(204,252,203),width=3)
            draw.rounded_rectangle([(14,14),(126,126)],radius=13,outline=(204,252,203),width=1)
            fnt = ImageFont.truetype("Font/Saira.ttf", 16)
            draw.text((60,105), "140x140", font=fnt, fill=(204,252,203))

            image = ImageTk.PhotoImage(image=img,master=window)
            labelImageSmall.configure(image=image)

    def genre(choice):
        """
        Parameters: choice - chosen genre from dropdown
        When a genre is chosen
        Check if genre is "Other" if it is then activates an entry
        If its not it hides this entry
        """
        if choice == "Other":
            frameGenreOther.place_forget()
            entryGenreOther.place(x=100,y=390)
        else:
            frameGenreOther.place(x=100,y=390)
            entryGenreOther.place_forget()

    def dev(choice):
        """
        Parameters: choice - chosen developer from dropdown
        When a developer is chosen
        Check if developer is "Other" if it is then activates an entry
        If its not it hides this entry
        """
        if choice == "Other":
            frameDevOther.place_forget()
            entryDevOther.place(x=420,y=390)
        else:
            frameDevOther.place(x=420,y=390)
            entryDevOther.place_forget()
            
   
    global imageBig, imageSmall

    for count,widget in enumerate(window.winfo_children()):
        if count == 2:
            widget.destroy()
        if isinstance(widget,tkinter.Toplevel):
            widget.destroy()
                
    
    frameIndividual = CustomFrame(master=window,
                                  width=635,
                                  height=700)
    frameIndividual.place(x=345,y=20)

    if game == -1:
            
        for count,widget in enumerate(frameSide.winfo_children()):
            if count < 2:
                widget.configure(border_width=1)
                for button in widget.winfo_children():
                        button.configure(text_color = textColour,
                                            fg_color = frameColour,
                                            bg_color = frameColour)
            if count == 2:
                widget.place(x=25,y=320)
            if count == 3:
                widget.place_forget()
            if count == 4:
                 widget.configure(fg_color=textColour,
                                  text_color=frameColour)
             
        for count,frame in enumerate(frameSide.winfo_children()):
            if count ==1:
                frame.configure(border_width=5)
                for button in frame.winfo_children():
                    if button.text == "Create":
                        button.configure(text_color = frameColour,
                                         fg_color = textColour,
                                        bg_color = textColour)

    getInfo = searchTable("gameID,genre,dev","game","")
    if game == -1:
        #get the last ID and increment by 1
        getID = int(getInfo[-1][0])+1
    else:
        getID = game
        
    numZeros = 4-len(str(getID))
    ID = numZeros*"0"+str(getID)


    getGenres = []
    for n in range(0, len(getInfo)):
        if getInfo[n][1] not in getGenres:
            getGenres.append(getInfo[n][1])
    getGenres = sorted(getGenres)
    getGenres.append("Other")

    getDevelopers = []
    for n in range(0, len(getInfo)):
        if getInfo[n][2] not in getDevelopers:
            getDevelopers.append(getInfo[n][2])

    getDevelopers = sorted(getDevelopers)
    getDevelopers.append("Other")

    frameID = CustomFrame(master=frameIndividual,
                          width=140,
                          height=35,
                          fgColour=bgColour,
                          cornerRadius=10)
    frameID.place(x=435,y=195)
    labelID = CustomLabel(master=frameID,
                          height=25,
                          text=f"ID: {ID}",
                          fgColour = bgColour,
                          fontSize=16)
    labelID.place(relx=0.5,rely=0.5,anchor="center")

    labelName = CustomTkLabelEntry(master=frameIndividual,
                                   text="Title:")
    labelName.place(x=25,y=250)
    entryName = CustomEntry(master=frameIndividual,
                            width=510)
    entryName.place(x=100,y=250)

    labelImageName = CustomTkLabelEntry(master=frameIndividual,
                                        text="Image Name:")
    labelImageName.place(x=25,y=295)
    frameImageName = CustomFrame(master=frameIndividual,
                                 width=450,
                                 height=35,
                                 fgColour=entryColour,
                                 cornerRadius=10)
    frameImageName.place(x=160,y=295)
    imageVar = customtkinter.StringVar()
    imageVar.trace_add('write', partial(imageName))
    entryImageName = CustomEntry(master=frameImageName,
                                 width=393,
                                 height=34,
                                 cornerRadius=0)
    entryImageName.place(x=7,y=0)
    entryImageName.configure(textvariable=imageVar)
    labelImageExtra = CustomLabel(master=frameImageName,
                                  height=31,
                                  text=".png",
                                  fgColour=entryColour,
                                  txtColour=frameColour,
                                  bgColour=entryColour,
                                  fontSize=16)
    labelImageExtra.place(x=405,y=0)

    labelImageBig = customtkinter.CTkLabel(master=frameIndividual,
                                           height=195,
                                           width=338)
    labelImageBig.place(x=60,y=35)

    labelImageSmall = customtkinter.CTkLabel(master=frameIndividual,
                                           height=140,
                                           width=140)
    labelImageSmall.place(x=435,y=35)

    imageName()

    genreVar = customtkinter.StringVar(value="-")
    labelGenre = CustomTkLabelEntry(master=frameIndividual,
                                    text="Genre:")
    labelGenre.place(x=25,y=345)
    dropdownGenre = CustomDropdown(master=frameIndividual,
                                   variable=genreVar,
                                   width=190,
                                   command=genre,
                                   values=getGenres)
    dropdownGenre.place(x=100,y=345)
    
    labelGenreOther = CustomTkLabelEntry(master=frameIndividual,
                                         text="If Other:")
    labelGenreOther.place(x=25,y=390)
    frameGenreOther = CustomFrame(master=frameIndividual,
                                  width=190,
                                  height=35,
                                  cornerRadius=10,
                                  fgColour=bgColour)
    frameGenreOther.place(x=100,y=390)
    entryGenreOther = CustomEntry(master=frameIndividual,
                                  width=190)


    devVar = customtkinter.StringVar(value="-")
    labelDev = CustomTkLabelEntry(master=frameIndividual,
                                    text="Developer:")
    labelDev.place(x=317,y=345)
    dropdownDev = CustomDropdown(master=frameIndividual,
                                   variable=devVar,
                                   width=190,
                                   command=dev,
                                   dynamicResizing=False,
                                   values=getDevelopers)
    dropdownDev.place(x=420,y=345)
    labelDevOther = CustomTkLabelEntry(master=frameIndividual,
                                         text="If Other:")
    labelDevOther.place(x=317,y=390)
    frameDevOther = CustomFrame(master=frameIndividual,
                                  width=190,
                                  height=35,
                                  cornerRadius=10,
                                  fgColour=bgColour)
    frameDevOther.place(x=420,y=390)
    entryDevOther = CustomEntry(master=frameIndividual,
                                  width=190)

    labelPrice = CustomTkLabelEntry(master=frameIndividual,
                                    text="Price:")
    labelPrice.place(x=25,y=445)
    framePrice = CustomFrame(master=frameIndividual,
                             height=35,
                             width=200,
                             fgColour=entryColour,
                             cornerRadius=10)
    framePrice.place(x=90,y=445)
    entryPrice = CustomEntry(master=framePrice,
                             width=175,
                             height=33)
    entryPrice.place(x=13,y=0)
    labelPriceExtra = CustomLabel(master=framePrice,
                                  height=31,
                                  text="£",
                                  fgColour=entryColour,
                                  txtColour=frameColour,
                                  bgColour=entryColour,
                                  fontSize=16)
    labelPriceExtra.place(x=8,y=0)

    multiVar = customtkinter.StringVar(value="-")
    labelMultiplayer = CustomTkLabelEntry(master=frameIndividual,
                                    text="Multiplayer:")
    labelMultiplayer.place(x=317,y=445)
    dropdownMultiplayer = CustomDropdown(master=frameIndividual,
                                       variable=multiVar,
                                       width=175,
                                       values=["Yes","No"])
    dropdownMultiplayer.place(x=435,y=445)

    labelDescription = CustomTkLabelEntry(master=frameIndividual,
                                          text="Description:")
    labelDescription.place(x=25,y=490)
    frameDescription = CustomFrame(master=frameIndividual,
                                   width=585,
                                   height=100,
                                   fgColour=entryColour)
    frameDescription.place(x=25,y=520)
    entryDescription = tkinter.Text(master=frameDescription,
                                    wrap=tkinter.WORD,
                                    width=60,
                                    height=4,
                                    font=(mainFont,14),
                                    bg=entryColour,
                                    fg=frameColour,
                                    relief="flat",
                                    selectbackground=hoverColour)
    entryDescription.place(x=20,y=0)

    if game == -1:
        buttonCreate = CustomButtonDark(master=frameIndividual,
                                      height=35,
                                      width=120,
                                      cornerRadius=10,
                                      text="Create",
                                      fgColour=bgColour,
                                      bgColour=frameColour,
                                      borderWidth=2,
                                      fontSize=14,
                                      command=partial(save,"create"))
        buttonCreate.place(x=490,y=645)
    else:
        fillInfo() 
        buttonBack = CustomHoverButton(master=frameIndividual,
                                             width=45,
                                             height=40,
                                             image1=backIcon,
                                            image2=backHover,
                                            command=destroy)
        buttonBack.place(x=10, y=10)
        buttonRevert = CustomButtonDark(master=frameIndividual,
                                      height=35,
                                      width=160,
                                      cornerRadius=10,
                                      text="Revert Changes",
                                      fgColour=bgColour,
                                      bgColour=frameColour,
                                      borderWidth=2,
                                      fontSize=14,
                                      command=fillInfo)
        buttonSave = CustomButtonDark(master=frameIndividual,
                                      height=35,
                                      width=160,
                                      cornerRadius=10,
                                      text="Save Changes",
                                      fgColour=bgColour,
                                      bgColour=frameColour,
                                      borderWidth=2,
                                      fontSize=14,
                                      command=partial(save,"update"))
        buttonListing = CustomButtonDark(master=frameIndividual,
                                            height=35,
                                            width=160,
                                            cornerRadius=10,
                                            fgColour=warningColour,
                                            hovColour="#EC805F",
                                            text="",
                                            bgColour=frameColour,
                                            borderWidth=2,
                                            fontSize=14)
        buttonListing.place(x=450,y=645)
        buttonDelete = CustomButtonDark(master=frameIndividual,
                                            height=35,
                                            width=180,
                                            cornerRadius=10,
                                            fgColour=warningColour,
                                            hovColour="#EC805F",
                                            text="Permanently Delete",
                                            bgColour=frameColour,
                                            borderWidth=2,
                                            fontSize=14,
                                            command=delete)
        
        if forSale == True:   
            buttonRevert.place(x=25,y=645)
            buttonSave.place(x=195,y=645)
            buttonListing.configure(text="Unlist Game",
                                    command=unlist)
        else:
            #deactivate all widgets except reinstate button
            buttonDelete.place(x=260,y=645)
            for count,widget in enumerate(frameIndividual.winfo_children()):
                if count == 2:
                    widget.configure(text_color="#C1C0BF")
                if count == 4 or count == 10 or count == 15 or count == 18 or count == 22:
                    for subcount,subwidget in enumerate(widget.winfo_children()):
                        if count == 22 and subcount == 0:
                            subwidget.configure(fg="#C1C0BF")
                            subwidget.configure(state="disabled")
                        elif subcount == 0:
                            subwidget.configure(state="disabled")
                        if count != 22:
                            subwidget.configure(text_color="#C1C0BF")
                elif count > 0 and count < 5 or count > 6 and count < 22:
                    widget.configure(state="disabled")
                
            buttonListing.configure(text="Put up for Sale",
                                    command=reinstate)
                                   
                                           

    
def Games(frameMain, frameSide, sortType="Most Popular"):
    """
    Parameters: frameMain - main frame of staff area
                frameSide - side frame of staff area holding the traversal buttons
                sortType - what the games are sorted by, eg. "Most Popular", "Least popular", "Alphabetical" or "Not for Sale". Default if "Most Popular"
    Displays all games with the option to click into, sort or search them
    """
    def fillGameFrames(gamesList,firstGame,lastGame):
        """
        Parameters: gamesList - List of games to be displayed
                    firstGame - index of first game to be displayed in gamesList
                    lastGame - index of last game to be displayed in gamesList
        Fills game frames displaying their image, title, genre and price
        """
        global game1Image, game2Image, game3Image, game4Image, game5Image, game6Image
        
        titles = []
        prices = []
        genres = []
        imageNames = []
        forSales = []

        for n in range(firstGame,(lastGame)):
            currentID = gamesList[n]
            currentRecord = searchTable("title,genre,price,imageName,forSale","game",("WHERE gameID = '" + str(currentID) + "'"))
                
            titles.append(currentRecord[0][0])
            genres.append(currentRecord[0][1])
            currentPrice = currentRecord[0][2]
            if currentPrice == 0.0 or currentPrice == 0.00:
                price="Free"
                prices.append(price)
            else:
                if len(str(currentPrice).rsplit('.')[-1]) == 2:
                    price = str(currentPrice)
                else:
                    price = str(currentPrice)+"0"
                prices.append("£"+price)
            imageNames.append(currentRecord[0][3]+"")

            forSales.append(currentRecord[0][4])

        images = []
        dif = lastGame-firstGame
        if dif > 0:
            game1Image =  openImage("GameImages",imageNames[0],140,140)
            images.append(game1Image)
        if dif > 1:
            game2Image =  openImage("GameImages",imageNames[1],140,140)
            images.append(game2Image)
        if dif > 2:
            game3Image =  openImage("GameImages",imageNames[2],140,140)
            images.append(game3Image)
        if dif > 3:
            game4Image =  openImage("GameImages",imageNames[3],140,140)
            images.append(game4Image)
        if dif > 4:
            game5Image =  openImage("GameImages",imageNames[4],140,140)
            images.append(game5Image)
        if dif > 5:
            game6Image =  openImage("GameImages",imageNames[5],140,140)
            images.append(game6Image)

        for n in range(0,dif):
            #clear frame
            for widget in frames[n].winfo_children():
                widget.destroy()

            thumbnail = customtkinter.CTkLabel(master=frames[n],
                                               width=140,
                                               height=140,
                                               fg_color=frameColour,
                                               corner_radius=0,
                                               image=images[n])
            thumbnail.place(x=15, y=15)

            textGame = titles[n] + "\n" + prices[n] + "\n" + genres[n]

            forSale = True
            if forSales[n] == 0:
                forSale = False
                
            buttonGame = CustomButtonText(master=frames[n],
                                         width=168,
                                         height=70,
                                         cornerRadius=0,
                                         text=textGame,
                                         fontSize=14,
                                         command=partial(individualGame,frameMain,frameSide,gamesList[n+firstGame],forSale))
            buttonGame.place(x=1, y=170)
                
    def nextPage(pageNo,firstItem,lastItem,displayList):
        """
        Parameters: pageNo - page number
                    firstItem - first item that is displayed
                    lastItem - last item that is displayed
                    displayList - list of games to display
        Goes forwards one page
        """
        pageNo += 1

        numGames = len(displayList)
        numPages = numGames//6
        numExtra = numGames%6
        if numExtra != 0:
            numPages += 1
            
        firstItem += 6

        if pageNo == 1:
            buttonBack.configure(state="disabled")
            buttonNext.configure(state="normal")
            frame1.place(x=43,y=85)
            frame2.place(x=232,y=85)
            frame3.place(x=422,y=85)
            frame4.place(x=43,y=365)
            frame5.place(x=232,y=365)
            frame6.place(x=422,y=365)
            
        if pageNo != numPages:
            lastItem += 6
        else:
            if numExtra != 0:
                lastItem += numExtra
                for n in range(numExtra,6):
                    frames[n].place_forget()
            else:
                lastItem += 6
            buttonNext.configure(state="disabled")
        if pageNo == 2:
            buttonBack.configure(state="normal")

        if numGames == 0:
            lastItem = 0

        labelPageNo.configure(text="Page "+str(pageNo))
        buttonNext.configure(command=partial(nextPage,pageNo,firstItem,lastItem,displayList))
        buttonBack.configure(command=partial(backPage,pageNo,firstItem,lastItem,displayList))

        fillGameFrames(displayList,firstItem,lastItem)
            
    def backPage(pageNo,firstItem,lastItem,displayList):
        """
        Parameters: pageNo - page number
                    firstItem - first item that is displayed
                    lastItem - last item that is displayed
                    displayList - list of games to display
        Goes backwards one page
        """
        pageNo -= 1

        numGames = len(displayList)
        numPages = numGames//6
        numExtra = numGames%6
        if numExtra != 0:
            numPages += 1

        firstItem -= 6
        if pageNo != numPages-1:
            lastItem -= 6
        else:
            if numExtra != 0:
                lastItem -= numExtra
                frame2.place(x=232,y=85)
                frame3.place(x=422,y=85)
                frame4.place(x=43,y=365)
                frame5.place(x=232,y=365)
                frame6.place(x=422,y=365)
            else:
                lastItem -= 6
            buttonNext.configure(state="normal")
            
        if pageNo == 1:
            buttonBack.configure(state="disabled")

        labelPageNo.configure(text="Page "+str(pageNo))
        buttonNext.configure(command=partial(nextPage,pageNo,firstItem,lastItem,displayList))
        buttonBack.configure(command=partial(backPage,pageNo,firstItem,lastItem,displayList))

        fillGameFrames(displayList,firstItem,lastItem)

    def search(event=None):
        """
        Searches games for games that match the results
        Orders games by relevence
        Calls fillFrames to display them
        """
        def backSearch():
            """
            Removes extra buttons and labels from searching
            Returns user to normal viewing mode
            """
            searchBar.delete(0,'end')
            frame1.focus_set()
            buttonX.place_forget()
            labelNoResults.place_forget()

            if len(searchResults) != 0:
                sortBy(sortVar.get())


        buttonX.place_forget()
        labelNoResults.place_forget()
            
        searchTerm=(searchBar.get()).lower()
        searchResults=[]
        
        if searchTerm == "":
            return
        
        getGames = searchTable("title,gameID","game","")

        array=[]
        IDs=[]
        for n in range(0,len(getGames)):
            array.append(getGames[n][0])
            IDs.append(getGames[n][1])

        sortMatches = sort.searchSort(array,searchTerm)

        searchResults=[]
        for n in range(0, len(sortMatches)):
            for m in range(0,len(array)):
                if sortMatches[n] == getGames[m][0].lower():
                    searchResults.append(getGames[m][1])
                    
        buttonX.place(x=527,y=36)
        buttonX.configure(command=backSearch)

        if len(searchResults) != 0:
            nextPage(0,-6,0,searchResults)
        else:           
            labelNoResults.place(x=385,y=70)
            labelNoResults.lift()
        
        
    def sortBy(choice):
        """
        Parameters: choice - the option which has been selected, eg."Most Popular", "Least popular", "Alphabetical" or "Not for Sale".
        Sorts the games by the choice and calls fillFrames to display them in the new order
        If searching when called, it will continue the search but now ordered by the choice
        """
        dropdownSortType.set(choice)
        searchBar.delete(0,'end')
        dropdownSortType.focus_set()
        buttonX.place_forget()
        labelNoResults.place_forget()
        labelNone.place_forget()

        for n in range(0,6):
            frames[n].place_forget()

        if choice == "Not for Sale":
            getGames = searchTable("gameID","game","WHERE forSale = 0")
        elif choice != "Alphabetical":
            getGames = searchTable("gameID","game","WHERE forSale = 1 ORDER BY numberBought DESC")
        else:
            getGames = searchTable("gameID","game","WHERE forSale = 1 ORDER BY title ASC")

        games = []
        for n in range(0, len(getGames)):
            games.append(getGames[n][0])
        if choice == "Least Popular":
            games.reverse()

        if len(games) > 0:
            nextPage(0,-6,0,games)
        else:
           labelNone.place(relx=0.5,y=310,anchor="center")

            
        
    #clear mainFrame
    for widget in frameMain.winfo_children():
        widget.destroy()

    for count,widget in enumerate(window.winfo_children()):
        if count == 2:
            widget.destroy()
        if isinstance(widget,tkinter.Toplevel):
            widget.destroy()

    #reset all buttons
    for count,widget in enumerate(frameSide.winfo_children()):
        if count < 2:
            widget.configure(border_width=1)
            for button in widget.winfo_children():
                    button.configure(text_color = textColour,
                                        fg_color = frameColour,
                                        bg_color = frameColour)
        if count == 2:
            widget.place(x=25,y=320)
        if count == 3:
            widget.place_forget()
        if count == 4:
             widget.configure(fg_color=textColour,
                              text_color=frameColour)

    #configure the pressed button and frame to be highlighted              
    for count,frame in enumerate(frameSide.winfo_children()):
        if count ==1:
            frame.configure(border_width=5)
            for button in frame.winfo_children():
                if button.text == "Edit":
                    button.configure(text_color = frameColour,
                                     fg_color = textColour,
                                     bg_color = textColour)

                    

    sortVar = customtkinter.StringVar(value="Most Popular")
    values = ["Most Popular","Least Popular","Alphabetical"]
    
    getGames = searchTable("gameID","game","WHERE forSale = 0")
    if len(getGames) != 0:
        values.append("Not for Sale")

        
    dropdownSortType = customtkinter.CTkOptionMenu(master=frameMain,
                                                   width=195,
                                                   height=40,
                                                   corner_radius=0,
                                                   fg_color=frameColour,
                                                   button_color=frameColour,
                                                   button_hover_color=hoverColour,
                                                   dropdown_color=bgColour,
                                                   dropdown_hover_color=hoverColour,
                                                   dropdown_text_color=textColour,
                                                   text_color=textColour,
                                                   text_font=(mainFont,20),
                                                   variable=sortVar,
                                                   dynamic_resizing=False,
                                                   command=sortBy,
                                                   values=values)
    dropdownSortType.place(x=42,y=35)                                              

    searchBar = CustomEntry(master=frameMain,
                            width=180,
                            height=35,
                            cornerRadius=20,
                            borderWidth=1,
                            fontSize=14,
                            placeholderText="Search for a Game")
    searchBar.place(x=375, y=35)
    buttonSearch = customtkinter.CTkButton(master=frameMain,
                                           width=40,
                                           height=40,
                                           text="",
                                           corner_radius=30,
                                           hover_color=hoverColour,
                                           fg_color=frameColour,
                                           image=searchIcon,
                                           command=search)
    buttonSearch.place(x=555, y=33)
    searchBar.bind("<Return>",search)

    buttonX = CustomButtonText(master=frameMain,
                           height=5,
                           width=1,
                           text="x",
                           fontSize=14,
                           txtColour=frameColour,
                           fgColour=entryColour,
                           cornerRadius=0)
    labelNoResults =  CustomButtonDark(master=frameMain,
                                        width=160,
                                        height=25,
                                        text="No Results",
                                        fontSize=14,
                                        borderWidth=1,
                                        hoverEnabled=False,
                                        fgColour=bgColour,
                                        cornerRadius=0)


    getGames = searchTable("gameID","game","WHERE forSale = 1 ORDER BY numberBought DESC")
    games = []
    for n in range(0, len(getGames)):
        games.append(getGames[n][0])
        
    #create frames but don't place
    frame1 = CustomFrame(master=frameMain,
                         width=170,
                         height=260,
                         borderWidth=1)
    frame2 = CustomFrame(master=frameMain,
                         width=170,
                         height=260,
                         borderWidth=1)
    frame3 = CustomFrame(master=frameMain,
                         width=170,
                         height=260,
                         borderWidth=1)
    frame4 = CustomFrame(master=frameMain,
                         width=170,
                         height=260,
                         borderWidth=1)
    frame5 = CustomFrame(master=frameMain,
                         width=170,
                         height=260,
                         borderWidth=1)
    frame6 = CustomFrame(master=frameMain,
                         width=170,
                         height=260,
                         borderWidth=1)
    
    labelNone = CustomLabel(master=frameMain,
                                height=60,
                                text="No Games for Sale Yet!\n Try creating one",
                                fontSize=20)
    
    frames=[frame1,frame2,frame3,frame4,frame5,frame6]

    #if enough games place frames
    if len(games) != 0:
        frame1.place(x=42,y=85)
        frame2.place(x=232,y=85)
        frame3.place(x=422,y=85)
        frame4.place(x=42,y=365)
        frame5.place(x=232,y=365)
        frame6.place(x=422,y=365)
        frames=[frame1,frame2,frame3,frame4,frame5,frame6]

    else:
        #if not place none label
        labelNone.place(relx=0.5,y=310,anchor="center")


    #navigation
    pageNo = 0
    firstGame=-6
    lastGame=0 
    labelPageNo = CustomLabel(master=frameMain,
                                    autoWidth=False,
                                    width=50,
                                    height=15,
                                    text="Page "+str(pageNo),
                                    fontSize=14)
    buttonBack =  CustomButtonText(master=frameMain,
                                     width=20,
                                     height=15,
                                     text="<",
                                     state="disabled",
                                     cornerRadius=0,
                                     fontSize=14,
                                     hoverEnabled=False,
                                     command=partial(backPage,pageNo,firstGame,lastGame,games))
    buttonNext = CustomButtonText(master=frameMain,
                                     width=20,
                                     height=15,
                                     text=">",
                                     cornerRadius=0,
                                     fontSize=14,
                                     hoverEnabled=False,
                                     command=partial(nextPage,pageNo,firstGame,lastGame,games))
    if len(games) > 6:
        labelPageNo.place(x=290,y=655)
        buttonBack.place(x=265, y=653)
        buttonNext.place(x=345, y=653)

    if len(games) > 0:
        sortBy(sortType)


        

    
    
def StaffMain(view):
    """
    Parameters: view - access level of user
    Creates the main page for Staff depending on their access level
    Displays Buttons in side frame and a logo in main frame
    """
    def fillSide(frame,title,buttons):
        """
        Parameters: frame - frame to fill
                    title - title for frame
                    buttons - an array of text for the button
        Fills a subframe of the side frame with its title and asscoiated buttons
        """
        labelTitle = CustomLabel(master=frame,
                                 height=25,
                                 text=title,
                                 fontSize=18)
        labelTitle.place(relx=0.5,y=20,anchor="center")
        if title == "Analytics":
            num=3
        if title == "Profiles" or title == "Games":
            num=2
        for n in range(0,num):
            ycoord = 35+32*n
            button = CustomButtonText(master=frame,
                                      height=20,
                                      width=30,
                                      text=buttons[n],
                                      fontSize=16,
                                      cornerRadius=0)
            button.place(x=15,y=ycoord)
            if title == "Analytics":
                button.configure(command=partial(Analytics,frameMain,frameSide,buttons[n]))
            if title == "Profiles":
                button.configure(command=partial(Profiles,view,frameMain,frameSide,buttons[n]))
            if title == "Games":
                if n == 0:
                    button.configure(command=partial(Games,frameMain,frameSide))
                if n == 1:
                    button.configure(command=partial(individualGame,frameMain,frameSide))
        
    for widget in window.winfo_children():
        widget.destroy()

    frameMain = CustomFrame(master=window,
                            width=635,
                            height=700)
    frameMain.place(x=345,y=20)
    labelLogo = customtkinter.CTkLabel(master=frameMain,
                                       image=logoBig,
                                       text="",
                                       width=370,
                                       height=340)
    labelLogo.place(x=125,y=160)
    
    frameSide = CustomFrame(master=window,
                            width=305,
                            height=700)
    frameSide.place(x=20, y=20)

    frameAnalytics = CustomFrame(master=frameSide,
                         width=255,
                         height=140,
                         borderWidth=1)
    frameAnalytics.place(x=25,y=25)
    fillSide(frameAnalytics,"Analytics",["Games","Genres","Developers"])

    if view == "Upper" or view == "Admin":
        frameProfiles = CustomFrame(master=frameSide,
                             width=255,
                             height=115,
                             borderWidth=1)
        frameProfiles.place(x=25,y=185)
        fillSide(frameProfiles,"Profiles",["Customers","Staff"])
        
        buttonOrdersUnpressed = CustomButtonDark(master=frameSide,
                                     width=252,
                                     height=58,
                                     text="View Orders",
                                     bgColour=frameColour,
                                     borderWidth=1,
                                     command=partial(StaffOrders,frameMain,frameSide))
        buttonOrdersUnpressed.place(x=25,y=320)
        buttonOrdersPressed = CustomButtonDark(master=frameSide,
                                     width=252,
                                     height=58,
                                     text="View Orders",
                                     bgColour=frameColour,
                                     borderWidth=5,
                                     command=partial(StaffOrders,frameMain,frameSide))

        buttonEmail = CustomButtonLight(master=frameSide,
                                     width=255,
                                     height=65,
                                     text="Email Customers",
                                     borderWidth=5,
                                     command=partial(MassEmail,frameMain,frameSide)) 
        buttonEmail.place(x=25,y=525)

    if view == "Lower":
        frameGames = CustomFrame(master=frameSide,
                             width=255,
                             height=115,
                             borderWidth=1)
        frameGames.place(x=25,y=185)
        fillSide(frameGames,"Games",["Edit","Create"])

        #Allow the widgets to be the same spacing as Upper so it is easier to manipulate the frames and buttons
        placeHolder1 = CustomButtonText(frameSide,1,1,"")
        placeHolder2 = CustomButtonText(frameSide,1,1,"")
        placeHolder3 = CustomButtonText(frameSide,1,1,"")
        
    buttonLogOut = CustomButtonLight(master=frameSide,
                                     width=255,
                                     height=65,
                                     text="Log Out",
                                     command=partial(LogOut,"staff"))
    buttonLogOut.place(x=25,y=610)
                            
    





###Customer User View

    

def emailLoading(transactionID,event=None):
    """
    Parameters: transactionID - ID of transaction to be emailed
    Creates loading screen for sending email
    Automaticlaly moves on to a confirmation or an error message
    """
    def sendReceipt():
        """
        Send the user's receipt to their email
        """
        try:
            getUserEmail = searchTable("emailAddress","customer","WHERE customerID = "+currentUserID)
            userEmail = getUserEmail[0][0]
            sendEmail(transactionID,currentUserID,userEmail)

            labelTitle.configure(text="Done!",width=20)

            for widget in frameInput.winfo_children():
                widget.configure(text="Email Sent")
                widget.place(relx=0.5,rely=0.45,anchor="center")
                
            buttonClose = CustomButtonDark(master=frameInput,
                                           height=20,
                                           width=50,
                                           text="Close",
                                           borderWidth=2,
                                           bgColour=frameColour,
                                           command=partial(cancel))
            buttonClose.place(x=380,y=115)
            
        except:
            def closeTopError():
                """
                Closes TopLevel Error
                """
                for count,widget in enumerate(window.winfo_children()):
                    if isinstance(widget,tkinter.Toplevel):
                        widget.destroy()
                        
            popup.destroy()
            pauseVar = tkinter.StringVar()
            topError = errorMessage(window,"Email could not send",
                                    "Possible reasons include:\n> No Internet Connection\n> Email blocked by System Settings\n> Your Email Address is invalid\n> Email request timed out\n\nWe apologise for any inconvenience this may\ncause you.",
                                    command=closeTopError)
            window.wait_variable(pauseVar) 
        
    def cancel():
        """
        Destroys TopLevel popup
        """
        popup.destroy()

    popup = tkinter.Toplevel(window)   
    popup.geometry("560x330")
    popup.title("Email")
    popup.resizable(False, False)
    popup.configure(bg=frameColour)

    center(popup)

    framePopup = CustomFrame(master=popup,
                             width=530,
                             height=300,
                             fgColour=bgColour,
                             cornerRadius=0)
    framePopup.place(x=15, y=15)

    frameTitle = CustomFrame(master=framePopup,
                            width=490,
                            height=70)
    frameTitle.place(x=20, y=20)

    labelLogoSmall = customtkinter.CTkLabel(master=frameTitle,
                                            width=120,
                                            height=70,
                                            image=logoLong2)
    labelLogoSmall.place(x=355, y=0)

    labelTitle = CustomSubtitle(master=frameTitle,
                                text="Sending...")
    labelTitle.place(x=20, y=10)

    frameInput = CustomFrame(master=framePopup,
                            width=490,
                            height=170)
    frameInput.place(x=20, y=110)
    
    labelSubtitle = CustomLabel(master=frameInput,
                                    height=60,
                                    autoWidth=False,
                                    width=490,
                                   text="Sending...\nPlease Wait",
                                   fontSize=20)
    labelSubtitle.place(relx=0.5,rely=0.5,anchor="center")

    popup.after(1000,sendReceipt)
  

def Home(buttonHome,event=None):
    """
    Parameter: buttonHome - home button pressed to call this function
    Destroys home button and returns user to BrowseMain
    """
    buttonHome.destroy()
    BrowseMain()

    

def back(event=None,buttonBack="",page="",lastPage=""):
    """
    parameters: buttonBack - button that was pressed to call this function
                page - page user was on. Default = ""
                lastPage - page the user was on before the last. Default = ""
    Transports the user back a page
    Typically to browseMain
    If coming from gamePage, user returns to page they were on before
    If coming from reviews, user returns to past orders
    """

    #remove back button and line
    buttonBack.destroy()
    for count,widget in enumerate(frameTop.winfo_children()):
        if count == 4:
            widget.place_forget()
        
    if page == "GamePage":
        widgets=[]
        for widget in window.winfo_children():
            widgets.append(widget)
            
        widgets[2].destroy()
        try: widgets[3].destroy()
        except: pass
        try:
            widgets[4].destroy()
            widgets[5].destroy()
        except: pass

        widgets2=[]
        for widget in frameTop.winfo_children():
            widgets2.append(widget)

        widgets2[3].toggleState=1
        widgets2[3].configure(image=profileIcon)
            
        if lastPage == "wishlist":
            widgets2[7].place(x=770, y=13)#back
            widgets2[5].place_forget()#wishlist
        if lastPage == "basket":
            widgets2[7].place(x=835, y=14)#home
            widgets2[6].place_forget()#basket
            
    elif page == "review":
        PastOrders()
        
    else:
        for count,widget in enumerate(window.winfo_children()):
            if count != 0:
                widget.destroy()
                
        BrowseMain()

def MoreDetails(transactionID):
    """
    Parameters: transactionID - ID of the transaction the user wants more details on
    Displays a version of the users reciept on screen and gives them the option to have it emailed to them.
    """
    def fillReceipt(pageNo):
        """
        Parameters: pageNo - receipt page number
        fill receipt with the game names and prices from the order depending on the page number
        """
        #Clear receipt
        for count,widget in enumerate(frameReceipt.winfo_children()):
            if count > 4:
                widget.destroy()

        #Get games from titlesSplit array and fill frame
        n=pageNo-1
        for m in range(0,len(titlesSplit[n])):
            ycoord=9+30*m
            labelTitle = CustomLabel(master=frameReceipt,
                                     autoWidth=False,
                                     width=180,
                                     height=30,
                                     text=titlesSplit[n][m],
                                     fontSize=16,
                                     anchor="w")
            labelTitle.place(x=45,y=ycoord)
            labelPrice = CustomLabel(master=frameReceipt,
                                     autoWidth=False,
                                     width=170,
                                     height=30,
                                     text=pricesSplit[n][m],
                                     fontSize=16,
                                     anchor="e")
            labelPrice.place(x=725,y=ycoord)


    def backPage(pageNo):
        """
        Parameters: pageNo - receipt page number
        Goes backwards one page on the receipt
        """
        pageNo -= 1
        buttonNext.configure(command=partial(nextPage,pageNo))
        buttonBack.configure(command=partial(backPage,pageNo))

        labelPageNo.configure(text="Page "+str(pageNo))

        if pageNo == 1:
            buttonBack.configure(state="disabled")

        buttonNext.configure(state="normal")
        fillReceipt(pageNo)
        
    def nextPage(pageNo):
        """
        Parameters: pageNo - receipt page number
        Goes forwards one page on the receipt
        """
        pageNo += 1
        buttonNext.configure(command=partial(nextPage,pageNo))
        buttonBack.configure(command=partial(backPage,pageNo))

        labelPageNo.configure(text="Page "+str(pageNo))

        if pageNo == numPages:
            buttonNext.configure(state="disabled")

        if pageNo == 2:
            buttonBack.configure(state="normal")
            
        fillReceipt(pageNo)


        
    global bigGoatImage

    #clear screen
    for count,widget in enumerate(window.winfo_children()):
        if count != 0:
            widget.destroy()#All but top frame

    for count,widget in enumerate(frameTop.winfo_children()):
        if count == 4:
            widget.place(x=890, y=18, relwidth=0.0005, relheight=0.6)#Place Line
            
    buttonBack = CustomHoverButton(master=frameTop,
                                         width=45,
                                         height=40,
                                         image1=backIcon,
                                        image2=backHover)
    buttonBack.place(x=825, y=20)
    buttonBack.command=partial(back,buttonBack=buttonBack,page="review")
    buttonBack.bind("<Button-1>",buttonBack.command)

    
    transactionDate = searchTable("total,date","gameTransaction","WHERE transactionID = "+str(transactionID))
    customerInfo = searchTable("customerForename,customerSurname,cardNumber","customer","WHERE customerID = "+str(currentUserID))

    numZeros = 4-len(str(transactionID))
    orderNum = "Order Number:      "+"0"*numZeros+ str(transactionID)
    
    date = str(transactionDate[0][1])
    
    total=transactionDate[0][0]
    if total == 0.0:
        totalStr="Total: £0.00 GBP"
    else:
        if len(str(total).rsplit('.')[-1]) == 2:
            totalStr = "Total: £"+str(total)+" GBP"
        elif len(str(total).rsplit('.')[-1]) == 1:
            totalStr = "Total: £"+str(total)+"0 GBP"
        if len(str(total).rsplit('.')[-1]) > 2:
            numExtra = len(str(total).rsplit('.')[-1]) - 2
            totalStr = "Total: £"+str(total)[:-numExtra]+" GBP"
            
    name = customerInfo[0][0].capitalize()+" "+customerInfo[0][1].capitalize()
    
    numZeros2 = 4-len(str(currentUserID))
    userID = "User ID:      "+"0"*numZeros2+ str(currentUserID)

    
    frameOrderNum = CustomFrame(master=window,
                                width=315,
                                height=55,
                                cornerRadius=10)
    frameOrderNum.place(x=25,y=115)
    labelOrderNum = CustomLabel(master=frameOrderNum,
                                height=50,
                                text=orderNum,
                                fontSize=22)
    labelOrderNum.place(x=20,y=2)
    
    frameDate = CustomFrame(master=window,
                                width=250,
                                height=55,
                                cornerRadius=10)
    frameDate.place(x=25,y=175)
    labelDate = CustomLabel(master=frameDate,
                                height=50,
                                text=date,
                                fontSize=20)
    labelDate.place(x=20,y=2)


    frameSize=len(name)*17
    xcoord=970-frameSize
    frameName = CustomFrame(master=window,
                                width=frameSize,
                                height=55,
                                cornerRadius=10)
    frameName.place(x=xcoord,y=115)
    labelName = CustomLabel(master=frameName,
                                height=50,
                                text=name,
                                fontSize=22)
    labelName.place(relx=0.5,rely=0.5,anchor="center")
    
    frameUserID = CustomFrame(master=window,
                                width=210,
                                height=55,
                                cornerRadius=10)
    frameUserID.place(x=760,y=175)
    labelUserID = CustomLabel(master=frameUserID,
                                height=50,
                                text=userID,
                                fontSize=20)
    labelUserID.place(x=20,y=2)
    
    frameDetails = CustomFrame(master=window,
                                width=950,
                                height=380)
    frameDetails.place(x=25,y=255)

    
    labelTitle = CustomLabel(master=frameDetails,
                                height=40,
                                text="Title",
                                fontSize=20)
    labelTitle.place(x=45,y=5)
    labelSubtotal = CustomLabel(master=frameDetails,
                                height=40,
                                text="Subtotal",
                                fontSize=20)
    labelSubtotal.place(x=805,y=5)
    
    line1 = ttk.Separator(frameDetails, orient="horizontal")
    line1.place(x=45, y=45, relwidth=0.8947, relheight=0.00005)


    frameReceipt = CustomFrame(master=frameDetails,
                               width=950,
                               height=278,
                               cornerRadius=0)
    frameReceipt.place(x=0,y=46)
    bigGoatImage = customtkinter.CTkLabel(master=frameReceipt,
                                          width=170,
                                          height=210,
                                          text="",
                                          bg_color=frameColour,
                                          image=bigGoat)
    bigGoatImage.place(x=430,y=19)
    
    line2 = ttk.Separator(frameDetails, orient="horizontal")
    line2.place(x=45, y=325, relwidth=0.8947, relheight=0.00005)
    
    labelTotal = CustomLabel(master=frameDetails,
                             autoWidth=False,
                             width=120,
                             anchor="west",
                                height=40,
                                text=totalStr,
                                fontSize=18)
    labelTotal.place(x=730,y=330)


    
    buttonEmail = CustomButtonDark(master=window,
                                   width=210,
                                   height=60,
                                   text="Send to Email",
                                   fontSize=20,
                                   command=partial(emailLoading,transactionID))
    buttonEmail.place(x=760,y=655)

    #get games details  
    gameDetails = searchTable("gameID","gameOrder","WHERE transactionID = "+str(transactionID))
    
    titles=[]
    prices=[]
    numGames=len(gameDetails)
    numPages = numGames//8
    numExtra = numGames%8
    pageNo=0
    
    if numExtra!=0:
        numPages+=1
    
    for n in range(0,numGames):
            currentRecord=searchTable("title,price","game","WHERE gameID = "+str(gameDetails[n][0]))
            titles.append(currentRecord[0][0])
            getPrice=currentRecord[0][1]
            if getPrice == 0.0 or getPrice == 0.00:
                currentPrice="£0.00"
            else:
                if len(str(getPrice).rsplit('.')[-1]) == 2:
                    currentPrice = "£"+str(getPrice)
                else:
                    currentPrice = "£"+str(getPrice)+"0"
            prices.append(currentPrice)


    #split the titles list into groups of 8, as 8 can fit on one page
    start = 0
    end = len(titles)
    step = 8
    titlesSplit=[]
    pricesSplit=[]
    for i in range(start, end, step):
        x = i
        titlesSplit.append(titles[x:x+step])
        pricesSplit.append(prices[x:x+step])

    if numPages > 1:
        labelPageNo = CustomLabel(master=frameReceipt,
                                  autoWidth=False,
                                  width=50,
                                  height=15,
                                  text="Page "+str(pageNo),
                                  fontSize=14)
        labelPageNo.place(x=470,y=249)
        buttonBack =  CustomButtonText(master=frameReceipt,
                                     width=20,
                                     height=15,
                                     text="<",
                                     state="disabled",
                                     cornerRadius=0,
                                       fontSize=14,
                                     hoverEnabled=False,
                                       command=partial(nextPage,pageNo))
        buttonBack.place(x=445, y=248)
        buttonNext = CustomButtonText(master=frameReceipt,
                                     width=20,
                                     height=15,
                                     text=">",
                                     cornerRadius=0,
                                      fontSize=14,
                                     hoverEnabled=False,
                                      command=partial(backPage,pageNo))
        buttonNext.place(x=530, y=249)
        nextPage(pageNo)
    else:
        fillReceipt(1)
        
    

def Review(transactionID):
    """
    Parameters: transactionID - ID of the transaction that the user is rating the games from
    Creates review page
    This page displays all games in the transaction along with a star system to rate them easily
    """
    def rateGame(button,message):
        """
        Parameters: button - rating button that was clicked
                    message - text underneath rating button
        Removes, adds or overwrites game rating from user
        Configures button and message to match
        """
        if button.game != -1:
            if button.toggleState==1:
                try:
                    deleteRecord("ratings","gameID",str(button.game)," AND userID = "+str(currentUserID))
                except: pass
                insertRating(currentUserID,button.game,button.rating)


                if button.rating == 1:
                    message.configure(text="(1 Star)")
                if button.rating == 2:
                    message.configure(text="(2 Stars)")
                if button.rating == 3:
                    message.configure(text="(3 Stars)")
                if button.rating == 4:
                    message.configure(text="(4 Stars)")
                if button.rating == 5:
                    message.configure(text="(5 Stars)")
                                       
            else:
                deleteRecord("ratings","gameID",str(button.game)," AND userID = "+str(currentUserID))
                message.configure(text="")
            
        
    def fillReviewFrames(lastGame,firstGame):
        """
        Parameters: lastGame - last game to be displayed
                    firstGame - first game to be displayed
        Fills the current frames on the screen with the desired game image and name
        If a rating exists the star widget will be configured to match the existing rating
        """
        global gameImage1, gameImage2,gameImage3,gameImage4
        
        dif=lastGame-firstGame

        titles =[]
        imageNames=[]
        IDs=[]
        for n in range(firstGame, lastGame):
            currentID = games[n]
            currentRecord = searchTable("title,imageName","game",("WHERE gameID = '" + str(currentID) + "'"))
            titles.append(currentRecord[0][0])
            imageNames.append(currentRecord[0][1]+"")
            IDs.append(currentID)

        images=[]
        if dif > 0:
            gameImage1 =  openImage("GameImages",imageNames[0],140,140)
            images.append(gameImage1)
        if dif > 1:
            gameImage2 =  openImage("GameImages",imageNames[1],140,140)
            images.append(gameImage2)
        if dif > 2:
            gameImage3 =  openImage("GameImages",imageNames[2],140,140)
            images.append(gameImage3)
        if dif > 3:
            gameImage4 =  openImage("GameImages",imageNames[3],140,140)
            images.append(gameImage4)

        for n in range(0,dif):
            for count,widget in enumerate(frames[n].winfo_children()):
                if count > 1:
                    widget.destroy()

            thumbnail = customtkinter.CTkLabel(master=frames[n],
                                               width=140,
                                               height=140,
                                               fg_color=frameColour,
                                               corner_radius=0,
                                               image=images[n])
            thumbnail.place(x=35, y=20)
            title = CustomLabel(master=frames[n],
                                autoWidth=False,
                                width=185,
                                height=30,
                                text=titles[n],
                                fontSize=16)
            title.place(x=15,y=160)

            stars = ratings[n]
            stars.game = IDs[n]
            message=messages[n]
            
            rating = searchTable("rating","ratings","WHERE gameID = "+str(IDs[n])+" AND userID = "+str(currentUserID))

            #set stars to 0 then configure to correct rating
            stars.clickFunction(num=0,setUp=True)
            stars.toggleState=-1
            
            if len(rating) == 1:
                stars.clickFunction(num=rating[0][0],setUp=True)
                message.configure(text=f"({rating[0][0]} Star)")
            else:
                message.configure(text="")

            
    #Clear Screen        
    for count,widget in enumerate(window.winfo_children()):
        if count != 0:
            widget.destroy()#All but top frame

    
    for count,widget in enumerate(frameTop.winfo_children()):
        if count == 4:
            widget.place(x=890, y=18, relwidth=0.0005, relheight=0.6)#Place line
            
    buttonBack = CustomHoverButton(master=frameTop,
                                         width=45,
                                         height=40,
                                         image1=backIcon,
                                        image2=backHover)
    buttonBack.place(x=825, y=20)
    buttonBack.command=partial(back,buttonBack=buttonBack,page="review")
    buttonBack.bind("<Button-1>",buttonBack.command)
            
    frameReviews = CustomFrame(master=window,
                               width=1000,
                               height=650,
                               fgColour=bgColour)
    frameReviews.place(x=0,y=90)    

    frameTitle = CustomFrame(master=frameReviews,
                             width=150,
                             height=60)
    frameTitle.place(x=15,y=20)
    labelTitle = CustomLabel(master=frameTitle,
                            height=60,
                            text="Review",
                            fontSize=26)
    labelTitle.place(relx=0.5, rely=0.5, anchor="center")


    getGames = searchTable("gameID","gameOrder","WHERE transactionID = "+str(transactionID))
    games=[]
    for n in range(0,len(getGames)):
        games.append(getGames[n][0])
    games.reverse()
    
    numGames = len(getGames)
    numPages = numGames//4
    numExtra = numGames%4
    firstGame = -4
    lastGame = 0
    page=0

    #create frames, stars and messages
    frame1 = CustomFrame(master=frameReviews,
                         width=470,
                         height=200)
    frame1.place(x=20,y=100)
    ratings1 = customRatingSystem(master=frame1,
                                  image1=hollowStar,
                                  image2=hoverStar,
                                  image3=fullStar)
    ratings1.place(x=225,y=70)
    message1 = CustomLabel(master=frame1,
                           autoWidth = False,
                           width=180,
                           height=35,
                           fontSize=18,
                            text="")
    message1.place(x=225,y=110)
    ratings1.command=partial(rateGame,ratings1,message1)
                   
    
    frame2 = CustomFrame(master=frameReviews,
                         width=470,
                         height=200)
    frame2.place(x=510,y=100)
    ratings2 = customRatingSystem(frame2,
                                  hollowStar,
                                  hoverStar,
                                  fullStar)
    ratings2.place(x=225,y=70)
    message2 = CustomLabel(master=frame2,
                           autoWidth = False,
                           width=180,
                           height=35,
                           fontSize=18,
                            text="")
    message2.place(x=225,y=110)
    ratings2.command=partial(rateGame,ratings2,message2)
    
    
    frame3 = CustomFrame(master=frameReviews,
                         width=470,
                         height=200)
    frame3.place(x=20,y=320)
    ratings3 = customRatingSystem(frame3,
                                  hollowStar,
                                  hoverStar,
                                  fullStar)
    ratings3.place(x=225,y=70)
    message3 = CustomLabel(master=frame3,
                           autoWidth = False,
                           width=180,
                           height=35,
                           fontSize=18,
                            text="")
    message3.place(x=225,y=110)
    ratings3.command=partial(rateGame,ratings3,message3)
    
    frame4 = CustomFrame(master=frameReviews,
                         width=470,
                         height=200)
    frame4.place(x=510,y=320)    
    ratings4 = customRatingSystem(frame4,
                                  hollowStar,
                                  hoverStar,
                                  fullStar)
    ratings4.place(x=225,y=70)
    message4 = CustomLabel(master=frame4,
                           autoWidth = False,
                           width=180,
                           height=35,
                           fontSize=18,
                            text="")
    message4.place(x=225,y=110)
    ratings4.command=partial(rateGame,ratings4,message4)

    frames=[frame1,frame2,frame3,frame4]
    ratings=[ratings1,ratings2,ratings3,ratings4]
    messages=[message1,message2,message3,message4]

    #navigation
    def backPage(page,firstGame,lastGame):
        """
        Parameters: page - the current page number
                    firstGame - the index of the firstGame being displayed
                    lastGame - the index of the lastGame being displayed
        Moves backwards one page
        """
        page -= 1
        
        numGames = len(getGames)
        numPages = numGames//4
        numExtra = numGames%4
        
        if numExtra != 0:
            numPages += 1
            
        if page == numPages-1:
            frame2.place(x=510,y=100)#places all frame back
            frame3.place(x=20,y=320)
            frame4.place(x=510,y=320)
            firstGame -= 4
            if lastGame%4 != 0:
                lastGame = lastGame-(lastGame%4)
            else:
                lastGame -= 4
        else:
            firstGame -= 4
            lastGame -= 4

        pageNo = "Page", page
        if page == (numPages - 1):
            buttonNextPage.place(x=130, y=2)
        
        if page == 1:
            buttonBackPage.place_forget()


        buttonBackPage.configure(command=partial(backPage,page,firstGame,lastGame))
        buttonNextPage.configure(command=partial(nextPage,page,firstGame,lastGame))

        labelPageNo.configure(text=pageNo)
        fillReviewFrames(lastGame,firstGame)

    def nextPage(page,firstGame,lastGame):
        """
        Parameters: page - the current page number
                    firstGame - the index of the first game being displayed
                    lastGame - the index of the last game being displayed
        Moves forewards one page
        """
        page += 1

        numGames = len(getGames)
        numPages = numGames//4
        numExtra = numGames%4
        
        if numExtra != 0:
            numPages += 1
            
        if page == numPages:
            buttonNextPage.place_forget()
            firstGame += 4
            lastGame = numGames
            for n in range(lastGame%4,4):#hides all frames not needed
                frames[n].place_forget()
        else:
            firstGame += 4
            lastGame += 4

        pageNo = "Page", page
        if page == 2:
            buttonBackPage.place(x=15, y=2)


        buttonNextPage.configure(command=partial(nextPage,page,firstGame,lastGame))
        buttonBackPage.configure(command=partial(backPage,page,firstGame,lastGame))
        
        labelPageNo.configure(text=pageNo)
        fillReviewFrames(lastGame,firstGame)

    if len(frames) != 0:
        framePages = CustomFrame(master=frameReviews,
                                width=160,
                                height=30, 
                                cornerRadius=10)
        framePages.place(x=420, y=550)

        pageNo = "Page", page

        labelPageNo = CustomLabel(master=framePages,
                                 height=20,
                                 text=pageNo,
                                 fontSize=12)
        labelPageNo.place(x=55, y=4)

        buttonNextPage = CustomButtonText(framePages,
                                        width=20,
                                        height=20,
                                        cornerRadius=0,
                                        text=">",
                                        fontSize=12,
                                        command=partial(nextPage,page,firstGame,lastGame))

        buttonBackPage = CustomButtonText(framePages,
                                    width=20,
                                    height=20,
                                    cornerRadius=0,
                                    text="<",
                                    fontSize=12,
                                    command=partial(backPage,page,firstGame,lastGame))
        if numPages != 0:
            buttonNextPage.place(x=130, y=2)
        
        nextPage(page,firstGame,lastGame)
        


            
def PastOrders():
    """
    Creates past orders screen
    This displays the users past transactions with the options to view more details or rate the games
    """
    def fillOrderFrames(lastTransaction,firstTransaction):
        """
        Parameters: lastTransaction - last transaction to be displayed
                    firstTransaction - first transaction to be displayed
        Fills order frames with Transaction information and Buttons for Ratings or viewing more details
        """
        global gameImage1, gameImage2
        
        def backImage(gameNum,frameNo):
            """
            Parameters: gameNum - Index of game whose image is the current image
                        frameNo - number of frame the button pressed was is
            Changes the picture on the frame back one
            """
            global image1, image0
            gameNum -= 1
            buttons[frameNo][1].configure(command=partial(nextImage,gameNum,frameNo))
            buttons[frameNo][0].configure(command=partial(backImage,gameNum,frameNo))
            
            if frameNo == 1:
                image1 =  openImage("GameImages",imageNames[1][gameNum],140,140)
                thumbnails[frameNo].configure(image=image1)
            if frameNo == 0:
                image0 =  openImage("GameImages",imageNames[0][gameNum],140,140)
                thumbnails[frameNo].configure(image=image0)

            if frameNo == 1:
                if imageNames[1][gameNum] == firstImages[1]:
                    buttons[frameNo][0].configure(state="disabled")
            
            if frameNo == 0:
                if imageNames[0][gameNum] == firstImages[0]:
                    buttons[frameNo][0].configure(state="disabled")

            buttons[frameNo][1].configure(state="normal")
            
        def nextImage(gameNum,frameNo):
            """
            Parameters: gameNum - Index of game whose image is the current image
                        frameNo - number of frame the button pressed was is
            Changes the picture on the frame forward one
            """
            global image1, image0
            gameNum += 1
            buttons[frameNo][1].configure(command=partial(nextImage,gameNum,frameNo))
            buttons[frameNo][0].configure(command=partial(backImage,gameNum,frameNo))
            
            if frameNo == 1:
                image1 =  openImage("GameImages",imageNames[1][gameNum],140,140)
                thumbnails[frameNo].configure(image=image1)
            if frameNo == 0:
                image0 =  openImage("GameImages",imageNames[0][gameNum],140,140)
                thumbnails[frameNo].configure(image=image0)
                
            if frameNo == 1:
                if imageNames[1][gameNum] == lastImages[1]:
                    buttons[frameNo][1].configure(state="disabled")
                    
            if frameNo == 0:
                if imageNames[0][gameNum] == lastImages[0]:
                   buttons[frameNo][1].configure(state="disabled")

            buttons[frameNo][0].configure(state="normal")

        
        dif=lastTransaction-firstTransaction
        print(lastTransaction,firstTransaction)
        imageNames=[[],[]]
        for n in range(firstTransaction,lastTransaction):
            currentTransaction = getTransactions[n][0]
            orderInfo = searchTable("gameID","gameOrder","WHERE transactionID = "+str(currentTransaction))
            orderInfo.reverse()
                                 
            for m in range(0,len(orderInfo)):
                getImageName =searchTable("imageName","game","WHERE gameID = "+str(orderInfo[m][0]))
                imageName = getImageName[0][0]+""
                imageNames[(n%2)].append(imageName)

        images=[]
        firstImages=[]
        lastImages=[]
        if dif > 0:
            gameImage1 =  openImage("GameImages",imageNames[0][0],140,140)
            images.append(gameImage1)
            firstImages.append(imageNames[0][0])
            lastImages.append(imageNames[0][-1])
        if dif > 1:
            gameImage2 =  openImage("GameImages",imageNames[1][0],140,140)
            images.append(gameImage2)
            firstImages.append(imageNames[1][0])
            lastImages.append(imageNames[1][-1])
        
        for n in range(firstTransaction,lastTransaction):
            for count,widget in enumerate(frames[n%2].winfo_children()):
                if count > 2:
                    widget.destroy()
            
            buttons[n%2][1].configure(state="normal")
            buttons[n%2][0].configure(state="disabled")
            
            currentTransaction = getTransactions[n][0]
            transactionInfo = searchTable("date,total","gameTransaction","WHERE transactionID = "+str(currentTransaction))

            numZeros = 4-len(str(currentTransaction))
            orderNumber = "0"*numZeros + str(currentTransaction)

            total = transactionInfo[0][1]
            if total == 0.0:
                totalStr="£00.00"
            else:
                if len(str(total).rsplit('.')[-1]) == 2:
                    totalStr = "£"+str(total)
                elif len(str(total).rsplit('.')[-1]) == 1:
                    totalStr = "£"+str(total)+"0"
                if len(str(total).rsplit('.')[-1]) > 2:
                    numExtra = len(str(total).rsplit('.')[-1]) - 2
                    totalStr = "£"+str(total)[:-numExtra]

            textInfo = transactionInfo[0][0]+"\nOrder Number: "+orderNumber+"\n\nTotal: "+totalStr+" GBP"
            labelDate = CustomLabel(master=frames[n%2],
                                    autoWidth=False,
                                    width=275,
                                    height=30,
                                    text=transactionInfo[0][0],
                                    fontSize=20,
                                    anchor="w")
            labelDate.place(x=280,y=30)
            labelOrderNo = CustomLabel(master=frames[n%2],
                                    autoWidth=False,
                                    width=275,
                                    height=30,
                                    text="Order Number: "+orderNumber,
                                    fontSize=20,
                                    anchor="w")
            labelOrderNo.place(x=280,y=60)
            labelTotal = CustomLabel(master=frames[n%2],
                                    autoWidth=False,
                                    width=275,
                                    height=30,
                                    text="Total: "+totalStr+" GBP",
                                    fontSize=20,
                                    anchor="w")
            labelTotal.place(x=280,y=150)

            buttonMoreDetails = CustomButtonLight(master=frames[n%2],
                                                  width=240,
                                                  height=70,
                                                  text="More Details",
                                                  command=partial(MoreDetails,currentTransaction),
                                                  fontSize=18)
            buttonMoreDetails.place(x=635,y=30)

            buttonReview = CustomButtonLight(master=frames[n%2],
                                                  width=240,
                                                  height=70,
                                                  text="Review Games",
                                                  command=partial(Review,currentTransaction),
                                                  fontSize=18)
            buttonReview.place(x=635,y=110)

            orderInfo = searchTable("gameID","gameOrder","WHERE transactionID = "+str(currentTransaction))
            numGames = 0
            for m in range(0,len(orderInfo)):
                numGames+=1

            if numGames == 1:
                numGamesTxt = str(numGames) + " game"
            else:
                numGamesTxt = str(numGames) + " games"
                
            labelNum = CustomLabel(master=frames[n%2],
                                   autoWidth=False,
                                   width=140,
                                    height=30,
                                    text=numGamesTxt,
                                    fontSize=18)
            labelNum.place(x=50,y=170)

            thumbnails[n%2].configure(image=images[n%2])
            thumbnails[n%2].place(x=50, y=30)

            if numGames != 1:
                buttons[n%2][0].configure(command=partial(backImage,0,n%2))
                buttons[n%2][0].place(x=25, y=80)
                buttons[n%2][1].configure(command=partial(nextImage,0,n%2))
                buttons[n%2][1].place(x=195, y=80)
            else:
                buttons[n%2][0].place_forget()
                buttons[n%2][1].place_forget()
                
            

            
    #Clear screen    
    for count,widget in enumerate(frameTop.winfo_children()):
        if count !=0:
            widget.place_forget()#All but logo

    for count,widget in enumerate(window.winfo_children()):
        if count != 0:
            widget.destroy()#All but top frame
            
    frameOrders = CustomFrame(master=window,
                              width=1000,
                              height=650,
                              fgColour=bgColour)
    frameOrders.place(x=0, y=90)

    buttonHome = CustomHoverButton(master=frameTop,
                                         width=50,
                                         height=50,
                                         image1=homeIcon,
                                         image2=homeHover)
    buttonHome.place(x=905, y=13)
    buttonHome.command=partial(Home,buttonHome)
    buttonHome.bind("<Button-1>", buttonHome.command)

    frameTitle = CustomFrame(master=frameOrders,
                             width=220,
                             height=60)
    frameTitle.place(x=50,y=20)
    labelTitle = CustomLabel(master=frameTitle,
                            height=60,
                            text="Past Orders",
                            fontSize=26)
    labelTitle.place(relx=0.5, rely=0.5, anchor="center")

    getTransactions = searchTable("transactionID","gameTransaction","WHERE userID = '"+currentUserID+"'")
    getTransactions.reverse()
    
    numTransactions = len(getTransactions)
    numPages = numTransactions//2
    numExtra = numTransactions%2
    firstTransaction = -2
    lastTransaction = 0
    page=0

    #create frames, thumbnails and buttons
    frames=[]
    frame1 = CustomFrame(master=frameOrders,
                             width=900,
                             height=220)
    frame1.place(x=50,y=100)
    if numTransactions == 0:
        labelNone = CustomLabel(master=frame1,
                                height=60,
                                text="No Past Orders\nBetter get shopping!",
                                fontSize=26)
        labelNone.place(relx=0.5,rely=0.5,anchor="center")
                                
    else:
        thumbnail1 = customtkinter.CTkLabel(master=frame1,
                                               width=140,
                                               height=140,
                                               fg_color=frameColour,
                                               corner_radius=0)
        buttonBackImage1 = CustomButtonText(master=frame1,
                                             width=20,
                                             height=1,
                                             text="<",
                                             state="disabled",
                                             cornerRadius=0,
                                             hoverEnabled=False)
        buttonNextImage1 = CustomButtonText(master=frame1,
                                             width=20,
                                             height=1,
                                             text=">",
                                             cornerRadius=0,
                                             hoverEnabled=False)
        
        frame2 = CustomFrame(master=frameOrders,
                             width=900,
                             height=220)
        frame2.place(x=50,y=330)
        thumbnail2 = customtkinter.CTkLabel(master=frame2,
                                               width=140,
                                               height=140,
                                               fg_color=frameColour,
                                               corner_radius=0)
        buttonBackImage2 = CustomButtonText(master=frame2,
                                             width=20,
                                             height=1,
                                             text="<",
                                             state="disabled",
                                             cornerRadius=0,
                                             hoverEnabled=False)
        buttonNextImage2 = CustomButtonText(master=frame2,
                                             width=20,
                                             height=1,
                                             text=">",
                                             cornerRadius=0,
                                             hoverEnabled=False)
        
        frames.append(frame1)
        frames.append(frame2)
        thumbnails=[thumbnail1,thumbnail2]
        buttons=[[buttonBackImage1,buttonNextImage1],[buttonBackImage2,buttonNextImage2]]
        
    #navigation
    def backPage(page,firstTransaction,lastTransaction):
        """
        Parameters: page - the current page number
                    firstTransaction - the index of the first transaction being displayed
                    lastTransaction - the index of the last transaction being displayed
        Moves backwards one page
        """
        page -= 1
        
        numTransactions = len(getTransactions)
        numPages = numTransactions//2
        numExtra = numTransactions%2
        
        if numExtra != 0:
            numPages += 1
            
        if page == numPages-1:
            frame2.place(x=50,y=330)
            firstTransaction -= 2
            if lastTransaction%2 != 0:
                lastTransaction = lastTransaction-(lastTransaction%2)
            else:
                lastTransaction -= 2
        else:
            firstTransaction -= 2
            lastTransaction -= 2

        pageNo = "Page", page
        if page == (numPages - 1):
            buttonNextPage.place(x=130, y=2)
        
        if page == 1:
            buttonBackPage.place_forget()


        buttonBackPage.configure(command=partial(backPage,page,firstTransaction,lastTransaction))
        buttonNextPage.configure(command=partial(nextPage,page,firstTransaction,lastTransaction))

        labelPageNo.configure(text=pageNo)
        fillOrderFrames(lastTransaction,firstTransaction)

    def nextPage(page,firstTransaction,lastTransaction):
        """
        Parameters: page - the current page number
                    firstTransaction - the index of the first transaction being displayed
                    lastTransaction - the index of the last transaction being displayed
        Moves forewards one page
        """
        page += 1

        numTransactions = len(getTransactions)
        print(getTransactions,numTransactions)
        numPages = numTransactions//2
        numExtra = numTransactions%2
        
        if numExtra != 0:
            numPages += 1

        print(page,numPages)
        if page == numPages:
            buttonNextPage.place_forget()
            firstTransaction += 2
            lastTransaction = numTransactions
            if lastTransaction-firstTransaction == 0:
                frame1.place_forget()
                frame2.place_forget()
            if lastTransaction-firstTransaction == 1:
                frame2.place_forget()
        else:
            firstTransaction += 2
            lastTransaction += 2

        pageNo = "Page", page
        if page == 2:
            buttonBackPage.place(x=15, y=2)


        buttonNextPage.configure(command=partial(nextPage,page,firstTransaction,lastTransaction))
        buttonBackPage.configure(command=partial(backPage,page,firstTransaction,lastTransaction))
        
        labelPageNo.configure(text=pageNo)
        print(firstTransaction,lastTransaction)
        fillOrderFrames(lastTransaction,firstTransaction)

    if len(frames) != 0:
        framePages = CustomFrame(master=frameOrders,
                                width=160,
                                height=30, 
                                cornerRadius=10)
        framePages.place(x=420, y=580)

        pageNo = "Page", page

        labelPageNo = CustomLabel(master=framePages,
                                 height=20,
                                 text=pageNo,
                                 fontSize=12)
        labelPageNo.place(x=55, y=4)

        buttonNextPage = CustomButtonText(framePages,
                                        width=20,
                                        height=20,
                                        cornerRadius=0,
                                        text=">",
                                        fontSize=12,
                                        command=partial(nextPage,page,firstTransaction,lastTransaction))

        buttonBackPage = CustomButtonText(framePages,
                                    width=20,
                                    height=20,
                                    cornerRadius=0,
                                    text="<",
                                    fontSize=12,
                                    command=partial(backPage,page,firstTransaction,lastTransaction))
        if numPages != 0:
            buttonNextPage.place(x=130, y=2)
        
        nextPage(page,firstTransaction,lastTransaction)


    
def LogOut(area="customer"):
    """
    Parameters: area - Which area of login you would like to return to, eg. "customer" or "staff". Default is "customer"
    clears screen and returns the user to the login screen
    """
    for widget in window.winfo_children():
        widget.destroy()
    Login(area)     


def DeleteUser():
    """
    Creates a TopLevel and asks for the users passsword to check the user is correct
    Then deletes user account
    """
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """
        frameMessage = CustomFrame(frameEntry,
                                 width=315,
                                 height=45,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=45, y=178)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=True,
                                   height=30,
                                   text=message,
                                   fontSize=16,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")


        
    def UserDeleted(entryPassword,delete):
        """
        Parameters: entryPassword - password entry widget
                    delete - delete TopLevel
        Checks that password is correct and then delete user and any records associated so as not to leave any orphan foreign keys
        Returns user to login page
        """
        getPassword = searchTable ("password","customer",("WHERE customerID = "+ currentUserID))
        password = getPassword[0][0]
        password = encryption.XOR(password)
        
        if entryPassword.get() == "":
            messageBox("Please enter your password")
            return
        if entryPassword.get() != password:
            messageBox("Password Incorrect")
            return
        
        delete.destroy()
        deleteRecord("customer", "customerID", str(currentUserID))
        transactions=searchTable("transactionID","gameTransaction","WHERE userID = "+str(currentUserID))
        deleteRecord("gameTransaction", "userID", str(currentUserID))
        for n in range(0,len(transactions)):
            deleteRecord("gameOrder", "transactionID", str(transactions[n][0]))
            
        deleteRecord("wishlist", "userID", str(currentUserID))
        deleteRecord("basket", "userID", str(currentUserID))
        deleteRecord("ratings", "userID", str(currentUserID))
        
        for widget in window.winfo_children():
            widget.destroy()
        Login()

    delete = tkinter.Toplevel(window)
    delete.geometry("600x450")
    delete.title("Security Check")
    delete.resizable(False, False)
    delete.configure(bg=frameColour)

    center(delete)

    frameDelete = CustomFrame(master=delete,
                             width=530,
                             height=380,
                             fgColour=bgColour,
                             cornerRadius=0)
    frameDelete.place(x=35, y=35)

    frameTitle = CustomFrame(master=frameDelete,
                            width=490,
                            height=70)
    frameTitle.place(x=20, y=20)

    labelLogoSmall = customtkinter.CTkLabel(master=frameTitle,
                                            width=120,
                                            height=70,
                                            image=logoLong2)
    labelLogoSmall.place(x=355, y=0)

    labelTitle = CustomSubtitle(master=frameTitle,
                                text="Security Check")
    labelTitle.place(x=20, y=10)

    frameEntry = CustomFrame(master=frameDelete,
                            width=490,
                            height=240)
    frameEntry.place(x=20, y=110)

    labelSubtitle = CustomSubtitle(master=frameEntry,
                                   text="Are You Sure?",
                                   fontSize=22)
    labelSubtitle.place(x=145, y=20)

    labelPassword = CustomTkLabelEntry(master=frameEntry,
                                        text="Enter your password to delete account:")
    labelPassword.place(x=45, y=85)

    entryPassword = CustomEntry(master=frameEntry,
                               width=400,
                               show="●",
                               fontSize=12)
    entryPassword.place(x=45, y=120)

    if testing == True:
        entryPassword.insert(0,testPassword)

    buttonDelete = CustomButtonDark(master=frameEntry,
                                   width=100,
                                   height=50,
                                   fgColour=warningColour,
                                   bgColour=frameColour,
                                   borderWidth=2,
                                   text="Delete",
                                   hovColour="#EC805F",
                                   command=partial(UserDeleted,entryPassword,delete))

    buttonDelete.place(x=370, y=175)


def ChangePassword():
    """
    Creates Toplevel to allow user to enter their current password and a new password to change their password.
    """
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """
        labelNew.place(x=50,y=95)
        entryNew.place(x=45,y=125)

        if message == "New Password too weak\n [must contain a capital, number and special character]":
            message = "New Password too weak [must contain\n a capital, number and special character]"
        fontSize = 16
        if len(message) > 50:
            fontSize=12
        
        frameMessage = CustomFrame(frameEntry,
                                 width=315,
                                 height=45,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=45, y=180)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=False,
                                   height=30,
                                   width=300,
                                   text=message,
                                   fontSize=fontSize,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")
        
    def updatePassword(event=None):
        """
        Checks current password is correct and new password is valid
        If not valid or matching calls messageBox to display appropriate error
        If valid saves details and returns to original profile page
        """
        getCurrentPassword = searchTable ("password","customer",("WHERE customerID = "+ currentUserID))
        currentPassword = getCurrentPassword[0][0]
        currentPassword = encryption.XOR(currentPassword)
        
        if entryCurrent.get() == "":
            messageBox("Please enter your current password")
            return
        if entryCurrent.get() != currentPassword:
            messageBox("Current password incorrect")
            return

        if testing == False:
            validPassword = validation.passwordCheck(entryNew.get(),"New")
            if validPassword != True:
                messageBox(validPassword)
                return
        else:
            if entryNew.get() == "":
                messageBox("Please enter a password")
                return
        
        newPassword = entryNew.get()
        newPassword = encryption.XOR(newPassword)
        updateCustomerPassword(currentUserID,newPassword)
        changePassword.destroy()

        
    changePassword = tkinter.Toplevel(window)
    changePassword.geometry("600x450")
    changePassword.title("Security Check")
    changePassword.resizable(False, False)
    changePassword.configure(bg=frameColour)

    center(changePassword)

    framePassword = CustomFrame(master=changePassword,
                               width=530,
                               height=380,
                               fgColour=bgColour,
                               cornerRadius=0)
    framePassword.place(x=35, y=35)

    ######
    frameTitle = CustomFrame(master=framePassword,
                            width=490,
                            height=70)
    frameTitle.place(x=20, y=20)

    labelLogoSmall = customtkinter.CTkLabel(master=frameTitle,
                                            width=120,
                                            height=70,
                                            image=logoLong2)
    labelLogoSmall.place(x=355, y=0)

    labelTitle = CustomSubtitle(master=frameTitle,
                                text="Change Password")
    labelTitle.place(x=20, y=10)

    frameEntry = CustomFrame(master=framePassword,
                            width=490,
                            height=240)
    frameEntry.place(x=20, y=110)

    labelCurrent = CustomTkLabelEntry(master=frameEntry,
                                  text="Current Password:")
    labelCurrent.place(x=50, y=25)
    entryCurrent = CustomEntry(master=frameEntry,
                                width=400)
    entryCurrent.place(x=45, y=55)
    entryCurrent.bind("<Return>",updatePassword)

    if testing == True:
        entryCurrent.insert(0,testPassword)

    labelNew = CustomTkLabelEntry(master=frameEntry,
                                  text="New Password:")
    labelNew.place(x=52, y=100)
    entryNew = CustomEntry(master=frameEntry,
                          width=400)
    entryNew.place(x=45, y=130)
    entryNew.bind("<Return>",updatePassword)

    buttonDone = CustomButtonLight(master=frameEntry,
                                 width=90,
                                 height=35,
                                 text="Done",
                                 fontSize=16,
                                 command=updatePassword)
    buttonDone.place(x=380, y=185)


def UserEdit(security,frameProfile,frameUserInfo):
    """"
    Parameters: security - Security popup
                frameProfile - main profile frame
                frameUserInfo - Frame containing users personal information
    Changes card details labels to entries, autofilled with the information, that are now editable
    Edit/add button changed to save button
    """
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """

        fontSize=16
        if len(message) > 40:
            fontSize=13

        if message == "Forename cannot include numbers or special characters":
            message = "Invalid Forename"

        if message == "Surname cannot include numbers or special characters":
            message = "Invalid Surname"
            
        frameMessage = CustomFrame(frameUserEdit,
                                 width=315,
                                 height=45,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=10, y=465)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=False,
                                   width=300,
                                   height=30,
                                   text=message,
                                   fontSize=fontSize,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")
        
    def updateUserInfo():
        """
        Takes entries and validates them
        If not valid calls messageBox to display appropriate error
        If valid saves details and returns to original profile page
        """
        newEmail = str(entryEmail.get()).lower()
        validEmail = validation.emailCheck(newEmail)
        if validEmail != True:
            messageBox(validEmail)
            return

        newForename = str.lower(entryForename.get())
        newSurname = str.lower(entrySurname.get())
        newDOB = entryDOB.get()
        newFavGenre = genreVar.get()
        
        if testing == False:
            validForename = validation.nameCheck(newForename,"forename")
            if validForename != True:
                messageBox(validForename)
                return
            
            validSurname = validation.nameCheck(newSurname,"surname")
            if validSurname != True:
                messageBox(validSurname)
                return
            
            validDOB = validation.dateCheck(newDOB)
            if validDOB != True:
                messageBox(validDOB)
                return
            
            if newFavGenre == "-":
                messageBox("Please select your favourite genre")
                return

        updateCustomerUser(userID, newEmail, newForename, newSurname, newDOB, newFavGenre)
        Profile()
        
    security.destroy()
    frameUserInfo.destroy()
    frameUserEdit = CustomFrame(master=frameProfile,
                               width=475,
                               height=524)
    frameUserEdit.place(x=15, y=85)

    #get user info
    recordFound = searchTable("*","customer",("WHERE customerID = "+str(currentUserID)))
    emailAddress = recordFound[0][4]
    userInfoList = [recordFound[0][0], emailAddress, str.capitalize(recordFound[0][1]),
                    str.capitalize(recordFound[0][2]), recordFound[0][3], recordFound[0][6]]

    email = userInfoList[1]
    numZeros = 4-int(len(str(recordFound[0][0])))
    userID = "0"*numZeros+str(recordFound[0][0])
    forename = userInfoList[2]
    surname = userInfoList[3]
    DOB = userInfoList[4]
    favourite = userInfoList[5]
    userTitleList = ["UserID:", "Email Address:", "Forename:", "Surname:", "Date of Birth:", "Favourite Genre:"]
    for n in range(0, len(userTitleList)):
        ycoord = 10 + 75 * n
        labelTitle = CustomTkLabelEntry(master=frameUserEdit,
                                       text=userTitleList[n])
        labelTitle.place(x=20, y=ycoord)

    labelBox = customtkinter.CTkLabel(master=frameUserEdit,
                                      width=450,
                                      height=35,
                                      corner_radius=10,
                                      fg_color=bgColour,
                                      text="")
    labelBox.place(x=12, y=40)

    labelID = tkinter.Label(master=frameUserEdit,
                            width=30,
                            height=1,
                            bg=bgColour,
                            text=userID,
                            fg=entryColour,
                            font=(mainFont, 16),
                            anchor="w")
    labelID.place(x=20, y=40)

    #create entries and fill info
    entryEmail = CustomEntry(master=frameUserEdit,
                               width=450)
    entryEmail.place(x=12, y=115)
    entryEmail.insert(-1, email)
    entryForename = CustomEntry(master=frameUserEdit,
                                width=450)
    entryForename.place(x=12, y=190)
    entryForename.insert(-1, forename)
    entrySurname = CustomEntry(master=frameUserEdit,
                                width=450)
    entrySurname.place(x=12, y=265)
    entrySurname.insert(-1, surname)
    entryDOB = CustomEntry(master=frameUserEdit,
                                width=450)
    entryDOB.place(x=12, y=340)
    entryDOB.insert(-1, DOB)

    genreVar = customtkinter.StringVar(value=favourite)
    genresSearch = searchTable("genre","game","ORDER BY genre ASC")
    genres = []
    for i in range(0,len(genresSearch)):
        if genresSearch[i][0] not in genres:
            genres.append(genresSearch[i][0])
            
    dropdownGenre = CustomDropdown(master=frameUserEdit,
                                    variable=genreVar,
                                   values=genres)
    dropdownGenre.place(x=12, y=415)

    buttonUserDone = CustomButtonDark(master=frameUserEdit,
                                     width=100,
                                     height=35,
                                     fgColour=bgColour,
                                     bgColour=frameColour,
                                     text="Done",
                                     fontSize=16,
                                     borderWidth=1,
                                     command=updateUserInfo)
    buttonUserDone.place(x=355, y=470)

    
def CardEdit(security,frameProfile,lastFrame):
    """
    Parameters: security - Security popup
                frameProfile - main profile frame
                lastFrame - Frame containing users card details. Either frameCardInfo or frameCardReveal
    Changes card details labels to entries, autofilled with the information, that are now editable
    Edit/add button changed to save button
    """
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """

        if message == "Card Number must be of format NNNN NNNN NNNN NNNN":
            message = "Card Number must be\n of format NNNN NNNN NNNN NNNN"
            
        fontsize=16
        if len(message) > 35:
            fontsize=14
        if len(message) > 45:
            fontsize=12
            
        frameMessage = CustomFrame(frameCardEdit,
                                 width=315,
                                 height=45,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=10, y=170)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=False,
                                   width=300,
                                   height=30,
                                   text=message,
                                   fontSize=fontsize,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")
        
    def updateCardInfo():
        """
        Takes entries and validates them
        If not valid calls messageBox to display appropriate error
        If valid saves details and returns to original profile page
        """
        newCardNo = str(entryCardNo.get())
        newExpiry = str(entryExpiry.get())
        
        if testing == False:
            validCard = validation.cardCheck(newCardNo)
            if validCard != True:
                messageBox(validCard)
                return
            
            validExpiry = validation.dateCheck(newExpiry,"expiry")
            if validExpiry != True:
                messageBox(validExpiry)
                return
            

        newCardNo = encryption.XOR(newCardNo)
        newExpiry = encryption.XOR(newExpiry)
        
        userID = currentUserID
        
        updateCustomerCard(userID, newCardNo, newExpiry)
        Profile()
        
    security.destroy()

    recordFound = searchTable("*","customer",("WHERE customerID = "+str(currentUserID)))
    
    lastFrame.destroy()

    frameCardEdit = CustomFrame(master=frameProfile,
                               width=475,
                               height=230)
    frameCardEdit.place(x=510, y=85)

    #get card info
    cardNo = encryption.XOR(recordFound[0][7])
    expiry = encryption.XOR(recordFound[0][8])
    cardInfoList = [cardNo, expiry]
    cardTitleList = ["Card Number:", "Expiry Date:"]
    for n in range(0, len(cardTitleList)):
        ycoord = 10 + 75 * n
        labelTitle = CustomTkLabelEntry(master=frameCardEdit,
                                       text=cardTitleList[n])
        labelTitle.place(x=20, y=ycoord)

    entryCardNo = CustomEntry(master=frameCardEdit,
                             width=450)
    entryCardNo.place(x=12, y=40)
    entryExpiry = CustomEntry(master=frameCardEdit,
                             width=450)
    entryExpiry.place(x=12, y=115)

    #if present autofill details
    if cardNo != None:
        entryCardNo.insert(-1, cardNo)
        entryExpiry.insert(-1, expiry)

    buttonCardDone = CustomButtonDark(master=frameCardEdit,
                                     width=100,
                                     height=35,
                                     fgColour=bgColour,
                                     bgColour=frameColour,
                                     text="Done",
                                     fontSize=16,
                                     borderWidth=1,
                                     command=updateCardInfo)
    buttonCardDone.place(x=355, y=175)

def CardReveal(security,frameProfile,frameCardInfo):
    """
    Parameters: security - Security popup
                frameProfile - Frame containing users personal information
                frameCardInfo - Frame containing users card details
    Reveals users card information by configuring the text to be the unhidden version.
    """
    security.destroy()
    frameCardInfo.destroy()

    recordFound = searchTable("*","customer",("WHERE customerID = "+str(currentUserID)))
    frameCardRevealed = CustomFrame(master=frameProfile,
                                       width=475,
                                       height=230)
    frameCardRevealed.place(x=510, y=85)
    cardNo = encryption.XOR(recordFound[0][7])
    expiry = encryption.XOR(recordFound[0][8])
    cardInfoList = [cardNo, expiry]
    cardTitleList = ["Card Number:", "Expiry Date:"]
    for n in range(0, len(cardTitleList)):
        ycoord = 10 + 75 * n
        labelTitle = CustomTkLabelEntry(master=frameCardRevealed,
                                       text=cardTitleList[n])
        labelTitle.place(x=20, y=ycoord)

        ycoord = 40 + 75 * n
        labelBox = customtkinter.CTkLabel(master=frameCardRevealed,
                                          width=450,
                                          height=35,
                                          corner_radius=10,
                                          fg_color=bgColour,
                                          text="")
        labelBox.place(x=12, y=ycoord)

        labelInfo = tkinter.Label(master=frameCardRevealed,
                                  width=30,
                                  height=1,
                                  bg=bgColour,
                                  text=cardInfoList[n],
                                  fg=entryColour,
                                  font=(mainFont, 16),
                                  anchor="w")
        labelInfo.place(x=20, y=ycoord)

    #Card edit no longer requires security check
    buttonCardEdit = CustomButtonLight(master=frameCardRevealed,
                                     width=100,
                                     height=35,
                                     text="Edit",
                                     fontSize=16,
                                     command=partial(CardEdit,security,frameProfile,frameCardRevealed))
    buttonCardEdit.place(x=355, y=175)


def Security(function,frameProfile,frameCardInfo,frameUserInfo):
    """
    Parameters: function - string describing function to be called after security check
                frameProfile - main frame from profile page
                frameCardInfo - frame for card information
                frameUserInfo - frame for personal information
    Creates a Toplevel popup prompting the user for their password to ensure no accidental or malicious changes are made
    """
    
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """
        frameMessage = CustomFrame(frameEntry,
                                 width=315,
                                 height=45,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=45, y=175)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=True,
                                   height=30,
                                   text=message,
                                   fontSize=16,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")
        
    def ProfileFunctions(event=None):
        """
        Checks password is valid
        If not it calls messageBox to outrput an error
        If it is valid it calls the function
        """
        password = searchTable ("password","customer",("WHERE customerID = "+ currentUserID))
        password = encryption.XOR(password[0][0])
        
        if entryPassword.get() == "":
            messageBox("Please enter your password")
            return
        
        if entryPassword.get() != password:
            messageBox("Password Incorrect")
            return
        
        if function == "UserEdit":
            UserEdit(security,frameProfile,frameUserInfo)
        elif function == "CardEdit":
            CardEdit(security,frameProfile,frameCardInfo)
        elif function == "CardReveal":
            CardReveal(security,frameProfile,frameCardInfo)

        
    global entryPassword, security
    security = tkinter.Toplevel(window)
    security.geometry("600x450")
    security.title("Security Check")
    security.resizable(False, False)
    security.configure(bg=frameColour)

    center(security)

    frameSecurity = CustomFrame(master=security,
                               width=530,
                               height=380,
                               fgColour=bgColour,
                               cornerRadius=0)
    frameSecurity.place(x=35, y=35)

    frameTitle = CustomFrame(master=frameSecurity,
                                width=490,
                                height=70)
    frameTitle.place(x=20, y=20)

    labelLogoSmall = customtkinter.CTkLabel(master=frameTitle,
                                            width=120,
                                            height=70,
                                            image=logoLong2)
    labelLogoSmall.place(x=355, y=0)

    labelTitle = CustomSubtitle(master=frameTitle,
                                text="Security Check")
    labelTitle.place(x=20, y=10)

    frameEntry = CustomFrame(master=frameSecurity,
                            width=490,
                            height=240)
    frameEntry.place(x=20, y=110)

    labelSubtitle = CustomSubtitle(master=frameEntry,
                                   text="We need to make sure it's you!",
                                   fontSize=22)
    labelSubtitle.place(x=25, y=20)

    labelPassword = CustomTkLabelEntry(master=frameEntry,
                                       text="Please enter your password:")
    labelPassword.place(x=50, y=85)

    entryPassword = CustomEntry(master=frameEntry,
                               width=400,
                               show="●",
                               fontSize=12)
    entryPassword.place(x=45, y=120)

    if testing == True:
        entryPassword.insert(0,testPassword)

    buttonDone = CustomButtonLight(master=frameEntry,
                                 width=90,
                                 height=35,
                                 text="Done",
                                 fontSize=16,
                                 command=ProfileFunctions)
    buttonDone.place(x=380, y=185)
    entryPassword.bind("<Return>",ProfileFunctions)


def Profile(event=None):
    """
    Creates Profile Page
    Consists of two sections displaying Personal Information and Card Details
    These sections have an edit button each and the Card Details have a reveal button
    The Screen also includes a Change Password and Delete Account Button
    """
    
    for count,widget in enumerate(frameTop.winfo_children()):
        if count !=0:
            widget.place_forget()#All but Logo

    #Clear screen except top frame
    for count,widget in enumerate(window.winfo_children()):
        if count != 0:
            widget.destroy()
            
    frameProfile = CustomFrame(master=window,
                              width=1000,
                              height=650,
                              fgColour=bgColour)
    frameProfile.place(x=0, y=90)

    buttonHome = CustomHoverButton(master=frameTop,
                                         width=50,
                                         height=50,
                                         image1=homeIcon,
                                           image2=homeHover)
    buttonHome.place(x=905, y=13)
    buttonHome.command=partial(Home,buttonHome)
    buttonHome.bind("<Button-1>", buttonHome.command)

    frameTitle = CustomFrame(master=frameProfile,
                             width=220,
                             height=60)
    frameTitle.place(x=15,y=15)
    labelTitle = CustomLabel(master=frameTitle,
                            height=60,
                            text="Your Details",
                            fontSize=26)
    labelTitle.place(relx=0.5, rely=0.5, anchor="center")

    frameUserInfo = CustomFrame(master=frameProfile,
                               width=475,
                               height=524)
    frameUserInfo.place(x=15, y=85)

    #Get users information
    recordFound = searchTable("*","customer",("WHERE customerID = "+str(currentUserID)))
    emailAddress = recordFound[0][4]
    numZeros = 4-int(len(str(recordFound[0][0])))
    userID = "0"*numZeros+str(recordFound[0][0])
    userInfoList = [userID, emailAddress, str.capitalize(recordFound[0][1]),
                    str.capitalize(recordFound[0][2]), recordFound[0][3], recordFound[0][6]]
    
    userTitleList = ["UserID:", "Email Address:", "Forename:", "Surname:", "Date of Birth:", "Favourite Genre:"]
    for n in range(0, len(userTitleList)):
        ycoord = 10 + 75 * n
        labelTitle = CustomTkLabelEntry(master=frameUserInfo,
                                       text=userTitleList[n])
        labelTitle.place(x=20, y=ycoord)

        ycoord = 40 + 75 * n
        labelBox = customtkinter.CTkLabel(master=frameUserInfo,
                                          width=450,
                                          height=35,
                                          corner_radius=10,
                                          fg_color=bgColour,
                                          text="")
        labelBox.place(x=12, y=ycoord)

        labelInfo = tkinter.Label(master=frameUserInfo,
                                  width=30,
                                  height=1,
                                  bg=bgColour,
                                  text=userInfoList[n],
                                  fg=entryColour,
                                  font=(mainFont, 16),
                                  anchor="w")
        labelInfo.place(x=20, y=ycoord)

    buttonUserEdit = CustomButtonLight(master=frameUserInfo,
                                         width=100,
                                         height=35,
                                         text="Edit",
                                         fontSize=16)
    buttonUserEdit.place(x=355, y=470)

    frameCardInfo = CustomFrame(master=frameProfile,
                               width=475,
                               height=230)
    frameCardInfo.place(x=510, y=85)

    cardNo = recordFound[0][7]
    expiry = recordFound[0][8]

    #If card information exists show hidden version, otherwise show an empty indicator
    if cardNo != None and cardNo != "":
        hiddenCardNo = "●●●● ●●●● ●●●● ●●●●"
        hiddenExpiry = "●●/●●"
        detailsPresent = True
    else:
        hiddenCardNo = "-"
        hiddenExpiry = "--/--"
        detailsPresent = False
        
    cardInfoList = [hiddenCardNo, hiddenExpiry]
    cardTitleList = ["Card Number:", "Expiry Date:"]
    for n in range(0, len(cardTitleList)):
        ycoord = 10 + 75 * n
        labelTitle = tkinter.Label(master=frameCardInfo,
                                   width=30,
                                   height=1,
                                   text=cardTitleList[n],
                                   anchor="w",
                                   fg=textColour,
                                   bg=frameColour,
                                   font=(mainFont, 16))
        labelTitle.place(x=20, y=ycoord)

        ycoord = 40 + 75 * n
        labelBox = customtkinter.CTkLabel(master=frameCardInfo,
                                          width=450,
                                          height=35,
                                          corner_radius=10,
                                          fg_color=bgColour,
                                          text="")
        labelBox.place(x=12, y=ycoord)

        labelInfo = tkinter.Label(master=frameCardInfo,
                                  width=30,
                                  height=1,
                                  bg=bgColour,
                                  text=cardInfoList[n],
                                  fg=entryColour,
                                  font=(mainFont, 14),
                                  anchor="w")
        labelInfo.place(x=20, y=ycoord)

    if detailsPresent == True:
        editOrAdd = "Edit"
    else:
        editOrAdd = "Add"
        
    buttonCardEdit = CustomButtonLight(master=frameCardInfo,
                                         width=100,
                                         height=35,
                                         text=editOrAdd,
                                         fontSize=16)
    buttonCardEdit.place(x=355, y=175)

    if detailsPresent == True:
        buttonCardReveal = CustomButtonLight(master=frameCardInfo,
                                               width=100,
                                               height=35,
                                               text="Reveal",
                                               fontSize=16)
        buttonCardReveal.place(x=245, y=175)
        buttonCardReveal.configure(command = partial(Security,"CardReveal",frameProfile,frameCardInfo,frameUserInfo))

    buttonUserEdit.configure(command = partial(Security,"UserEdit",frameProfile,frameCardInfo,frameUserInfo))
    buttonCardEdit.configure(command = partial(Security,"CardEdit",frameProfile,frameCardInfo,frameUserInfo))
    

    buttonChangePassword = CustomButtonDark(master=frameProfile,
                                           width=210,
                                           height=65,
                                           text="Change Password",
                                           command=ChangePassword)
    buttonChangePassword.place(x=530, y=540)

    buttonDelete = CustomButtonDark(master=frameProfile,
                                   width=210,
                                   height=65,
                                   fgColour=warningColour,
                                   text="Delete Account",
                                   hovColour="#EC805F",
                                   command=DeleteUser)
    buttonDelete.place(x=760, y=540)

    
    
def ThankYou(extra=""):
    """
    Displays Thank you message to user
    Includes a Continue button that calls BrowseMain
    """
    #Update the labels from the loading screen to new messages
    for count,frame in enumerate(window.winfo_children()):
        if count == 1:
            for count,widget in enumerate(frame.winfo_children()):
                if count == 2:
                    widget.configure(text="Thank you for your order!")
                if count == 3:
                    if extra == "no email":
                        widget.destroy()
                    else:
                        widget.configure(text="Check your email for your reciept")
        
        buttonContinue = CustomButtonLight(master=frame,
                                           width=300,
                                           height=60,
                                           text="Continue Shopping",
                                           fontSize=20,
                                           command=BrowseMain)
        buttonContinue.place(x=90,y=560)
    

def Checkout(frameBasket, basket, buttonCheckout):
    """
    Parameters: frameBasket - frame containing basket and summary information
                basket - list of game IDs in basket
                buttonCheckout - checkout button from basket page
    Creates Checkout screen with entries for the user to input their card details
    Provides user the option to save their card details to their profile
    Checkout button becomes Confirm Order Button
    """
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """

        labelExpiration.place(x=119, y=150)
        entryExpiration.place(x=117, y=180)

        labelCVC.place(x=339, y=150)
        entryCVC.place(x=337, y=180)

        labelForename.place(x=119, y=225)
        entryForename.place(x=117, y=255)

        labelSurname.place(x=339, y=225)
        entrySurname.place(x=337, y=255)

        labelPassword.place(x=119, y=300)
        entryPassword.place(x=117, y=330)

        checkboxSave.place(x=117,y=455)

        fontSize=16
        if len(message) > 40:
            fontSize=14
        if len(message)>48:
            fontSize=13
             
        frameMessage = CustomFrame(frameCardDetails,
                                 width=400,
                                 height=50,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=117, y=385)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=False,
                                   width=390,
                                   height=30,
                                   text=message,
                                   fontSize=fontSize,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")

        
    def BuyGames(cardNo,expiry):
        
        if checkboxSave.get() == 1:
            #save card details to profile, overwriting any old ones if necessary
            newCardNo = cardNo
            newExpiry = expiry
            updateCustomerCard(currentUserID, newCardNo, newExpiry)

        whenAdded=datetime.now()
        dtFormatted = whenAdded.strftime("%d/%m/%Y %H:%M:%S")


        #remove games from wishlist and basket from basket table
        total=0
        for n in range(0,len(basket)):
            increment("game","numberBought","WHERE gameID = '"+str(basket[n])+"'")
            currentPrice = searchTable("price","game","WHERE gameID = '"+str(basket[n])+"'")
            total += currentPrice[0][0]

            deleteRecord("wishlist","userID",currentUserID," AND gameID = '"+str(basket[n])+"'")
            

        deleteRecord("basket","userID",currentUserID)

        #insert Transaction
        insertTransaction(currentUserID,total,dtFormatted)
        transactionID = searchTable("transactionID","gameTransaction","WHERE date = '"+dtFormatted+"' AND userID = '"+currentUserID+"'")
        for n in range(0,len(basket)):
            insertOrder(basket[n],transactionID[0][0])

        try:
            #send the user a receipt to their email address
            getEmail = searchTable("emailAddress","customer","WHERE customerID = "+currentUserID)
            sendEmail(transactionID[0][0],currentUserID,getEmail[0][0])
        except:
            def closeTopError():
                for count,widget in enumerate(window.winfo_children()):
                    if isinstance(widget,tkinter.Toplevel):
                        widget.destroy()
                ThankYou("no email")
                        
            pauseVar = tkinter.StringVar()
            topError = errorMessage(window,"Email could not send",
                                    "Your reciept could not be send at this time.\nA virtual receipt can be found in your Past Orders\nand you can request an email from there at another\ntime.\n\nWe apologise for any inconvenieance this may\nhave caused you.",
                                    command=closeTopError,button="Continue")
            window.wait_variable(pauseVar)
        
        ThankYou()

    def loading():
        """
        Validates Entries
        If not valid calls messageBox to display error message
        If valid displays loading message whilst waiting for order to process
        Automatically moves onto the next screen once complete
        """
        cardNo = entryCardNo.get()
        expiry = entryExpiration.get()
        CVC = entryCVC.get()

        forename = entryForename.get()
        surname = entrySurname.get()

        
        if testing == False:
            validCard = validation.cardCheck(cardNo)
            if validCard != True:
                messageBox(validCard)
                return
            cardNo = encryption.XOR(cardNo)

            validExpiry = validation.dateCheck(expiry,"expiry")
            if validExpiry != True:
                messageBox(validExpiry)
                return
            expiry = encryption.XOR(expiry)
        
            validCVC = validation.CVCCheck(CVC)
            if validCVC != True:
                messageBox(validCVC)
                return

            validForename = validation.nameCheck(forename,"forename")
            if validForename != True:
                messageBox(validForename)
                return

            validSurname = validation.nameCheck(surname,"surname")
            if validSurname != True:
                messageBox(validSurname)
                return
            
        else:
            cardNo = encryption.XOR(cardNo)
            expiry = encryption.XOR(expiry)

            
        passwordRetrieved = searchTable("password","customer",("WHERE customerID = "+ currentUserID))
        passwordRetrieved = encryption.XOR(passwordRetrieved[0][0])
        
        if entryPassword.get() == "":
            messageBox("Please enter your Password")
            return 
        if entryPassword.get() != passwordRetrieved:
            messageBox("Password Incorrect")
            return

        
        for count,widget in enumerate(window.winfo_children()):
            if count == 0:
                widget.place_forget()
            else:
                widget.destroy()

        frameLoading=CustomFrame(window,
                                  width=480,
                                  height=660)
        frameLoading.place(x=260,y=40)
        
        labelLogoBig = customtkinter.CTkLabel(master=frameLoading,
                                              width=370,
                                              height=340,
                                              image=logoBig)
        labelLogoBig.place(x=55, y=0)

        line = ttk.Separator(frameLoading, orient="horizontal")
        line.place(x=30, y=355, relwidth=0.9, relheight=0.00005)

        labelLoading = CustomLabel(master=frameLoading,
                                   height=40,
                                   text="Order Processing...",
                                   fontSize=30)
        labelLoading.place(relx=0.5, rely=0.60, anchor="center")
        labelWait = CustomLabel(master=frameLoading,
                                 height=30,
                                 text="Please Wait",
                                 fontSize=24)
        labelWait.place(relx=0.5, rely=0.67, anchor="center")

        frameLoading.after(1000,lambda: BuyGames(cardNo,expiry))

    #clear frameBasket other than prices summary
    for count,widget in enumerate(frameBasket.winfo_children()):
        if count != 3:
            widget.destroy()

    #clear top frame other than logo
    for count,widget in enumerate(frameTop.winfo_children()):
        if count != 0:
            widget.place_forget()
        if count == 7 or count == 8:
            widget.destroy()
            
    buttonBack = CustomHoverButton(master=frameTop,
                                     width=50,
                                     height=50,
                                     image1=backIcon,
                                     image2=backHover,
                                     command=Basket)
    buttonBack.place(x=900, y=13)


    buttonCheckout.configure(text="Confirm Order",
                             command=loading)

    frameCardDetails = CustomFrame(master=frameBasket,
                                   width=635,
                                   height=510)
    frameCardDetails.place(x=24,y=66)
                                   

    #get users information to autofill entries
    userInfo = searchTable("cardNumber,expiryDate,customerForename,customerSurname","customer",("WHERE customerID = '"+currentUserID+"'"))
    cardNumber =  encryption.XOR(userInfo[0][0])
    expiry = encryption.XOR(userInfo[0][1])
    forename = userInfo[0][2].capitalize()
    surname = userInfo[0][3].capitalize()
    

    labelSubtitle = CustomSubtitle(master=frameCardDetails,
                                   text="Card Details",
                                   fontSize=26)
    labelSubtitle.place(x=317, y=40,anchor="center")

    #CardNo
    labelCardNo = CustomTkLabelEntry(master=frameCardDetails,
                                     text="Card Number:")
    labelCardNo.place(x=119, y=75)

    entryCardNo = CustomEntry(master=frameCardDetails,
                             width=400,
                             placeholderText="NNNN NNNN NNNN NNNN")
    entryCardNo.place(x=117, y=105)

    if cardNumber != None:
        entryCardNo.insert(0,cardNumber)

    #Expiration
    labelExpiration = CustomTkLabelEntry(master=frameCardDetails,
                                         text="Expiration:")
    labelExpiration.place(x=119, y=160)

    entryExpiration = CustomEntry(master=frameCardDetails,
                                     width=180,
                                     placeholderText="NN/NN")
    entryExpiration.place(x=117, y=190)

    if expiry != None:
        entryExpiration.insert(0,expiry)

    #CVC
    labelCVC = CustomTkLabelEntry(master=frameCardDetails,
                                      text="CVC:")
    labelCVC.place(x=339, y=160)

    entryCVC = CustomEntry(master=frameCardDetails,
                          width=180,
                          placeholderText="NNN")
    entryCVC.place(x=337, y=190)

    
    #Forename
    labelForename = CustomTkLabelEntry(master=frameCardDetails,
                                      text="Forname:")
    labelForename.place(x=119, y=245)

    entryForename = CustomEntry(master=frameCardDetails,
                              width=180)
    entryForename.place(x=117, y=275)
    entryForename.insert(0,forename)

    #Surname
    labelSurname = CustomTkLabelEntry(master=frameCardDetails,
                                      text="Surname:")
    labelSurname.place(x=339, y=245)

    entrySurname = CustomEntry(master=frameCardDetails,
                              width=180)
    entrySurname.place(x=337, y=275)
    entrySurname.insert(0,surname)

    
    #Password
    labelPassword = CustomTkLabelEntry(master=frameCardDetails,
                                     text="Password:")
    labelPassword.place(x=119, y=330)

    entryPassword = CustomEntry(master=frameCardDetails,
                             width=400,
                             show="●",
                             fontSize=14)
    entryPassword.place(x=117, y=360)

    if testing == True:
        entryPassword.insert(0,testPassword)

    #Checkbox
    checkboxSave = CustomCheckbox(master=frameCardDetails,
                                text = "Save card details?")
    checkboxSave.place(x=117,y=420)
                                             
   
            

def editBasket(editType,gameID,button,lastPage,gamePageID = "",event=None):
    """
    Parameters: editType - the type of editing to be done, eg. "add" or "remove"
                gameID - ID of game to be added or removed
                button - if applicable, at to/remove from basket button from game page
                lastPage - the last page the user was on
                gamePageID - if on game page, the ID of the game on the game page
    Adds or Removes games from the users basket
    """
    if editType == "add":
        whenAdded=datetime.now()
        dtFormatted = whenAdded.strftime("%d/%m/%Y %H:%M:%S")
        insertBasket(currentUserID,gameID,dtFormatted)
        
        button.configure(text="Remove from\nBasket",
                         command=partial(editBasket,"remove",gameID,gamePageID=gameID,lastPage="gamePage",button=button),
                        text_font=(mainFont,15))
        
    else:
        deleteRecord("basket","gameID",str(gameID) ,extra=" AND userID = "+str(currentUserID))
        if gameID == gamePageID:
            button.configure(text="Add to Basket",
                             command=partial(editBasket,"add",gameID,gamePageID=gameID,lastPage="gamePage",button=button),
                             text_font=(mainFont,17))

    if lastPage == "gamePage":
        #refresh popup
        BasketPopup(gamePageID,button)
    if lastPage == "basket":
        #refresh basket
        Basket()

    
def editWishlist(gameID,button="",Event=None,wishlist=True):
    """
    Parameters: gameID - ID of game to be added or removed
                button - if applicable, heart button from bestsellers section of wishlist page
                wishlist - indicator of if the user is on the wishlist page or not
    Adds or Removes games from the users wishlist
    """
    if button != "":
        toggle=button.toggleState
    else:
        toggle = 1
        
    if toggle == -1:
        #add to wishlist
        whenAdded=datetime.now()
        dtFormatted = whenAdded.strftime("%d/%m/%Y %H:%M:%S")
        insertWishlist(gameID,currentUserID,dtFormatted)
        
    else:
        #remove from wishlist
        deleteRecord("wishlist","gameID",str(gameID) ,extra=" AND userID = "+str(currentUserID))

    if wishlist == True:
        for count,widget in enumerate(window.winfo_children()):
            if count == 2:
                widget.destroy()
        #refresh wishlist page
        Wishlist()

        
def fillFrames(firstGame,lastGame,mainFrame,numFrames,typeDisplay,specificType,gamesList,frames):
    """
    Parameters: firstGame - index of first game to be displayed in gamesList
                lastGame - index of last game to be displayed in gamesList
                mainFrame - frame that holds game frames
                numFrames - number of game frames to be filled
                typeDisplay - type of display, eg. "category", "genre", "main" or "search"
                specificType - if applicable this is the specific genre or category that is being displayed
                gamesList - list of games to be displayed
                frames - list of frames to fill
    Fills frames with the correct games and displays information about them depending on the type of display
    """
    global game1Image, game2Image, game3Image, game4Image, game5Image, game6Image
    lastChoice = 0
    
    titles = []
    ratings = []
    prices = []
    genres = []
    imageNames = []
    developers = []
    dates=[]

    #fill arrays with information pertaining to the games being displayed
    for n in range(firstGame,(lastGame)):
        currentID = gamesList[n]
        currentRecord = searchTable("title,genre,price,imageName,dev","game",("WHERE gameID = '" + str(currentID) + "'"))
        
        if typeDisplay == "wishlist":
            currentDates = searchTable("dateAdded","wishlist",("WHERE gameID = '" + str(currentID) + "' AND userID = '"+currentUserID+"'"))
            dates.append(currentDates[0][0])
        if typeDisplay == "basket":
            currentDates = searchTable("dateAdded","basket",("WHERE gameID = '" + str(currentID) + "' AND userID = '"+currentUserID+"'"))
            dates.append(currentDates[0][0])


        developers.append(currentRecord[0][4])
        titles.append(currentRecord[0][0])
        genres.append(currentRecord[0][1])
        currentPrice = currentRecord[0][2]
        if currentPrice == 0.0 or currentPrice == 0.00:
            price="Free"
            prices.append(price)
        else:
            if len(str(currentPrice).rsplit('.')[-1]) == 2:
                price = str(currentPrice)
            else:
                price = str(currentPrice)+"0"
            prices.append("£"+price)
        imageNames.append(currentRecord[0][3]+"")
        
        getRatings = searchTable("rating","ratings","WHERE gameID = "+str(currentID))
        gameRating = 0
        count = 0
        for m in range(0,len(getRatings)):
            gameRating += getRatings[m][0]
            count += 1
        if count != 0:
            actualRating = int(round(gameRating/count,0))
            rating = actualRating*"★"+(5-actualRating)*"☆"
        else:
            rating = "[Not Rated]" 
        ratings.append(rating)

    #Create images
    images = []
    dif = lastGame-firstGame
    if dif > 0:
        game1Image =  openImage("GameImages",imageNames[0],140,140)
        images.append(game1Image)
    if dif > 1:
        game2Image =  openImage("GameImages",imageNames[1],140,140)
        images.append(game2Image)
    if dif > 2:
        game3Image =  openImage("GameImages",imageNames[2],140,140)
        images.append(game3Image)
    if dif > 3:
        game4Image =  openImage("GameImages",imageNames[3],140,140)
        images.append(game4Image)
    if dif > 4:
        game5Image =  openImage("GameImages",imageNames[4],140,140)
        images.append(game5Image)
    if dif > 5:
        game6Image =  openImage("GameImages",imageNames[5],140,140)
        images.append(game6Image)

    #Display information on frames
    for n in range(0,dif):
        #clear frame
        for widget in frames[n].winfo_children():
            widget.destroy()

        thumbnail = customtkinter.CTkLabel(master=frames[n],
                                           width=140,
                                           height=140,
                                           fg_color=frameColour,
                                           corner_radius=0,
                                           image=images[n])
        if typeDisplay == "wishlist" or typeDisplay == "basket":
            thumbnail.place(x=10,y=10)
        else:
            thumbnail.place(x=35, y=20)

        if typeDisplay == "wishlist" or typeDisplay == "basket":
            buttonTitle = CustomButtonText(master=frames[n],
                                           width = "scale",
                                           height= 40,
                                           text = titles[n],
                                           fontSize=22,
                                           cornerRadius=0,
                                            command=partial(GamePage,gamesList[n+firstGame],lastPage=typeDisplay))
            buttonTitle.place(x=169,y=20)
            buttonTitle.text_label.place(relx=0,rely=0.5,anchor="w")

            thumbnail.bind("<Button-1>",partial(GamePage,gamesList[n+firstGame],lastPage=typeDisplay))
            
            labelDev = CustomLabel(master=frames[n],
                                       height=30,
                                       anchor = "w",
                                       text = developers[n],
                                       fontSize=20)
            labelDev.place(x=170,y=60)
            labelPrice = CustomLabel(master=frames[n],
                                     autoWidth=False,
                                     width=80,
                                       height=30,
                                       anchor = "e", 
                                       text = prices[n],
                                       fontSize=20)
            labelPrice.place(x=540,y=60)
            dateText = "Added on "+ (dates[n])[:-8]
            labelDate = CustomLabel(master=frames[n],
                                       height=30,
                                       anchor = "w",
                                       text = dateText,
                                       fontSize=16)
            labelDate.place(x=170,y=110)

            buttonRemove = CustomToggleButton(master=frames[n],
                                              width=0,
                                              height=0,
                                              image1=XIcon,
                                              image2=XHover,
                                              image3=XHover)
            buttonRemove.place(x=585,y=10)
            if typeDisplay == "wishlist":
                buttonRemove.command=partial(editWishlist,gamesList[n],"")
            else:
                buttonRemove.command=partial(editBasket,"remove",gamesList[n],"","basket")
            buttonRemove.refresh()

            
        else:  
            if specificType == "Free":
                textGame = titles[n] + "\n" + ratings[n] + "\n" + genres[n]
            elif typeDisplay == "genre":
                textGame = titles[n] + "\n" + ratings[n] + "\n" + prices[n] 
            else:
                textGame = titles[n] + "\n" + ratings[n] + "\n" + prices[n] + "\n" + genres[n]
                
            buttonGame = CustomButtonText(master=frames[n],
                                         width=175,
                                         height=70,
                                         cornerRadius=0,
                                         text=textGame,
                                         fontSize=14)
            buttonGame.configure(command=partial(GamePage,gamesList[firstGame+n],lastPage="browse"))

            thumbnail.bind("<Button-1>",partial(GamePage,gamesList[firstGame+n],lastPage="browse"))

            if specificType == "Free" or typeDisplay == "genre":
                buttonGame.place(x=20, y=175)
            else:
                buttonGame.place(x=20, y=160)

    if typeDisplay == "main":
        #Random Advertisement
        getGamesList = searchTable("gameID, imageName","game","WHERE forSale = 1")
        getTransactions = searchTable("transactionID","gameTransaction","WHERE userID = "+currentUserID)
        
        ownedGames=[]
        for n in range(0,len(getTransactions)):
            getGames = searchTable("gameID","gameOrder","WHERE transactionID = "+str(getTransactions[n][0]))
            for m in range(0,len(getGames)):
                ownedGames.append(getGames[m][0])
                
        imagesList = []
        for n in range(0,len(getGamesList)):
            if getGamesList[n][0] not in ownedGames:
                currentField = getGamesList[n][1] + "Big"
                imagesList.append(currentField)

        #Pick a random image and if it is not the same as the last one display it
        picked = False
        while picked == False:
            randomImage = random.choice(imagesList)
            if randomImage != lastChoice:
                lastChoice = randomImage
                picked = True
        
        adImage =  openImage("GameImages",randomImage)

        searchTerm = "WHERE imageName = "+ "'"+randomImage[:-3]+"'"
        moreInfoColour = searchTable("moreInfoColour", "game", searchTerm)
        moreInfoBg = moreInfoColour[0][0]
        ID = (searchTable("gameID", "game", searchTerm))[0][0]
        buttonGameAd = customtkinter.CTkButton(master=mainFrame,
                                               width=450,
                                               height=260,
                                               corner_radius=50,
                                               fg_color=bgColour,
                                               text="",
                                               hover=False,
                                               image=adImage,
                                               command=partial(GamePage, ID))
        buttonGameAd.place(x=275, y=25)

        buttonMoreInfo = CustomButtonDark(master=mainFrame,
                                         width=100,
                                         height=40,
                                         borderWidth=2,
                                         cornerRadius=15,
                                         bgColour=moreInfoBg,
                                         text="More Info",
                                         fontSize=13,
                                         command=partial(GamePage, ID))
        buttonMoreInfo.place(x=610, y=230)
    
def Basket(event=None):
    """
    Displays the users basket of games and their information
    Games are sorted by most recently added
    Allows the user to remove games from their basket
    Displays a summary of price and includes a Checkout button
    """
    
    #Clear screen except for top frame
    for count,widget in enumerate(window.winfo_children()):
        if count != 0:
            widget.destroy()

    frameBasket = CustomFrame(master=window,
                                width=1000,
                                height=645,
                                fgColour=bgColour)
    frameBasket.place(x=0, y=95)
    
    widgets = []
    for widget in frameTop.winfo_children():
        widgets.append(widget)

    widgets[6].place_forget()#Basket Button
    widgets[4].place_forget()#Line
    widgets[5].place(x=770, y=15)#Wishlist Button
    widgets[3].place(x=905, y=13)#Profile Button
    widgets[3].toggleState=1
    widgets[3].configure(image=profileIcon)
    try:
        widgets[7].destroy()#Back Button
    except: pass
    try:
        widgets[8].destroy()#Back Button
    except: pass
    

     
    buttonHome = CustomHoverButton(master=frameTop,
                                    width=50,
                                    height=50,
                                    image1=homeIcon,
                                    image2=homeHover)
    buttonHome.place(x=835, y=14)
    buttonHome.command=partial(back,buttonBack=buttonHome)
    buttonHome.bind("<Button-1>", buttonHome.command)
    
    

    frameSubtitle = CustomFrame(master=frameBasket,
                                width=205,
                                height=47)
    frameSubtitle.place(x=20,y=14)
    labelSubtitle = CustomSubtitle(master=frameSubtitle,
                                text="Your Basket:",)
    labelSubtitle.place(relx=0.5, rely=0.49, anchor = "center")
    

    frameGames = CustomFrame(master=frameBasket,
                            width=650,
                            height=520,
                            fgColour=bgColour)
    frameGames.place(x=10,y=62)
    

    getBasket = searchTable("gameID,dateAdded","basket",("WHERE userID = "+currentUserID))
    sortedBasket = sort.SortByRecent(getBasket)
    basket=[]
    for n in range(0,len(sortedBasket)):
        basket.append(sortedBasket[n][0])
    
    numGames = len(basket)
    numPages = numGames//3
    numExtra = numGames%3
   
    firstGame = -3
    lastGame = 0
    page = 0

    #creates frames
    framesList = []
    
    if numGames == 0:
        frameGames.configure(width=970)
        frameLabels = CustomFrame(frameGames,
                                  width=960,
                                  height=160)
        frameLabels.place(x=10,y=5)
        label1 = CustomLabel(master=frameLabels,
                             height=45,
                             text="Your Basket is empty",
                             fontSize=24)
        label1.place(relx=0.5,y=55,anchor="center")
        label2 = CustomLabel(master=frameLabels,
                             height=45,
                             text="Better get shopping!",
                             fontSize=18)
        label2.place(relx=0.5,y=95,anchor="center")
    else:
        frame1 = CustomFrame(frameGames,
                  width=630,
                  height=160)
        frame1.place(x=10,y=5)
        framesList.append(frame1)
        frame2 = CustomFrame(frameGames,
                  width=630,
                  height=160)
        frame2.place(x=10,y=180)
        framesList.append(frame2)
        frame3 = CustomFrame(frameGames,
                  width=630,
                  height=160)
        frame3.place(x=10,y=355)
        framesList.append(frame3)    

    def backPage(page,firstGame,lastGame):
        """
        Parameters: page - the current page number
                    firstGame - the index of the firstGame being displayed
                    lastGame - the index of the lastGame being displayed
        Moves backwards one page
        """
        page -= 1
        
        numGames = len(basket)
        numPages = numGames//3
        numExtra = numGames%3
        
        if numExtra != 0:
            numPages += 1
            
        if page == numPages-1:
            frame2.place(x=10,y=180)
            frame3.place(x=10,y=355)
            firstGame -= 3
            if lastGame%3 != 0:
                lastGame = lastGame-(lastGame%3)
            else:
                lastGame -= 3
        else:
            firstGame -= 3
            lastGame -= 3

        pageNo = "Page", page
        if page == (numPages - 1):
            buttonNextPage.place(x=130, y=2)
        
        if page == 1:
            buttonBackPage.place_forget()

        try:
            buttonBackPage.configure(command=partial(backPage,page,firstGame,lastGame))
        except: pass
        try:
            buttonNextPage.configure(command=partial(nextPage,page,firstGame,lastGame))
        except: pass

        labelPageNo.configure(text=pageNo)
        fillFrames(firstGame,lastGame,frameBasket,3,"basket","basket",basket,framesList)#

    def nextPage(page,firstGame,lastGame):
        """
        Parameters: page - the current page number
                    firstGame - the index of the first game being displayed
                    lastGame - the index of the last game being displayed
        Moves forewards one page
        """
        page += 1

        numGames = len(basket)
        numPages = numGames//3
        numExtra = numGames%3
        
        if numExtra != 0:
            numPages += 1
            
        if page == numPages:
            buttonNextPage.place_forget()
            firstGame += 3
            lastGame = numGames
            if lastGame-firstGame == 0:
                frame1.place_forget()
                frame2.place_forget()
                frame3.place_forget()
            if lastGame-firstGame == 1:
                frame2.place_forget()
                frame3.place_forget()
            if lastGame-firstGame == 2:
                frame3.place_forget()
        else:
            firstGame += 3
            lastGame += 3

        pageNo = "Page", page
        if page == 2:
            buttonBackPage.place(x=15, y=2)

        try:
            buttonNextPage.configure(command=partial(nextPage,page,firstGame,lastGame))
        except: pass
        try:
            buttonBackPage.configure(command=partial(backPage,page,firstGame,lastGame))
        except: pass
        
        labelPageNo.configure(text=pageNo)
        fillFrames(firstGame,lastGame,frameBasket,3,"basket","basket",basket,framesList)

    if len(framesList) != 0:
        framePages = CustomFrame(master=frameBasket,
                                width=160,
                                height=30, 
                                cornerRadius=10)
        framePages.place(x=260, y=590)

        pageNo = "Page", page

        labelPageNo = CustomLabel(master=framePages,
                                 height=20,
                                 text=pageNo,
                                 fontSize=12)
        labelPageNo.place(x=55, y=4)

        buttonNextPage = CustomButtonText(framePages,
                                        width=20,
                                        height=20,
                                        cornerRadius=0,
                                        text=">",
                                        fontSize=12,
                                        command=partial(nextPage,page,firstGame,lastGame))

        buttonBackPage = CustomButtonText(framePages,
                                    width=20,
                                    height=20,
                                    cornerRadius=0,
                                    text="<",
                                    fontSize=12,
                                    command=partial(backPage,page,firstGame,lastGame))
        if numPages != 0:
            buttonNextPage.place(x=130, y=2)
        
        nextPage(page,firstGame,lastGame)
 
    if numGames != 0:
        #Summary of prices 
        frameSummary = CustomFrame(master=frameBasket,
                                          width=300,
                                          height=510)
        frameSummary.place(x=678,y=66)

        labelSummary = CustomLabel(frameSummary,
                                    height=50,
                                    anchor="w",
                                    text="Games Summary:",
                                    fontSize=24)
        labelSummary.place(x=15,y=10)

        line = ttk.Separator(frameSummary, orient="horizontal")
        line.place(x=15, y=65, relwidth=0.9, relheight=0.0005)

        numExtra = len(basket)-7
        if numExtra == 1:
            numTimes = 8
        else:
            numTimes = len(basket)
            if numTimes > 7:
                numTimes=7

        total = 0
        for n in range(0,numTimes):
            ycoord= 90 + 30*n
            currentRecord = searchTable("title,price","game",("WHERE gameID = "+str(basket[n])))
            currentTitle = currentRecord[0][0]
            getPrice = currentRecord[0][1]
            
            if getPrice == 0.0 or getPrice == 0.00:
                currentPrice="£00.00"
            else:
                if len(str(getPrice).rsplit('.')[-1]) == 2:
                    currentPrice = "£"+str(getPrice)
                else:
                    currentPrice = "£"+str(getPrice)+"0"

            label1 = CustomLabel(frameSummary,
                                 height=30,
                                 anchor="w",
                                 text=currentTitle,
                                 fontSize=16)
            label1.place(x=15,y=ycoord)
            label2 = CustomLabel(frameSummary,
                                 autoWidth=False,
                                 width=70,
                                 height=30,
                                 anchor="e",
                                 text=currentPrice,
                                 fontSize=16)
            label2.place(x=215,y=ycoord)

            total += getPrice

        if numExtra > 1:
            text = "+"+(str(numExtra))+" more"
            label1 = CustomButtonText(frameSummary,
                                      width=60,
                                     height=20,
                                     text=text,
                                      cornerRadius=0,
                                     fontSize=16)
            label1.place(relx=0.5,y=325,anchor="center")

            #if more than 8 games, summary shows a message saying how many more with a tooltip showing the extras information when hovered over
            msg=""
            for n in range(0,numExtra):
                m=7+n
                currentRecord = searchTable("title,price","game",("WHERE gameID = "+str(basket[m])))
                currentTitle = currentRecord[0][0]
                getPrice = currentRecord[0][1]
                if getPrice == 0.0 or getPrice == 0.00:
                    currentPrice="£00.00"
                else:
                    if len(str(getPrice).rsplit('.')[-1]) == 2:
                        currentPrice = "£"+str(getPrice)
                    else:
                        currentPrice = "£"+str(getPrice)+"0"
                if n != 0:
                    msg = msg + "\n" 
                
                msg = msg + currentTitle + " - " + currentPrice 

                
            ToolTip(label1,msg=msg,follow=True,delay=0,fg=textColour,bg=frameColour)
            
        line2 = ttk.Separator(frameSummary, orient="horizontal")
        line2.place(x=15, y=360, relwidth=0.9, relheight=0.0005)

        if len(str(total).rsplit('.')[-1]) == 2:
            totalStr = "£"+str(total)
            
        elif len(str(total).rsplit('.')[-1]) > 2:
            extra = len(str(total).rsplit('.')[-1]) - 2
            totalStr = "£"+(str(total)[:-extra])
            
        if len(str(total).rsplit('.')[-1]) == 1:
            totalStr = "£"+str(total)+"0"

        if total == 0:
            totalStr = "£00.00"


        labelTotal = CustomLabel(frameSummary,
                             height=30,
                             anchor="w",
                             text="Total",
                             fontSize=20)
        labelTotal.place(x=15,y=370)

        
        labelTotalMoney = CustomLabel(frameSummary,
                             autoWidth=False,
                             width=100,
                             height=30,
                             anchor="e",
                             text=totalStr,
                             fontSize=20)
        labelTotalMoney.place(x=185,y=370)

        buttonCheckout = CustomButtonLight(frameSummary,
                                           width=270,
                                           height=65,
                                           text="Check out",
                                           fontSize=20)
        buttonCheckout.place(x=15,y=425)
        buttonCheckout.configure(command=partial(Checkout,frameBasket,basket,buttonCheckout))
    
    
def BasketPopup(gamePageID,buttonBasket):
    """
    Parameters: gamePageID - ID of the game from the game page the user is on
                buttonBasket - add to/remove from basket button
    Creates a popup that displays the contents of the users basket in a summarised form
    Includes a button to the users Basket
    """
    def closePopUp(event=None):
        """
        Closes Basket Popup
        """
        frameBasketPopup.destroy()
        
    global imageGame1, imageGame2, imageGame3, imageGame4, imageGame5

    getBasket = searchTable("gameID,dateAdded","basket",("WHERE userID = "+currentUserID))
    sortedBasket = sort.SortByRecent(getBasket)
    basket=[]
    for n in range(0,len(sortedBasket)):
        basket.append(sortedBasket[n][0])

    getPrices=[]
    for n in range(0,len(basket)):
        currentPrice = searchTable("price","game",("WHERE gameID = "+str(basket[n])))
        getPrices.append(currentPrice[0][0])
    
    total = 0
    for n in range(0,len(getPrices)):
        total += float(getPrices[n])
        
    if len(str(total).rsplit('.')[-1]) == 2:
        totalStr = "£"+str(total)
        
    elif len(str(total).rsplit('.')[-1]) > 2:
        extra = len(str(total).rsplit('.')[-1]) - 2
        totalStr = "£"+(str(total)[:-extra])
        
    else:
        totalStr = "£"+str(total)+"0"

    if total == 0:
        totalStr = "£00.00"

    #Scales height based on amount of games in basket
    if len(basket) < 6 and len(basket) > 0:
        varHeight = 225 + 90 * (len(basket)-1)
    elif len(basket) >= 6:
        varHeight = 645
    elif len(basket) < 1:
        varHeight = 170

    widgets=[]
    for widget in window.winfo_children():
        widgets.append(widget)
    try:
        widgets[3].destroy()
    except:pass
        
        
    frameBasketPopup = CustomFrame(master=window,
                                   width=275,
                                   height=varHeight,
                                   cornerRadius=0,
                                   borderWidth=2)
    frameBasketPopup.place(x=725,y=0)
    frameBasket = CustomFrame(master=frameBasketPopup,
                              width=265,
                              height=varHeight-10,
                              cornerRadius=0,
                              borderWidth=5,
                              fgColour=bgColour)
    frameBasket.place(x=5,y=5)

    frameTitle = CustomFrame(master=frameBasket,
                             width=145,
                             height=42)
    frameTitle.place(x=15,y=15)
    labelTitle = CustomLabel(master=frameTitle,
                            height=35,
                             text="Your Basket:",
                             fontSize=18)
    labelTitle.place(relx=0.5,rely=0.5,anchor="center")

    buttonExit = CustomToggleButton(master=frameBasket,
                                    width=0,
                                    height=0,
                                    image1=XIcon,
                                    image2=XHover,
                                    image3=XHover,
                                    command=closePopUp,
                                    bgColour=bgColour)
    buttonExit.place(x=215,y=10)
                            

    imageNames=[]
    for n in range(0,len(basket)):
        currentRecord  = searchTable("imageName","game","WHERE gameID = "+str(basket[n]))
        imageName = currentRecord[0][0]+"Mini"
        imageNames.append(imageName)
        
    frameGames = []
    images=[]
    if len(basket) < 1:
        frameEmpty = CustomFrame(master=frameBasket,
                                width=240,
                                height=80,
                                cornerRadius=10)
        frameEmpty.place(x=13,y=65)
        labelEmpty = CustomLabel(master=frameEmpty,
                                 height=35,
                                 text="Basket is Empty",
                                 fontSize=20)
        labelEmpty.place(relx=0.5,rely=0.5,anchor="center")
    else:
        frameTotal = CustomFrame(master=frameBasket,
                                 width=115,
                                 height=40,
                                 cornerRadius=10)
        frameTotal.place(x=15,y=(varHeight-70))
        labelTotal = CustomLabel(master=frameTotal,
                                height=35,
                                text=totalStr,
                                fontSize=18)
        labelTotal.place(relx=0.5,rely=0.5,anchor="center")

        buttonView = CustomButtonDark(master=frameBasket,
                                      width=115,
                                      height=40,
                                      text="View Basket",
                                      borderWidth=1,
                                      cornerRadius=10,
                                      fontSize=15,
                                      command=Basket)
        buttonView.place(x=135,y=(varHeight-70))
        
    if len(basket) > 0:
        frameGame1 = CustomFrame(master=frameBasket,
                                width=240,
                                height=80,
                                cornerRadius=10)
        frameGame1.place(x=13,y=65)
        frameGames.append(frameGame1)
        imageGame1 =  openImage("GameImages",imageNames[0],70,70)
        images.append(imageGame1)
        
    if len(basket) > 1:
        frameGame2 = CustomFrame(master=frameBasket,
                                width=240,
                                height=80,
                                cornerRadius=10)
        frameGame2.place(x=13,y=155)
        frameGames.append(frameGame2)
        imageGame2 =  openImage("GameImages",imageNames[1],70,70)
        images.append(imageGame2)

    if len(basket) > 2:
        frameGame3 = CustomFrame(master=frameBasket,
                                width=240,
                                height=80,
                                cornerRadius=10)
        frameGame3.place(x=13,y=245)
        frameGames.append(frameGame3)
        imageGame3 =  openImage("GameImages",imageNames[2],70,70)
        images.append(imageGame3)

    if len(basket) > 3:
        frameGame4 = CustomFrame(master=frameBasket,
                                width=240,
                                height=80,
                                cornerRadius=10)
        frameGame4.place(x=13,y=335)
        frameGames.append(frameGame4)
        imageGame4 =  openImage("GameImages",imageNames[3],70,70)
        images.append(imageGame4)

    if len(basket) > 4:
        frameGame5 = CustomFrame(master=frameBasket,
                                width=240,
                                height=80,
                                cornerRadius=10)
        frameGame5.place(x=13,y=425)
        frameGames.append(frameGame5)
        imageGame5 =  openImage("GameImages",imageNames[4],70,70)
        images.append(imageGame5)

    if len(basket) > 5:
        #if more than 5 creates a label displaying how many more which has a tooltip to let the user see what the extra ones are when it's hovered over
        more = "+"+str(len(basket)-5)+" more"
        buttonMore = CustomButtonDark(master=frameBasket,
                                      width=240,
                                      borderWidth=0,
                                      height=40,
                                      cornerRadius=10,
                                      text=more,
                                      fontSize=18)
        buttonMore.place(x=13,y=515)

        numExtra = len(basket)-5
        msg=""
        for n in range(0,numExtra):
            m=5+n
            currentRecord = searchTable("title,price","game",("WHERE gameID = "+str(basket[m])))
            currentTitle = currentRecord[0][0]
            getPrice = currentRecord[0][1]
            if getPrice == 0.0 or getPrice == 0.00:
                currentPrice="£00.00"
            else:
                if len(str(getPrice).rsplit('.')[-1]) == 2:
                    currentPrice = "£"+str(getPrice)
                else:
                    currentPrice = "£"+str(getPrice)+"0"
            if n != 0:
                msg = msg + "\n" 
            
            msg = msg + currentTitle + " - " + currentPrice
            
        ToolTip(buttonMore,msg=msg,follow=True,delay=0,fg=textColour,bg=frameColour)


    #Fill popup frames
    for n in range(0,len(frameGames)):
        currentRecord  = searchTable("title,price,gameID","game","WHERE gameID = "+str(basket[n]))
        currentName = currentRecord[0][0]
        getPrice = currentRecord[0][1]
        currentID=currentRecord[0][2]
        if getPrice == 0.0 or getPrice == 0.00:
            currentPrice="Free"
        else:
            if len(str(getPrice).rsplit('.')[-1]) == 2:
                currentPrice = "£"+str(getPrice)
            else:
                currentPrice = "£"+str(getPrice)+"0"
 
        labelMiniThumbnail = customtkinter.CTkLabel(frameGames[n],
                                                     width=70,
                                                     height=70,
                                                     corner_radius=10,
                                                     fg_color = frameColour,
                                                     image=images[n])
        labelMiniThumbnail.place(x=0,y=5)
        
        if len(currentName) > 14:
            textSize = 12
            ycoord=5
            if len(currentName)>20:
                index=currentName.rfind(" ")
                currentName = currentName[:index] + "\n" + currentName[index+1:]
                ycoord=2
        elif len(currentName) > 13:
            textSize=14
            ycoord=5
        else:
            textSize = 15
            ycoord=5


        buttonName = CustomButtonText(frameGames[n],
                                    width=125,
                                      cornerRadius=0,
                                    height=35,
                                    fontSize=textSize,
                                    text=currentName,
                                     command=partial(GamePage,basket[n],lastPage="wishlist"))
        buttonName.place(x=90,y=ycoord)
        buttonName.text_label.place(relx=0,rely=0.5,anchor="w")
        labelPrice = CustomLabel(frameGames[n],
                                autoWidth=False,
                                width=105,
                                height=20,
                                fontSize=14,
                                 anchor="w",
                                text=currentPrice)
        labelPrice.place(x=90,y=40)
    

def GamePage(gameID,lastPage=""):
    """
    Parameters: gameID - ID of game to be displayed
                lastPage - The last page the user was on. Default = ""
    Displays all information about an individual game
    Includes an add to basket button and an add to wishlist button
    """
    global imageSmall, imageBig

    widgets=[]
    for count,widget in enumerate(frameTop.winfo_children()):
        widgets.append(widget)
        if count > 7:
            widget.destroy()
    widgets[5].place(x=770, y=15)#Wishlist button
    widgets[6].place(x=835, y=14)#Basket button
    widgets[4].place(x=750, y=18, relwidth=0.0005, relheight=0.6)#Line
    widgets[3].toggleState=1 #Profile button
    widgets[3].configure(image=profileIcon)
    if lastPage != "browse":
        try:
            widgets[7].place_forget()#Back button
        except: pass


    for count,widget in enumerate(window.winfo_children()):
        if count in [2,3]:
            widget.destroy()



    gameInfo = searchTable("*" , "game", ("WHERE gameID = "+str(gameID)))
    title = gameInfo[0][1]
    priceSearch = gameInfo[0][5]
    if priceSearch == 0.0 or priceSearch == 0.00:
        price="Free"
    else:
        if len(str(priceSearch).rsplit('.')[-1]) == 2:
            price = "£"+str(gameInfo[0][5])
        else:
            price = "£"+str(gameInfo[0][5])+"0"
    developer = gameInfo[0][2]
    
    getRatings = searchTable("rating","ratings","WHERE gameID = "+str(gameInfo[0][0]))
    gameRating = 0
    count = 0
    for m in range(0,len(getRatings)):
        gameRating += getRatings[m][0]
        count += 1
    if count != 0:
        actualRating = int(round(gameRating/count,0))
        rating = actualRating*"★"+(5-actualRating)*"☆"
    else:
        rating = "[Not Rated]" 
        
    genre = gameInfo[0][4]
    imageSmallName = gameInfo[0][7]+""
    imageBigName =  gameInfo[0][7]+"Big"

    imageSmall =  openImage("GameImages",imageSmallName)
    imageBig =  openImage("GameImages",imageBigName)
    
    description = gameInfo[0][9]

    
    info = developer + "   |   " + rating + "   |   " + genre
    length = len(info)
    #scales font size based on length of information to be displayed so that it fits within the frame
    if length >= 48:
        fontSize = 14
    elif length >= 44:
        fontSize = 16
    elif length >= 40:
        fontSize = 18
    else:
        fontSize = 20

    frameGamePage = CustomFrame(master=window,
                               width=1000,
                               height=645,
                               fgColour=bgColour)
    frameGamePage.place(x=0, y=95)
 
    buttonBack = CustomHoverButton(master=frameTop,
                                 width=45,
                                 height=40,
                                 image1=backIcon,
                                 image2=backHover)
    buttonBack.place(x=690, y=20)
    buttonBack.command=partial(back,buttonBack=buttonBack,page="GamePage",lastPage=lastPage)
    buttonBack.bind("<Button-1>", buttonBack.command)

    frameTitle = CustomFrame(master=frameGamePage,
                             width=680,
                             height=70)
    frameTitle.place(x=160, y=20)
    labelTitle = CustomLabel(master=frameTitle,
                            height=70,
                            text=title,
                            fontSize=26)
    labelTitle.place(relx=0.5, rely=0.5,anchor="center")


    frameBigImage = CustomFrame(master=frameGamePage,
                               width=490,
                               height=300,
                               cornerRadius=50)
    frameBigImage.place(x=160, y=100)

    labelBigImage = customtkinter.CTkLabel(master=frameBigImage,
                                           width=450,
                                           height=260,
                                           image=imageBig,
                                           corner_radius=0)
    labelBigImage.place(x=20, y=20)


    framePrice = CustomFrame(master=frameGamePage,
                            width=170,
                            height=210)
    framePrice.place(x=670, y=135)

    labelLittleImage = customtkinter.CTkLabel(master=framePrice,
                                              width=140,
                                              height=140,
                                              image=imageSmall,
                                              corner_radius=0)
    labelLittleImage.place(x=15, y=15)

    labelPrice = CustomLabel(master=framePrice,
                                height=35,
                                text=price,
                                fontSize=24)
    labelPrice.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

    frameInfo = CustomFrame(master=frameGamePage,
                            width=490,
                            height=70)
    frameInfo.place(x=160, y=410)
    
    labelInfo = CustomLabel(master=frameInfo,
                               height=70,
                               fontSize=fontSize,
                               text=info)
    labelInfo.place(relx=0.5, rely=0.5, anchor="center")

    frameWishlist = CustomFrame(master=frameGamePage,
                                height=45,
                                width=170)
    frameWishlist.place(x=670, y=355)

    labelWishlist = CustomLabel(master=frameWishlist,
                                height=35,
                                text="Wishlist:",
                                fontSize=20)
    labelWishlist.place(x=15, y=4)

    gameID = (searchTable("gameID", "game", ("WHERE title = '"+title+"'")))[0][0]

    buttonHeart = CustomToggleButton(frameWishlist,
                                        width=40,
                                        height=35,
                                        image1=hollowHeart,
                                        image2=fullHeart,
                                        image3=hoverHeart)
    buttonHeart.place(x=110,y=3)
    buttonHeart.command=partial(editWishlist,gameID,buttonHeart,wishlist=False)
    buttonHeart.refresh()

    #If game has been wishlisted fill in wishlist button
    getWishlist = searchTable("gameID,dateAdded","wishlist",("WHERE userID = "+currentUserID))
    wishlist=[]
    for n in range(0,len(getWishlist)):
        wishlist.append(getWishlist[n][0])

    if gameID in wishlist:
        buttonHeart.clickFunction()
        
    buttonBasket = CustomButtonDark(master=frameGamePage,
                                    width=170,
                                    height=70,
                                    text="")
    buttonBasket.place(x=670, y=410)

    #Checks whether the game is in the users basket and configures button accordingly
    getBasket = searchTable("gameID","basket",("WHERE userID = "+currentUserID))
    basket=[]
    for n in range(0,len(getBasket)):
        basket.append(getBasket[n][0])
        
    if gameID in basket:
        buttonBasket.configure(text="Remove from\nBasket",
                             command=partial(editBasket,"remove",gameID,button=buttonBasket,lastPage="gamePage",gamePageID=gameID),
                               text_font=(mainFont,15))
    else:
        buttonBasket.configure(text="Add to Basket",
                               command=partial(editBasket,"add",gameID,button=buttonBasket,lastPage="gamePage",gamePageID=gameID),
                               text_font=(mainFont,17))

    frameDescription = CustomFrame(master=frameGamePage,
                                  width=680,
                                  height=130)
    frameDescription.place(x=160, y=490)

    labelDescription = CustomLabel(frameDescription, 
                                   autoWidth=False,
                                   width=620,
                                     height=100,
                                     text=description,
                                     fontSize=16,
                                     anchor="n",
                                     wraplength=630)
    labelDescription.place(x=30, y=15)
    


            

def Wishlist(event=None):
    """
    Displays the users wishlist of games and their information
    Games are sorted by most recently added
    Allows the user to wishlist other bestsellers or remove games from their wishlist
    """
    global bestsellers1Image,bestsellers2Image,bestsellers3Image,bestsellers4Image,bestsellers5Image

    #Clear screen except for top frame
    for count,widget in enumerate(window.winfo_children()):
        if count != 0:
            widget.destroy()

    frameWishlist = CustomFrame(master=window,
                                width=1000,
                                height=645,
                                fgColour=bgColour)
    frameWishlist.place(x=0, y=95)
        
    widgets = []
    for widget in frameTop.winfo_children():
        widgets.append(widget)

    widgets[5].place_forget()#Wishlist button
    widgets[4].place_forget()#Line
    widgets[6].place(x=835, y=14)#Basket button
    widgets[3].toggleState=1 #Profile button
    widgets[3].configure(image=profileIcon)
    try:
        widgets[7].destroy()#Back button
    except: pass
    try:
        widgets[8].destroy()#Back button
    except: pass

    buttonBack = CustomHoverButton(master=frameTop,
                                     width=50,
                                     height=50,
                                     image1=homeIcon,
                                     image2=homeHover)
    buttonBack.place(x=770, y=13)
    buttonBack.command=partial(back,buttonBack=buttonBack)
    buttonBack.bind("<Button-1>", buttonBack.command)

    frameSubtitle = CustomFrame(master=frameWishlist,
                                width=146,
                                height=47)
    frameSubtitle.place(x=20,y=14)
    labelSubtitle = CustomSubtitle(master=frameSubtitle,
                                text="Wishlist",)
    labelSubtitle.place(relx=0.5, rely=0.49, anchor = "center")
    

    frameGames = CustomFrame(master=frameWishlist,
                            width=650,
                            height=520,
                            fgColour=bgColour)
    frameGames.place(x=10,y=62)
    

    getWishlist = searchTable("gameID,dateAdded","wishlist",("WHERE userID = "+currentUserID))
    sortedWishlist = sort.SortByRecent(getWishlist)
    wishlist=[]
    for n in range(0,len(sortedWishlist)):
        wishlist.append(sortedWishlist[n][0])
    
    numGames = len(wishlist)
    numPages = numGames//3
    numExtra = numGames%3
   
    firstGame = -3
    lastGame = 0
    page = 0

    framesList = []
    
    if numGames == 0:
        frameLabels = CustomFrame(frameGames,
                                  width=630,
                                  height=160)
        frameLabels.place(x=10,y=5)
        label1 = CustomLabel(master=frameLabels,
                             height=45,
                             text="Your Wishlist is empty",
                             fontSize=24)
        label1.place(relx=0.5,y=55,anchor="center")
        label2 = CustomLabel(master=frameLabels,
                             height=45,
                             text="Try liking a game to add it to your wishlist!",
                             fontSize=18)
        label2.place(relx=0.5,y=95,anchor="center")
    else:
        frame1 = CustomFrame(frameGames,
                  width=630,
                  height=160)
        frame1.place(x=10,y=5)
        framesList.append(frame1)
        frame2 = CustomFrame(frameGames,
                  width=630,
                  height=160)
        frame2.place(x=10,y=180)
        framesList.append(frame2)
        frame3 = CustomFrame(frameGames,
                  width=630,
                  height=160)
        frame3.place(x=10,y=355)
        framesList.append(frame3)
        
    #navigation
    def backPage(page,firstGame,lastGame):
        """
        Parameters: page - the current page number
                    firstGame - the index of the firstGame being displayed
                    lastGame - the index of the lastGame being displayed
        Moves backwards one page
        """
        page -= 1
        
        numGames = len(wishlist)
        numPages = numGames//3
        numExtra = numGames%3
        
        if numExtra != 0:
            numPages += 1
            
        if page == numPages-1:
            frame2.place(x=10,y=180)
            frame3.place(x=10,y=355)
            firstGame -= 3
            if lastGame%3 != 0:
                lastGame = lastGame-(lastGame%3)
            else:
                lastGame -= 3
        else:
            firstGame -= 3
            lastGame -= 3

        pageNo = "Page", page
        if page == (numPages - 1):
            buttonNextPage.place(x=130, y=2)
        
        if page == 1:
            buttonBackPage.place_forget()

        try:
            buttonBackPage.configure(command=partial(backPage,page,firstGame,lastGame))
        except: pass
        try:
            buttonNextPage.configure(command=partial(nextPage,page,firstGame,lastGame))
        except: pass

        labelPageNo.configure(text=pageNo)
        fillFrames(firstGame,lastGame,frameWishlist,3,"wishlist","wishlist",wishlist,framesList)

    def nextPage(page,firstGame,lastGame):
        """
        Parameters: page - the current page number
                    firstGame - the index of the first game being displayed
                    lastGame - the index of the last game being displayed
        Moves forewards one page
        """
        page += 1

        numGames = len(wishlist)
        numPages = numGames//3
        numExtra = numGames%3
        
        if numExtra != 0:
            numPages += 1
            
        if page == numPages:
            buttonNextPage.place_forget()
            firstGame += 3
            lastGame = numGames
            if lastGame-firstGame == 0:
                frame1.place_forget()
                frame2.place_forget()
                frame3.place_forget()
            if lastGame-firstGame == 1:
                frame2.place_forget()
                frame3.place_forget()
            if lastGame-firstGame == 2:
                frame3.place_forget()
        else:
            firstGame += 3
            lastGame += 3

        pageNo = "Page", page
        if page == 2:
            buttonBackPage.place(x=15, y=2)

        try:
            buttonNextPage.configure(command=partial(nextPage,page,firstGame,lastGame))
        except: pass
        try:
            buttonBackPage.configure(command=partial(backPage,page,firstGame,lastGame))
        except: pass
        
        labelPageNo.configure(text=pageNo)
        fillFrames(firstGame,lastGame,frameWishlist,3,"wishlist","wishlist",wishlist,framesList)

    if len(framesList) != 0:
        framePages = CustomFrame(master=frameWishlist,
                                width=160,
                                height=30, 
                                cornerRadius=10)
        framePages.place(x=260, y=590)

        pageNo = "Page", page

        labelPageNo = CustomLabel(master=framePages,
                                 height=20,
                                 text=pageNo,
                                 fontSize=12)
        labelPageNo.place(x=55, y=4)

        buttonNextPage = CustomButtonText(framePages,
                                        width=20,
                                        height=20,
                                        cornerRadius=0,
                                        text=">",
                                        fontSize=12,
                                        command=partial(nextPage,page,firstGame,lastGame))

        buttonBackPage = CustomButtonText(framePages,
                                    width=20,
                                    height=20,
                                    cornerRadius=0,
                                    text="<",
                                    fontSize=12,
                                    command=partial(backPage,page,firstGame,lastGame))
        if numPages != 0:
            buttonNextPage.place(x=130, y=2)
        
        nextPage(page,firstGame,lastGame)


    #Bestsellers section
    frameBestsellers = CustomFrame(master=frameWishlist,
                                      width=300,
                                      height=605)
    frameBestsellers.place(x=680,y=20)

    labelBestsellers = CustomLabel(frameBestsellers,
                                     height=50,
                                     anchor="w",
                                     text="Bestsellers:",
                                     fontSize=22)
    labelBestsellers.place(x=20,y=5)

    line = ttk.Separator(frameBestsellers, orient="horizontal")
    line.place(x=15, y=50, relwidth=0.9, relheight=0.0005)

    getGamesList = searchTable("gameID","game","WHERE forSale = 1 ORDER BY numberBought DESC")   
    getTransactions = searchTable("transactionID","gameTransaction","WHERE userID = "+currentUserID)
    
    ownedGames=[]
    for n in range(0,len(getTransactions)):
        getGames = searchTable("gameID","gameOrder","WHERE transactionID = "+str(getTransactions[n][0]))
        for m in range(0,len(getGames)):
            ownedGames.append(getGames[m][0])

    bestsellers=[]
    for n in range(0,len(getGamesList)):
        if getGamesList[n][0] in wishlist or getGamesList[n][0] in ownedGames:
            pass
        else:
            bestsellers.append(getGamesList[n][0])

    imageNames=[]
    for n in range(0,len(bestsellers)):
        currentRecord  = searchTable("imageName","game","WHERE gameID = "+str(bestsellers[n]))
        imageName = currentRecord[0][0]+"Mini"
        imageNames.append(imageName)
        

    frameLists = []
    images = []
    if len(bestsellers) > 0:
        frameBestsellers1 = CustomFrameBestsellers(frameBestsellers)
        frameBestsellers1.place(x=15,y=70)
        frameLists.append(frameBestsellers1)
        bestsellers1Image =  openImage("GameImages",imageNames[0],70,70)
        images.append(bestsellers1Image)
        buttonHeart1 = CustomToggleButton(frameBestsellers1,
                                    width=40,
                                    height=35,
                                    image1=hollowHeart,
                                    image2=fullHeart,
                                    image3=hoverHeart)
        buttonHeart1.place(x=10,y=23)
        buttonHeart1.command = partial(editWishlist,bestsellers[0],buttonHeart1)
        buttonHeart1.refresh()
                                               
    if len(bestsellers) > 1:
        frameBestsellers2 = CustomFrameBestsellers(frameBestsellers)
        frameBestsellers2.place(x=15,y=175)
        frameLists.append(frameBestsellers2)
        bestsellers2Image =  openImage("GameImages",imageNames[1],70,70)
        images.append(bestsellers2Image)
        buttonHeart2 = CustomToggleButton(frameBestsellers2,
                                        width=40,
                                        height=35,
                                        image1=hollowHeart,
                                        image2=fullHeart,
                                        image3=hoverHeart)
        buttonHeart2.place(x=10,y=23)
        buttonHeart2.command = partial(editWishlist,bestsellers[1],buttonHeart2)
        buttonHeart2.refresh()
                                               
    if len(bestsellers) >= 3:
        frameBestsellers3 = CustomFrameBestsellers(frameBestsellers)
        frameBestsellers3.place(x=15,y=280)
        frameLists.append(frameBestsellers3)
        bestsellers3Image =  openImage("GameImages",imageNames[2],70,70)
        images.append(bestsellers3Image)
        buttonHeart3 = CustomToggleButton(frameBestsellers3,
                                        width=40,
                                        height=35,
                                        image1=hollowHeart,
                                        image2=fullHeart,
                                        image3=hoverHeart)
        buttonHeart3.place(x=10,y=23)
        buttonHeart3.command=partial(editWishlist,bestsellers[2],buttonHeart3)
        buttonHeart3.refresh()
                                               
    if len(bestsellers) >= 4:
        frameBestsellers4 = CustomFrameBestsellers(frameBestsellers)
        frameBestsellers4.place(x=15,y=385)
        frameLists.append(frameBestsellers4)
        bestsellers4Image =  openImage("GameImages",imageNames[3],70,70)
        images.append(bestsellers4Image)
        buttonHeart4 = CustomToggleButton(frameBestsellers4,
                                        width=40,
                                        height=35,
                                        image1=hollowHeart,
                                        image2=fullHeart,
                                        image3=hoverHeart)
        buttonHeart4.place(x=10,y=23)
        buttonHeart4.command=partial(editWishlist,bestsellers[3],buttonHeart4)
        buttonHeart4.refresh()
                                               
    if len(bestsellers) >= 5:
        frameBestsellers5 = CustomFrameBestsellers(frameBestsellers)
        frameBestsellers5.place(x=15,y=490)
        frameLists.append(frameBestsellers5)
        bestsellers5Image =  openImage("GameImages",imageNames[4],70,70)                                               
        images.append(bestsellers5Image)
        buttonHeart5 = CustomToggleButton(frameBestsellers5,
                                        width=40,
                                        height=35,
                                        image1=hollowHeart,
                                        image2=fullHeart,
                                        image3=hoverHeart)
        buttonHeart5.place(x=10,y=23)
        buttonHeart5.command=partial(editWishlist,bestsellers[4],buttonHeart5)
        buttonHeart5.refresh()
                                               
    #fill bestsellers frame
    for n in range(0,len(frameLists)):
        currentRecord  = searchTable("title,genre,price","game","WHERE gameID = "+str(bestsellers[n]))
        currentName = currentRecord[0][0]
        currentGenre = currentRecord[0][1]
        getPrice = currentRecord[0][2]
        if getPrice == 0.0 or getPrice == 0.00:
            currentPrice="Free"
        else:
            if len(str(getPrice).rsplit('.')[-1]) == 2:
                currentPrice = "£"+str(getPrice)
            else:
                currentPrice = "£"+str(getPrice)+"0"

        infoText = currentGenre+"\n"+str(currentPrice)

                                    
        
        labelMiniThumbnail = customtkinter.CTkLabel(frameLists[n],
                                                     width=70,
                                                     height=70,
                                                     corner_radius=10,
                                                     fg_color = frameColour,
                                                     image=images[n])
        labelMiniThumbnail.place(x=55,y=10)

        #scales font size based on length of name so all fit 
        if len(currentName) > 14:
            textSize = 11
            ycoord=10
            if len(currentName)>17:
                index=currentName.rfind(" ")
                currentName = currentName[:index] + "\n" + currentName[index+1:]
                ycoord=2
        elif len(currentName) > 13:
            textSize=13
            ycoord=10
        else:
            textSize = 14
            ycoord=10

        buttonName = CustomButtonText(frameLists[n],
                                width=105,
                                      cornerRadius=0,
                                height=25,
                                fontSize=textSize,
                                text=currentName,
                                 command=partial(GamePage,bestsellers[n],lastPage="wishlist"))
        buttonName.place(x=145,y=ycoord)
        labelInfo2 = CustomLabel(frameLists[n],
                                 autoWidth=False,
                                width=105,
                                height=10,
                                fontSize=12,
                                text=infoText)
        labelInfo2.place(x=145,y=40)
        
       
def clearSearch(buttonX,searchBar):
    """
    Parameters: buttonX - the X button used to clear the searchBar
                searchBar - the searchBar widget in the top frame
    Clears the searchbar entry widget
    """
    searchBar.delete(0,tkinter.END)
    buttonX.focus_set()
    buttonX.destroy()


def BrowseMain(event=None):
    """
    Gets a list of all listed and unowned game IDs sorted by popularity and calls DisplayGames
    """
    
    getGamesList = searchTable("gameID","game","WHERE forSale = 1 ORDER BY numberBought DESC")
    getTransactions = searchTable("transactionID","gameTransaction","WHERE userID = "+currentUserID)
    
    ownedGames=[]
    for n in range(0,len(getTransactions)):
        getGames = searchTable("gameID","gameOrder","WHERE transactionID = "+str(getTransactions[n][0]))
        for m in range(0,len(getGames)):
            ownedGames.append(getGames[m][0])

    gamesList=[]
    for n in range(0,len(getGamesList)):
        if getGamesList[n][0] not in ownedGames:
            gamesList.append(getGamesList[n][0])

    DisplayGames(4,"main","",gamesList)

def BrowseByCategory(category):
    """
    Parameters: category - The category that has been chosen, eg. "New this year", "Multiplayer" etc.
    Gets a list of all listed and unowned game IDs that match the current category and calls DisplayGames
    """
    if category != "New This Year":
        if category == "Free":
            getGamesList = searchTable("gameID","game","WHERE forSale = 1 AND price = 0.0 ORDER BY numberBought DESC")
        elif category == "Singleplayer":
            getGamesList = searchTable("gameID","game","WHERE forSale = 1 AND multiplayer = 0 ORDER BY numberBought DESC")
        elif category == "Multiplayer":
            getGamesList = searchTable("gameID","game","WHERE forSale = 1 AND multiplayer = 1 ORDER BY numberBought DESC")
            
    else:
        getDatesList = searchTable("creationDate","game","WHERE forSale = 1 ORDER BY numberBought DESC")
        todaysDate = str(datetime.today())
        currentYear = todaysDate[0:4]
        datesList=[]
        for n in range(0,len(getDatesList)):
            if (getDatesList[n][0])[-4:] == currentYear:
                if getDatesList[n][0] not in datesList:
                    datesList.append(getDatesList[n][0])
                
        getGamesList = []
        for n in range(0,len(datesList)):
            newGames = searchTable("gameID","game","WHERE forSale = 1 AND creationDate = '"+datesList[n]+"' AND forSale = 1")
            for m in range(0,len(newGames)):
                getGamesList.append(newGames[m])


    getTransactions = searchTable("transactionID","gameTransaction","WHERE userID = "+currentUserID)
    ownedGames=[]
    for n in range(0,len(getTransactions)):
        getGames = searchTable("gameID","gameOrder","WHERE transactionID = "+str(getTransactions[n][0]))
        for m in range(0,len(getGames)):
            ownedGames.append(getGames[m][0])
    
    gamesList=[]
    for n in range(0,len(getGamesList)):
        if getGamesList[n][0] not in ownedGames:
            gamesList.append(getGamesList[n][0])

    DisplayGames(6,"category",category,gamesList)

def BrowseByGenre(genre):
    """
    Parameters: genre - The genre that has been chosen, eg. "Action", "Role-playing" etc.
    Gets a list of all listed and unowned game IDs that match the current genre and calls DisplayGames
    """
    
    getGamesList = searchTable("gameID","game","WHERE forSale = 1 AND genre = '"+genre+"' ORDER BY numberBought DESC")

    getTransactions = searchTable("transactionID","gameTransaction","WHERE userID = "+currentUserID)
    ownedGames=[]
    for n in range(0,len(getTransactions)):
        getGames = searchTable("gameID","gameOrder","WHERE transactionID = "+str(getTransactions[n][0]))
        for m in range(0,len(getGames)):
            ownedGames.append(getGames[m][0])
            
    gamesList=[]
    for n in range(0,len(getGamesList)):
        if getGamesList[n][0] not in ownedGames:
            gamesList.append(getGamesList[n][0])

    DisplayGames(6,"genre",genre,gamesList)

def BrowseSearchResults(searchBar, event=None):
    """
    Parameters: searchBar - the searchBar widget in the top frame
    Gets a list of all listed and unowned game IDs that match the searchTerm, sorts them by relevence and calls DisplayGames
    """
    searchValue = (searchBar.get()).lower()
    getTitlesList = searchTable("title","game","WHERE forSale = 1 ORDER BY numberBought DESC")
    titlesList= []
    if searchValue == "" or searchValue == " ":
        pass
    else:
        getGamesList = []
        getGames = searchTable("gameID,title","game","WHERE forSale = 1")
        for n in range(0,len(getGames)):
            getGamesList.append(getGames[n])

        getTransactions = searchTable("transactionID","gameTransaction","WHERE userID = "+currentUserID)
        ownedGames=[]
        for n in range(0,len(getTransactions)):
            getGames = searchTable("gameID","gameOrder","WHERE transactionID = "+str(getTransactions[n][0]))
            for m in range(0,len(getGames)):
                ownedGames.append(getGames[m][0])
        
        gamesList=[]
        IDList=[]
        for n in range(0,len(getGamesList)):
            if getGamesList[n][0] not in ownedGames:
                gamesList.append(getGamesList[n][1])
                IDList.append(getGamesList[n][0])
                
        sortedResults=sort.searchSort(gamesList,searchValue)

        finalList=[]
        for n in range(0, len(sortedResults)):
            for m in range(0,len(gamesList)):
                if sortedResults[n] == gamesList[m].lower():
                    finalList.append(IDList[m])

        DisplayGames(6,"search","",finalList)

def DisplayGames(numFrames,typeDisplay,specificType,gamesList):
    """
    Parameters: numFrames - number of frames to be displayed
                typeDisplay - the type of display wanted, eg. "main", "genre", "category" or "search"
                specificType - if applicable this is the specific genre or category to be displayed
                gamesList - an array of integers of gameIDs to be displayed
    Updates side frame buttons to highlight if any are selected
    Creates the frames for games calls FillFrames to fill them
    """
    lastChoice = 0
     
    numGames = len(gamesList)
    numPages = numGames//numFrames
    numExtra = numGames%numFrames

    if numPages == 0:
        numFrames = numExtra

    if numPages == 1 and numExtra == 0:
        numPages=0
    
    firstGame = 0-numFrames
    lastGame = 0
    page = 0

    #Clear screen except for top frame
    for count,widget in enumerate(window.winfo_children()):
        if count != 0:
            widget.destroy()
        else:
            widget.place(x=10, y=10)

    #Remove any back or home buttons and place the others where they should be
    widgets = []
    for count,widget in enumerate(frameTop.winfo_children()):
        widgets.append(widget)
        if count > 6:
            widget.place_forget()

    widgets[3].place(x=905, y=13)#Profile button
    widgets[3].toggleState=1
    widgets[3].configure(image=profileIcon)
    widgets[1].place(x=270, y=20)#Search Entry
    widgets[2].place(x=470, y=20)#Search Button
    widgets[5].place(x=770, y=15)#Wishlist Button
    widgets[6].place(x=835, y=14)#Basket Button
    widgets[4].place_forget()#Line

    
    frameBrowseGames = CustomFrame(master=window,
                                    width=1000,
                                    height=645,
                                    fgColour=bgColour)
    frameBrowseGames.place(x=0, y=95)

    if typeDisplay != "main":
        for count,widget in enumerate(frameTop.winfo_children()):
            if count == 4:
                widget.place(x=750, y=18, relwidth=0.0005, relheight=0.6)#Line
        
        buttonBack = CustomHoverButton(master=frameTop,
                                             width=45,
                                             height=40,
                                             image1=backIcon,
                                            image2=backHover)
        buttonBack.place(x=690, y=20)
        buttonBack.command=partial(back,buttonBack=buttonBack)
        buttonBack.bind("<Button-1>",buttonBack.command)

    searchBar = widgets[1]
            
    if window.focus_get() == searchBar.entry: #If the user has typed something in the searchbar
        #Add a clear button
        buttonX = CustomButtonText(master=frameTop,
                                   height=1,
                                   width=1,
                                   text="X",
                                   fontSize=14,
                                   txtColour=frameColour,
                                   fgColour=entryColour,
                                   cornerRadius=0)
        buttonX.place(x=440,y=25)
        buttonX.configure(command=partial(clearSearch,buttonX,searchBar))
        

    frameSide = CustomFrame(master=frameBrowseGames,
                           width=220,
                           height=630,)
    frameSide.place(x=10, y=5)

    labelSubtitle1 = CustomLabel(master=frameSide,
                                   height=35,
                                   anchor="w",
                                   text="Browse by Category: ",
                                   fontSize=16)
    labelSubtitle1.place(x=10, y=25)

    #Create Browse by Category Buttons, if one has been pressed then it is configured differently
    categories = ["New This Year", "Free", "Multiplayer", "Singleplayer"]
    for n in range(0, len(categories)):
        text1 = categories[n]
        ycoord = 60 + n * 30

        if text1 != specificType:
            buttonColour = frameColour
            categoryColour = textColour
        else:
            buttonColour = textColour
            categoryColour = frameColour
        button=CustomButtonText(master=frameSide,
                               width=120,
                               height=30,
                               cornerRadius=0,
                               fgColour=buttonColour,
                               text=text1,
                               fontSize=14,
                               txtColour=categoryColour,
                               command=partial(BrowseByCategory, text1))
        button.text_label.place(relx=0,rely=0.5,anchor="w")
        button.place(x=40, y=ycoord)


    labelSubtitle2 = CustomLabel(master=frameSide,
                                   height=35,
                                   text="Browse by Genre: ",
                                   anchor="w",
                                   fontSize=16)
    labelSubtitle2.place(x=10, y=190)

    #Create Browse by Genre Buttons, if one has been pressed then it is configured differently
    genresSearch = searchTable("genre","game","ORDER BY genre ASC")
    genres = []
    for i in range(0,len(genresSearch)):
        if genresSearch[i][0] not in genres:
            genres.append(genresSearch[i][0])

    for m in range(0, len(genres)):
        text2 = genres[m]
        ycoord = 225 + m * 30
        
        if text2 != specificType:
            buttonColour = frameColour
            genreColour = textColour
        else:
            buttonColour = textColour
            genreColour = frameColour
                
        button=CustomButtonText(master=frameSide,
                               width=120,
                               height=30,
                               cornerRadius=0,
                               fgColour=buttonColour,
                               text=text2,
                               fontSize=14,
                               txtColour=genreColour,
                               command=partial(BrowseByGenre, text2))
        button.text_label.place(relx=0,rely=0.5,anchor="w")
        button.place(x=40, y=ycoord)

        m = m + 1

    #Create Frames
    frames = []
    if numFrames < 1:
        label = CustomLabel(master=frameBrowseGames,
                            height=60,
                            fontSize=28,
                            text="",
                            fgColour=bgColour)
        label.place(x=610,y=250,anchor="center")
        if typeDisplay == "main":
            label.configure(text="Wow, looks like you've bought all the games!")
        if typeDisplay == "search":
            label.configure(text="Seems like no games match your search")
        if typeDisplay == "genre" or typeDisplay == "category":
            label.configure(text="No games in this category right now")
        label2 = CustomLabel(master=frameBrowseGames,
                            height=40,
                            fontSize=24,
                            text="Come back when more games are released",
                            fgColour=bgColour)
        label2.place(x=610,y=300,anchor="center")
        if typeDisplay == "search":
            label2.configure(text="Check your spelling or try another search term")
            
    if numFrames >= 1:
        frameGame1 = CustomFrameGame(frameBrowseGames)
        if typeDisplay == "main":
            frameGame1.place(x=760, y=25)
        else:
            frameGame1.place(x=270, y=25)
        frames.append(frameGame1)

    if numFrames >= 2:
        frameGame2 = CustomFrameGame(frameBrowseGames)
        if typeDisplay == "main":
            frameGame2.place(x=270, y=315)
        else:
            frameGame2.place(x=522, y=25)
        frames.append(frameGame2)

    if numFrames >= 3:
        frameGame3 = CustomFrameGame(frameBrowseGames)
        if typeDisplay == "main":
            frameGame3.place(x=522, y=315)
        else:
            frameGame3.place(x=760, y=25)
        frames.append(frameGame3)

    if numFrames >= 4:
        frameGame4 = CustomFrameGame(frameBrowseGames)
        if typeDisplay == "main":
            frameGame4.place(x=760, y=315)
        else:
            frameGame4.place(x=270, y=315)
        frames.append(frameGame4)

    if numFrames >= 5:
        frameGame5 = CustomFrameGame(frameBrowseGames)
        frameGame5.place(x=522, y=315)
        frames.append(frameGame5)

    if numFrames == 6:
        frameGame6 = CustomFrameGame(frameBrowseGames)
        frameGame6.place(x=760, y=315)
        frames.append(frameGame6)

    #Navigation
    def backPage(page,firstGame,lastGame):
        """
        Parameters: page - the current page number
                    firstGame - the index of the firstGame being displayed
                    lastGame - the index of the lastGame being displayed
        Moves backwards one page
        """
        page -= 1
        
        numGames = len(gamesList)
        numPages = numGames//numFrames
        numExtra = numGames%numFrames
        
        if numExtra != 0:
            numPages += 1
            if page == numPages-1:
                #If was previously the last page and there was less than the number of frames then suffle the games back by the number extra so it returns to normal.
                firstGame -= numExtra
                lastGame -= numExtra
            else:
                firstGame -= numFrames
                lastGame -= numFrames
        else:
            firstGame -= numFrames
            lastGame -= numFrames

        pageNo = "Page", page
        if page == (numPages - 1):
            buttonNextPage.place(x=130, y=2)
        
        if page == 1:
            buttonBackPage.place_forget()

        try:
            buttonBackPage.configure(command=partial(backPage,page,firstGame,lastGame))
        except: pass
        try:
            buttonNextPage.configure(command=partial(nextPage,page,firstGame,lastGame))
        except: pass

        labelPageNo.configure(text=pageNo)
        fillFrames(firstGame,lastGame,frameBrowseGames,numFrames,typeDisplay,specificType,gamesList,frames)

    def nextPage(page,firstGame,lastGame):
        """
        Parameters: page - the current page number
                    firstGame - the index of the first game being displayed
                    lastGame - the index of the last game being displayed
        Moves forewards one page
        """
        page += 1

        numGames = len(gamesList)
        numPages = numGames//numFrames
        numExtra = numGames%numFrames
        
        if numExtra != 0:
            numPages += 1
            if page == numPages:
                #If its the last page and there is extra to display then suffle the games by the number extra so the screen is still full.
                buttonNextPage.place_forget()
                firstGame += numExtra
                lastGame += numExtra
            else:
                firstGame += numFrames
                lastGame += numFrames
        else:
            if page == numPages:
                buttonNextPage.place_forget()
            firstGame += numFrames
            lastGame += numFrames

        pageNo = "Page", page
        if page == 2:
            buttonBackPage.place(x=15, y=2)

        try:
            buttonNextPage.configure(command=partial(nextPage,page,firstGame,lastGame))
        except: pass
        try:
            buttonBackPage.configure(command=partial(backPage,page,firstGame,lastGame))
        except: pass
        
        labelPageNo.configure(text=pageNo)
        fillFrames(firstGame,lastGame,frameBrowseGames,numFrames,typeDisplay,specificType,gamesList,frames)#
        
    if numFrames != 0:
        framePages = CustomFrame(master=frameBrowseGames,
                                width=160,
                                height=30,
                                cornerRadius=10)
        framePages.place(x=550, y=600)

        pageNo = "Page", page

        labelPageNo = CustomLabel(master=framePages,
                                 height=20,
                                 text=pageNo,
                                 fontSize=12)
        labelPageNo.place(x=55, y=4)

        buttonNextPage = CustomButtonText(framePages,
                                        width=20,
                                        height=20,
                                        cornerRadius=0,
                                        text=">",
                                        fontSize=12,
                                        command=partial(nextPage,page,firstGame,lastGame))

        buttonBackPage = CustomButtonText(framePages,
                                    width=20,
                                    height=20,
                                    cornerRadius=0,
                                    text="<",
                                    fontSize=12,
                                    command=partial(backPage,page,firstGame,lastGame))

        if numPages != 0:
            buttonNextPage.place(x=130, y=2)
        
        nextPage(page,firstGame,lastGame)


def ProfileDropDown(button,event=None):
    """
    Parameters: button - profileButton
    Called when profile button is clicked
    Toggles the image and displays a dropdown menu providing buttons including, "Your Details", "Past Orders" and "Log Out" or removes dropdown
    """
    if button.toggleState == -1:
        #If it is being pressed display dropdown
        squareCorner = CustomFrame(master=window,
                                   width=20,
                                   height=20,
                                   cornerRadius=0)
        squareCorner.place(x=970,y=70)

        frameOutside = CustomFrame(master=window,
                                   width=105,
                                   height=77,
                                   borderColour=frameColour,
                                   borderWidth=2,
                                   fgColour=textColour,
                                   cornerRadius=0)
        frameOutside.place(x=885,y=90)
        frameDropDown = CustomFrame(master=frameOutside,
                                    width=99,
                                    height=71,
                                    cornerRadius=0)
        frameDropDown.place(x=3,y=3)

        buttonDetails = CustomButtonText(master=frameDropDown,
                                         width=97,
                                         height=20,
                                         text="Your Details",
                                         cornerRadius=0,
                                         fontSize=14,
                                         command=Profile)
        buttonDetails.place(x=1,y=1)
        buttonDetails.text_label.place(relx=0,rely=0.5,anchor="w")
        line= ttk.Separator(frameDropDown, orient="horizontal")
        line.place(x=0, y=22, relheight=0.00005,relwidth=1)
        buttonOrders = CustomButtonText(master=frameDropDown,
                                         width=97,
                                         height=20,
                                         text="Past Orders",
                                         cornerRadius=0,
                                        fontSize=14,
                                        command=PastOrders)
        buttonOrders.place(x=1,y=24)
        buttonOrders.text_label.place(relx=0,rely=0.5,anchor="w")
        line2= ttk.Separator(frameDropDown, orient="horizontal")
        line2.place(x=0, y=45, relheight=0.00005,relwidth=1)
        buttonLogOut = CustomButtonText(master=frameDropDown,
                                         width=97,
                                         height=22,
                                         text="Log Out",
                                         cornerRadius=0,
                                        fontSize=14,
                                        command=LogOut)
        buttonLogOut.place(x=1,y=47)
        buttonLogOut.text_label.place(relx=0,rely=0.5,anchor="w")
    else:
        #If it is being unpressed remove dropdown
        widgets=[]
        for widget in window.winfo_children():
            widgets.append(widget)

        widgets[-1].destroy()
        widgets[-2].destroy()
                               

def mainPage():
    """
    Creates Top frame and all the buttons in it
    Then calls BrowseMain
    """
    global frameTop#accessed very often 
    
    for widget in window.winfo_children():
        widget.destroy()

    frameTop = CustomFrame(master=window,
                          width=980,
                          height=80)
    frameTop.place(x=10, y=10)

    buttonLogo = CustomHoverButton(master=frameTop,
                                   width=178,
                                   height=80,
                                   image1=logoLong1,
                                   image2=logoLong1,
                                   command=BrowseMain)
    buttonLogo.place(x=16, y=0)

    searchBar = CustomEntry(master=frameTop,
                            width=200,
                            height=40,
                            cornerRadius=20,
                            borderWidth=1,
                            placeholderText="Search for a Game")

    searchBar.place(x=270, y=20)

    buttonSearch = customtkinter.CTkButton(master=frameTop,
                                           width=40,
                                           height=40,
                                           corner_radius=30,
                                           text="",
                                           hover_color=hoverColour,
                                           fg_color=frameColour,
                                           image=searchIcon,
                                           command=partial(BrowseSearchResults,searchBar))
    buttonSearch.place(x=470, y=20)
    
    searchBar.bind("<Return>",partial(BrowseSearchResults,searchBar))

    buttonProfile = CustomToggleButton(master=frameTop,
                                        width=50,
                                        height=50,
                                        image1=profileIcon,
                                       image2=profileHover,
                                       image3=profileHover)
    buttonProfile.place(x=905, y=13)
    buttonProfile.command=partial(ProfileDropDown,buttonProfile)
    buttonProfile.refresh()

    lineV1= ttk.Separator(frameTop, orient="vertical")

    buttonWishlist = CustomHoverButton(master=frameTop,
                                    width=50,
                                    height=50,
                                       image1=wishlistIcon,
                                       image2=wishlistHover,
                                    command=Wishlist)
    buttonWishlist.place(x=770, y=15)

    buttonBasket = CustomHoverButton(master=frameTop,
                                        width=50,
                                        height=50,
                                        image1=basketIcon,
                                       image2=basketHover,
                                        command=Basket)
    buttonBasket.place(x=835, y=14)
                        

    BrowseMain()


def Welcome(forename,surname):
    """
    Parameters: forename - The forename the customer entered
                surname - The surname the customer entered
    Displays welcome message to the user using their name
    Creates a continue button which calls mainPage()
    """
    #Clear screen
    for widget in window.winfo_children():
        widget.destroy()
        
    frameWelcome = CustomFrame(master=window,
                                width=480,
                                height=660)
    frameWelcome.place(x=260, y=40)

    labelLogo = customtkinter.CTkLabel(master=frameWelcome,
                                       width=370,
                                       height=340,
                                       image=logoBig,
                                       text = "")
    labelLogo.place(x=55, y=35)

    line = ttk.Separator(frameWelcome, orient="horizontal")
    line.place(x=45, y=395, relwidth=0.8, relheight=0.0005)

    welcomeMsg = "Welcome " + str.title(forename) + " " + str.title(surname) + "!"
    labelCreateAccount = CustomLabel(master=frameWelcome,
                                       height=100,
                                       text=welcomeMsg,
                                       fontSize=26,
                                       wraplength=500)
    labelCreateAccount.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    buttonContinue = CustomButtonLight(master=frameWelcome,
                                         width=170,
                                         height=50,
                                         text="Continue",
                                         fontSize=16,
                                         command=mainPage)
    buttonContinue.place(x=153, y=540)


def SignUp():
    """
    Creates sign up screen including entry widgets and dropdowns for all information for a new customer account
    Includes a Done button
    """
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """
        #Move all entry widgets closer together and up the screen to allow error message to be displayed
        for count,widget in enumerate(frameEntry.winfo_children()):
            if count < 6:
                ycoord = 10 + 65 * (count)
                widget.place(x=20, y=ycoord)
            if count >= 6 and count < 12:
                ycoord2 = 41 + 65 * (count-6)
                widget.place(x=15, y=ycoord2)
                
            if count > 12:
                widget.destroy()

        fontSize=16
        if len(message) > 50:
            fontSize=14
        frameMessage = CustomFrame(frameEntry,
                                 width=450,
                                 height=50,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=15, y=415)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=False,
                                   width=440,
                                   height=30,
                                   text=message,
                                   fontSize=fontSize,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")

        
    def createNewCustomer():
        """
        Checks validation for all entries
        If any are invalid calls error message
        If all valid creates new customer account and calls Welcome()
        """
        global currentUserID
        
        newEmail = str(entryEmail.get()).lower()
        validEmail = validation.emailCheck(newEmail)
        if validEmail != True:
            messageBox(validEmail)
            return

        getEmails = searchTable("emailAddress","customer","")
        emails = []
        for field in getEmails:
            emails.append(field[0])
        if newEmail in emails:
            messageBox("Email address is taken, try logging in")
            return
        
        newPassword = entryPassword.get()

        newForename = str.lower(entryForename.get())
        newSurname = str.lower(entrySurname.get())

        newDOB = entryDOB.get()

        newFavGenre = genreVar.get()
        
        if testing == False:
            validPassword = validation.passwordCheck(newPassword)
            if validPassword != True:
                messageBox(validPassword)
                return
        
            validForename = validation.nameCheck(newForename,"forename")
            if validForename != True:
                messageBox(validForename)
                return
            
            validSurname = validation.nameCheck(newSurname,"surname")
            if validSurname != True:
                messageBox(validSurname)
                return
        
            validDOB = validation.dateCheck(newDOB)
            if validDOB != True:
                messageBox(validDOB)
                return
        
            if newFavGenre == "-":
                messageBox("Please select your favourite genre")
        else:
            if newPassword == "":
                messageBox("Please enter a Password")
                return

        newPassword = encryption.XOR(newPassword)

        insertCustomer(newForename,newSurname,newDOB,newEmail,newPassword,newFavGenre)
        
        searchTerm = "WHERE emailAddress = '"+ newEmail +"'"
        results = searchTable("customerID","customer",searchTerm)
        currentUserID = str(results[0][0])
        
        Welcome(newForename,newSurname)

    #Clear screen
    for widget in window.winfo_children():
        widget.destroy()
    
        
    frameSignUp = CustomFrame(master=window,
                              width=480,
                              height=660)
    frameSignUp.place(x=260, y=40)

    labelLogo = customtkinter.CTkLabel(master=frameSignUp,
                                       width=178,
                                       height=78,
                                       image=logoLong1,
                                       text="")
    labelLogo.place(x=149, y=15)

    line = ttk.Separator(frameSignUp, orient="horizontal")
    line.place(x=40, y=95, relwidth=0.8, relheight=0.0005)

    labelCreateAccount = CustomSubtitle(master=frameSignUp,
                                        text="Create an Account")
    labelCreateAccount.place(x=110, y=100)

    frameEntry = CustomFrame(master=frameSignUp,
                            width=480,
                            height=470,
                            cornerRadius=0)
    frameEntry.place(x=0, y=137)

    labelList = ("Email Address:", "Password:", "Forename:", "Surname:", "Date of Birth:", "Favourite Genre:")
    for n in range(0, len(labelList)):
        ycoord = 10 + 75 * n
        label = CustomTkLabelEntry(master=frameEntry,
                                  text=labelList[n])
        label.place(x=20, y=ycoord)

    entryEmail = CustomEntry(master=frameEntry,
                               width=450)
    entryEmail.place(x=15, y=40)
    entryPassword = CustomEntry(master=frameEntry,
                               width=450)
    entryPassword.place(x=15, y=115)
    entryForename = CustomEntry(master=frameEntry,
                               width=450)
    entryForename.place(x=15, y=190)
    entrySurname = CustomEntry(master=frameEntry,
                              width=450)
    entrySurname.place(x=15, y=265)
    entryDOB = CustomEntry(master=frameEntry,
                          width=450)
    entryDOB.place(x=15, y=340)

    #Get all genres currently available
    genreVar = customtkinter.StringVar(value="-")
    genresSearch = searchTable("genre","game","ORDER BY genre ASC")
    genres = []
    for i in range(0,len(genresSearch)):
        if genresSearch[i][0] not in genres:
            genres.append(genresSearch[i][0])

    #Make these genres the options for favourite genre        
    dropdownGenre = CustomDropdown(master=frameEntry,
                                    variable=genreVar,
                                   values=genres)
    dropdownGenre.place(x=15, y=415)

    buttonBack = CustomButtonLight(master=frameSignUp,
                                     width=90,
                                     height=35,
                                     text="Back",
                                     fontSize=16)
    buttonBack.place(x=270, y=610)
    buttonBack.configure(command=Login)

    buttonDone = CustomButtonLight(master=frameSignUp,
                                    width=90,
                                    height=35,
                                    text="Done",
                                    fontSize=16,
                                    command=createNewCustomer)
    buttonDone.place(x=370, y=610)


def Login(level="customer"):
    """
    Parameters: level - access level of login. Default is "customer"
    Creates login screen including entry widgets
    Includes buttons for SignUp and other access level Login
    """
    def messageBox(message):
        """
        Parameters: message - error message to be displayed
        Displays given error message on screen
        """
        labelPassword.place(x=57, y=375)
        entryPassword.place(x=55, y=403)

        buttonLogin.place(x=145, y=520)

        if level != "staff":
            labelQuestion.place(x=100, y=600)
            buttonSignUp.place(x=310, y=600)

        frameMessage = CustomFrame(frameLogin,
                                 width=370,
                                 height=50,
                                 borderWidth=2,
                                 cornerRadius=10,
                                 fgColour=warningColour)
        frameMessage.place(x=55, y=455)

        labelMessage = CustomLabel(frameMessage,
                                   autoWidth=True,
                                   height=30,
                                   text=message,
                                   fontSize=16,
                                   fgColour=warningColour)
        labelMessage.place(relx=0.5,rely=0.5,anchor="center")

        
    def LoginCheck(event=None):
        """
        Checks the Username or email exists
        If it does, checks that the entered password matches
        If incorrect displays the correct error message
        If correct logs the user into their account and correct access level
        """
        global currentUserID #Used in almost every fucntion so is globaled
        getEmail = str(entryEmail.get())
        if getEmail == "":
            messageBox("Please enter an Email")
            return

        if level != "staff":
            searchEmail = str.lower(getEmail)
            searchTerm = "WHERE emailAddress = '"+ searchEmail +"'"
            results = searchTable("customerID","customer",searchTerm)
        else:
            searchUsername = str.lower(getEmail)
            searchTerm = "WHERE username = '"+ searchUsername +"'"
            results = searchTable("staffID","staff",searchTerm)

        if len(results) != 0:
            currentUserID = str(results[0][0])
        else:
            if level != "staff":
                messageBox("No account with that Email")
            else:
                messageBox("No account with that Username")
            return

        if level != "staff":
            passwordRetrieved = searchTable ("password","customer",("WHERE customerID = "+ currentUserID))
        else:
            passwordRetrieved = searchTable ("password,jobTitle","staff",("WHERE staffID = "+ currentUserID))
            
        if entryPassword.get() == "":
            messageBox("Please enter your Password")
            return

        if entryPassword.get() == encryption.XOR(passwordRetrieved[0][0]):
            if level != "staff":
                mainPage()
            else:
                view = passwordRetrieved[0][1]
                StaffMain(view)
        else:
            messageBox("Password Incorrect")
            return

    for widget in window.winfo_children():
        widget.destroy()
        
    frameLogin = CustomFrame(master=window,
                            width=480,
                            height=660)
    frameLogin.place(x=260, y=40)

    labelLogo = customtkinter.CTkLabel(master=frameLogin,
                                       width=250,
                                       height=210,
                                       image=logoSmall,
                                       text="")
    labelLogo.place(x=115, y=0)

    line = ttk.Separator(frameLogin, orient="horizontal")
    line.place(x=50, y=230, relwidth=0.8, relheight=0.0005)

    labelLogin = CustomSubtitle(master=frameLogin,
                                text="Log In")
    labelLogin.place(relx=0.5, y=250,anchor="n")

    labelEmail = CustomTkLabelEntry(master=frameLogin,
                                  text="Email Address:")
    labelEmail.place(x=57, y=310)
    if level == "staff":
        labelEmail.configure(text="Username:")
        labelLogin.configure(text="Staff Log In")
        labelLogin.place(relx=0.5, y=250,anchor="n")
        
    entryEmail = CustomEntry(master=frameLogin,
                            width=370)
    entryEmail.place(x=55, y=337)
    entryEmail.bind("<Return>",LoginCheck)

    labelPassword = CustomTkLabelEntry(master=frameLogin,
                                       text="Password:")
    labelPassword.place(x=57, y=385)
    entryPassword = CustomEntry(master=frameLogin,
                                width=370,
                                show = "●",
                                fontSize=12)
    entryPassword.place(x=55, y=413)
    entryPassword.bind("<Return>",LoginCheck)

    #If testing mode is activated information is autofilled
    if testing == True:
        if level == "staff":
            entryEmail.insert(0,staffTestEmail)
            entryPassword.insert(0,staffTestPassword)
        else:
            entryEmail.insert(0,testEmail)
            entryPassword.insert(0,testPassword)
        

    buttonLogin = CustomButtonLight(master=frameLogin,
                                  width=200,
                                  height=60,
                                  text="Log In",
                                  fontSize=20,
                                  command=LoginCheck)
    buttonLogin.place(x=145, y=485)

    if level != "staff":
        labelQuestion = CustomLabel(master=frameLogin,
                                      height=30,
                                      text="Don't have an Account?",
                                      txtColour=entryColour,
                                      fontSize=16)
        labelQuestion.place(x=100, y=570)

        buttonSignUp = CustomButtonLight(master=frameLogin,
                                       width=80,
                                       height=30,
                                       text="Sign up",
                                       fontSize=16,
                                       command=SignUp)
        buttonSignUp.place(x=310, y=570)

        labelStaff = CustomLabel(master=frameLogin,
                                  height=30,
                                  text="Staff?",
                                  txtColour=entryColour,
                                  fontSize=14)
        labelStaff.place(x=320,y=15)
        buttonStaff = CustomButtonDark(master=frameLogin,
                                        width=20,
                                        height=30,
                                        text="Log In",
                                       borderWidth=1,
                                       bgColour=frameColour,
                                        fontSize=14,
                                       command=partial(Login,"staff"))
        buttonStaff.place(x=370,y=15)
    else:
        buttonBack = CustomHoverButton(master=frameLogin,
                                        width=45,
                                        height=40,
                                        image1=backIcon,
                                        image2=backHover,
                                       command=Login)
        buttonBack.place(x=400, y=15)

#Call Login screen to start program
Login()

#Loop main window
window.mainloop()
