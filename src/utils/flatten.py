def flatten(inputList):
    newList = []
    for i in inputList:
        for j in i:
            newList.append(j)
    return newList
