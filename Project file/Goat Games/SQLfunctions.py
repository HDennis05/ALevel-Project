import sqlite3

conn = sqlite3.connect("GoatGamesDB.db")#connects to the database
cur = conn.cursor()#cursor object executes SQL statements

#Insert
def insertGame(title, dev, creationDate, genre, price, image, moreInfo, description, multi):
    """
    Parameters: game details
    Inserts game into game table in database
    ID, NumberBought, rating and forSale are automatically assigned
    """
    cur.execute("INSERT INTO game VALUES(NULL,?,?,?,?,?,0,?,?,?,?,1)",
                (title, dev, creationDate, genre, price, image, moreInfo, description, multi))
    conn.commit()
    
def insertCustomer(forename, surname, DOB, email, password, favGenre):
    """
    Parameters: customer details without card details
    Inserts customer into customer table in database
    ID is automatically assigned and card details are set to NULL
    """
    cur.execute("INSERT INTO customer VALUES(NULL,?,?,?,?,?,?,NULL,NULL)",
                (forename, surname, DOB, email, password, favGenre))
    conn.commit()

def insertStaff(forename,surname,username,jobTitle,password):
    """
    Parameters: staff details
    Inserts staff into staff table in database
    ID is automatically assigned
    """
    cur.execute("INSERT INTO staff VALUES(NULL,?,?,?,?,?)",
                (forename, surname, username, password,jobTitle))
    conn.commit()

def insertOrder(gameID, transactionID):
    """
    Parameters: order details
    Inserts order into gameOrder table in database
    """
    cur.execute("INSERT INTO gameOrder VALUES(?,?)",
                (gameID, transactionID))
    conn.commit()
def insertTransaction(userID, total, date):
    """
    Parameters: transaction details
    Inserts transaction into gameTransaction table in database
    transactionID is automaticlaly assigned
    """
    cur.execute("INSERT INTO gameTransaction VALUES(NULL,?,?,?)",
                (userID, total, date))
    conn.commit()

def insertWishlist(gameID,userID,dateAdded):
    """
    Parameters: wishlist item details
    Inserts wishlist item into wishlist table in database
    """
    cur.execute("INSERT INTO wishlist VALUES(?,?,?)",
                (userID,gameID,dateAdded))
    conn.commit()
    
def insertBasket(userID,gameID,dateAdded):
    """
    Parameters: basket item details
    Inserts basket item into basket table in database
    """
    cur.execute("INSERT INTO basket VALUES(?,?,?)",
                (userID,gameID,dateAdded))
    conn.commit()

def insertRating(userID,gameID,rating):
    """
    Parameters: rating item details
    Inserts rating item into rating table in database
    """
    cur.execute("INSERT INTO ratings VALUES(?,?,?)",
                (userID,gameID,rating))
    conn.commit()

#Update
def updateGame(gameID, title, dev, genre, price, image, moreInfo, description, multi):
    """
    Parameters: game details  
    Updates game with corresponding gameID
    """
    cur.execute("UPDATE game SET title=?,dev=?,genre=?,price=?,imageName=?,moreInfoColour=?,description=?,multiplayer=? WHERE gameID = ?",
                (title, dev, genre, price, image, moreInfo, description, multi, gameID))
    conn.commit()

def unlistGame(gameID):
    """
    Parameters: gameID 
    Updates forSale column of game with corresponding gameID to 0
    """
    cur.execute("UPDATE game SET forSale = 0 WHERE gameID = "+gameID)
    conn.commit()

def listGame(gameID):
    """
    Parameters: gameID 
    Updates forSale column of game with corresponding gameID to 1
    """
    cur.execute("UPDATE game SET forSale = 1 WHERE gameID = "+gameID)
    conn.commit()
    
def updateCustomerUser(customerID, email, forename, surname, DOB, favourite, password=""):
    """
    Parameters: Customer personal details  
    Updates customers personal details with corresponding customerID
    """
    if password == "":
        cur.execute("UPDATE customer SET customerForename = ?, customerSurname =?,customerDOB = ?, emailAddress = ?, favGenre = ? WHERE customerID = ?",
                    (forename, surname, DOB, email, favourite, customerID))
    else:
        cur.execute("UPDATE customer SET customerForename = ?, customerSurname =?,customerDOB = ?, emailAddress = ?, password=?, favGenre = ? WHERE customerID = ?",
                    (forename, surname, DOB, email, password, favourite, customerID))
    conn.commit()

def updateCustomerCard(customerID, cardNo, expiry):
    """
    Parameters: Customer card details  
    Updates customers card details with corresponding customerID
    """
    cur.execute("UPDATE customer SET cardNumber = ?, expiryDate = ? WHERE customerID = ?",
                (cardNo, expiry, customerID))
    conn.commit()

def updateCustomerPassword(customerID, newPassword):
    """
    Parameters: Customer ID and password  
    Updates password of customer with corresponding customerID
    """
    cur.execute("UPDATE customer SET password = ? WHERE customerID = ?",
                (newPassword, customerID))
    conn.commit()

def updateStaff(staffID,username,forename,surname,jobTitle,password):
    """
    Parameters: staff details 
    Updates staff details of staff member with corresponding staffID
    """
    cur.execute("UPDATE staff SET username = ?, staffForename = ?, staffSurname = ?, jobTitle = ?, password = ? WHERE staffID = ?",
                (username,forename,surname,jobTitle,password,staffID))
    conn.commit()

    
#Routines for all
def viewTable(table):
    """
    Parameters: table - table to be retrieved from
    Retrieves all information from table
    """
    cur.execute("SELECT * FROM "+table)
    rows = cur.fetchall()
    return rows

def deleteRecord(table, searchid, searchTerm,extra=""):
    """
    Parameters: table - table to be deleted from
                searchID - column name to searched
                searchTerm - search term of record(s) to be deleted
                extra - any extra information to search with
    Deletes any record that matches the search term(s)
    """
    cur.execute("DELETE FROM "+ table +" WHERE "+ searchid +" = "+ searchTerm + extra)
    conn.commit()

def searchTable(retrieval,tableName,search):
    """
    Parameters: retrieval - information to be retrieved
                tableName - table to searched
                search - search phrase
    Returns any record that matches the search phrase
    """
    cur.execute("SELECT "+retrieval+" FROM "+ tableName + " " + search)
    rows = cur.fetchall()
    return rows

def increment(table,column,searchTerm):
    """
    Parameters: table - table to be accessed
                column - column to be incremented
                searchTerm - search phrase
    Increments any record's column where the searchTerm matches
    """
    cur.execute("UPDATE "+table+" SET "+column+" = "+column+" + 1 "+ searchTerm)
    conn.commit()



#Create table
def createTable():
    """
    Creates an new database with an admin staff record
    """
    #GAME
    cur.execute("""CREATE TABLE IF NOT EXISTS game
                (gameID INTEGER PRIMARY KEY,
                title TEXT,
                dev TEXT,
                creationDate TEXT,
                genre TEXT,
                price REAL,
                numberBought INTEGER DEFAULT 0,
                imageName TEXT,
                moreInfoColour TEXT DEFAULT "#2A2B2A",
                description TEXT,
                multiplayer INTEGER,
                forSale INTEGER DEFAULT 1)""")

    #ORDER (Linking table)
    cur.execute("""CREATE TABLE IF NOT EXISTS gameOrder
                (gameID INTEGER,
                transactionID INTEGER)""")

    #TRANSACTION
    cur.execute("""CREATE TABLE IF NOT EXISTS gameTransaction
                (transactionID INTEGER PRIMARY KEY,
                userID INTEGER,
                total REAL,
                date TEXT)""")

    #CUSTOMER
    cur.execute("""CREATE TABLE IF NOT EXISTS customer
                (customerID INTEGER PRIMARY KEY,
                customerForename TEXT,
                customerSurname TEXT,
                customerDOB TEXT,
                emailAddress TEXT,
                password TEXT,
                favGenre TEXT,
                cardNumber TEXT,
                expiryDate TEXT)""")


    #STAFF
    cur.execute("""CREATE TABLE IF NOT EXISTS staff
                (staffID INTEGER PRIMARY KEY,
                staffForename TEXT,
                staffSurname TEXT,
                username TEXT,
                password TEXT,
                jobTitle TEXT)""")

    #BASKET
    cur.execute("""CREATE TABLE IF NOT EXISTS basket
                (userID INTEGER,
                gameID INTEGER,
                dateAdded TEXT)""")

    #WISHLIST
    cur.execute("""CREATE TABLE IF NOT EXISTS wishlist
                (userID INTEGER,
                gameID INTEGER,
                dateAdded TEXT)""")

    #RATING
    cur.execute("""CREATE TABLE IF NOT EXISTS ratings
                (userID INTEGER,
                gameID INTEGER,
                rating INTEGER)""")

    try:
        cur.execute("INSERT INTO staff VALUES(1,'admin','account','aaccount0001','Qcpwriul(88','Admin')")
    except:
        cur.execute("UPDATE staff SET staffForename='admin', staffSurname='account',username='aaccount0001',password='Qcpwriul(88',jobTitle='Admin') WHERE staffID = 1")

    conn.commit()

