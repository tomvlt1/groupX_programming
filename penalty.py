import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simple Football Game')

# Define colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER1_COLOR = (0, 0, 255)  # Blue
PLAYER2_COLOR = (255, 0, 0)  # Red

# Define player properties
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
player_speed = 5

# Ball properties
BALL_RADIUS = 10

# Define player positions
player1_pos = [WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT * 2]
player2_pos = [WIDTH // 2 - PLAYER_WIDTH // 2, PLAYER_HEIGHT]

# Ball position
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]

# Set up the clock
clock = pygame.time.Clock()

# Scores
player1_score = 0
player2_score = 0

# Font for score display
font = pygame.font.SysFont(None, 36)

def draw_field():
    WINDOW.fill(GREEN)
    # Draw midline
    pygame.draw.line(WINDOW, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)
    # Draw goals
    pygame.draw.rect(WINDOW, WHITE, (0, HEIGHT // 2 - 50, 5, 100))
    pygame.draw.rect(WINDOW, WHITE, (WIDTH - 5, HEIGHT // 2 - 50, 5, 100))

def draw_players():
    # Draw player 1
    pygame.draw.rect(WINDOW, PLAYER1_COLOR, (player1_pos[0], player1_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))
    # Draw player 2
    pygame.draw.rect(WINDOW, PLAYER2_COLOR, (player2_pos[0], player2_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_ball():
    pygame.draw.circle(WINDOW, BLACK, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

def move_ball():
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Ball collision with walls
    if ball_pos[0] <= BALL_RADIUS or ball_pos[0] >= WIDTH - BALL_RADIUS:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # Slow down the ball over time (friction)
    ball_vel[0] *= 0.99
    ball_vel[1] *= 0.99

def check_goal():
    global player1_score, player2_score
    # Left goal
    if ball_pos[0] <= BALL_RADIUS and HEIGHT // 2 - 50 < ball_pos[1] < HEIGHT // 2 + 50:
        player2_score += 1
        reset_ball()
    # Right goal
    if ball_pos[0] >= WIDTH - BALL_RADIUS and HEIGHT // 2 - 50 < ball_pos[1] < HEIGHT // 2 + 50:
        player1_score += 1
        reset_ball()

def reset_positions():
    # Reset player positions
    player1_pos[0] = WIDTH // 2 - PLAYER_WIDTH // 2
    player1_pos[1] = HEIGHT - PLAYER_HEIGHT * 2
    player2_pos[0] = WIDTH // 2 - PLAYER_WIDTH // 2
    player2_pos[1] = PLAYER_HEIGHT

def reset_ball():
    reset_positions()
    ball_pos[0] = WIDTH // 2
    ball_pos[1] = HEIGHT // 2
    ball_vel[0] = 0
    ball_vel[1] = 0

def display_score():
    score_text = font.render(f"{player1_score} : {player2_score}", True, BLACK)
    WINDOW.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

def main():
    running = True
    while running:
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Player 1 controls (Arrow keys)
        if keys[pygame.K_LEFT] and player1_pos[0] > 0:
            player1_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player1_pos[0] < WIDTH - PLAYER_WIDTH:
            player1_pos[0] += player_speed
        if keys[pygame.K_UP] and player1_pos[1] > 0:
            player1_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player1_pos[1] < HEIGHT - PLAYER_HEIGHT:
            player1_pos[1] += player_speed

        # Player 2 controls (WASD)
        if keys[pygame.K_a] and player2_pos[0] > 0:
            player2_pos[0] -= player_speed
        if keys[pygame.K_d] and player2_pos[0] < WIDTH - PLAYER_WIDTH:
            player2_pos[0] += player_speed
        if keys[pygame.K_w] and player2_pos[1] > 0:
            player2_pos[1] -= player_speed
        if keys[pygame.K_s] and player2_pos[1] < HEIGHT - PLAYER_HEIGHT:
            player2_pos[1] += player_speed

        # Collision between player and ball
        player1_rect = pygame.Rect(player1_pos[0], player1_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT)
        player2_rect = pygame.Rect(player2_pos[0], player2_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT)
        ball_rect = pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

        if player1_rect.colliderect(ball_rect):
            ball_vel[0] = 3 * ((ball_pos[0] - (player1_pos[0] + PLAYER_WIDTH / 2)) / PLAYER_WIDTH)
            ball_vel[1] = -3
        if player2_rect.colliderect(ball_rect):
            ball_vel[0] = 3 * ((ball_pos[0] - (player2_pos[0] + PLAYER_WIDTH / 2)) / PLAYER_WIDTH)
            ball_vel[1] = 3

        move_ball()
        check_goal()

        draw_field()
        draw_players()
        draw_ball()
        display_score()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
