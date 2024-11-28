session = {}

def setIDUser(IdUser):
    session['IdUser']= IdUser
def getIDUser():
    return session.get('IdUser', None)   
def setCurrentWindow(Win):
    session['CurrentWindow']= Win
def getCurrentWindow():
    return session.get('CurrentWindow', None)   

