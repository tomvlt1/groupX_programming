from Dashboard import * 
from Dashboard import create_dashboard
def main():
    from Login import LoginGUI
    if getIDUser() == None:
        LoginGUI()
    else:              
        create_dashboard

main()


