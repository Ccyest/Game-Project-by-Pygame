# Yichi Zhang
# pcv9ha

import pygame
import gamebox
import random

camera = gamebox.Camera(800, 600)
character = None
floors = []
game_over = None
alive = True
time_counter = 0
counter = 0
score = 0
record = 0
record_list = [0]
ticks_per_second = 45



def setup():
    global character, camera, floors, counter, game_over, alive, record_list, record
    character = gamebox.from_color(400, 100, 'orange', 20, 20)
    floors = [
        gamebox.from_color(400, 350, "black", 200, 10),
        gamebox.from_color(400, 550, "black", 300, 10),
        gamebox.from_color(100, 550, "black", 200, 10),
        gamebox.from_color(500, 650, "black", 200, 10),
        gamebox.from_color(100, 650, "black", 400, 10),
        gamebox.from_color(300, 750, "black", 200, 10),
        gamebox.from_color(700, 750, "black", 400, 10),

    ]
    game_over = gamebox.from_text(400, 300, "Game Over", 72, "red")
    record = gamebox.from_text(400, 400, 'Your record is: ' + str(max(record_list)), 30, 'red')
    alive = True
    counter = 0


setup()


def tick(keys):
    global counter, alive, game_over, floors, character, score, record, record_list

    if alive:
        camera.clear("lightblue")
        # Handle player controls
        if pygame.K_RIGHT in keys:
            character.x += 15
            if character.x > 805:
                character.x = 805
        if pygame.K_LEFT in keys:
            character.x -= 15

            if character.x < -5:
                character.x = -5

        character.yspeed += 1
        character.y = character.y + character.yspeed

        camera.draw(character)


        if camera.y >= 3000:
            camera.y += 5
        else:
            camera.y += 3

        print(camera.y)

        if camera.y % 150 == 0:
            Gap = random.randint(1,2)
            if Gap == 1:
                a = random.randint(0, 740)
                new_wall = gamebox.from_color(1, camera.y + 500, "black", a, 10)
                new_wall.left = 0
                new_wall2 = gamebox.from_color(2, camera.y + 500, "black", 740 - a, 10)
                new_wall2.right = 800
                floors.append(new_wall)
                floors.append(new_wall2)
            elif Gap == 2:
                position = random.randint(250, 550)
                length = random.randint(100, 200)
                middle_wall = gamebox.from_color(position, camera.y + 500, 'black', length, 10)
                new_wall = gamebox.from_color(0, camera.y + 500, "black", 1000, 10)
                new_wall.right = position - length / 2 - 60

                new_wall2 = gamebox.from_color(800, camera.y + 500, "black", 1000, 10)
                new_wall2.left = position + length / 2 + 60
                floors.append(new_wall)
                floors.append(new_wall2)
                floors.append(middle_wall)



        score += 1
        camera.draw(gamebox.from_text(60, camera.y + 270, 'Score:' + str(score // 30), 40, 'red'))

        for wall in floors:
            if character.bottom_touches(wall):
                character.yspeed = 0
            if character.touches(wall):
                character.move_to_stop_overlapping(wall)
            camera.draw(wall)

        if character.y > camera.y + 350:
            character.y = camera.y + 350

        if character.y < camera.y - 500:  # if the character falls off the bottom of the screen
            game_over.y = camera.y  # Make sure message appears on screen
            record_list.append(score // 30)
            record = gamebox.from_text(400, 400, 'Your record is:' + str(max(record_list)), 30, 'red')
            record.y = camera.y + 100
            camera.draw(game_over)
            camera.draw(record)
            alive = False  # no longer alive


    else:
        # if the player hits r to restart
        if pygame.K_r in keys:
            score = 0

            alive = True
            camera.y = 300
            setup()
            difficulty = 60

    camera.display()


gamebox.timer_loop(ticks_per_second, tick)

seconds = 0
