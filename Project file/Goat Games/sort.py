from datetime import datetime

def SortByRecent(entry):
    """
    Parameters: entry - 2D array to be sorted
    Sorts 2D array, of information and its date, by most recent first
    Returns sorted 2D array
    """
    array = []
    for n in range(0,len(entry)):
        date = (entry[n][1])
        array.append(date)

    array.sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y %H:%M:%S"), reverse=True)

    finalArray = []
    for n in range(0,len(array)):
        date = array[n]
        for n in range(0,len(entry)):
            record = entry[n]
            if date in record:
                finalArray.append(record)
        
    return finalArray



def searchSort(entry,searchTerm):
    """
    Parameters: entry - array of strings to be sorted
                searchTerm - string which is being search
    Sorts array by the index in which the searchTerm appears within the string. Therefore most relevant results first.
    Returns sorted array
    """
    array = []
    for n in range(0,len(entry)):
        currentEntry = entry[n].lower()
        index = currentEntry.find(searchTerm.lower())
        if index != -1:
            array.append((currentEntry,index))

    array.sort(key=lambda x:x[1])

    finalArray = []
    for n in range(0,len(array)):
        finalArray.append(array[n][0])

    return finalArray


