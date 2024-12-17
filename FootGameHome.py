# mini_game.py

from graphics import *
import random
import time
import mysql.connector

class MiniGame:
    def __init__(self, win):
        """
        Initialize the MiniGame with the given window.
        
        :param win: GraphWin object where the game will be rendered.
        """
        self.win = win
        self.db_config = {
            "host": "matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com",
            "user": "MATCHIEAdmin",
            "password": "IeUniversity123",
            "database": "LaLiga"
        }
        
        # Constants for the mini-game area
        self.MINI_GAME_LEFT = 220
        self.MINI_GAME_TOP = 140
        self.MINI_GAME_RIGHT = 880
        self.MINI_GAME_BOTTOM = 480
        self.SCALE_X = (self.MINI_GAME_RIGHT - self.MINI_GAME_LEFT) / 1100  # Original field width was 1100
        self.SCALE_Y = (self.MINI_GAME_BOTTOM - self.MINI_GAME_TOP) / 700   # Original field height was 700

    def scale_point(self, x, y):
        """
        Scale a point to fit within the mini-game area.
        
        :param x: Original x-coordinate.
        :param y: Original y-coordinate.
        :return: Tuple of scaled (x, y) coordinates.
        """
        scaled_x = self.MINI_GAME_LEFT + (x - 100) * self.SCALE_X
        scaled_y = self.MINI_GAME_TOP + (y - 50) * self.SCALE_Y
        return scaled_x, scaled_y

    def clear_area(self):
        """
        Clear the mini-game area within the window.
        """
        clear_rect = Rectangle(Point(self.MINI_GAME_LEFT, self.MINI_GAME_TOP),
                               Point(self.MINI_GAME_RIGHT, self.MINI_GAME_BOTTOM))
        clear_rect.setFill(color_rgb(224, 224, 224))  # Match the background color of the mini-game area
        clear_rect.setOutline(color_rgb(224, 224, 224))  # Hide border to make clearing look smooth
        clear_rect.draw(self.win)

    def draw_pitch(self):
        """
        Draw the scaled-down football field with alternating green stripes.
        """
        left, top = self.scale_point(100, 50)
        right, bottom = self.scale_point(1200, 750)

        # Draw alternating green stripes
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
            stripe.draw(self.win)

        # Draw field boundary
        boundary = Rectangle(Point(left, top), Point(right, bottom))
        boundary.setOutline("white")
        boundary.setWidth(2)
        boundary.draw(self.win)

        # Draw center line
        center_x, _ = self.scale_point(650, 0)
        top_y = self.scale_point(0, 50)[1]
        bottom_y = self.scale_point(0, 750)[1]
        center_line = Line(Point(center_x, top_y), Point(center_x, bottom_y))
        center_line.setFill("white")
        center_line.draw(self.win)

        # Draw center circle
        center_x, center_y = self.scale_point(650, 400)
        radius = 75 * self.SCALE_X  # Scale circle radius
        center_circle = Circle(Point(center_x, center_y), radius)
        center_circle.setOutline("white")
        center_circle.setWidth(2)
        center_circle.draw(self.win)

        # Draw goal boxes
        left_goal = Rectangle(
            Point(*self.scale_point(100, 300)), Point(*self.scale_point(150, 500))
        )
        right_goal = Rectangle(
            Point(*self.scale_point(1150, 300)), Point(*self.scale_point(1200, 500))
        )
        for goal in [left_goal, right_goal]:
            goal.setOutline("white")
            goal.setWidth(2)
            goal.draw(self.win)

    def draw_scoreboard(self, home_team, away_team):
        """
        Draw the scoreboard higher up in the mini-game area and make it larger.
        
        :param home_team: Name of the home team.
        :param away_team: Name of the away team.
        :return: Text object representing the scoreboard.
        """
        scoreboard_x, scoreboard_y = self.scale_point(650, 100)  # Move the scoreboard higher up
        scoreboard = Text(Point(scoreboard_x, scoreboard_y), f"{home_team} 0 - 0 {away_team}")
        scoreboard.setSize(20)  # Increase the font size to make it more prominent
        scoreboard.setTextColor("white")
        scoreboard.draw(self.win)
        return scoreboard

    def draw_players(self, team_color, positions):
        """
        Draw the scaled-down players.
        
        :param team_color: Color of the team (e.g., "blue", "red").
        :param positions: List of tuples representing player positions.
        :return: List of Circle objects representing players.
        """
        players = []
        for x, y in positions:
            scaled_x, scaled_y = self.scale_point(x, y)
            player = Circle(Point(scaled_x, scaled_y), 6)  # Scaled size for players
            player.setFill(team_color)
            player.draw(self.win)
            players.append(player)
        return players

    def draw_ball(self):
        """
        Draw the scaled-down ball.
        
        :return: Circle object representing the ball.
        """
        x, y = self.scale_point(650, 400)
        ball = Circle(Point(x, y), 5)  # Scaled size for the ball
        ball.setFill("white")
        ball.draw(self.win)
        return ball

    def reset_ball_to_center(self, ball):
        """
        Reset the ball to the center of the field.
        
        :param ball: Circle object representing the ball.
        """
        center_x, center_y = self.scale_point(650, 400)
        dx = center_x - ball.getCenter().getX()
        dy = center_y - ball.getCenter().getY()
        ball.move(dx, dy)

    def move_ball(self, ball, start_point, end_point):
        """
        Move the ball from start_point to end_point.
        
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

    def move_players(self, players):
        """
        Move players randomly within their respective zones.
        
        :param players: List of Circle objects representing players.
        """
        for player in players:
            offset_x = random.randint(-5, 5) * self.SCALE_X
            offset_y = random.randint(-5, 5) * self.SCALE_Y
            player.move(offset_x, offset_y)

    def pass_ball_between_players(self, ball, players):
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

        self.move_ball(ball, start_point, end_point)

    def simulate_goal_attempt(self, ball, scoring_team, strikers):
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

        # Move the ball to the striker before attempting the goal
        self.move_ball(ball, ball_position, striker_position)

        if scoring_team == "home":
            goal_x, goal_y = self.scale_point(1175, random.randint(350, 450))  # Home team aims for the right goal
        else:
            goal_x, goal_y = self.scale_point(125, random.randint(350, 450))   # Away team aims for the left goal

        self.move_ball(ball, (ball.getCenter().getX(), ball.getCenter().getY()), (goal_x, goal_y))
        
        # Assume a 70% chance that the goal is successful
        return random.random() < 0.7

    def update_score(self, scoreboard, home_team, away_team, home_score, away_score):
        """
        Update the score on the scoreboard.
        
        :param scoreboard: Text object representing the scoreboard.
        :param home_team: Name of the home team.
        :param away_team: Name of the away team.
        :param home_score: Current score of the home team.
        :param away_score: Current score of the away team.
        """
        scoreboard.setText(f"{home_team} {home_score} - {away_score} {away_team}")

    def get_random_match(self):
        """
        Connect to the database and retrieve a random match.
        
        :return: Dictionary containing match data or None if an error occurs.
        """
        try:
            # Seed randomness for better results
            random.seed(time.time())

            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Correct SQL query with backticks to handle column names with special characters or spaces
            cursor.execute(
                "SELECT `Home Team`, `Away Team`, `Score` FROM DataDetail ORDER BY RAND() LIMIT 1;"
            )
            match = cursor.fetchone()

            # Close the database connection to ensure fresh state
            cursor.close()
            conn.close()

            if match is None:
                print("No match found in the database.")
                return None

            # Map the match data to variables
            match_data = {
                "Home Team": match[0],
                "Away Team": match[1],
                "Score": match[2]
            }

            return match_data

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None

    def simulate_mini_game(self, home_team, away_team, home_score, away_score):
        """
        Simulate a brief sequence of moves for the mini-game using actual match data.
        
        :param home_team: Name of the home team.
        :param away_team: Name of the away team.
        :param home_score: Target score for the home team.
        :param away_score: Target score for the away team.
        """
        self.draw_pitch()
        scoreboard = self.draw_scoreboard(home_team, away_team)

        # Scaled player positions (4-4-2 formation)
        home_positions = [
            (150, 400), (300, 200), (300, 600), (400, 100), (400, 700),  # Defenders
            (500, 300), (500, 500), (600, 200), (600, 600),              # Midfielders
            (900, 350), (900, 450)                                       # Forwards
        ]
        away_positions = [
            (1150, 400), (1000, 200), (1000, 600), (900, 100), (900, 700),  # Defenders
            (800, 300), (800, 500), (700, 200), (700, 600),                 # Midfielders
            (400, 350), (400, 450)                                         # Forwards
        ]

        players_home = self.draw_players("blue", home_positions)
        players_away = self.draw_players("red", away_positions)
        ball = self.draw_ball()

        current_home_score, current_away_score = 0, 0

        # Set the target scores to the actual scores from the match
        target_home_score = home_score
        target_away_score = away_score

        # Define strikers
        strikers_home = players_home[-2:]  # Last two players are forwards
        strikers_away = players_away[-2:]  # Last two players are forwards

        while current_home_score < target_home_score or current_away_score < target_away_score:
            # Home or Away team passes the ball
            if random.random() < 0.5:
                self.pass_ball_between_players(ball, players_home)  # Home team pass
            else:
                self.pass_ball_between_players(ball, players_away)  # Away team pass

            # Randomly determine if a goal attempt happens by a striker
            if random.random() < 0.5:  # 50% chance for a goal attempt
                if current_home_score < target_home_score and random.random() < 0.5:
                    scoring_team = "home"
                    strikers = strikers_home
                elif current_away_score < target_away_score:
                    scoring_team = "away"
                    strikers = strikers_away
                else:
                    continue  # Both teams have reached their target scores

                success = self.simulate_goal_attempt(ball, scoring_team, strikers)
                if success:
                    if scoring_team == "home":
                        current_home_score += 1
                    else:
                        current_away_score += 1

                    # Update the score
                    self.update_score(scoreboard, home_team, away_team, current_home_score, current_away_score)

                    # Reset ball to center after a goal
                    self.reset_ball_to_center(ball)

            # Check if target scores have been reached to avoid freezing
            if current_home_score >= target_home_score and current_away_score >= target_away_score:
                break

            # Move players randomly during each play
            self.move_players(players_home + players_away)
            time.sleep(0.5)  # Pause briefly for visualization

        # Display the final result
        result_text = Text(Point(550, 600), f"Final Score: {home_team} {target_home_score} - {target_away_score} {away_team}")
        result_text.setSize(12)
        result_text.draw(self.win)
        print(f"Mini-game completed: Final score {home_team} {home_score} - {away_score} {away_team}.")

    def run(self):
        """
        Run the mini-game simulation.
        """
        print("Mini-game initialized.")

        # Clear the mini-game area
        self.clear_area()

        # Fetch a random match
        match_data = self.get_random_match()
        if match_data is None:
            print("No match data available. Exiting mini-game.")
            return

        # Extract match details
        home_team = match_data["Home Team"]
        away_team = match_data["Away Team"]
        try:
            home_score = int(match_data["Score"].split('-')[0])
            away_score = int(match_data["Score"].split('-')[1])
        except (IndexError, ValueError):
            home_score = 0
            away_score = 0

        print(f"Game setup complete: {home_team} vs {away_team}.")

        # Run the simulation
        self.simulate_mini_game(home_team, away_team, home_score, away_score)

