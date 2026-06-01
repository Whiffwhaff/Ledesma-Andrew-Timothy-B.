import tkinter as tk
import random

# ======================
# WINDOW
# ======================
WIDTH = 500
HEIGHT = 600

root = tk.Tk()
root.title("Texxt Galaga By Ledesma,Andrew Timothy B.")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# ======================
# GAME VARIABLES
# ======================
score = 0
lives = 3
level = 1
max_levels = 5
boss_health = 25

game_started = False
game_over = False

player_x = WIDTH // 2
player_y = HEIGHT - 50

bullets = []
enemy_bullets = []
enemies = []

enemy_direction = 1

# ======================
# PLAYER
# ======================
player = canvas.create_text(
    player_x,
    player_y,
    text="A",
    fill="cyan",
    font=("Arial", 22, "bold")
)

# ======================
# UI
# ======================
score_text = canvas.create_text(
    70, 20,
    text="Score: 0",
    fill="white",
    font=("Arial", 12)
)

level_text = canvas.create_text(
    WIDTH - 70, 20,
    text="Level 1",
    fill="white",
    font=("Arial", 12)
)

lives_text = canvas.create_text(
    WIDTH // 2, 20,
    text="Lives: 3",
    fill="white",
    font=("Arial", 12)
)

# ======================
# MENU
# ======================
title = canvas.create_text(
    WIDTH // 2,
    HEIGHT // 2 - 60,
    text="MINI GALAGA",
    fill="yellow",
    font=("Arial", 28, "bold")
)

start_text = canvas.create_text(
    WIDTH // 2,
    HEIGHT // 2,
    text="Press SPACE to Start",
    fill="white",
    font=("Arial", 16)
)

controls = canvas.create_text(
    WIDTH // 2,
    HEIGHT // 2 + 40,
    text="← → Move | SPACE Shoot",
    fill="lightblue",
    font=("Arial", 12)
)

# ======================
# CREATE LEVEL
# ======================
def create_level():
    global enemies

    enemies.clear()

    rows = 2
    cols = min((6, 2 + level))

    start_x = 80
    start_y = 60

    spacing_x = 70
    spacing_y = 50

    for row in range(rows):
        for col in range(cols):

            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            enemy = canvas.create_text(
                x,
                y,
                text="W",
                fill="red",
                font=("Arial", 20, "bold")
            )

            enemies.append(enemy)

# ======================
# CREATE BOSS
# ======================
def create_boss():
    global boss

    boss = canvas.create_text(
        WIDTH // 2,
        100,
        text="M",
        fill="orange",
        font=("Arial", 50, "bold")
    )

# ======================
# START GAME
# ======================
def start_game(event=None):
    global game_started

    if not game_started:
        game_started = True

        canvas.delete(title)
        canvas.delete(start_text)
        canvas.delete(controls)

        create_level()

        enemy_shoot()

        update_game()

    else:
        shoot()

# ======================
# PLAYER MOVEMENT
# ======================
def move_left(event):
    global player_x

    if not game_over:
        player_x -= 20

        if player_x < 20:
            player_x = 20

        canvas.coords(player, player_x, player_y)

def move_right(event):
    global player_x

    if not game_over:
        player_x += 20

        if player_x > WIDTH - 20:
            player_x = WIDTH - 20

        canvas.coords(player, player_x, player_y)

# ======================
# PLAYER SHOOT
# ======================
def shoot():
    bullet = canvas.create_text(
        player_x,
        player_y - 20,
        text="|",
        fill="white",
        font=("Arial", 18)
    )

    bullets.append(bullet)

# ======================
# ENEMY SHOOT
# ======================
def enemy_shoot():

    if game_over:
        return

    if level < max_levels and enemies:

        enemy = random.choice(enemies)

        ex, ey = canvas.coords(enemy)

        bullet = canvas.create_text(
            ex,
            ey + 20,
            text="!",
            fill="yellow",
            font=("Arial", 18, "bold")
        )

        enemy_bullets.append(bullet)

    elif level == max_levels:

        bx, by = canvas.coords(boss)

        bullet = canvas.create_text(
            bx,
            by + 40,
            text="!",
            fill="orange",
            font=("Arial", 22, "bold")
        )

        enemy_bullets.append(bullet)

    root.after(1200, enemy_shoot)

# ======================
# UPDATE UI
# ======================
def update_ui():
    canvas.itemconfig(score_text, text=f"Score: {score}")
    canvas.itemconfig(level_text, text=f"Level {level}")
    canvas.itemconfig(lives_text, text=f"Lives: {lives}")

# ======================
# GAME OVER
# ======================
def game_over_screen():
    global game_over

    game_over = True

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text="GAME OVER",
        fill="red",
        font=("Arial", 32, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 40,
        text=f"Final Score: {score}",
        fill="white",
        font=("Arial", 16)
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 80,
        text="Press R to Retry",
        fill="yellow",
        font=("Arial", 14)
    )

# ======================
# WIN SCREEN
# ======================
def win_screen():
    global game_over

    game_over = True

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text="YOU WIN!",
        fill="yellow",
        font=("Arial", 32, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 40,
        text=f"Final Score: {score}",
        fill="white",
        font=("Arial", 16)
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 80,
        text="Press R to Play Again",
        fill="lightgreen",
        font=("Arial", 14)
    )

# ======================
# RETRY GAME
# ======================
def retry_game(event=None):
    global score
    global lives
    global level
    global boss_health
    global game_over
    global game_started
    global bullets
    global enemy_bullets
    global enemies
    global player
    global score_text
    global level_text
    global lives_text
    global enemy_direction

    canvas.delete("all")

    score = 0
    lives = 3
    level = 1
    boss_health = 25

    game_over = False
    game_started = True

    enemy_direction = 1

    bullets = []
    enemy_bullets = []
    enemies = []

    player = canvas.create_text(
        player_x,
        player_y,
        text="A",
        fill="cyan",
        font=("Arial", 22, "bold")
    )

    score_text = canvas.create_text(
        70, 20,
        text="Score: 0",
        fill="white",
        font=("Arial", 12)
    )

    level_text = canvas.create_text(
        WIDTH - 70, 20,
        text="Level 1",
        fill="white",
        font=("Arial", 12)
    )

    lives_text = canvas.create_text(
        WIDTH // 2, 20,
        text="Lives: 3",
        fill="white",
        font=("Arial", 12)
    )

    create_level()

    update_game()

# ======================
# UPDATE GAME
# ======================
def update_game():
    global score
    global lives
    global level
    global boss_health
    global enemy_direction

    if game_over:
        return

    # ======================
    # PLAYER BULLETS
    # ======================
    for bullet in bullets[:]:

        canvas.move(bullet, 0, -10)

        bx, by = canvas.coords(bullet)

        if by < 0:
            canvas.delete(bullet)

            if bullet in bullets:
                bullets.remove(bullet)

    # ======================
    # ENEMY BULLETS
    # ======================
    for bullet in enemy_bullets[:]:

        canvas.move(bullet, 0, 8)

        bx, by = canvas.coords(bullet)

        # Hit player
        if abs(bx - player_x) < 20 and abs(by - player_y) < 20:

            canvas.delete(bullet)

            if bullet in enemy_bullets:
                enemy_bullets.remove(bullet)

            lives -= 1

            update_ui()

            if lives <= 0:
                game_over_screen()
                return

        elif by > HEIGHT:

            canvas.delete(bullet)

            if bullet in enemy_bullets:
                enemy_bullets.remove(bullet)

    # ======================
    # NORMAL LEVELS
    # ======================
    if level < max_levels:

        change_direction = False

        # Move enemies horizontally
        for enemy in enemies:

            canvas.move(enemy, enemy_direction * (1 + level * 0.5), 0)

            ex, ey = canvas.coords(enemy)

            # Screen edge
            if ex > WIDTH - 30 or ex < 30:
                change_direction = True

        # Move downward
        if change_direction:

            enemy_direction *= -1

            for enemy in enemies:
                canvas.move(enemy, 0, 20)

        # Bullet collision
        for enemy in enemies[:]:

            ex, ey = canvas.coords(enemy)

            # Enemy reaches bottom
            if ey > HEIGHT - 120:

                lives -= 1

                canvas.delete(enemy)

                if enemy in enemies:
                    enemies.remove(enemy)

                update_ui()

                if lives <= 0:
                    game_over_screen()
                    return

            for bullet in bullets[:]:

                bx, by = canvas.coords(bullet)

                if abs(ex - bx) < 20 and abs(ey - by) < 20:

                    canvas.delete(enemy)
                    canvas.delete(bullet)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    if bullet in bullets:
                        bullets.remove(bullet)

                    score += 10

                    update_ui()

        # Next level
        if len(enemies) == 0:

            level += 1

            update_ui()

            if level == max_levels:
                create_boss()
            else:
                create_level()

    # ======================
    # BOSS LEVEL
    # ======================
    elif level == max_levels:

        move = random.choice([-15, 15])

        canvas.move(boss, move, 0)

        bx, by = canvas.coords(boss)

        if bx < 50:
            canvas.move(boss, 30, 0)

        if bx > WIDTH - 50:
            canvas.move(boss, -30, 0)

        # Bullet hits boss
        for bullet in bullets[:]:

            bullet_x, bullet_y = canvas.coords(bullet)

            if abs(bx - bullet_x) < 50 and abs(by - bullet_y) < 50:

                canvas.delete(bullet)

                if bullet in bullets:
                    bullets.remove(bullet)

                boss_health -= 1

                score += 20

                update_ui()

        if boss_health <= 0:

            canvas.delete(boss)

            win_screen()

            return

    root.after(50, update_game)

# ======================
# CONTROLS
# ======================
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<space>", start_game)

root.bind("r", retry_game)
root.bind("R", retry_game)

# ======================
# RUN GAME
# ======================
root.mainloop()