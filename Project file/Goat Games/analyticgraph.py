import matplotlib.pyplot as plt
import numpy as np
from SQLfunctions import *
from datetime import datetime
from PIL import Image

def createBar(typeBar,timeFrame="All"):
    """
    Parameters: typeBar - type of bar chart wanted, eg. "Games" or "Developers"
                timeFrame - length of time the bar chart refers to, eg. "All" or "Month"
    Creates a bar chart of sales, depending on which type, and saves it as a png
    """
    #Creation of figure and styling
    plt.style.use('ggplot')
    fig = plt.figure(facecolor = "#2a2b2a",figsize=(7,2.5))
    ax = fig.subplots()
    ax.set_facecolor('#2A2B2A')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color("#495051")
    ax.spines['bottom'].set_color("#495051")
    ax.tick_params(axis="x", colors="#ccfccb", labelsize=8)
    ax.tick_params(axis="y", colors="#ccfccb")
    plt.autoscale()
    plt.grid(color="#495051")

    plt.ylabel("Number Sold",color="#ccfccb", fontsize=10)


    #Get titles and data
    titles = []
    data=[]
    if typeBar == "Games":
        if timeFrame == "All":
            getGames = searchTable("title,numberBought","game","")
            for n in range(0,len(getGames)):
                titles.append(getGames[n][0])
                data.append(getGames[n][1])
        if timeFrame == "Month":
            date=datetime.today()
            todaysDate = date.strftime("%d/%m/%Y")
            month = int(todaysDate[3:5])
            if month==1:
                month=13
            numZeros = 2-len(str(month-1))
            lastMonth = numZeros*"0"+str(month-1)
            lastMonthDate = (todaysDate[:3])+(lastMonth)+(todaysDate[5:])
            if lastMonth == "02" and int(todaysDate[:2]) > 28:
                lastMonthDate = ("28/")+(lastMonth)+(todaysDate[5:])
            if lastMonth in ["09","04","06","11"] and int(todaysDate[:2]) > 30:
                lastMonthDate = ("30/")+(lastMonth)+(todaysDate[5:])

            getGames = searchTable("gameID","game","")
            displayList=[]
            for n in range(0,len(getGames)):
                displayList.append(getGames[n][0])

            array=[]
            for n in range(0,len(displayList)):
                currentGame = searchTable("title,price","game","WHERE gameID = "+str(displayList[n]))
                getTransactions = searchTable("transactionID,total,date","gameTransaction","")
                titles.append(currentGame[0][0])
                
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
                data.append(totalSold)

    if typeBar == "Developers":
        devs=[]
        getDevelopers = searchTable("dev","game","")
        for n in range(0,len(getDevelopers)):
            if getDevelopers[n][0] not in devs:
                devs.append(getDevelopers[n][0])
        for n in range(0,len(devs)):
            amount=0
            titles.append(devs[n])
            getNums = searchTable("numberBought","game",("WHERE dev = '"+str(devs[n])+"'"))
            for m in range(0,len(getNums)):
                amount += getNums[m][0]
            data.append(amount)
            

    barPos = []
    for n in range(0,len(data)):
        barPos.append(round(n*0.6,1))

    #Make gradient colours
    mycolours = ["#ccfccb", "#aedead", "#86c08f", "#68a271"]
    nums = [0,1,2,3,2,1]
    colours = []
    for n in range(0,(len(data))):
        index = nums[n%6]
        colours.append(mycolours[index])

    #Plot bars
    plt.bar(x=barPos,
            height=data,
            width=0.5,
            color=colours,
            edgecolor="#aedead",
            linewidth=1,
            tick_label=titles)

    plt.xticks(barPos, titles, rotation=30, ha="right")

    #Save 
    if typeBar == "Games":
        plt.savefig("Media/Analytics/gameBar.png", bbox_inches='tight',dpi=100)
        if timeFrame == "Month":
            image = Image.open("Media/Analytics/gameBar.png")
            resized = image.resize((500,280))
            resized.save("Media/Analytics/gameBarMonth.png")
    if typeBar == "Developers":
        plt.savefig("Media/Analytics/devBar.png", bbox_inches='tight',dpi=100)
        if timeFrame == "Month":
            image = Image.open("Media/Analytics/devBar.png")
            resized = image.resize((500,280))
            resized.save("Media/Analytics/devBarMonth.png")

        


def createPie(typePie,timeFrame="All"):
    """
    Parameters: typePie - type of pie chart wanted, eg. "Genre" or "Developers"
                timeFrame - length of time the pie chart refers to, eg. "All" or "Month"
    Creates a pie chart of sales, depending on which type, and saves it as a png
    """
    #Creation of figure and styling
    fig = plt.figure(facecolor = "#2a2b2a",figsize=(6,3))
    ax = fig.subplots(subplot_kw=dict(aspect="equal"))
    fig.patch.set_facecolor('#2A2B2A')
    plt.rcParams['text.color'] = '#ccfccb'
    
    if typePie == "Genre":
        title = "Sales per Genre"
    if typePie == "Developers":
        title = "Sales per Developer"
        
    ax.set_title(title, y=1.0, pad=-5, color="#ccfccb", fontsize=10)

    #Get titles and data
    getGenres = searchTable("genre","game","")
    titles = []
    genres=[]
    data=[]
    if typePie == "Genre":
        if timeFrame == "All":
            for n in range(0,len(getGenres)):
                if getGenres[n][0] not in genres:
                    title = getGenres[n][0]
                    genres.append(title)
                    getGames = searchTable("gameID","game",("WHERE genre = '"+title+"'"))
                    numSales = 0
                    for m in range(0,len(getGames)):
                        getNum = searchTable("numberBought","game",("WHERE gameID = "+str(getGames[m][0])))
                        numSales += getNum[0][0]
                        
                    data.append(numSales)
                    titles.append(f"{title} ({numSales})")
                    
        if timeFrame == "Month":
            date=datetime.today()
            todaysDate = date.strftime("%d/%m/%Y")
            month = int(todaysDate[3:5])
            if month==1:
                month=13
            numZeros = 2-len(str(month-1))
            lastMonth = numZeros*"0"+str(month-1)
            lastMonthDate = (todaysDate[:3])+(lastMonth)+(todaysDate[5:])
            if lastMonth == "02" and int(todaysDate[:2]) > 28:
                lastMonthDate = ("28/")+(lastMonth)+(todaysDate[5:])
            if lastMonth in ["09","04","06","11"] and int(todaysDate[:2]) > 30:
                lastMonthDate = ("30/")+(lastMonth)+(todaysDate[5:])
                
                
            
            for n in range(0,len(getGenres)):
                if getGenres[n][0] not in genres:
                    title = getGenres[n][0]
                    genres.append(title)
                    getGames = searchTable("gameID","game",("WHERE genre = '"+title+"'"))
                    displayList=[]
                    for m in range(0,len(getGames)):
                        displayList.append(getGames[m][0])

                    array=[]
                    totalSold=0
                    for m in range(0,len(displayList)):
                        currentGame = searchTable("title,price","game","WHERE gameID = "+str(displayList[m]))
                        getTransactions = searchTable("transactionID,total,date","gameTransaction","")
                        
                        for p in range(0,len(getTransactions)):
                            #get dates
                            transactionDate = datetime.strptime((getTransactions[p][2])[:10],"%d/%m/%Y")
                            startDate = datetime.strptime(todaysDate,"%d/%m/%Y")
                            endDate = datetime.strptime(lastMonthDate,"%d/%m/%Y")
                            #if in timeframe
                            if transactionDate <= startDate and transactionDate >= endDate:
                                getOrders = searchTable("*","gameOrder","WHERE transactionID = "+str(getTransactions[p][0])+" AND gameID = "+str(displayList[m]))
                                for q in range(0,len(getOrders)):
                                    totalSold += 1
                        
                    data.append(totalSold)
                    titles.append(f"{title} ({totalSold})")
        startAng=180

    if typePie == "Developers":
        if timeFrame == "Month":
            date=datetime.today()
            todaysDate = date.strftime("%d/%m/%Y")
            month = int(todaysDate[3:5])
            if month==1:
                month=13
            numZeros = 2-len(str(month-1))
            lastMonth = numZeros*"0"+str(month-1)
            lastMonthDate = (todaysDate[:3])+(lastMonth)+(todaysDate[5:])
            if lastMonth == "02" and int(todaysDate[:2]) > 28:
                lastMonthDate = ("28/")+(lastMonth)+(todaysDate[5:])
            if lastMonth in ["09","04","06","11"] and int(todaysDate[:2]) > 30:
                lastMonthDate = ("30/")+(lastMonth)+(todaysDate[5:])
            
            devs=[]
            getDevelopers = searchTable("dev","game","")
            for n in range(0,len(getDevelopers)):
                if getDevelopers[n][0] not in devs:
                    devs.append(getDevelopers[n][0])
                    
            for n in range(0,len(devs)):
                title=devs[n]
                amount=0
                getGames = searchTable("gameID","game",("WHERE dev = '"+str(devs[n])+"'"))
                displayList=[]
                for m in range(0,len(getGames)):
                    displayList.append(getGames[m][0])

                array=[]
                totalSold=0
                for m in range(0,len(displayList)):
                    currentGame = searchTable("title,price","game","WHERE gameID = "+str(displayList[m]))
                    getTransactions = searchTable("transactionID,total,date","gameTransaction","")
                    
                    for p in range(0,len(getTransactions)):
                        #get dates
                        transactionDate = datetime.strptime((getTransactions[p][2])[:10],"%d/%m/%Y")
                        startDate = datetime.strptime(todaysDate,"%d/%m/%Y")
                        endDate = datetime.strptime(lastMonthDate,"%d/%m/%Y")
                        #if in timeframe
                        if transactionDate <= startDate and transactionDate >= endDate:
                            getOrders = searchTable("*","gameOrder","WHERE transactionID = "+str(getTransactions[p][0])+" AND gameID = "+str(displayList[m]))
                            for q in range(0,len(getOrders)):
                                totalSold += 1
                                    
                data.append(totalSold)
                titles.append(f"{title} ({totalSold})")
        startAng = 90



    #Make gradient colours
    mycolours = ["#ccfccb", "#aedead", "#86c08f", "#68a271"]
    nums = [0,1,2,3,2,1]
    colours = []
    for n in range(0,(len(data))):
        if len(data) == 7 and n == len(data)-1:
            index=nums[n%6+2]
        else:
            index = nums[n%6]
        colours.append(mycolours[index])

    #Make pie chart   
    wedges, texts = ax.pie(data, startangle=startAng, colors=colours)

    kw = dict(arrowprops=dict(arrowstyle="-",color="#ccfccb"),
              zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        
        side = np.sign(x)
        
        horizontalalignment = {-1: "right", 1: "left"}[int(side)]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(titles[i], xy=(x, y), xytext=(1.5*side, y),
                    horizontalalignment=horizontalalignment, **kw)

    #Save
    if typePie == "Genre":
        plt.savefig("Media/Analytics/genrePie.png", bbox_inches='tight',dpi=120)
        if timeFrame == "Month":
            image = Image.open("Media/Analytics/genrePie.png")
            resized = image.resize((400,205))
            resized.save("Media/Analytics/genrePieMonth.png")
    if typePie == "Developers":
        plt.savefig("Media/Analytics/devPie.png", bbox_inches='tight',dpi=120)
        if timeFrame == "Month":
            image = Image.open("Media/Analytics/devPie.png")
            resized = image.resize((440,205))
            resized.save("Media/Analytics/devPieMonth.png")
            

