def getStatus(open, close):
    if close > open:
        return 1
    if open > close:
        return -1
    return 0
