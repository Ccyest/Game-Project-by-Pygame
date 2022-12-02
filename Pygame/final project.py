# Yichi Zhang
# pcv9ha
import gamebox
import pygame
import random

# setup the game
camera = gamebox.Camera(800, 600)
ticks_per_second = 40
score = 0
score_list = []
time_counter = 0
floors = [gamebox.from_color(400, 600, 'brown', 1000, 20),
          gamebox.from_color(100, 510, 'brown', 500, 10),
          gamebox.from_color(600, 400, 'brown', 500, 10),
          gamebox.from_color(300, 300, 'brown', 300, 10)]

game_on = False
backgrounds = gamebox.from_image(400,300,'backgrounds.png')
instructions = [gamebox.from_text(650,100,'Press J for melee attack',30,'white'),
                gamebox.from_text(650,80,'Press A&D for move',30,'white'),
                gamebox.from_text(650,140,'Press K for jump',30,'white'),
                gamebox.from_text(650,160,'Press L for dash',30,'white'),
                gamebox.from_text(650,120,'Press U for ranged attack',30,'white'),
                gamebox.from_text(650,50,'Instructions:',50,'white'),
                gamebox.from_text(650,180,'Difficulty will increase',30,'red'),
                gamebox.from_text(640,200,'as the number of zombies killed',30,'red'),
                gamebox.from_text(400,300,'Press F to start',80,'orange'),
                gamebox.from_text(100,500,'By Yichi Zhang',30,'white'),
                gamebox.from_text(100,530,'and Kelvin Li',30,'white')]





# setup the player
player_move = gamebox.load_sprite_sheet('spritesheet_run.png', 1, 8)
player_dash = gamebox.load_sprite_sheet('spritesheet_dash.png',1,10)
player_attack = gamebox.load_sprite_sheet('spritesheet_attack.png',1,13)
player_idle = gamebox.load_sprite_sheet('spritesheet_idle.png',1,2)

player_HP = 100
player_HP_bar = gamebox.from_color(400,30,'lightgreen',player_HP*5,8)

DPS = 100


# animation
frame_idle = 0
frame_move = 0
frame_dash = 0
frame_attack = 0
frame_jump = 0
player = gamebox.from_color(200,200,'white',30,30)
move_time_counter = 0
idle_time_counter = 0
attack_time_counter = 0


# others
alive = True
fire_balls = []
able_to_launch = True
fireball_counter = 0
facing_right = True
hit_counter = 0
health_flask_counter = 0
health_flasks = []

# setup enemies
enemies = []
reborn_counter = 0
enemy_DPS = 2
reborn_difficulty = 150

enemy_walk_frame = 0
enemy_attack_frame = 0
enemy_hurt_frame = 0
enemy_idle_frame = 0
enemy_death_frame = 0
enemy_speed = 3


enemy_walk = gamebox.load_sprite_sheet('zombie_walk.png', 1, 9)
enemy_attack = gamebox.load_sprite_sheet('zombie_attack.png',1,9)
enemy_death = gamebox.load_sprite_sheet('zombie_death.png',1,10)
enemy_hurt = gamebox.load_sprite_sheet('zombie_hurt.png',1,2)
enemy_idle = gamebox.load_sprite_sheet('zombie_idle.png',1,7)

enemy_time_counter = 0



def tick(keys):
    global alive, floors, fire_balls, score, score_list, able_to_launch, fireball_counter, game_on, backgrounds, instruction
    global enemies, reborn_counter, enemy_walk_frame, enemy_attack_frame, enemy_hurt_frame, enemy_idle_frame, enemy_death_frame, enemy_time_counter, enemy_DPS,reborn_difficulty, enemy_speed
    global player, player_attributes, player_move, player_HP,player_HP_bar, facing_right, DPS, health_flask_counter, health_flasks
    global frame_move, frame_dash, frame_attack, frame_idle,time_counter, hit_counter, move_time_counter, attack_time_counter,idle_time_counter

    if not game_on:
        camera.draw(backgrounds)
        for instruction in instructions:
            camera.draw(instruction)
        if pygame.K_f in keys:
            game_on = True


    else:
        if alive:
            camera.clear("black")

            player_defense = 1

            health_flask_counter += 1
            if health_flask_counter % 500 == 0:
                health_flask = gamebox.from_image(random.randint(0,800),0,'Health Flask.png')
                health_flasks.append(health_flask)

            for health_flask in health_flasks:
                health_flask.speedy += 1
                health_flask.move_speed()
                for floor in floors:
                    if health_flask.touches(floor):
                        health_flask.move_to_stop_overlapping(floor)

                if health_flask.touches(player):
                    if player_HP < 70:
                        player_HP += 30
                    else:
                        player_HP = 100
                    player_HP_bar = gamebox.from_color(400, 30, 'lightgreen', player_HP * 5, 8)
                    health_flasks.remove(health_flask)
                camera.draw(health_flask)


            # player idle
            if pygame.K_a not in keys and pygame.K_d not in keys and pygame.K_k not in keys and pygame.K_l not in keys and pygame.K_j not in keys:
                idle_time_counter += 1
                if idle_time_counter % 5 == 0:
                    frame_idle += 1
                    if frame_idle == 2:
                        frame_idle = 0

                    if facing_right:
                        player = gamebox.from_image(player.x, player.y,
                                                    pygame.transform.scale(player_idle[frame_idle], (100, 50)))
                    else:
                        player = gamebox.from_image(player.x, player.y,
                                                    pygame.transform.flip(
                                                        pygame.transform.scale(player_idle[frame_idle], (100, 50)),
                                                        True, False))

                    idle_time_counter = 0

            # horizontal moving
            if pygame.K_a in keys:
                player.x -= 15
                facing_right = False
                move_time_counter += 1
                if move_time_counter % 2 == 0:
                    frame_move += 1
                    move_time_counter = 0
                    if frame_move == 8:
                        frame_move = 0
                    player = gamebox.from_image(player.x, player.y,
                                                pygame.transform.flip(
                                                    pygame.transform.scale(player_move[frame_move], (100, 50)),
                                                    True, False))

            if pygame.K_d in keys:
                player.x += 15
                facing_right = True
                move_time_counter += 1
                if move_time_counter % 2 == 0:
                    frame_move += 1
                    move_time_counter = 0
                    if frame_move == 8:
                        frame_move = 0
                    player = gamebox.from_image(player.x, player.y,
                                                pygame.transform.scale(player_move[frame_move], (100, 50)))

            if player.x > 800:
                player.x = 800
            if player.x < 0:
                player.x = 0
            if player.y > 600:
                player.y = 300

            # gravity
            player.speedy += 1
            player.move_speed()

            # player health
            camera.draw(player_HP_bar)

            # jump
            for floor in floors:
                if player.bottom_touches(floor):
                    player.speedy = 0
                    if pygame.K_k in keys:
                        player.speedy -= 20

                # set up the terrain
                if player.touches(floor):
                    player.move_to_stop_overlapping(floor)
                camera.draw(floor)

            # dash
            if pygame.K_l in keys:
                player_defense = 10000000
                if facing_right == True:
                    player.x += 50
                    time_counter += 1
                    if time_counter % 1 == 0:
                        frame_dash += 1
                        if frame_dash == 10:
                            frame_dash = 0
                        player = gamebox.from_image(player.x, player.y,
                                                    pygame.transform.scale(player_dash[frame_dash], (200, 50)))
                        time_counter = 0

                elif facing_right == False:
                    frame_dash += 1
                    if frame_dash == 10:
                        frame_dash = 0
                    player = gamebox.from_image(player.x, player.y, pygame.transform.flip(
                        pygame.transform.scale(player_dash[frame_dash], (200, 50)), True, False))
                    player.x -= 50

            # player melee attack
            if pygame.K_j in keys:
                player_defense = 3
                if facing_right:
                    attack_time_counter += 1
                    if attack_time_counter % 2 == 0:
                        frame_attack += 1
                        if frame_attack == 13:
                            frame_attack = 0
                        player = gamebox.from_image(player.x, player.y,
                                                    pygame.transform.scale(player_attack[frame_attack], (100, 50)))
                        attack_time_counter = 0
                else:

                    attack_time_counter += 1
                    if attack_time_counter % 2 == 0:
                        frame_attack += 1
                        if frame_attack == 13:
                            frame_attack = 0
                        player = gamebox.from_image(player.x, player.y,
                                                    pygame.transform.flip(
                                                        pygame.transform.scale(player_attack[frame_attack], (100, 50)),
                                                        True, False))
                        attack_time_counter = 0

                for enemy in enemies:
                    if player.touches(enemy[0]):
                        hit_counter += 1
                        if hit_counter % 10 == 1:
                            enemy[1] -= DPS

            # player ranged attack
            fireball_counter += 1

            if fireball_counter % 15 == 0:
                able_to_launch = True

            if pygame.K_u in keys and able_to_launch:
                if facing_right:
                    fire_ball = gamebox.from_image(player.x, player.y, 'fireball2.jpg')
                else:
                    fire_ball = gamebox.from_image(player.x, player.y, 'fireball.jpeg')

                fire_balls.append(fire_ball)
                able_to_launch = False

            for fire_ball in fire_balls:
                if facing_right:
                    fire_ball.speedx = 30
                    if fire_ball.x > 800 or fire_ball.x < 0:
                        fire_balls.remove(fire_ball)


                else:
                    fire_ball.speedx = -30
                    if fire_ball.x > 800 or fire_ball.x < 0:
                        fire_balls.remove(fire_ball)

                for enemy in enemies:
                    if fire_ball.touches(enemy[0]):
                        fire_ball.move_to_stop_overlapping(enemy[0])
                        fire_balls = []
                        enemy[1] -= DPS

                fire_ball.move_speed()
                camera.draw(fire_ball)

            # generate enemies
            reborn_counter += 1
            if reborn_counter % reborn_difficulty == 1:
                new_enemy = gamebox.from_image(random.randint(0, 800), 0, enemy_idle[1])
                enemies.append([new_enemy, 100, 100, 0])

            # enemy animation
            enemy_time_counter += 1
            if enemy_time_counter % 6 == 0:

                enemy_idle_frame += 1
                if enemy_idle_frame == 7:
                    enemy_idle_frame = 0

                enemy_walk_frame += 1
                if enemy_walk_frame == 9:
                    enemy_walk_frame = 0

                enemy_attack_frame += 1
                if enemy_attack_frame == 9:
                    enemy_attack_frame = 0

            for enemy in enemies:
                # setup gravity
                enemy[0].speedy += 10
                enemy[0].move_speed()

                for floor in floors:
                    if enemy[0].touches(floor):
                        enemy[0].move_to_stop_overlapping(floor)

                # enemy idle
                if enemy[0].y - player.y >= 100 or enemy[0].y - player.y <= -100 and enemy[1] > 0:
                    enemy[0] = gamebox.from_image(enemy[0].x, enemy[0].y, enemy_idle[enemy_idle_frame])
                    camera.draw(enemy[0])

                # add action patterns to enemies
                if enemy[0].x < player.x - 15 and -100 < enemy[0].y - player.y < 100:
                    enemy[0].x += enemy_speed
                    enemy[0] = gamebox.from_image(enemy[0].x, enemy[0].y, pygame.transform.flip(
                        enemy_walk[enemy_walk_frame], True, False))

                elif enemy[0].x > player.x + 15 and -100 < enemy[0].y - player.y < 100:
                    enemy[0].x -= enemy_speed
                    enemy[0] = gamebox.from_image(enemy[0].x, enemy[0].y,
                                                  (enemy_walk[enemy_walk_frame]))

                if enemy[0].x > 805:
                    enemy[0].x = 805

                elif enemy[0].x < -5:
                    enemy[0].x = -5

                # enemy attack:
                if -25 < enemy[0].x - player.x < 25:
                    if enemy[0].y == player.y:
                        if enemy[0].x < player.x:
                            enemy[0] = gamebox.from_image(enemy[0].x, enemy[0].y,
                                                          pygame.transform.flip(enemy_attack[enemy_attack_frame], True,
                                                                                False))
                            if enemy_attack_frame == 4:
                                if enemy[0].touches(player):
                                    player_HP -= enemy_DPS / player_defense
                                    player_HP_bar = gamebox.from_color(400, 30, 'lightgreen', player_HP * 5, 8)



                        else:
                            enemy[0] = gamebox.from_image(enemy[0].x, enemy[0].y, enemy_attack[enemy_attack_frame])
                            if enemy_attack_frame == 4:
                                if enemy[0].touches(player):
                                    player_HP -= enemy_DPS / player_defense
                                    player_HP_bar = gamebox.from_color(400, 30, 'lightgreen', player_HP * 5, 8)

                    else:
                        enemy[0] = gamebox.from_image(enemy[0].x, enemy[0].y, enemy_idle[enemy_idle_frame])
                        camera.draw(enemy[0])

                # enemy hurt
                if enemy[1] < enemy[2]:
                    hit_counter += 1
                    if hit_counter % 5 == 0:
                        enemy_hurt_frame += 1
                        if enemy_hurt_frame == 2:
                            enemy_hurt_frame = 0
                            enemy[2] = enemy[1]
                    enemy[0] = gamebox.from_image(enemy[0].x, enemy[0].y, enemy_hurt[enemy_hurt_frame])
                    camera.draw(enemy[0])

                # enemy die & zombies killed
                if enemy[1] < 0:
                    enemy[3] += 1
                    if enemy[3] % 3 == 0:
                        enemy_death_frame += 1
                        if enemy_death_frame == 10:
                            enemies.remove(enemy)
                            enemy_death_frame = 0
                            score += 1

                        enemy[3] = 0

                    enemy[0] = gamebox.from_image(enemy[0].x, enemy[0].y, enemy_death[enemy_death_frame])

                camera.draw(enemy[0])

            # setup difficulty
            camera.draw(gamebox.from_text(100, 70, 'Zombie killed: ' + str(score), 30, 'yellow'))
            camera.draw(gamebox.from_text(100, 100, 'Difficulty factor:' + str(score // 10 + 1), 25, 'yellow'))
            if score // 10 == 0:
                camera.draw(gamebox.from_text(400, 50, 'Welcome to the starter town!', 25, 'green'))

            elif score // 10 == 1:
                DPS = 40
                enemy_DPS = 4
                enemy_speed = 4
                camera.draw(gamebox.from_text(400, 50, 'Enemy are stronger!', 25, 'orange'))
                reborn_difficulty = 100

            elif score // 10 == 2:
                DPS = 30
                enemy_DPS = 6
                enemy_speed = 5
                camera.draw(gamebox.from_text(400, 50, "Nightmare difficulty!", 25, 'purple'))
                reborn_difficulty = 70

            elif score // 10 > 2:
                DPS = 30
                enemy_DPS = 6
                enemy_speed = 6
                camera.draw(gamebox.from_text(400, 50, "Tips: nothing will happen if you press 'B & I' ", 25, 'white'))
                reborn_difficulty = 10

            # plug-in

            if pygame.K_i in keys and pygame.K_b in keys:
                for enemy in enemies:
                    enemy[1] = -10

            camera.draw(player)

            # player die
            if player_HP < 0:
                camera.draw(player_HP_bar)
                alive = False
                score_list.append(score)

        # restart
        else:

            camera.draw(gamebox.from_text(400, 300, 'You died!', 100, 'orange'))
            camera.draw(gamebox.from_text(400, 400, 'Press R to restart', 50, 'orange'))
            camera.draw(gamebox.from_text(400, 450, 'Your Record Is : ' + str(max(score_list)), 30, 'orange'))
            camera.draw(gamebox.from_color(400, 20, 'black', 200, 40))

            if pygame.K_r in keys:
                alive = True
                player_HP = 100
                player_HP_bar = gamebox.from_color(400, 30, 'lightgreen', player_HP * 5, 8)
                enemies = []
                score = 0
                DPS = 100
                enemy_DPS = 2
                enemy_speed = 3
                reborn_difficulty = 150





    camera.display()


gamebox.timer_loop(ticks_per_second, tick)






