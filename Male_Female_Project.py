import pygame
import sys

pygame.init()

# Screen setup
screen_w = 1000
screen_h = 353
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Male Walking")

# Sprite sheet setup
fps = 10
f1_w = 87
f1_h = 93
frame_count = 3

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

speed = 6
frame_delay = 5

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(fps)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement input
    keys = pygame.key.get_pressed()
    moving = False  # This controls player1 animation

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
        
    # Draw sprites
    screen.blit(background, (0, 0))
    screen.blit(sprite1, (player1["x"], player1["y"]))
    screen.blit(sprite2, (player2["x"], player2["y"]))
    pygame.display.update()

pygame.quit()
sys.exit()