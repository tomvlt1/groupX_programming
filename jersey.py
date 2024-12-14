# Pseudocode:
# Define a dictionary for team colors with primary and secondary colors.
# Define a function to draw a custom jersey on a window.
# Check if the chosen team exists in the team colors dictionary.
# Retrieve the primary and secondary colors for the chosen team.
# Create and draw the torso of the jersey with the primary color.
# Create and draw the left sleeve of the jersey with the secondary color.
# Create and draw the right sleeve of the jersey with the secondary color.
# Create and draw the collar of the jersey with the secondary color.
# Display the player's username above the number.
# Display the player's favorite number below the username.
# Initialize the window and draw the custom jersey.
# Wait for a mouse click and close the window.

from graphics import *

team_colors = {
    "MÁLAGA": {"primary": "#4AADD4", "secondary": "#FFFFFF"},
    "SEVILLA FC": {"primary": "#D71A28", "secondary": "#FFFFFF"},
    "GRANADA": {"primary": "#E30613", "secondary": "#FFFFFF"},
    "ALMERÍA": {"primary": "#FF0000", "secondary": "#FFFFFF"},
    "EIBAR": {"primary": "#800000", "secondary": "#0044FF"},
    "BARCELONA": {"primary": "#A50044", "secondary": "#004D98"},
    "CELTA": {"primary": "#C0E6F1", "secondary": "#FFFFFF"},
    "LEVANTE": {"primary": "#003DA5", "secondary": "#ED1C24"},
    "REAL MADRID": {"primary": "#FFFFFF", "secondary": "#FEBE10"},
    "RAYO VALLECANO": {"primary": "#FFFFFF", "secondary": "#FF0000"},
    "GETAFE": {"primary": "#003DA5", "secondary": "#FFFFFF"},
    "VALENCIA": {"primary": "#FFFFFF", "secondary": "#FF8800"},
    "ATHLETIC": {"primary": "#D6001C", "secondary": "#FFFFFF"},
    "CÓRDOBA": {"primary": "#339933", "secondary": "#FFFFFF"},
    "ATLETICO MADRID": {"primary": "#D81920", "secondary": "#FFFFFF"},
    "ESPANYOL": {"primary": "#005CB9", "secondary": "#FFFFFF"},
    "VILLARREAL": {"primary": "#FFEF00", "secondary": "#005BAC"},
    "DEPORTIVO": {"primary": "#0071C5", "secondary": "#FFFFFF"},
    "REAL SOCIEDAD": {"primary": "#005BAC", "secondary": "#FFFFFF"},
    "ELCHE": {"primary": "#008542", "secondary": "#FFFFFF"},
    "GIJÓN": {"primary": "#D6001C", "secondary": "#FFFFFF"},
    "REAL BETIS": {"primary": "#008542", "secondary": "#FFFFFF"},
    "LAS PALMAS": {"primary": "#FFD700", "secondary": "#0070C0"},
    "OSASUNA": {"primary": "#D6001C", "secondary": "#001E62"},
    "LEGANÉS": {"primary": "#0044FF", "secondary": "#FFFFFF"},
    "ALAVÉS": {"primary": "#0044FF", "secondary": "#FFFFFF"},
    "GIRONA": {"primary": "#D6001C", "secondary": "#FFFFFF"},
    "VALLADOLID": {"primary": "#4A2C81", "secondary": "#FFFFFF"},
    "HUESCA": {"primary": "#900C3F", "secondary": "#0044FF"},
    "MALLORCA": {"primary": "#D6001C", "secondary": "#000000"},
    "CÁDIZ CF": {"primary": "#FFD700", "secondary": "#0000FF"},
}

def draw_custom_jersey(win, team_chosen, username, favorite_number):
    if team_chosen not in team_colors:
        print("Invalid team chosen. Please select a valid team.")
        return
    
    primary_color = team_colors[team_chosen]["primary"]
    secondary_color = team_colors[team_chosen]["secondary"]

    torso = Rectangle(Point(150, 80), Point(350, 380))
    torso.setFill(primary_color)
    torso.setOutline("black")
    torso.setWidth(3)
    torso.draw(win)

    left_sleeve = Polygon(Point(150, 80), Point(100, 200), Point(150, 200))
    left_sleeve.setFill(secondary_color)
    left_sleeve.setOutline("black")
    left_sleeve.setWidth(3)
    left_sleeve.draw(win)

    right_sleeve = Polygon(Point(350, 80), Point(400, 200), Point(350, 200))
    right_sleeve.setFill(secondary_color)
    right_sleeve.setOutline("black")
    right_sleeve.setWidth(3)
    right_sleeve.draw(win)

    collar = Rectangle(Point(215, 70), Point(285, 90))
    collar.setFill(secondary_color)
    collar.setOutline("black")
    collar.setWidth(2)
    collar.draw(win)

    username_text = Text(Point(250, 140), username.upper())
    username_text.setSize(20)
    username_text.setTextColor(secondary_color)
    username_text.setStyle("bold")
    username_text.draw(win)

    number_text = Text(Point(250, 200), str(favorite_number))
    number_text.setSize(30)
    number_text.setTextColor(secondary_color)
    number_text.setStyle("bold")
    number_text.draw(win)

def main():
    win = GraphWin("Football Jersey", 500, 400)
    draw_custom_jersey(win, "REAL MADRID", "PlayerOne", 10)
    win.getMouse()
    win.close()

main()