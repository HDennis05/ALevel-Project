import re
#validation


def typeCheck(entry,typ):
    """
    Parameters: entry - string to check
                typ - type the string should be
    Checks entry against type to check that they match
    If they match returns True, if they do not returns False
    """
    if typ == "int":
        if entry.isdigit():
            return True
        else:
            return False

    if typ == "str":
        if entry.isalpha():
            return True
        else:
            return False

    if typ == "flt":
        try:
            float(entry)
            return True
        except:
            return False
            

def lengthCheck(entry,length,side="below"):
    """
    Parameters: entry - string to check
                length - length the string should be
                side - determines whether the length of the string should be below, above or equal to the length. Default is "below"
    Checks if the string is the correct length
    If it is returns True, if not returns False
    """
    if side == "below":
        if len(entry) < length:
            return True
        else:
            return False
    if side == "above":
        if len(entry) > length:
            return True
        else:
            return False
    if side == "equal":
        if len(entry) == length:
            return True
        else:
            return False


def nameCheck(entry,nameType,extra="your",length=41):
    """
    Parameters: entry - string to check
                nameType - the type of name being validated, used in output message
                extra - changes article used in the output message, eg. "a","an","your". Default is "your"
                length - the length the name should be
    Checks if the string present and the correct length, and only contains letters, hyphens or spaces
    If name is valid returns True, If not returns a message describing why it is not valid
    """
    if entry != "":
        if lengthCheck(entry,length):
            if all(char.isalpha() or char == "-" or char == " " for char in entry):
                return True
            else:
                return f"{nameType.capitalize()} cannot include numbers or special characters"
        else:
            return f"{nameType.capitalize()} cannot be longer than {length-1} characters"
    else:
        return f"Please enter {extra} {nameType.capitalize()}"
        

                     
def passwordCheck(entry,extra=""):
    """
    Parameters: entry - string to check
                extra - changes article used in the output message, eg. "a","an","your". Default is "your"
    Checks if the string is present and strong enough. Must contain a capital, number and special character"
    If password is valid returns True, If not returns a message describing why it is not valid
    """
    if entry != "":
        #creates a mask to check if the entry contains at least one capital letter, number and special character
        mask = re.compile("^(?=.*[A-Z])(?=.*[0-9])(?=.*[#?!@$%^&*-]).{1,}$")
        if mask.match(entry):
            return True
        else:
            return f"{extra} Password too weak\n [must contain a capital, number and special character]"
    else:
        return f"Please enter a {extra.lower()} password"

def descriptionCheck(entry):
    """
    Parameters: entry - string to check
    Checks if the string is less than 286 characters and 4 lines or less
    If description is valid returns True, If not returns a message describing why it is not valid
    """
    if len(entry) <= 285:
        if entry.count("\n") <= 3:
            return True
        else:
            return "Description must be 4 lines or less"
    else:
        return "Description cannot exceed 285 characters"

def cardCheck(entry):
    """
    Parameters: entry - string to check
    Checks if the string is present and in format NNNN NNNN NNNN NNNN
    If card number is valid returns True, If not returns a message describing why it is not valid
    """
    if entry != "":
        mask = re.compile("^[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}$")
        if mask.match(entry):
            return True
        else:
            return "Card Number must be of format NNNN NNNN NNNN NNNN"
    else:
        return "Please enter your Card Number"

def CVCCheck(entry):
    """
    Parameters: entry - string to check
    Checks if the string is present and contains 3 number
    If CVC is valid returns True, If not returns a message describing why it is not valid
    """
    if entry != "":
        if lengthCheck(entry,3,"equal"):
            if typeCheck(entry,"int"):
                return True
            else:
                return "CVC cannot include letters or special characters"
        else:
            return "CVC must be 3 digits"
    else:
        return "Please enter your CVC"

def emailCheck(entry,extra="your"):
    """
    Parameters: entry - string to check
                extra - changes article used in the output message, eg. "a","an","your". Default is "your"
    Checks if the string is present and a valid email. It must include "@gmail.com" and have no spaces
    If email is valid returns True, If not returns a message describing why it is not valid
    """
    if entry != "":
        if "@gmail.com" == entry[-10:]:
            if len(entry) >= 11:
                if " " not in entry:
                    return True
                else:
                    return "Email must not include spaces"
            else:
                return "Invalid Email"
        else:
            return "Email must include '@gmail.com'"
    else:
        return f"Please enter {extra} Email"

def dateCheck(entry,formatType="date",extra="your"):
    """
    Parameters: entry - string to check
                formatType - determines the type of format that the string should be, eg. "date" or "expiry"
                extra - changes article used in the output message, eg. "a","an","your". Default is "your"
    Checks if the string is present and in the correct format. DD/MM/YYYY or MM/YY
    If date is valid returns True, If not returns a message describing why it is not valid
    """
    if formatType == "date":
        if entry != "":
            mask = re.compile("^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
            if mask.match(entry):
                if int(entry[-4:]) <= 2023:
                    if int(entry[3:5]) <= 12 and int(entry[3:5]) > 0:
                        months = [9,4,6,11]
                        if int(entry[3:5]) in months:
                            if int(entry[:2]) <= 30 and int(entry[:2]) > 0:
                                return True
                        elif int(entry[3:5]) == 2:
                            if int(entry[:2]) <= 29 and int(entry[:2]) > 0:
                                return True
                        else:
                            if int(entry[:2]) <= 31 and int(entry[:2]) > 0:
                                return True
            else:  
                return "Date of Birth must be of format DD/MM/YYYY"
            
            return "Invalid Date of Birth"
        else:
            return f"Please enter {extra} Date of Birth"
    
    if formatType == "expiry":
        if entry != "":
            mask = re.compile("^[0-9]{2}/[0-9]{2}$")
            if mask.match(entry):
                if "00" not in entry and int(entry[:2]) <= 12 and int(entry[3:5]) >= 23:
                    return True
            else:  
                return "Expiration Date must be of format MM/YY"
            return "Invalid Expiration Date"
        else:
            return "Please enter your Card Expiration Date"


