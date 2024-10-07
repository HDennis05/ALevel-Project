from fpdf import FPDF
from SQLfunctions import *
import yagmail
from pathlib import Path
from PIL import Image
from datetime import datetime
from analyticgraph import *

import warnings
warnings.filterwarnings("ignore")

def downloadReport(reportType):
    """
    Parameters: reportType - type of remort eg. "Game","Genre","Developer"
    Creates a Summary Report for the desired information and saves it to the users download files.
    """
    createBar("Games","Month")
    if reportType != "Developer":
        createPie("Genre","Month")
    else:
        createPie("Developers","Month")
        
    class PDF(FPDF):     
        def header(self):
            """
            Creates header for every page
            """
            self.add_font(fname="font/saira.ttf")
            self.set_text_color(204, 252, 203)
            self.set_font("saira", "", 30)
            
            self.set_fill_color(73, 80, 81)
            self.set_draw_color(204, 252, 203)
            #background
            self.rect(0, 0, 595, 842, round_corners=False,style="F")

            #frames
            self.set_fill_color(42, 43, 42)
            self.rect(10, 10, 575, 80, round_corners=True,style="F")#top frame

            #logo
            self.image("Media/Icons/LogoLong2.png", x=20, y=15)

            #title
            if reportType == "Game":
                self.text(255,45,f"Game Analytics Summary")#fontSize=30
            if reportType == "Developer":
                self.text(205,45,f"Developer Analytics Summary")#fontSize=30
            if reportType == "Genre":
                self.text(250,45,f"Genre Analytics Summary")#fontSize=30
                
            self.set_font("saira", "", 20)
            self.text(400,75,timeRange)#fontSize=20

            if self.page_no() == 1:
                #round corners for main frame
                self.rect(30, 110, 535, 100, round_corners=True,style="DF")
                self.rect(30, 111, 100, 640, round_corners=True,style="DF")
                self.rect(465, 111, 100, 640, round_corners=True,style="DF")
                self.rect(30, 650, 535, 100, round_corners=True,style="DF")
                
                self.rect(31, 111, 533, 638, round_corners=True,style="F")

                self.line(119,111,476,111)


                self.image("Media/Analytics/gameBarMonth.png", x=55, y=125)
                self.line(30,420,565,420)
                if reportType != "Developer":
                    self.image("Media/Analytics/genrePieMonth.png", x=90, y=445)
                else:
                    self.image("Media/Analytics/devPieMonth.png", x=70, y=445)
                self.line(30,675,565,675)

                pdf.set_xy(55,680)
                pdf.cell(100, 30, "Total Sales:",ln=2)#fontSize=20
                pdf.cell(100, 30, "Total Revenue:")#fontSize=20
                pdf.set_xy(440,680)
                pdf.cell(100, 30, str(totalSold), ln=2, align="R")#fontSize=20
                pdf.cell(100, 30, f"£{round((totalMade),2)}", align="R")#fontSize=20
            else:
                self.set_font("saira", "", 24)
                self.rect(30, 110, 260, 40, round_corners=True,style="F")#fontSize=24
                
                #round corners for main frame
                self.rect(30, 160, 535, 100, round_corners=True,style="DF")
                self.rect(30, 161, 100, 590, round_corners=True,style="DF")
                self.rect(465, 161, 100, 590, round_corners=True,style="DF")
                self.rect(30, 650, 535, 100, round_corners=True,style="DF")
                
                self.rect(31, 161, 533, 588, round_corners=True,style="F")

                self.line(119,161,476,161)

                
                self.line(30,210,565,210)
                self.line(30,211,565,211)
                self.line(30,209,565,209)

                self.line(95,160,95,750)
                self.line(96,160,96,210)
                self.line(94,160,94,210)
                
                self.line(283,160,283,750)
                self.line(284,160,284,210)
                self.line(282,160,282,210)
                
                self.line(368,160,368,750)
                self.line(369,160,369,210)
                self.line(367,160,367,210)
                
                self.line(462,160,462,750)
                self.line(463,160,463,210)
                self.line(461,160,461,210)

                pdf.set_xy(35,175)
                pdf.cell(90, 40, "Rank")#fontSize=24
                pdf.set_x(100)
                pdf.cell(50, 40, "Title")#fontSize=24
                pdf.set_x(372)
                pdf.cell(50, 40, "No. Sold")#fontSize=24
                pdf.set_x(468)
                pdf.cell(50, 40, "Revenue")#fontSize=24
                

        def footer(self):
            """
            Creates footer for every page
            """
            self.set_fill_color(42, 43, 42)
            self.rect(232, 780, 130, 40, round_corners=True,style="F")
            
            self.add_font(fname="font/saira.ttf")
            self.set_font("saira", "", 18)
            self.set_text_color(204, 252, 203)
            self.text(258, 807, f"Page {self.page_no()} of {{nb}}")#fontSize=18


    #get todays date and work out last months date
    date=datetime.today()
    todaysDate = date.strftime("%d/%m/%Y")
    todaysDateFormatted= todaysDate[:6]+todaysDate[8:]
    month = int(todaysDate[3:5])
    if month==1:
        month=13
    numZeros = 2-len(str(month-1))
    lastMonth = numZeros*"0"+str(month-1)
    lastMonthDate = (todaysDate[:3])+(lastMonth)+(todaysDate[5:])
    lastMonthFormatted = (todaysDateFormatted[:3])+(lastMonth)+(todaysDateFormatted[5:])
    
    if lastMonth == "02" and int(todaysDate[:2]) > 28:
        lastMonthFormatted = ("28/")+(lastMonth)+(todaysDateFormatted[5:])
        lastMonthDate = ("28/")+(lastMonth)+(todaysDate[5:])
    if lastMonth in ["09","04","06","11"] and int(todaysDate[:2]) > 30:
        lastMonthFormatted = ("30/")+(lastMonth)+(todaysDateFormatted[5:])
        lastMonthDate = ("30/")+(lastMonth)+(todaysDate[5:])

    timeRange = lastMonthFormatted+" - "+todaysDateFormatted

    if reportType == "Game":
        getGames = searchTable("gameID","game","")
        displayList=[]
        for n in range(0,len(getGames)):
            displayList.append(getGames[n][0])

        array=[]
        for n in range(0,len(displayList)):
            currentGame = searchTable("title,price","game","WHERE gameID = "+str(displayList[n]))
            getTransactions = searchTable("transactionID,total,date","gameTransaction","")
            totalMade=0
            totalSold=0
            
            for m in range(0,len(getTransactions)):
                #get dates
                transactionDate = datetime.strptime((getTransactions[m][2])[:10],"%d/%m/%Y")
                startDate = datetime.strptime(todaysDate,"%d/%m/%Y")
                endDate = datetime.strptime(lastMonthDate,"%d/%m/%Y")
                #if in timeframe
                if transactionDate <= startDate and transactionDate >= endDate:
                    getOrders = searchTable("*","gameOrder","WHERE transactionID = "+str(getTransactions[m][0])+" AND gameID = "+str(displayList[n]))
                    for i in range(0,len(getOrders)):
                        totalSold += 1

            totalMade += currentGame[0][1]*totalSold
                    
            getRatings = searchTable("rating","ratings","WHERE gameID = "+str(displayList[n]))
            gameRating = 0
            count = 0
            for m in range(0,len(getRatings)):
                gameRating += getRatings[m][0]
                count += 1
            if count != 0:
                rating = int(round(gameRating/count,0))
            else:
                rating = 0
            array.append([currentGame[0][0],rating,totalSold,round(totalMade,2)])
            
    if reportType == "Genre":
        getGenres = searchTable("genre","game","")
        genres=[]
        array=[]
        for n in range(0,len(getGenres)):
            if getGenres[n][0] not in genres:
                title = getGenres[n][0]
                genres.append(title)
                getGames = searchTable("gameID,price","game",("WHERE genre = '"+title+"'"))
                displayList=[]
                for m in range(0,len(getGames)):
                    displayList.append(getGames[m][0])

                totalMade=0
                totalSold=0
                for m in range(0,len(displayList)):
                    currentGame = searchTable("title,price","game","WHERE gameID = "+str(displayList[m]))
                    getTransactions = searchTable("transactionID,total,date","gameTransaction","")

                    temp=0
                    for p in range(0,len(getTransactions)):
                        #get dates
                        transactionDate = datetime.strptime((getTransactions[p][2])[:10],"%d/%m/%Y")
                        startDate = datetime.strptime(todaysDate,"%d/%m/%Y")
                        endDate = datetime.strptime(lastMonthDate,"%d/%m/%Y")
                        #if in timeframe
                        if transactionDate <= startDate and transactionDate >= endDate:
                            getOrders = searchTable("*","gameOrder","WHERE transactionID = "+str(getTransactions[p][0])+" AND gameID = "+str(displayList[m]))
                            for q in range(0,len(getOrders)):
                                temp += 1
                        
                    totalSold += temp
                    totalMade += currentGame[0][1]*temp

                getFavourites = searchTable("*","customer","WHERE favGenre = '"+title+"'")
                favourites=len(getFavourites)
                
                array.append([title,favourites,totalSold,round(totalMade,2)])
                
    if reportType == "Developer":
        array=[]
        devs=[]
        getDevelopers = searchTable("dev","game","")
        for n in range(0,len(getDevelopers)):
            if getDevelopers[n][0] not in devs:
                devs.append(getDevelopers[n][0])
                title=getDevelopers[n][0]
                amount=0
                getGames = searchTable("gameID","game",("WHERE dev = '"+str(getDevelopers[n][0])+"'"))
                displayList=[]
                for m in range(0,len(getGames)):
                    displayList.append(getGames[m][0])

                totalMade=0
                totalSold=0
                ratingTotal=0
                countTotal=0  
                for m in range(0,len(displayList)):
                    currentGame = searchTable("title,price","game","WHERE gameID = "+str(displayList[m]))
                    getTransactions = searchTable("transactionID,total,date","gameTransaction","")

                    temp = 0
                    for p in range(0,len(getTransactions)):
                        #get dates
                        transactionDate = datetime.strptime((getTransactions[p][2])[:10],"%d/%m/%Y")
                        startDate = datetime.strptime(todaysDate,"%d/%m/%Y")
                        endDate = datetime.strptime(lastMonthDate,"%d/%m/%Y")
                        #if in timeframe
                        if transactionDate <= startDate and transactionDate >= endDate:
                            getOrders = searchTable("*","gameOrder","WHERE transactionID = "+str(getTransactions[p][0])+" AND gameID = "+str(displayList[m]))
                            for q in range(0,len(getOrders)):
                                temp += 1

                    totalSold += temp
                    totalMade += currentGame[0][1]*temp

                    getRatings = searchTable("rating","ratings","WHERE gameID = "+str(displayList[m]))
                    gameRating = 0
                    count = 0
                    for m in range(0,len(getRatings)):
                        gameRating += getRatings[m][0]
                        count += 1
                    ratingTotal += gameRating
                    countTotal += count
                        
                if countTotal != 0:
                    rating = int(round(ratingTotal/countTotal,0))
                else:
                    rating = 0
                    
                array.append([title,rating,totalSold,round(totalMade,2)])
                                
        

    array.sort(key=lambda x:x[3],reverse=True)
        
    getTransactions = searchTable("transactionID,total,date","gameTransaction","")
    totalMade=0
    totalSold=0
    for n in range(0,len(getTransactions)):
        transactionDate = datetime.strptime((getTransactions[n][2])[:10],"%d/%m/%Y")
        startDate = datetime.strptime(todaysDate,"%d/%m/%Y")
        endDate = datetime.strptime(lastMonthDate,"%d/%m/%Y")
        if transactionDate <= startDate and transactionDate >= endDate:
            totalMade += getTransactions[n][1]
            getOrders = searchTable("*","gameOrder","WHERE transactionID = "+str(getTransactions[n][0]))
            for m in range(0,len(getOrders)):
                totalSold += 1

    #find users downloads folder
    downloadPath = str(Path.home() / "Downloads")

    #create pdf
    pdf = PDF(unit="pt")
    pdf.add_page()
    pdf.add_font(fname="font/saira.ttf")
    pdf.set_font("saira", "", 20)
    pdf.set_text_color(204, 252, 203)

    pdf.set_auto_page_break(True,80)
    pdf.set_margins(left=30,top=50)

    def fillPage(array,title):
        """
        Parameters: array - 2D array of records and fields
                    title - Title for the top of the page
        Fills the Table with the correct information and adds a title to the top
        """
        for n in range(0, len(array)):
            if n%17 == 0:
                pdf.add_page()
                pdf.set_font("saira", "", 24)
                pdf.set_xy(50,110)
                pdf.cell(220, 40, title, align="C")#fontSize=24
                if "Genres" not in title:
                    pdf.set_xy(290,175)
                    pdf.cell(50, 40, "Rating")#fontSize=24
                if "Genres" in title:
                    pdf.set_xy(295,175)
                    pdf.cell(50, 40, "Favs")#fontSize=24
                pdf.set_font("saira", "", 20)
                pdf.set_y(225)
                
            pdf.set_x(48)
            pdf.cell(30, 30, str(n+1),align="C")#fontSize=20
            pdf.set_x(100)
            pdf.cell(100, 30, array[n][0])
            pdf.set_x(310)
            pdf.cell(30, 30, str(array[n][1]),align="C")#fontSize=20
            pdf.set_x(405)
            pdf.cell(30, 30, str(array[n][2]),align="C")#fontSize=20
            pdf.set_x(510)
            rev= "{:.2f}".format(array[n][3])
            pdf.cell(50, 30, f"£{rev}",align="R")#fontSize=20
            pdf.ln()


    if reportType == "Game":
        fillPage(array,"Games by Revenue")
        array.sort(key=lambda x:x[2],reverse=True)
        fillPage(array,"Games by Sales")
        array.sort(key=lambda x:x[1],reverse=True)
        fillPage(array,"Games by Rating")
    if reportType=="Genre":
        fillPage(array,"Genres by Revenue")
        array.sort(key=lambda x:x[2],reverse=True)
        fillPage(array,"Genres by Sales")
        array.sort(key=lambda x:x[1],reverse=True)
        fillPage(array,"Genres by Favourites")
    if reportType  == "Developer":
        fillPage(array,"Developers by Revenue")
        array.sort(key=lambda x:x[2],reverse=True)
        fillPage(array,"Developers by Sales")
        array.sort(key=lambda x:x[1],reverse=True)
        fillPage(array,"Developers by Rating")       

    #save file to users downloads file
    fileName=f"GoatGames_{reportType}Analytics_{todaysDate[:2]}-{todaysDate[3:5]}-{todaysDate[6:10]}"
    pdf.output(f"{downloadPath}/{fileName}.pdf")

def sendEmail(transactionID=0,currentUserID=0,userEmail=""):
    """
    Parameters: transactionID - Transaction the receipt will be refering to
                currentUserID - Current user's account
                userEmail - The current user's email address      
    Create reciept for order and send it to the users email address
    """
    class PDF(FPDF):     
        def header(self):
            """
            Creates header for every page
            """
            nameSize = 0
            #Works out the size of the users name to create the correctly sized widget
            for n in range(0,len(name)):
                if name[n:n+1] in ["i","I","j","l"]:
                    nameSize += 5
                elif name[n:n+1] in ["J","r","t"]:
                    nameSize += 7
                elif name[n:n+1] in ["f"]:
                    nameSize += 9
                elif name[n:n+1] in [" "]:
                    nameSize += 10
                elif name[n:n+1] in ["c","e","k","L","s","v","x","z"]:
                    nameSize += 11
                elif name[n:n+1] in ["F","g","o","p","T","y","Y"]:
                    nameSize += 12
                elif name[n:n+1] in ["a","b","B","C","d","E","h","n","P","q","S","u","X","Z"]:
                    nameSize += 13
                elif name[n:n+1] in ["A","D","G","K","R","V"]:
                    nameSize += 14
                elif name[n:n+1] in ["H","N","O","Q","U"]:
                    nameSize += 15
                elif name[n:n+1] in ["w"]:
                    nameSize += 17
                elif name[n:n+1] in ["m","M"]:
                    nameSize += 19
                elif name[n:n+1] in ["W"]:
                    nameSize += 21
            nameSize += 25
            nameX=585-nameSize

            dateSize = 0
            #works out the size of the date to create the correctly sized widget
            for n in range(0,len(date)):
                if date[n:n+1] in ["/"," ",":"]:
                    dateSize += 10
                elif date[n:n+1] in ["1"]:
                    dateSize += 8
                elif date[n:n+1] in ["7"]:
                    dateSize += 12
                elif date[n:n+1] in ["2","3","5"]:
                    dateSize += 13
                elif date[n:n+1] in ["4","6","8","9","0"]:
                    dateSize += 14
                else:
                    dateSize += 10
       
            self.add_font(fname="font/saira.ttf")
            self.set_font("saira", "", 14)
            self.set_text_color(204, 252, 203)
            self.set_font("saira", "", 30)
            
            self.set_fill_color(73, 80, 81)
            self.set_draw_color(204, 252, 203)
            #background
            self.rect(0, 0, 595, 842, round_corners=False,style="F")

            #frames
            self.set_fill_color(42, 43, 42)
            self.rect(10, 10, 575, 80, round_corners=True,style="F")#top frame
            self.rect(10, 105, 270, 45, round_corners=True,style="F")#order frame
            self.rect(10, 160, dateSize, 45, round_corners=True,style="F")#date frame
            self.rect(nameX, 105, nameSize, 45, round_corners=True,style="F")#name frame
            self.rect(405, 160, 180, 45, round_corners=True,style="F")#id frame

            #frameDetails(with round corners)
            self.rect(10, 230, 575, 100, round_corners=True,style="F")
            self.rect(10, 230, 100, 540, round_corners=True,style="F")
            self.rect(10, 680, 575, 100, round_corners=True,style="F")
            self.rect(485, 230, 100, 540, round_corners=True,style="F")
            self.rect(10, 230, 575, 540, round_corners=True,style="F")

            #lines
            self.line(35,285,560,285)
            self.line(35,725,560,725)

            #logo
            self.image("Media/Icons/LogoLong2.png", x=20, y=15)

            #title
            self.text(400,60,"Your Receipt")#fontSize=30
            #topLabels
            self.set_font("saira", "", 26)
            self.text(20,138,orderNum)#fontSize=26
            self.text(nameX+10,138,name)#fontSize=26

            self.set_font("saira", "", 24)
            self.text(20,192,date)#fontSize=24
            self.text(415,192,userID)#fontSize=24

            #labels for details
            self.set_font("saira", "", 26)
            self.text(35,275,"Title")#fontSize=26
            self.text(470,275,"Subtotal")#fontSize=26
            self.set_font("saira", "", 22)
            if len(totalStr) == 16:
                xcoord=410
            if len(totalStr) == 17:
                xcoord=400
            if len(totalStr) > 17:
                xcoord=390
            self.text(xcoord,750,totalStr)#fontSize=22

        def footer(self):
            """
            Creates footer for every page
            """
            self.add_font(fname="font/saira.ttf")
            self.set_font("saira", "", 18)
            self.set_text_color(204, 252, 203)
            self.text(272, 812, f"Page {self.page_no()}/{{nb}}")

            
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

    #creat pdf
    pdf = PDF(unit="pt")
    pdf.add_page()
    pdf.add_font(fname="font/saira.ttf")
    pdf.set_font("saira", "", 22)
    pdf.set_text_color(204, 252, 203)

    pdf.set_auto_page_break(True,120)
    pdf.set_margins(left=35,top=300)

    for i in range(0, len(titles)):
        pdf.cell(0, 30, titles[i])#fontSize=22
        pdf.cell(0, 30, prices[i], new_x="LMARGIN", new_y="NEXT",align="R")#fontSize=22

    #save file
    fileName=f"receipt_{orderNum[-4:]}_{date[0:2]}{date[3:5]}{date[6:10]}"
    pdf.output(f"Receipts/{fileName}.pdf")


    #email receipt to user
    mailer=yagmail.SMTP(user="goatgamescompany@gmail.com", password="xnzrrgtqfbsuodil")

    recipient=userEmail
    subject="Your Goat Games Receipt"
    contents=["Thank you for your Order!"]
    attachments=[f"Receipts/{fileName}.pdf"]
    mailer.send(to=recipient, subject=subject, contents=contents, attachments=attachments)
    
