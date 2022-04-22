# import pygame and pygame menu
import pygame
import pygame_menu
import random
from pygame_menu import sound
# initialize pygame fonts
pygame.font.init()
# initialize pygame mixer to use sounds
pygame.mixer.init()
## initialize pygame
pygame.init()
surface = pygame.display.set_mode((600, 400))

# the constants for the screen width and height
WIDTH, HEIGHT = 900,500

#create screen
gala_win = pygame.display.set_mode(( WIDTH, HEIGHT ))

# change the titile of window screen
pygame.display.set_caption('Galagala D')

# Rate . frame per second
FPS = 30
# speed of missile/torpedo
speed = 7
speed_1 = 5



# sounds used in game
#missile_hit_sound = pygame.mixer.Sound()
missile_fire = pygame.mixer.Sound('missile.mp3')
# sound when bullet/torpedo/missel is fired
bullet_fire = pygame.mixer.Sound('bulletfire.mp3')
#explosion sound
target_hit = pygame.mixer.Sound('explosion.wav')
# menu click sound
mouseclick= pygame.mixer.Sound('mouseclick.mp3')
#game music sound
music = pygame.mixer.Sound('music.mp3')

# fonts used in game
health_font = pygame.font.SysFont('comicsans',20)
score_font = pygame.font.SysFont('comicsans',20)
d_end_font = pygame.font.SysFont('comicsans',50)
end_font = pygame.font.SysFont('comicsans',50)
ins = pygame.font.SysFont('comicsans',20)
# maximum number of enemy ships at any moment on screen
max_small_enemy_ships = 6
#maximum missiles/bullets/torpedo that ship can fire , the ship can only fire when there are less than five missiles/torpedo/bullets on screen
max_player_ship_bullets =  5
# maximum number of large ships on screen
max_large_enemy_ships = 3
#maximum bullets
max__enemy_bullets = 5
#color red
red = (255,0,0)
green = (0,255,0)

#event recorded when there is a collission, collission can be bullet and bullet or enemy ship and ship
collision = pygame.USEREVENT + 1
ship_bullet_hit = pygame.USEREVENT + 2
enemy_bullet_hit = pygame.USEREVENT + 3
small_ship_coll = pygame.USEREVENT + 4
large_ship_hit = pygame.USEREVENT + 5

# upload images to represent ships and torpedos/missiles
#the space image background
space_image = pygame.transform.scale(pygame.image.load("space.png"),(WIDTH,HEIGHT))
# ship and bullets representation images
# ship will be the name of the ship controlled by the player
player_ship_image =  pygame.image.load("ship.png")
#small enemy ship
small_enemy_ship_image =  pygame.image.load("enemy.png")
#large enemy ship
large_enemy_ship_image =  pygame.image.load("enemy1.png")
#friendly bullet
bullet_image =  pygame.image.load("bullet.png")
#enemy bullet
enemy_bullet_image =  pygame.image.load("bullet.png")

# Rotate the ships to required orientation
player_ship_i = pygame.transform.rotate(player_ship_image ,90)
#enemy ships will face down
smallEnemyShip=pygame.transform.rotate(small_enemy_ship_image ,270)
enemy_ship_large=pygame.transform.rotate(large_enemy_ship_image ,270)
#bullet from ship will move up
bullet_player_ship =pygame.transform.rotate(bullet_image,90)
#bullet from enemy will move down
enemy_bullet_i =pygame.transform.rotate(enemy_bullet_image,270)

#screen when game ends/  Occures when collision happens
def endGame(disp,info):
    #writing information to be diplayed on screen
    displayResult = d_end_font.render(info,1,(255,240,255))
    gala_win.blit(displayResult,(WIDTH/2 - displayResult.get_width()/2, HEIGHT/3 - displayResult.get_height()))
    displayResults = end_font.render(disp,1,(255,240,255))
    gala_win.blit(displayResults,(WIDTH/2 - displayResults.get_width()/2, HEIGHT/2 - displayResults.get_height()/2))
    pygame.display.update()
    #the delay helps user to see his score before game restarts
    pygame.time.delay(5000)

# instructions to play the game
def instructions():
    inst_0 = "To Play Game: "
    inst_1 = [" Press W to move up" ,"Press S to move backwards" ," Press A to move left", " Press D to move right", "Press Right control to fire bullet"]

    ret = "Press enter to return to Main Menu"

    running = True

    #music.play()

    while True:

        num = 6
        # handles events when user is in instruction window
        for event in pygame.event.get():

            # quit when user closes window      
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
             # Returning to main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #play sound when button is clicked
                    mouseclick.play()
                    #call menu select
                    menuSelect()
        # display window with space image background
        gala_win.blit(space_image,(0,0))
        #write/render instructions on screen
        s_inst = ins.render(inst_0,1,(255,240,255))
        #write instructions on the following positions on screen
        gala_win.blit(s_inst ,(WIDTH/2 - s_inst .get_width()/2, HEIGHT/10 - s_inst .get_height()))
        # a for loop to write instructions in the list on screen
        for line in inst_1:
            show = ins.render(line,1,(255,240,255))
            #write/render instructions on the following positions on screen
            gala_win.blit(show,(WIDTH/2 - show.get_width()/2, HEIGHT/num - show.get_height()))
            num -= 1
        
        show_r= ins.render(ret,1,(255,240,255))
        gala_win.blit(show_r,(WIDTH/2 - show_r.get_width()/2, HEIGHT/1.5 - show_r.get_height()/2))
        
        pygame.display.update()
    
        
def start_the_game():
    # Do the job here !
    #rectangle for ship
    player_ship = pygame.Rect((410,410,30,44))
    #Only run when true
   
    #lists
    # list of all bullets on screen fired by ship
    player_bullets = []
    #list of all bullets on screen fired by enemy
    enemy_bullets = []
    #player Ship status when it collides with a large enmy ship
    largeShipCollide_health = 1
    # player ships health when it collides with a small enemy ship
    smallShipCollide = 2
    #will take two bullets to shoot large enemy ship  down
    largeShipHealth= 2
    # status of bullet hit for ship and small enemy ship
    bulletHit = 1
    # list of all large ships that have been hit
    enemy_hit = []
    # list of small enemy ship on screen
    small_enemy_ship_list = []
    #score count
    score = 0
    #list of large ships n screen
    large_e_ships = []
    # health status
    val1 = 100
    val =90
    # ships health
    ship_health = 2
   
    # rate of frame movement
    clock = pygame.time.Clock()
    run = True
    while run:
        #check whether the number of small enemy ships allowed on screen has been reached to avoid enemy ships flooding the screen
        
        if len(small_enemy_ship_list) < max_small_enemy_ships:
            # if less than the set number add in a random position with a random sized rect
            small_enemy_r = pygame.Rect(random.randint(100,800),random.randint(0,50),random.randint(20,40),random.randint(20,40))
            # add new small enemy ship to the list to track it
            small_enemy_ship_list.append(small_enemy_r)
    
        #check whether the number of large enemy ships allowed on screen has been reached to avoid enemy ships flooding the screen
        if len(large_e_ships)< max_large_enemy_ships:
             # if less than the set number add in a random position with a random sized rect
            large_ship = pygame.Rect(random.randint(0,WIDTH),random.randint(0,50),random.randint(20,30),random.randint(20,30))
             # add new large enemy ship to the list to track it
            large_e_ships.append(large_ship)
            #check whether the number of large enemy ships bullets allowed on screen has been reached to avoid enemy bullets flooding the screen
            if len(enemy_bullets) < max__enemy_bullets:
                # if less than the set number add in a new one in a random position with a random sized rect
                enemy_bullet = pygame.Rect(large_ship.x , large_ship.y,10,5)
                # add new large enemy ship to the list to track it
                enemy_bullets.append(enemy_bullet)
                #play sound of bullet fire
                bullet_fire.play()
        #handling events
        for event in pygame.event.get():

          # quit when user closes window      
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
         # press enter to return to main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menuSelect()
         #press right control key to fire bullet
            if event.type == pygame.KEYDOWN and len(player_bullets) <= max_player_ship_bullets:
                if event.key == pygame.K_RCTRL:
                    #create rect for missile/torpedo
                    bullet_p = pygame.Rect(player_ship.x , player_ship.y,10,5)
                    
                    player_bullets.append(bullet_p)
                    bullet_fire.play()
        # missile/torpedo from enemy ship
            # check whther a collision has occurred and degrade health of affected ship
            if event.type == collision:
                largeShipCollide_health  -= 1
                
            if event.type == ship_bullet_hit :
                bulletHit -= 1
            if event.type == small_ship_coll:
                smallShipCollide -= 1
        # when ships health is zero end game and display the following information
        if largeShipCollide_health <= 0:
            endGame("Your score is: " + str(score ),"Game Over ....")
            #music.play()
            break
           
        elif bulletHit <= 0:
            endGame("Your score is: " + str(score ),'Game Over ....')
           # music.play()
            break
        elif smallShipCollide <= 0:
            val1 =0
            val =0
            endGame("Your score is: " + str(score ),'Game Over ....')
           # music.play()
            break
                  
        
        # listenting to key presses
        # control of the ship
        keys_pressed = pygame.key.get_pressed()
        

        if keys_pressed[pygame.K_a] and player_ship.x - 5 > 0: # move left
             player_ship.x -= 5
        if keys_pressed[pygame.K_d] and player_ship.x + 5 < 850: # move right
             player_ship.x += 5
        if keys_pressed[pygame.K_w] and player_ship.y - 5 > 380: # move up
             player_ship.y -= 5
        if keys_pressed[pygame.K_s] and player_ship.y + 5 < 450:# move reverse
             player_ship.y += 5
        #check for misile hits for the ship
         # this for loop handles the large enemy ship activities
        for large_e_ship in large_e_ships:
            # speed of enemy ship on screen
            large_e_ship.y += 2
            #check for a collision with ship
            if large_e_ship.colliderect(player_ship):
                val1 =0
                val =0
                # add an event when it happens
                pygame.event.post(pygame.event.Event(collision))
                #remove ship from screen
                large_e_ships.remove(large_e_ship)
                #play explosion sound
                target_hit.play()
            # check whether ship is still visible on the screen/ if not remove from the list of enemy ships
            elif large_e_ship.y > HEIGHT:
                large_e_ships.remove(large_e_ship)
            # this for loop looks for any instance when the large enemy ship is hit by the ship's bullets/
            for bullet in player_bullets:
                if bullet.colliderect(large_e_ship):
                    # if it is hit, check whether it was previosuly hit
                    if large_e_ship in enemy_hit:
                       # Remove it from screen if it was hit preiosly
                        large_e_ships.remove(large_e_ship)
                        # play explosion sound
                        target_hit.play()
                        player_bullets.remove(bullet)
                        # score for killing large enemy ship
                        score += 10
                        
                    else:
                        # if not record it in list of large ships hit
                       enemy_hit.append(large_e_ship)
                       # remove bullet from screen
                       player_bullets.remove(bullet)
                        # play explosion sound
                       target_hit.play()

        # this for loop handles all the actions of the small enemy ship
                
        for small_e_ship in small_enemy_ship_list:
            # if small enemy ship collides with ship
            if small_e_ship.colliderect(player_ship):
                #note the collision to handle event
                pygame.event.post(pygame.event.Event(small_ship_coll))
                #check health
                if ship_health == 2:
                    # cut helath by half
                    val1 /=2
                    val /=2
                    ship_health -=1
                # remove all health
                else:
                    val1 =0
                    val =0
                # remove ship from screen
                small_enemy_ship_list.remove(small_e_ship)
            # speed of smaller enemy ship
            small_e_ship.y += 7
            #space.x += random.randint(-10,10)
            # check whether ship is beyond screen view and remove it from the list
            if small_e_ship.y > HEIGHT:
                small_enemy_ship_list.remove(small_e_ship)
                
            # track  all  ship bullets
            for bull in player_bullets:
                # speed of bullets
                bull.y -= 4
                # movement of bullet beyond screen
                if bull.y <= 0:
                    player_bullets.remove(bull)
                #collision with  small small ship
                if bull.colliderect(small_e_ship):
                    #note collision
                    pygame.event.post(pygame.event.Event(enemy_bullet_hit))
                    #reomve it from list of enemy ships
                    small_enemy_ship_list.remove(small_e_ship)
                    #remove bullet
                    player_bullets.remove(bull)
                    #add score
                    score += 5
                    #play explosion sound
                    target_hit.play()
                # movement out of screen
                elif small_e_ship in small_enemy_ship_list  and small_e_ship.y > HEIGHT:
                    # remove small enemy ship
                    small_enemy_ship_list.remove(small_e_ship)
            
        # check for every enemy bullet
        #tracks enemy bullets
        for fired_enemy_bullet in enemy_bullets:
            #speed of enemy missiles
            fired_enemy_bullet.y +=8
            # in case it hits the ship
            if fired_enemy_bullet.colliderect(player_ship):
               # note the event
                val1 =0
                val =0
                pygame.event.post(pygame.event.Event(ship_bullet_hit))
                # remove bullet from list
                enemy_bullets.remove(fired_enemy_bullet)
                # play explosion soud
                target_hit.play()
            # move beyond screen
            elif fired_enemy_bullet.y > HEIGHT:
                enemy_bullets.remove(fired_enemy_bullet)
            # bullets collision
            for s_bullet in player_bullets:
                # Incase tow bullets collide
                if s_bullet.colliderect(fired_enemy_bullet):
                    # remove both of them from their respective lists
                    enemy_bullets.remove(fired_enemy_bullet)
                    player_bullets.remove(s_bullet)
                    #play explosion sound
                    target_hit.play()

        
                
        # draw screen with space background
        gala_win.blit(space_image,(0,0))
        #position of the ship
        gala_win.blit(player_ship_i,(player_ship.x,player_ship.y))
        #score display
        ship_score = score_font.render("Score: " + str(score ),1,(255,255,255))
        gala_win.blit(ship_score,(10,10))

  
        # Drawing Rectangle
        
        
        health_d = health_font.render("Health:" ,1,(255,255,255))
        gala_win.blit(health_d,(WIDTH-100,10))

        pygame.draw.rect(gala_win, red, pygame.Rect(WIDTH-100, 40, 90, 10))
        pygame.draw.rect(gala_win, green, pygame.Rect(WIDTH-val1, 40, val, 10))

        # Display small ships
        
        for enemy_s in small_enemy_ship_list: 
            gala_win.blit(smallEnemyShip,(enemy_s.x,enemy_s.y))

         #  Display large ships   
        for large_ship in large_e_ships:
            gala_win.blit(enemy_ship_large,(large_ship.x,large_ship.y))
          ## Display bullets 
        for p_bullet in player_bullets:
            gala_win.blit(bullet_player_ship,(p_bullet))

        ## Display enemy bullets
        for e_bullet in enemy_bullets:
            gala_win.blit(enemy_bullet_i,(e_bullet))
            #pygame.draw.rect(gala_win,red,missileS)
        pygame.display.update()
        clock.tick(FPS)
        
def set_difficulty(value, difficulty):
    # created difficulty levels
    pass
#Menu
def menuSelect():
    #music.play()
    #sounds in menu
    engine = sound.Sound()
    engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'mouseclick.mp3')
    engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, 'mouseclick.mp3')
    menu = pygame_menu.Menu('Welcome', 400, 300,
                           theme=pygame_menu.themes.THEME_BLUE)
    #Componenets in menu
    menu.add.text_input('Name:', default='Play game')
    # select difficulty
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    # play game
    menu.add.button('Play', start_the_game)
    # read instructions
    menu.add.button('Instructions', instructions)
    # quit the game
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.set_sound(engine, recursive=True)
    menu.mainloop(surface)
menuSelect()
