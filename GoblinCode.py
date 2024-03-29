import pygame
import random

pygame.init() # initialize all of pygame

pygame.display.set_caption("Goblin Code") # set the window title
screen = pygame.display.set_mode((1280, 720)) # set the window size

clock = pygame.time.Clock() # create a clock object to help control the frame rate
running = True
dt = 0 # delta time

center_pos = (screen.get_width() / 2, screen.get_height() / 2)

game_state = "start_menu"

bullets = [] # List to store bullets
bullet_cooldown = 0  # Time since the last bullet was shot
bullet_cooldown_max = 0.5  # 0.5 seconds cooldown between bullets

enemies = []  # List to store enemies
enemy_spawn_timer = 0 # Time since the last enemy was spawned
enemy_spawn_interval = 1.7  # Spawn an enemy every 1.7 seconds

git_commits = []  # List to store git commits
git_commit_spawn_timer = 0 # Time since the last git commit was spawned
git_commit_spawn_interval = 30  # Spawn a git commit every 30 seconds

high_score = 0  # Player's high score

# start menu
def draw_start_menu():

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # draw a start page with the title <Goblin Code/> and instructions to start
    title_font = pygame.font.Font('./SourceCodePro.ttf', 100)
    title_text = title_font.render('<Goblin Code/>', False, (255, 255, 255))
    screen.blit(title_text, (center_pos[0] - title_text.get_width() / 2, center_pos[1] - title_text.get_height()))

    # draw the start instructions
    start_font = pygame.font.Font('./SourceCodePro.ttf', 30)
    start_text = start_font.render('Press enter to start...', False, (255, 255, 255))
    screen.blit(start_text, (center_pos[0] - start_text.get_width() / 2, center_pos[1] + 50 + 5))

    # update the display
    pygame.display.update()

# game over screen
def draw_game_over_screen():

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # draw a game over page with the title <Game Over/> and a restart and quit button
    game_over_font = pygame.font.Font('./SourceCodePro.ttf', 100)
    game_over_text = game_over_font.render('<Game Over/>', False, (255, 255, 255))
    screen.blit(game_over_text, (center_pos[0] - game_over_text.get_width() / 2, center_pos[1] - game_over_text.get_height()))

    # draw the restart button text
    restart_font = pygame.font.Font('./SourceCodePro.ttf', 30)
    restart_text = restart_font.render('Press R to restart...', False, (255, 255, 255))
    screen.blit(restart_text, (center_pos[0] - restart_text.get_width() / 2, center_pos[1] + 50 + 5))

    # draw the quit button text
    quit_font = pygame.font.Font('./SourceCodePro.ttf', 30)
    quit_text = quit_font.render('Press Q to quit...', False, (255, 255, 255))
    screen.blit(quit_text, (center_pos[0] - quit_text.get_width() / 2, center_pos[1] + 100 + 5))

    # update the display
    pygame.display.update()

while running:

    # pygame.QUIT event means the user clicked X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # start menu
    if game_state == "start_menu":
        draw_start_menu()

        # check for the enter key to start the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            player_x = 200
            player_y = 430

            lives = 3 # Set the number of lives
            score = 0 # Set the score to 0

            game_state = "game"
    
    # run game over screen
    elif game_state == "game_over":
        draw_game_over_screen()

        # check for the r key to restart the game or the q key to quit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_state = "start_menu"
        if keys[pygame.K_q]:
            pygame.quit()
            quit()

    elif game_state == "game":

        # fill the screen with black to wipe away anything from last frame
        screen.fill("black")

        # draw the ground as the image './floor_<option>.png'
        floor = pygame.image.load('./floor_2.png')
        floor = pygame.transform.scale(floor, (screen.get_width(), 190))
        screen.blit(floor, (0, screen.get_height() - 190))

        # display the lives as X's
        lives_text = pygame.font.Font('./SourceCodePro.ttf', 17).render(f'{"X " * lives}', False, (255, 0, 0))
        screen.blit(lives_text, (85, 589))  # Position the lives count

        # display the current score
        score_text = pygame.font.Font('./SourceCodePro.ttf', 17).render(f'{score}', False, (0, 0, 255))
        screen.blit(score_text, (160, 631))  # Position the current score

        # display the high score
        high_score_text = pygame.font.Font('./SourceCodePro.ttf', 17).render(f'{high_score}', False, (0, 0, 0))
        screen.blit(high_score_text, (132, 652))  # Position the high score

        ############
        ## PLAYER ##
        ############

        # draw the player on the bottom left side of the screen on top of the ground
        # player image path is './player.png'
        player = pygame.image.load('./player.png')
        player = pygame.transform.scale(player, (100, 100))
        screen.blit(player, (player_x, player_y))

        # create a rectangle for the player
        player_rect = pygame.Rect(player_x, player_y, player.get_width(), player.get_height())

        # set the lowest x and y values for the player
        if player_x < 0:
            player_x = 0
        if player_y < 0:
            player_y = 0
        
        # set the highest x and y values for the player
        if player_x > screen.get_width() - player.get_width():
            player_x = screen.get_width() - player.get_width()
        if player_y > screen.get_height() - player.get_height() - 190:
            player_y = screen.get_height() - player.get_height() - 190

        # add gravity to the player
        ''' DO THIS LATER I"M RUNNING OUT OF TIME! '''

        # create player movement with wasd keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= 5
        if keys[pygame.K_d]:
            player_x += 5
        if keys[pygame.K_w]:
            player_y -= 5
        if keys[pygame.K_s]:
            player_y += 5
        
        #############
        ## BULLETS ##
        #############

        if bullet_cooldown > 0:
            bullet_cooldown -= dt  # Decrease cooldown timer by the delta time

        # shoot a text bullet with the space bar
        # the bullet moves continously to the right until it goes off screen
        if keys[pygame.K_SPACE] and bullet_cooldown <= 0:
        
            # Create a new bullet at the player's position
            new_bullet = {
                "x": player_x + 80,
                "y": player_y + 40,
                "speed": 10  # Speed at which the bullet moves
            }

            bullets.append(new_bullet)  # Add the new bullet to the bullets list

            bullet_cooldown = bullet_cooldown_max  # Reset the bullet cooldown

        # Draw the bullets
        for bullet in bullets:
            bullet["x"] += bullet["speed"]  # Move the bullet

            bullet_font = pygame.font.Font('./SourceCodePro.ttf', 30)  # Define the font
            
            bullet_text = bullet_font.render('</>', False, (255, 255, 255))  # bullet text

            bullet_width, bullet_height = bullet_font.size('</>')  # Get the size of the text

            screen.blit(bullet_text, (bullet["x"], bullet["y"])) # Draw the bullet

        bullets = [bullet for bullet in bullets if bullet["x"] < screen.get_width()]  # Remove bullets that have gone off screen

        ############
        ## ENEMYS ##
        ############

        # Handle enemy spawning and movement
        enemy_spawn_timer -= dt
        if enemy_spawn_timer <= 0:

            enemy_font = pygame.font.Font('./SourceCodePro.ttf', 30)  # Define the font
            
            enemy_text_list = [
                "ERR 404",
                "ERR 500",
                "ERR 403",
                "ERR 401",
                "ERR 400",
                "Syntax ERR",
                "Null Pointer",
                "Type ERR",
                "Key ERR",
                "File Not Found",
                "Index ERR",
                "Value ERR",
                "Memory ERR",
                "Name ERR",
                "Overflow ERR",
                "Recursion ERR",
                "Indentation ERR",
                "Import ERR",
                "Attribute ERR",
                "Assertion ERR",
                "Floating Point ERR",
                "Zero Division ERR",
                "Keyboard Interrupt",
                "System ERR",
            ]

            enemy_text = random.choice(enemy_text_list)  # Randomly select a text from the list
            enemy_speed = random.randint(5, 15)  # Random speed for the enemy

            enemy_width, enemy_height = enemy_font.size(enemy_text)  # Get the size of the text

            new_enemy = {
                "x": screen.get_width(),  # Start at the right edge of the screen
                "y": random.randint(50, screen.get_height() - 220),  # Random height
                "speed": enemy_speed,  # Speed at which the enemy moves
                "text": enemy_text # The text to display 
            }

            enemies.append(new_enemy) # Add the new enemy to the enemies list
            enemy_spawn_timer = enemy_spawn_interval # Reset the spawn timer
            
        # Draw the enemies and check for collision with the player
        for enemy in enemies:
            enemy["x"] -= enemy["speed"]  # Move the enemy towards the left

            enemy_text = pygame.font.Font('./SourceCodePro.ttf', 30).render(enemy["text"], False, (255, 0, 0))
            screen.blit(enemy_text, (enemy["x"], enemy["y"]))

            # set the enemy's width and height
            enemy_width, enemy_height = enemy_font.size(enemy["text"])

            # Create a rectangle for the enemy
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)  # enemy_height as before

            # Check for collision with the player
            if player_rect.colliderect(enemy_rect):
                # Collision detected, remove enemy
                enemies.remove(enemy)

                # Decrease life
                lives -= 1
                if lives <= 0:
                    game_state = "game_over"  # Switch to a game over state
                break  # Exit the loop to avoid modifying the list during iteration

        enemies = [enemy for enemy in enemies if enemy["x"] + enemy_width > 0]  # Remove enemies that have gone off screen

        #################
        ## Git Commits ##
        #################

        # Handle git commit spawning
        git_commit_spawn_timer -= dt
        if git_commit_spawn_timer <= 0:
            new_git_commit = {
                "x": screen.get_width(),  # Start at the right edge of the screen
                "y": random.randint(50, screen.get_height() - 220),  # Random height
                "speed": 5  # Speed at which the git commit moves
            }
            git_commits.append(new_git_commit)
            git_commit_spawn_timer = git_commit_spawn_interval

        # Draw the git commits and check for collision with the player
        for git_commit in git_commits:
            git_commit["x"] -= git_commit["speed"]
        
            git_commit_font = pygame.font.Font('./SourceCodePro.ttf', 30)  # Define the font
            git_commit_text = git_commit_font.render('Git Commit', False, (0, 255, 0))  # git commit text
            git_commit_width, git_commit_height = git_commit_font.size('git commit')  # Get the size of the text
            screen.blit(git_commit_text, (git_commit["x"], git_commit["y"]))  # Draw the git commit

            # Create a rectangle for the git commit
            git_commit_rect = pygame.Rect(git_commit["x"], git_commit["y"], git_commit_width, git_commit_height)

            # Check for collision with the player
            if player_rect.colliderect(git_commit_rect):
                # Collision detected, remove git commit
                git_commits.remove(git_commit)

                # Increase lives
                lives += 1
                break

        git_commits = [git_commit for git_commit in git_commits if git_commit["x"] + git_commit_width > 0]  # Remove git commits that have gone off screen


        ###################################
        ## ENEMY DEATH && SCORE INCREASE ##
        ###################################

        for bullet in bullets[:]:  # Iterate over a copy of the bullets list
            for enemy in enemies[:]:  # Iterate over a copy of the enemies list
                # Check for collision
                bullet_rect = pygame.Rect(bullet["x"], bullet["y"], bullet_width, bullet_height)
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)

                # Check if the bullet collides with the enemy
                if bullet_rect.colliderect(enemy_rect):

                    # Collision detected, remove bullet and enemy
                    bullets.remove(bullet)
                    enemies.remove(enemy)

                    # Increase score
                    score += 1
                    break  # Exit the inner loop to avoid modifying the list during iteration

        # set the high score
        if score > high_score:
            high_score = score

    # draw the screen
    pygame.display.update()
    
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame
    dt = clock.tick(60) / 1000

pygame.quit()