import pygame
import sys

pygame.init()

# Screen setup
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Male Walking")

# Sprite sheet setup
fps = 10
f1_w = 87
f1_h = 93
frame_count = 3

title_font = pygame.font.SysFont("Arial", 72, bold=True)
button_font = pygame.font.SysFont("Arial", 36)
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont("Arial", 64, bold=True)

game_state = "menu"
volume_on = True

background = pygame.image.load("Male_Female_Background.png")

pygame.mixer.music.load("Male_Female_MP3.mp3")
pygame.mixer.music.play(-1)

sprite_sheet1 = pygame.image.load("M_01.png").convert_alpha()
sprite_sheet2 = pygame.image.load("F_01.png").convert_alpha()
print("Image size:", sprite_sheet1.get_width(), "x", sprite_sheet1.get_height())
print("Image size:", sprite_sheet2.get_width(), "x", sprite_sheet2.get_height())

# Function to extract frames from one row
def get_frames(col, sheet):
    frames = []
    for row in range(frame_count): #00 01 02
        rect = pygame.Rect(col * f1_w, row * f1_h, f1_w, f1_h)
        if rect.right <= sheet.get_width() and rect.bottom <= sheet.get_height():
            frames.append(sheet.subsurface(rect))
    return frames

# Load animation frames
walk_down_1= get_frames(0, sprite_sheet1)
walk_left_1 = get_frames(3, sprite_sheet1)
walk_right_1= get_frames(1, sprite_sheet1)
walk_up_1 = get_frames(2, sprite_sheet1)

#============= PLAYER 2
walk_down_2= get_frames(0, sprite_sheet2)
walk_left_2 = get_frames(3, sprite_sheet2)
walk_right_2= get_frames(1, sprite_sheet2)
walk_up_2 = get_frames(2, sprite_sheet2)

# Position and animation setup
player1={"x":100, "y":100, "dir":"down", "frame":0, "timer":0}
player2={"x":300, "y":100, "dir":"down", "frame":0, "timer":0}

# Jump variables
player1_jump = False
player1_vel_y = 0
player1_ground = 100  # initial y
player2_jump = False
player2_vel_y = 0
player2_ground = 100  # initial y
GRAVITY = 1
JUMP_STRENGTH = 18

you_win = False
you_win_timer = 30

speed = 6
frame_delay = 5

def draw_menu():
    screen.fill((30, 30, 30))
    title = title_font.render("Male and Female Walking", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    start_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)
    pygame.draw.rect(screen, (0, 255, 0), start_rect)
    start_text = button_font.render("START", True, (255, 255, 255))
    screen.blit(start_text, (start_rect.centerx - start_text.get_width() // 2, start_rect.centery - start_text.get_height() // 2))

    volume_text = "VOLUME: ON" if volume_on else "VOLUME: OFF"
    volume_rect = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, (100, 100, 200), volume_rect)
    text = button_font.render(volume_text, True, (255, 255, 255))
    screen.blit(text, (volume_rect.centerx - text.get_width() // 2, volume_rect.centery - text.get_height() // 2))

    return start_rect, volume_rect

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(fps)
    screen.fill((30, 30, 30))

    if game_state == "menu":
        start_button, volume_button = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    # Change window size when game starts
                    WIDTH = 1000
                    HEIGHT = 353
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    game_state = "playing"
                elif volume_button.collidepoint(event.pos):
                    volume_on = not volume_on
                    pygame.mixer.music.set_volume(0.3 if volume_on else 0.0)
        pygame.display.update()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement input
    keys = pygame.key.get_pressed()
    moving = False  # This controls player1 animation

    if keys[pygame.K_m]:
        volume_on = not volume_on
        pygame.mixer.music.set_volume(0.3 if volume_on else 0.0)
        pygame.time.wait(200)

    # --- PLAYER 1 JUMP ---
    if not player1_jump and keys[pygame.K_SPACE]:
        player1_jump = True
        player1_vel_y = -JUMP_STRENGTH
    if player1_jump:
        player1["y"] += player1_vel_y
        player1_vel_y += GRAVITY
        if player1["y"] >= player1_ground:
            player1["y"] = player1_ground
            player1_jump = False
            player1_vel_y = 0

    # Only allow movement if not jumping
    if not player1_jump:
        if keys[pygame.K_RIGHT]:
            player1["x"] += speed
            player1["dir"]  = "right"
            moving = True
        elif keys[pygame.K_LEFT]:
            player1["x"]  -= speed
            player1["dir"] = "left"
            moving = True
        elif keys[pygame.K_UP]:
            player1["y"]  -= speed
            player1["dir"] = "up"
            moving = True
        elif keys[pygame.K_DOWN]:
            player1["y"]  += speed
            player1["dir"]= "down"
            moving = True

    # Animate only when moving - FIXED: using 'moving' instead of 'moving1'
    if moving:
        player1["timer"] += 1
        if player1["timer"] >= frame_delay:
            player1["timer"] = 0
            player1["frame"] = (player1["frame"] + 1) % len(walk_down_1)
    else:
        player1["frame"] = 0  # idle pose

    # Player 2 movement
    moving2 = False
    # --- PLAYER 2 JUMP ---
    if not player2_jump and keys[pygame.K_LSHIFT]:
        player2_jump = True
        player2_vel_y = -JUMP_STRENGTH
    if player2_jump:
        player2["y"] += player2_vel_y
        player2_vel_y += GRAVITY
        if player2["y"] >= player2_ground:
            player2["y"] = player2_ground
            player2_jump = False
            player2_vel_y = 0
    # Only allow movement if not jumping
    if not player2_jump:
        if keys[pygame.K_d]:
            player2["x"] += speed
            player2["dir"]  = "right"
            moving2 = True
        elif keys[pygame.K_a]:
            player2["x"]  -= speed
            player2["dir"] = "left"
            moving2 = True
        elif keys[pygame.K_w]:
            player2["y"]  -= speed
            player2["dir"] = "up"
            moving2 = True
        elif keys[pygame.K_s]:
            player2["y"]  += speed
            player2["dir"]= "down"
            moving2 = True

    # Animate only when moving
    if moving2:
        player2["timer"] += 1
        if player2["timer"] >= frame_delay:
            player2["timer"] = 0
            player2["frame"] = (player2["frame"] + 1) % len(walk_down_2)
    else:
        player2["frame"] = 0  # idle pose
    
    # Choose correct frame based on direction for player1
    if player1["dir"] == "right":
        sprite1 = walk_right_1[player1["frame"]]
    elif player1["dir"] == "left":
        sprite1 = walk_left_1[player1["frame"]]
    elif player1["dir"] == "up":
        sprite1 = walk_up_1[player1["frame"]]
    else:
        sprite1 = walk_down_1[player1["frame"]]

    # Choose correct frame based on direction for player2
    if player2["dir"] == "right":
        sprite2= walk_right_2[player2["frame"]]
    elif player2["dir"] == "left":
        sprite2 = walk_left_2[player2["frame"]]
    elif player2["dir"] == "up":
        sprite2 = walk_up_2[player2["frame"]]
    else:
        sprite2 = walk_down_2[player2["frame"]]

    if you_win:
        if you_win_timer > 0:
            text = big_font.render("YOU WIN!", True, (255, 255, 0))
            alpha = int((1 - you_win_timer / 30) * 255)
            text.set_alpha(alpha)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            you_win_timer -= 1
        else:
            text = big_font.render("YOU WIN!", True, (0, 255, 0))
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    # Draw sprites
    screen.blit(background, (0, 0))
    screen.blit(sprite1, (player1["x"], player1["y"]))
    screen.blit(sprite2, (player2["x"], player2["y"]))
    pygame.display.update()

pygame.quit()
sys.exit()
