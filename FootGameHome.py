from graphics import *
import random
import time
import mysql.connector

def FootGameHomeMain(win):
    """
    Initialize and run the mini-game within the given graphical window.
    
    :param win: GraphWin object where the mini-game will be rendered.
    """
    
    MINI_GAME_LEFT = 220
    MINI_GAME_TOP = 140
    MINI_GAME_RIGHT = 880
    MINI_GAME_BOTTOM = 480
    SCALE_X = (MINI_GAME_RIGHT - MINI_GAME_LEFT) / 1100  
    SCALE_Y = (MINI_GAME_BOTTOM - MINI_GAME_TOP) / 700   
    
    def scale_point(x, y):
        """
        Scale a point to fit within the mini-game area.
        
        :param x: Original x-coordinate.
        :param y: Original y-coordinate.
        :return: Tuple of scaled (x, y) coordinates.
        """
        scaled_x = MINI_GAME_LEFT + (x - 100) * SCALE_X
        scaled_y = MINI_GAME_TOP + (y - 50) * SCALE_Y
        return scaled_x, scaled_y

    def clear_area(left, top, right, bottom):
        """
        Clear a specific area within the existing window by drawing a filled rectangle.
        
        :param left: Left x-coordinate of the area to clear.
        :param top: Top y-coordinate of the area to clear.
        :param right: Right x-coordinate of the area to clear.
        :param bottom: Bottom y-coordinate of the area to clear.
        """
        clear_rect = Rectangle(Point(left, top), Point(right, bottom))
        clear_rect.setFill(color_rgb(224, 224, 224))  
        clear_rect.setOutline(color_rgb(224, 224, 224))
        clear_rect.draw(win)

    def draw_pitch():
        """
        Draw the scaled-down football field with alternating green stripes.
        """
        left, top = scale_point(100, 50)
        right, bottom = scale_point(1200, 750)

        stripe_width = (right - left) / 11
        for i in range(11):
            stripe = Rectangle(
                Point(left + i * stripe_width, top),
                Point(left + (i + 1) * stripe_width, bottom)
            )
            if i % 2 == 0:
                stripe.setFill("darkgreen")
            else:
                stripe.setFill("lightgreen")
            stripe.setOutline("lightgreen")
            stripe.draw(win)

        boundary = Rectangle(Point(left, top), Point(right, bottom))
        boundary.setOutline("white")
        boundary.setWidth(2)
        boundary.draw(win)

        center_x, _ = scale_point(650, 0)
        top_y = scale_point(0, 50)[1]
        bottom_y = scale_point(0, 750)[1]
        center_line = Line(Point(center_x, top_y), Point(center_x, bottom_y))
        center_line.setFill("white")
        center_line.draw(win)

        center_x, center_y = scale_point(650, 400)
        radius = 75 * SCALE_X  
        center_circle = Circle(Point(center_x, center_y), radius)
        center_circle.setOutline("white")
        center_circle.setWidth(2)
        center_circle.draw(win)

        left_goal = Rectangle(
            Point(*scale_point(100, 300)), Point(*scale_point(150, 500))
        )
        right_goal = Rectangle(
            Point(*scale_point(1150, 300)), Point(*scale_point(1200, 500))
        )
        for goal in [left_goal, right_goal]:
            goal.setOutline("white")
            goal.setWidth(2)
            goal.draw(win)

    def draw_scoreboard(home_team, away_team):
        """
        Draw the scoreboard higher up in the mini-game area and make it larger.
        
        :param home_team: Name of the home team.
        :param away_team: Name of the away team.
        :return: Text object representing the scoreboard.
        """
        scoreboard_x, scoreboard_y = scale_point(650, 100)  
        scoreboard = Text(Point(scoreboard_x, scoreboard_y), f"{home_team} 0 - 0 {away_team}")
        scoreboard.setSize(20)  
        scoreboard.setTextColor("white")
        scoreboard.draw(win)
        return scoreboard

    def draw_players(team_color, positions):
        """
        Draw the scaled-down players.
        
        :param team_color: Color of the team (e.g., "blue", "red").
        :param positions: List of tuples representing player positions.
        :return: List of Circle objects representing players.
        """
        players = []
        for x, y in positions:
            scaled_x, scaled_y = scale_point(x, y)
            player = Circle(Point(scaled_x, scaled_y), 6)  
            player.setFill(team_color)
            player.draw(win)
            players.append(player)
        return players

    def draw_ball():
        """
        Draw the scaled-down ball.
        
        :return: Circle object representing the ball.
        """
        x, y = scale_point(650, 400)
        ball = Circle(Point(x, y), 5)  
        ball.setFill("white")
        ball.draw(win)
        return ball

    def reset_ball_to_center(ball):
        """
        Reset the ball to the center of the field.
        
        :param ball: Circle object representing the ball.
        """
        center_x, center_y = scale_point(650, 400)
        dx = center_x - ball.getCenter().getX()
        dy = center_y - ball.getCenter().getY()
        ball.move(dx, dy)

    def move_ball(ball, start_point, end_point):
        """
        Move the ball from start_point to end_point smoothly.
        
        :param ball: Circle object representing the ball.
        :param start_point: Tuple of (x, y) coordinates for the start.
        :param end_point: Tuple of (x, y) coordinates for the end.
        """
        while True:
            ball_x = ball.getCenter().getX()
            ball_y = ball.getCenter().getY()

            if abs(ball_x - end_point[0]) < 3 and abs(ball_y - end_point[1]) < 3:
                break

            dx = (end_point[0] - ball_x) / 8
            dy = (end_point[1] - ball_y) / 8
            ball.move(dx, dy)
            time.sleep(0.05)

    def move_players(players):
        """
        Move players randomly within their respective zones.
        
        :param players: List of Circle objects representing players.
        """
        for player in players:
            offset_x = random.randint(-5, 5) * SCALE_X
            offset_y = random.randint(-5, 5) * SCALE_Y
            player.move(offset_x, offset_y)

    def pass_ball_between_players(ball, players):
        """
        Pass the ball between players of the same team.
        
        :param ball: Circle object representing the ball.
        :param players: List of Circle objects representing players.
        """
        start_player = random.choice(players)
        start_point = (start_player.getCenter().getX(), start_player.getCenter().getY())

        target_player = random.choice(players)
        while target_player == start_player:
            target_player = random.choice(players)
        end_point = (target_player.getCenter().getX(), target_player.getCenter().getY())

        move_ball(ball, start_point, end_point)

    def simulate_goal_attempt(ball, scoring_team, strikers):
        """
        Attempt a goal and move the ball towards the goal.
        
        :param ball: Circle object representing the ball.
        :param scoring_team: String indicating which team is scoring ("home" or "away").
        :param strikers: List of Circle objects representing strikers.
        :return: Boolean indicating if the goal was successful.
        """
        striker = random.choice(strikers)
        ball_position = (ball.getCenter().getX(), ball.getCenter().getY())
        striker_position = (striker.getCenter().getX(), striker.getCenter().getY())

        move_ball(ball, ball_position, striker_position)

        if scoring_team == "home":
            goal_x, goal_y = scale_point(1175, random.randint(350, 450))  
        else:
            goal_x, goal_y = scale_point(125, random.randint(350, 450))   

        move_ball(ball, (ball.getCenter().getX(), ball.getCenter().getY()), (goal_x, goal_y))
        
        return random.random() < 0.7

    def update_score(scoreboard, home_team, away_team, home_score, away_score):
        """
        Update the score on the scoreboard.
        
        :param scoreboard: Text object representing the scoreboard.
        :param home_team: Name of the home team.
        :param away_team: Name of the away team.
        :param home_score: Current score of the home team.
        :param away_score: Current score of the away team.
        """
        scoreboard.setText(f"{home_team} {home_score} - {away_score} {away_team}")

    def get_random_match():
        """
        Connect to the database and retrieve a random match.
        
        :return: Dictionary containing match data or None if an error occurs.
        """
        db_config = {
            "host": "matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com",
            "user": "MATCHIEAdmin",
            "password": "IeUniversity123",
            "database": "LaLiga"
        }
        try:
            random.seed(time.time())

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT `Home Team`, `Away Team`, `Score` FROM DataDetail ORDER BY RAND() LIMIT 1;"
            )
            match = cursor.fetchone()

            cursor.close()
            conn.close()

            if match is None:
                print("No match found in the database.")
                return None

            match_data = {
                "Home Team": match[0],
                "Away Team": match[1],
                "Score": match[2]
            }

            return match_data

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None

    def simulate_mini_game(home_team, away_team, home_score, away_score):
        """
        Simulate a brief sequence of moves for the mini-game using actual match data.
        
        :param home_team: Name of the home team.
        :param away_team: Name of the away team.
        :param home_score: Target score for the home team.
        :param away_score: Target score for the away team.
        """
        draw_pitch()
        scoreboard = draw_scoreboard(home_team, away_team)

        # Scaled player positions (4-4-2 formation)
        home_positions = [
            (150, 400), (300, 200), (300, 600), (400, 100), (400, 700),  
            (500, 300), (500, 500), (600, 200), (600, 600),              
            (900, 350), (900, 450)                                       
        ]
        away_positions = [
            (1150, 400), (1000, 200), (1000, 600), (900, 100), (900, 700), 
            (800, 300), (800, 500), (700, 200), (700, 600),                
            (400, 350), (400, 450)                                         
        ]

        players_home = draw_players("blue", home_positions)
        players_away = draw_players("red", away_positions)
        ball = draw_ball()

        current_home_score, current_away_score = 0, 0

        target_home_score = home_score
        target_away_score = away_score

        strikers_home = players_home[-2:]  
        strikers_away = players_away[-2:]  

        while current_home_score < target_home_score or current_away_score < target_away_score:
            if random.random() < 0.5:
                pass_ball_between_players(ball, players_home)  
            else:
                pass_ball_between_players(ball, players_away)  

            if random.random() < 0.5:  
                if current_home_score < target_home_score and random.random() < 0.5:
                    scoring_team = "home"
                    strikers = strikers_home
                elif current_away_score < target_away_score:
                    scoring_team = "away"
                    strikers = strikers_away
                else:
                    continue  

                success = simulate_goal_attempt(ball, scoring_team, strikers)
                if success:
                    if scoring_team == "home":
                        current_home_score += 1
                    else:
                        current_away_score += 1

                    update_score(scoreboard, home_team, away_team, current_home_score, current_away_score)

                    reset_ball_to_center(ball)

            if current_home_score >= target_home_score and current_away_score >= target_away_score:
                break

            move_players(players_home + players_away)
            time.sleep(0.5)  

        result_text = Text(Point(550, 600), f"Final Score: {home_team} {target_home_score} - {target_away_score} {away_team}")
        result_text.setSize(12)
        result_text.draw(win)
        print(f"Mini-game completed: Final score {home_team} {current_home_score} - {current_away_score} {away_team}.")

    def get_random_match():
        """
        Connect to the database and retrieve a random match.
        
        :return: Dictionary containing match data or None if an error occurs.
        """
        db_config = {
            "host": "matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com",
            "user": "MATCHIEAdmin",
            "password": "IeUniversity123",
            "database": "LaLiga"
        }
        try:
            random.seed(time.time())

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT `Home Team`, `Away Team`, `Score` FROM DataDetail ORDER BY RAND() LIMIT 1;"
            )
            match = cursor.fetchone()

            cursor.close()
            conn.close()

            if match is None:
                print("No match found in the database.")
                return None

            match_data = {
                "Home Team": match[0],
                "Away Team": match[1],
                "Score": match[2]
            }

            return match_data

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None

    def simulate_mini_game(home_team, away_team, home_score, away_score):
        """
        Simulate a brief sequence of moves for the mini-game using actual match data.
        
        :param home_team: Name of the home team.
        :param away_team: Name of the away team.
        :param home_score: Target score for the home team.
        :param away_score: Target score for the away team.
        """
        draw_pitch()
        scoreboard = draw_scoreboard(home_team, away_team)

        home_positions = [
            (150, 400), (300, 200), (300, 600), (400, 100), (400, 700),  
            (500, 300), (500, 500), (600, 200), (600, 600),              
            (900, 350), (900, 450)                                       
        ]
        away_positions = [
            (1150, 400), (1000, 200), (1000, 600), (900, 100), (900, 700),
            (800, 300), (800, 500), (700, 200), (700, 600),               
            (400, 350), (400, 450)                                        
        ]

        players_home = draw_players("blue", home_positions)
        players_away = draw_players("red", away_positions)
        ball = draw_ball()

        current_home_score, current_away_score = 0, 0

        target_home_score = home_score
        target_away_score = away_score

        
        strikers_home = players_home[-2:]  
        strikers_away = players_away[-2:]  

        while current_home_score < target_home_score or current_away_score < target_away_score:
        
            if random.random() < 0.5:
                pass_ball_between_players(ball, players_home)
            else:
                pass_ball_between_players(ball, players_away)

            if random.random() < 0.5:  
                if current_home_score < target_home_score and random.random() < 0.5:
                    scoring_team = "home"
                    strikers = strikers_home
                elif current_away_score < target_away_score:
                    scoring_team = "away"
                    strikers = strikers_away
                else:
                    continue  

                success = simulate_goal_attempt(ball, scoring_team, strikers)
                if success:
                    if scoring_team == "home":
                        current_home_score += 1
                    else:
                        current_away_score += 1

                    update_score(scoreboard, home_team, away_team, current_home_score, current_away_score)

                    reset_ball_to_center(ball)

            if current_home_score >= target_home_score and current_away_score >= target_away_score:
                break

            move_players(players_home + players_away)
            time.sleep(0.5)  

        result_text = Text(Point(550, 600), f"Final Score: {home_team} {target_home_score} - {target_away_score} {away_team}")
        result_text.setSize(12)
        result_text.draw(win)
        print(f"Mini-game completed: Final score {home_team} {current_home_score} - {current_away_score} {away_team}.")

    print("Mini-game initialized.")

    clear_area(MINI_GAME_LEFT, MINI_GAME_TOP, MINI_GAME_RIGHT, MINI_GAME_BOTTOM)

    match_data = get_random_match()
    if match_data is None:
        print("No match data available. Exiting mini-game.")
        return

    home_team = match_data["Home Team"]
    away_team = match_data["Away Team"]
    try:
        home_score = int(match_data["Score"].split('-')[0])
        away_score = int(match_data["Score"].split('-')[1])
    except (IndexError, ValueError):
        home_score = 0
        away_score = 0

    print(f"Game setup complete: {home_team} vs {away_team}.")

    simulate_mini_game(home_team, away_team, home_score, away_score)
    print(f"Mini-game completed: Final score {home_team} {home_score} - {away_score} {away_team}.")
