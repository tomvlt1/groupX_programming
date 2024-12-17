from graphics import *


def draw_custom_jersey(win, p1, p2, team_chosen, username, favorite_number, jersey_objects=None):
    team_colors = {
    "BASE": {"primary": "#FFFFFF", "secondary": "#000000"},
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

    if jersey_objects:
        for obj in jersey_objects:
            obj.undraw()  
            

    
    team_chosen = team_chosen.lower()
    team_colors_lower = {}  
    for key, value in team_colors.items():        
        team_colors_lower[key.lower()] = value

    
    if team_chosen.lower() not in team_colors_lower:
        team_chosen = "base"  
    

    primary_color = team_colors_lower[team_chosen]["primary"]
    secondary_color = team_colors_lower[team_chosen]["secondary"]
    
    area_width = p2.getX() - p1.getX()
    area_height = p2.getY() - p1.getY()
    
    torso_top_left = Point(p1.getX() + 0.25 * area_width, p1.getY() + 0.2 * area_height)
    torso_bottom_right = Point(p1.getX() + 0.75 * area_width, p1.getY() + 0.8 * area_height)
    
    left_sleeve_points = [
        Point(p1.getX() + 0.25 * area_width, p1.getY() + 0.2 * area_height),
        Point(p1.getX() + 0.10 * area_width, p1.getY() + 0.5 * area_height),
        Point(p1.getX() + 0.25 * area_width, p1.getY() + 0.5 * area_height)
    ]
    
    right_sleeve_points = [
        Point(p1.getX() + 0.75 * area_width, p1.getY() + 0.2 * area_height),
        Point(p1.getX() + 0.90 * area_width, p1.getY() + 0.5 * area_height),
        Point(p1.getX() + 0.75 * area_width, p1.getY() + 0.5 * area_height)
    ]
    
    collar_top_left = Point(p1.getX() + 0.40 * area_width, p1.getY() + 0.10 * area_height)
    collar_bottom_right = Point(p1.getX() + 0.60 * area_width, p1.getY() + 0.20 * area_height)
    
    torso = Rectangle(torso_top_left, torso_bottom_right)
    torso.setFill(primary_color)
    torso.setOutline("black")
    torso.setWidth(int(0.005 * area_width))  
    torso.draw(win)
    
    left_sleeve = Polygon(left_sleeve_points)
    left_sleeve.setFill(secondary_color)
    left_sleeve.setOutline("black")
    left_sleeve.setWidth(int(0.005 * area_width))
    left_sleeve.draw(win)
    
    right_sleeve = Polygon(right_sleeve_points)
    right_sleeve.setFill(secondary_color)
    right_sleeve.setOutline("black")
    right_sleeve.setWidth(int(0.005 * area_width))
    right_sleeve.draw(win)
    
    collar = Rectangle(collar_top_left, collar_bottom_right)
    collar.setFill(secondary_color)
    collar.setOutline("black")
    collar.setWidth(int(0.003 * area_width))
    collar.draw(win)
    
    username_position = Point(p1.getX() + 0.5 * area_width, p1.getY() + 0.45 * area_height)
    username_text = Text(username_position, username.upper())
    username_text.setSize(int(0.05 * area_height))  
    username_text.setTextColor(secondary_color)
    username_text.setStyle("bold")
    username_text.draw(win)
    
    number_position = Point(p1.getX() + 0.5 * area_width, p1.getY() + 0.65 * area_height)
    number_text = Text(number_position, str(favorite_number))
    number_text.setSize(int(0.07 * area_height))  
    number_text.setTextColor(secondary_color)
    number_text.setStyle("bold")
    number_text.draw(win)
    
    return [torso, left_sleeve, right_sleeve, collar, username_text, number_text]

def main():
    win = GraphWin("Football Jersey", 500, 400)

    p1 = Point(50, 50)
    p2 = Point(450, 350)
    jersey_objects=[]
    jersey_objects =draw_custom_jersey(win, p1, p2, "REAL MADRID", "PlayerOne", 1,jersey_objects)

    win.getMouse()
    win.close()


if __name__ == '__main__':
    main()
