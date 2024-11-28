import graphics
import random
import time

# Constants for the mini-game area
MINI_GAME_LEFT = 220
MINI_GAME_TOP = 140
MINI_GAME_RIGHT = 880
MINI_GAME_BOTTOM = 480
SCALE_X = (MINI_GAME_RIGHT - MINI_GAME_LEFT) / 1100  # Original field width was 1100
SCALE_Y = (MINI_GAME_BOTTOM - MINI_GAME_TOP) / 700   # Original field height was 700

def scale_point(x, y):
    """Scale a point to fit within the mini-game area."""
    return MINI_GAME_LEFT + (x - 100) * SCALE_X, MINI_GAME_TOP + (y - 50) * SCALE_Y

def draw_pitch(win):
    """Draw the scaled-down football field with alternating green stripes."""
    left, top = scale_point(100, 50)
    right, bottom = scale_point(1200, 750)

    # Draw alternating green stripes
    stripe_width = (right - left) / 11
    for i in range(11):
        stripe = graphics.Rectangle(
            graphics.Point(left + i * stripe_width, top),
            graphics.Point(left + (i + 1) * stripe_width, bottom)
        )
        if i % 2 == 0:
            stripe.setFill("darkgreen")
        else:
            stripe.setFill("lightgreen")
        stripe.setOutline("lightgreen")
        stripe.draw(win)

    # Draw field boundary
    boundary = graphics.Rectangle(graphics.Point(left, top), graphics.Point(right, bottom))
    boundary.setOutline("white")
    boundary.setWidth(2)
    boundary.draw(win)

    # Draw center line
    center_x, _ = scale_point(650, 0)
    top_y = scale_point(0, 50)[1]
    bottom_y = scale_point(0, 750)[1]
    center_line = graphics.Line(graphics.Point(center_x, top_y), graphics.Point(center_x, bottom_y))
    center_line.setFill("white")
    center_line.draw(win)

    # Draw center circle
    center_x, center_y = scale_point(650, 400)
    radius = 75 * SCALE_X  # Scale circle radius
    center_circle = graphics.Circle(graphics.Point(center_x, center_y), radius)
    center_circle.setOutline("white")
    center_circle.setWidth(2)
    center_circle.draw(win)

    # Draw goal boxes
    left_goal = graphics.Rectangle(
        graphics.Point(*scale_point(100, 300)), graphics.Point(*scale_point(150, 500))
    )
    right_goal = graphics.Rectangle(
        graphics.Point(*scale_point(1150, 300)), graphics.Point(*scale_point(1200, 500))
    )
    for goal in [left_goal, right_goal]:
        goal.setOutline("white")
        goal.setWidth(2)
        goal.draw(win)

def draw_scoreboard(win, home_team, away_team):
    """Draw the scoreboard below the mini-game area."""
    scoreboard_x, scoreboard_y = scale_point(650, 490)
    scoreboard = graphics.Text(graphics.Point(scoreboard_x, scoreboard_y), f"{home_team} 0 - 0 {away_team}")
    scoreboard.setSize(12)  # Adjust font size to fit
    scoreboard.setTextColor("black")
    scoreboard.draw(win)
    return scoreboard

def draw_players(win, team_color, positions, is_goalkeeper=False):
    """Draw the scaled-down players."""
    players = []
    for x, y in positions:
        scaled_x, scaled_y = scale_point(x, y)
        player = graphics.Circle(graphics.Point(scaled_x, scaled_y), 6)  # Scaled size for players
        player.setFill(team_color if not is_goalkeeper else "yellow")  # Goalkeepers are yellow
        player.draw(win)
        players.append(player)
    return players

def draw_ball(win):
    """Draw the scaled-down ball."""
    x, y = scale_point(650, 400)
    ball = graphics.Circle(graphics.Point(x, y), 5)  # Scaled size for the ball
    ball.setFill("white")
    ball.draw(win)
    return ball

def reset_ball_to_center(ball):
    """Reset the ball to the center of the field."""
    center_x, center_y = scale_point(650, 400)
    ball.move(center_x - ball.getCenter().getX(), center_y - ball.getCenter().getY())

def move_ball(ball, start_point, end_point):
    """Move the ball from start_point to end_point."""
    while True:
        ball_x = ball.getCenter().getX()
        ball_y = ball.getCenter().getY()

        if abs(ball_x - end_point[0]) < 3 and abs(ball_y - end_point[1]) < 3:
            break

        dx = (end_point[0] - ball_x) / 8
        dy = (end_point[1] - ball_y) / 8
        ball.move(dx, dy)
        time.sleep(0.05)

def move_players(players, goalkeeper_positions):
    """Move players randomly within their respective zones."""
    for i, player in enumerate(players):
        offset_x = random.randint(-5, 5) * SCALE_X
        offset_y = random.randint(-5, 5) * SCALE_Y
        player.move(offset_x, offset_y)

def pass_ball_between_players(ball, players):
    """Pass the ball between players of the same team."""
    start_player = random.choice(players)
    start_point = (start_player.getCenter().getX(), start_player.getCenter().getY())

    target_player = random.choice(players)
    while target_player == start_player:
        target_player = random.choice(players)
    end_point = (target_player.getCenter().getX(), target_player.getCenter().getY())

    move_ball(ball, start_point, end_point)

def simulate_goal_attempt(ball, scoring_team, strikers):
    """Attempt a goal and move the ball towards the goal."""
    striker = random.choice(strikers)
    ball_position = (ball.getCenter().getX(), ball.getCenter().getY())
    striker_position = (striker.getCenter().getX(), striker.getCenter().getY())

    # Move the ball to the striker before attempting the goal
    move_ball(ball, ball_position, striker_position)

    if scoring_team == "home":
        goal_x, goal_y = scale_point(1175, random.randint(350, 450))  # Home team aims for the right goal
    else:
        goal_x, goal_y = scale_point(125, random.randint(350, 450))   # Away team aims for the left goal

    move_ball(ball, (ball.getCenter().getX(), ball.getCenter().getY()), (goal_x, goal_y))
    
    # Assume a 70% chance that the goal is successful
    return random.random() < 0.7

def simulate_mini_game(win, home_team, away_team):
    """Simulate a brief sequence of moves for the mini-game."""
    draw_pitch(win)
    scoreboard = draw_scoreboard(win, home_team, away_team)

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

    players_home = draw_players(win, "blue", home_positions)
    players_away = draw_players(win, "red", away_positions)
    ball = draw_ball(win)

    current_home_score, current_away_score = 0, 0

    # Generate random target scores between 0-4 for both teams
    target_home_score = random.randint(0, 2)
    target_away_score = random.randint(0, 2)

    # Define strikers
    strikers_home = players_home[-2:]  # Last two players are forwards
    strikers_away = players_away[-2:]  # Last two players are forwards

    while current_home_score < target_home_score or current_away_score < target_away_score:
        # Home or Away team passes the ball
        if random.random() < 0.5:
            pass_ball_between_players(ball, players_home)  # Home team pass
        else:
            pass_ball_between_players(ball, players_away)  # Away team pass

        # Randomly determine if a goal attempt happens by a striker
        if random.random() < 0.3:  # 30% chance for a goal attempt
            scoring_team = random.choice(["home", "away"])
            strikers = strikers_home if scoring_team == "home" else strikers_away
            success = simulate_goal_attempt(ball, scoring_team, strikers)
            if success:
                if scoring_team == "home":
                    current_home_score += 1
                else:
                    current_away_score += 1

                # Update the score
                update_score(scoreboard, home_team, away_team, current_home_score, current_away_score)

                # Reset ball to center after a goal
                reset_ball_to_center(ball)

        # Move players randomly during each play
        move_players(players_home + players_away, goalkeeper_positions=[0, 11])
        time.sleep(0.5)  # Pause briefly for visualization

    # Once the target scores are reached, reset the game
    reset_ball_to_center(ball)
    update_score(scoreboard, home_team, away_team, 0, 0)
    current_home_score, current_away_score = 0, 0

def update_score(scoreboard, home_team, away_team, home_score, away_score):
    """Update the score on the scoreboard."""
    scoreboard.setText(f"{home_team} {home_score} - {away_score} {away_team}")
