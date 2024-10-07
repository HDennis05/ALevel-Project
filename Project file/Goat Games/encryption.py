from SQLfunctions import *


def XOR(data):
    """
    Parameters: data - string to be encrypted
    Uses XOR encryption to encrypt or decrypt the data
    Returns encrypted or decrypted data
    """
    if data == None:
        return
    result=""
    for n in range(0,len(data)):
        oldChar = data[n:n+1]
        oldIndex = (ord(oldChar))
        temp=(1+n)%30
        newIndex = (oldIndex^(temp))
        result = result + chr(newIndex)
    return result
    
