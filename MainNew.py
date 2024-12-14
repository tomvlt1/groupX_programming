from LoginNew import LoginGUI
from Dashboard import create_dashboard

def main():
    """
    Orchestrate the login and dashboard sequence.
    """
    # 1) Start by showing the login GUI
    LoginGUI()
    # As soon as the user logs in, create_dashboard() is triggered from within the login logic
    # (login_user). If you prefer to handle it explicitly here, you can call create_dashboard()
    # after login returns a success. For now, the code calls create_dashboard() inside login_user().
    #
    # If you want a more direct approach, comment out 'create_dashboard()' in login_user()
    # and do something like this:
    # 
    # is_logged_in = LoginGUI()
    # if is_logged_in:
    #     create_dashboard()
    # else:
    #     # handle login failure or exit

if __name__ == "__main__":
    main()
