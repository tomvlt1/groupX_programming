import graphics
import random
import time

def draw_field(win):
    # Draw the field's boundary
    boundary = graphics.Rectangle(graphics.Point(100, 50), graphics.Point(1200, 750))
    boundary.setWidth(3)
    boundary.setOutline("white")
    boundary.draw(win)

    # Draw center line
    center_line = graphics.Line(graphics.Point(650, 50), graphics.Point(650, 750))
    center_line.setWidth(2)
    center_line.setFill("white")
    center_line.draw(win)

    # Draw center circle
    center_circle = graphics.Circle(graphics.Point(650, 400), 75)
    center_circle.setWidth(2)
    center_circle.setOutline("white")
    center_circle.draw(win)

    # Draw goal boxes
    left_goal_box = graphics.Rectangle(graphics.Point(100, 300), graphics.Point(150, 500))
    left_goal_box.setWidth(3)
    left_goal_box.setOutline("white")
    left_goal_box.draw(win)

    right_goal_box = graphics.Rectangle(graphics.Point(1150, 300), graphics.Point(1200, 500))
    right_goal_box.setWidth(3)
    right_goal_box.setOutline("white")
    right_goal_box.draw(win)

def draw_scoreboard(win, home_team, away_team):
    scoreboard = graphics.Text(graphics.Point(650, 30), f"{home_team} 0 - 0 {away_team}")
    scoreboard.setSize(20)
    scoreboard.setTextColor("white")
    scoreboard.draw(win)
    return scoreboard

def draw_players(win, team_color, positions, is_goalkeeper=False):
    players = []
    for pos in positions:
        player = graphics.Circle(graphics.Point(pos[0], pos[1]), 10)
        player.setFill(team_color if not is_goalkeeper else "yellow")  # Goalkeepers are yellow
        player.draw(win)
        players.append(player)
    return players

def draw_ball(win):
    ball = graphics.Circle(graphics.Point(650, 400), 8)
    ball.setFill("white")
    ball.draw(win)
    return ball

def update_score(scoreboard, home_team, away_team, home_score, away_score):
    scoreboard.setText(f"{home_team} {home_score} - {away_score} {away_team}")

def pass_ball(ball, start_point, end_point):
    # Move ball from start_point to end_point
    while True:
        ball_x = ball.getCenter().getX()
        ball_y = ball.getCenter().getY()

        if abs(ball_x - end_point.getX()) < 5 and abs(ball_y - end_point.getY()) < 5:
            break

        dx = (end_point.getX() - ball_x) / 8  # Slower movement for more realistic speed
        dy = (end_point.getY() - ball_y) / 8  # Slower movement for more realistic speed

        ball.move(dx, dy)
        time.sleep(0.05)

def move_players(players, goalkeeper_positions):
    for i, player in enumerate(players):
        if i in goalkeeper_positions:  # Goalkeeper logic
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            new_x = player.getCenter().getX() + offset_x
            new_y = player.getCenter().getY() + offset_y

            # Check boundaries for goalkeepers
            if 100 <= new_x <= 150 and 300 <= new_y <= 500:  # Home goalkeeper area
                player.move(offset_x, offset_y)
            elif 1150 <= new_x <= 1200 and 300 <= new_y <= 500:  # Away goalkeeper area
                player.move(offset_x, offset_y)
        else:
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            player.move(offset_x, offset_y)

def simulate_goal(ball, players, scoring_team, win):
    # Increase the random offset for player positions before each goal
    for player in players:
        offset_x = random.randint(-20, 20)
        offset_y = random.randint(-20, 20)
        player.move(offset_x, offset_y)
    
    # Determine target players and goal positions based on scoring_team
    if scoring_team == "home":
        target_players = [p for p in players[1:11] if p.getCenter().getX() > 650]  # Home players in opponent's half
        goal_x = 1175  # Home team scores on the right side
        goal_y = random.randint(350, 450)
    else:
        target_players = [p for p in players[12:] if p.getCenter().getX() < 650]  # Away players in opponent's half
        goal_x = 125  # Away team scores on the left side
        goal_y = random.randint(350, 450)

    # Randomize the number of passes before the goal
    num_passes = random.randint(3, 6)
    current_team = scoring_team
    for _ in range(num_passes):
        if random.random() < 0.1:  # 10% chance of the other team stealing the ball
            if current_team == "home":
                current_team = "away"
                target_players = [p for p in players[12:] if p.getCenter().getX() < 650]
                goal_x, goal_y = 125, random.randint(350, 450)  # Away goal target
            else:
                current_team = "home"
                target_players = [p for p in players[1:11] if p.getCenter().getX() > 650]
                goal_x, goal_y = 1175, random.randint(350, 450)  # Home goal target

        # Ensure the ball is passed between players of the same team
        if len(target_players) > 1:
            start_player = random.choice(target_players).getCenter()
            end_player = random.choice([p for p in target_players if p.getCenter() != start_player]).getCenter()
            pass_ball(ball, start_player, end_player)

        # Move players during the game
        move_players(players, goalkeeper_positions=[0, 11])

    # Move the ball towards the correct goal
    end_point = graphics.Point(goal_x, goal_y)
    pass_ball(ball, target_players[-1].getCenter(), end_point)

    # Reset ball to center after goal attempt
    ball.move(650 - ball.getCenter().getX(), 400 - ball.getCenter().getY())

def simulate_match(win, home_team, away_team, final_result):
    home_score, away_score = map(int, final_result.split("-"))
    scoreboard = draw_scoreboard(win, home_team, away_team)
    
    # Player positions in a typical 4-4-2 formation including goalkeepers
    home_positions = [
        (150, 400),  # Goalkeeper
        (300, 200), (300, 600), (400, 100), (400, 700),  # Defenders
        (500, 300), (500, 500), (600, 200), (600, 600),  # Midfielders
        (900, 350), (900, 450)                           # Forwards deep into opponent's half
    ]
    away_positions = [
        (1150, 400),  # Goalkeeper
        (1000, 200), (1000, 600), (900, 100), (900, 700),  # Defenders
        (800, 300), (800, 500), (700, 200), (700, 600),    # Midfielders
        (400, 350), (400, 450)                             # Forwards deep into opponent's half
    ]
    
    players_home = draw_players(win, "blue", home_positions[1:])
    players_away = draw_players(win, "red", away_positions[1:])
    goalkeepers_home = draw_players(win, "yellow", [home_positions[0]], is_goalkeeper=True)
    goalkeepers_away = draw_players(win, "yellow", [away_positions[0]], is_goalkeeper=True)
    players = goalkeepers_home + players_home + goalkeepers_away + players_away
    ball = draw_ball(win)

    current_home_score, current_away_score = 0, 0
    total_goals = home_score + away_score
    goals_sequence = ['home'] * home_score + ['away'] * away_score
    random.shuffle(goals_sequence)  # Randomize the order of goals

    for scoring_team in goals_sequence:
        time.sleep(0.5)  # Shorter wait before the next goal
        simulate_goal(ball, players, scoring_team, win)

        if scoring_team == "home":
            current_home_score += 1
        else:
            current_away_score += 1

        update_score(scoreboard, home_team, away_team, current_home_score, current_away_score)

    # Determine the winning team
    if current_home_score > current_away_score:
        winning_team = home_team
    elif current_away_score > current_home_score:
        winning_team = away_team
    else:
        winning_team = "draw"

    # Call the celebration end screen
    celebration_end_screen(win, winning_team)

import graphics
import random
import time

# Previous functions omitted for brevity...

def celebration_end_screen(win, winning_team):
    # Exaggerated celebration
    # Fade out the field
    rect = graphics.Rectangle(graphics.Point(0, 0), graphics.Point(1300, 800))
    rect.setFill("black")
    rect.setOutline("black")
    rect.draw(win)

    # Display the winning team's name in large, flashy text
    if winning_team == "draw":
        message_text = "It's a Draw!"
    else:
        message_text = f"{winning_team} Wins!"

    message = graphics.Text(graphics.Point(650, 400), message_text)
    message.setSize(36)
    message.setTextColor("gold")
    message.setStyle("bold italic")
    message.draw(win)

    # Create fireworks animation
    for _ in range(15):
        firework_center = graphics.Point(random.randint(100, 1200), random.randint(100, 700))
        for size in range(2, 50, 2):
            # Draw expanding circle as firework
            firework = graphics.Circle(firework_center, size)
            firework.setFill(random.choice(["red", "blue", "green", "yellow", "purple", "pink"]))
            firework.draw(win)
            time.sleep(0.01)
            firework.undraw()

    # Confetti
    confetti = []
    for _ in range(200):
        confetto = graphics.Circle(graphics.Point(random.randint(0, 1300), random.randint(-800, 0)), 2)
        confetto.setFill(random.choice(["red", "blue", "green", "yellow", "purple", "pink", "orange"]))
        confetto.setOutline(confetto.getFill())
        confetto.draw(win)
        confetti.append(confetto)

    # Make confetti fall
    for _ in range(160):
        for confetto in confetti:
            confetto.move(0, 5)
        time.sleep(0.05)

    # Optional: Add more exaggerated elements (e.g., animated stars, moving banners, etc.)

    # Wait for user to close
    win.getMouse()
    win.close()

# Rest of the code omitted for brevity...

def main():
    win = graphics.GraphWin("Football Match Simulation", 1300, 800)
    win.setBackground("dark green")

    draw_field(win)

    home_team = input("Enter home team name: ")
    away_team = input("Enter away team name: ")
    final_result = input("Enter final result (e.g., 3-2): ")

    simulate_match(win, home_team, away_team, final_result)

if __name__ == "__main__":
    main()