import pygame
import pygame_menu
import random
from pygame_menu import sound
pygame.font.init()
pygame.mixer.init()
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


# sounds used in game
#missile_hit_sound = pygame.mixer.Sound()
missile_fire = pygame.mixer.Sound('missile.mp3')
torpedo_fire = pygame.mixer.Sound('torpedo.mp3')
target_hit = pygame.mixer.Sound('explosion.wav')
mouseclick= pygame.mixer.Sound('mouseclick.mp3')
music = pygame.mixer.Sound('music.mp3')

# fonts used in game
health_font = pygame.font.SysFont('comicsans',20)
d_end_font = pygame.font.SysFont('comicsans',50)
end_font = pygame.font.SysFont('comicsans',50)
ins = pygame.font.SysFont('comicsans',20)
# maximum number of enemy ships at any moment on screen
max_enemy = 6
max_missiles =  5
max_enemy_ship = 3
max_bullets = 5
#color red
red = (255,0,0)


collision = pygame.USEREVENT + 1
missile_hit = pygame.USEREVENT + 2
enemy_missile_hit = pygame.USEREVENT + 3
small_ship_coll = pygame.USEREVENT + 4
large_ship_hit = pygame.USEREVENT + 5

# upload images to represent ships and torpedos/missiles
space_image = pygame.transform.scale(pygame.image.load("space.png"),(WIDTH,HEIGHT))
ship_image =  pygame.image.load("jet.png")
enemy_image =  pygame.image.load("enemy.png")
large_enemy_ship_image =  pygame.image.load("enemy1.png")
missile_image =  pygame.image.load("torpedo.png")
torpedo_image =  pygame.image.load("torpedo1.png")

# Rotate the images to required orientation
ship=pygame.transform.rotate(ship_image ,90)
enemy=pygame.transform.rotate(enemy_image ,270)
enemy_ship_large=pygame.transform.rotate(large_enemy_ship_image ,270)
torpedo =pygame.transform.rotate(missile_image,90)
torpedo_e =pygame.transform.rotate(torpedo_image,270)

#screen when game ends
def endGame(disp,info):
    displayResult = d_end_font.render(info,1,(255,240,255))
    gala_win.blit(displayResult,(WIDTH/2 - displayResult.get_width()/2, HEIGHT/3 - displayResult.get_height()))
    displayResults = end_font.render(disp,1,(255,240,255))
    gala_win.blit(displayResults,(WIDTH/2 - displayResults.get_width()/2, HEIGHT/2 - displayResults.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# instructions to play the game
def instructions():
    inst_0 = "To Play Game: "
    inst_1 = [" Press W to move up" ,"Press S to move backwards" ," Press A to move left", " Press D to move right"]

    ret = "Press enter to return to Main Menu"

    running = True

    #music.play()

    while True:

        num = 6

        for event in pygame.event.get():

            # quit when user closes window      
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
             # firing to enemy
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    mouseclick.play()
                    menuSelect()
        gala_win.blit(space_image,(0,0))
        
        s_inst = ins.render(inst_0,1,(255,240,255))
        gala_win.blit(s_inst ,(WIDTH/2 - s_inst .get_width()/2, HEIGHT/10 - s_inst .get_height()))
        for line in inst_1:
            show = ins.render(line,1,(255,240,255))
            gala_win.blit(show,(WIDTH/2 - show.get_width()/2, HEIGHT/num - show.get_height()))
            num -= 1
            
        show_r= ins.render(ret,1,(255,240,255))
        gala_win.blit(show_r,(WIDTH/2 - show_r.get_width()/2, HEIGHT/1.5 - show_r.get_height()/2))
        
        pygame.display.update()
    
        
def start_the_game():
    # Do the job here !
    
    #rectangle for ship
    ship_r = pygame.Rect((410,410,30,44))
    #Only run when true
   
    #lists 
    missiles = []
    missiles_e = []
    largeShipCollide_health = 1
    smallShipCollide = 2
    largeShipHealth= 2
    missileHit = 1
    enemy_hit = []
    enemy_d = []
    colision_count = 0
    enemy_l = []
    score = 0
    l_e_ship = []
   
    # set time of playing
    clock = pygame.time.Clock()
    run = True
    while run:
        #check whether the number of small ships allowed has been reached
        if len(enemy_l) < max_enemy:
            enemy_r = pygame.Rect(random.randint(100,800),random.randint(0,50),random.randint(20,40),random.randint(20,40))
            enemy_l.append(enemy_r)
        #check whether the number of large ships allowed has been reached
        if len(l_e_ship)< max_enemy_ship:
            l_ship = pygame.Rect(random.randint(0,WIDTH),random.randint(0,50),random.randint(20,30),random.randint(20,30))
            l_e_ship.append(l_ship)
            if len(missiles_e) < max_missiles: 
                missile_e = pygame.Rect(l_ship.x , l_ship.y,10,5)
                missiles_e.append(missile_e)
                torpedo_fire.play()
        #handling events
        for event in pygame.event.get():

          # quit when user closes window      
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
         # firing to enemy
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menuSelect()
                       
            if event.type == pygame.KEYDOWN and len(missiles) <= max_bullets:
                if event.key == pygame.K_RCTRL:
                    #create rect for missile/torpedo
                    missile = pygame.Rect(ship_r.x , ship_r.y,10,5)
                    missiles.append(missile)
                    torpedo_fire.play()
        # missile/torpedo from enemy ship

            if event.type == collision:
                largeShipCollide_health  -= 1
                
            if event.type == missile_hit :
                missileHit -= 1
            if event.type == small_ship_coll:
                smallShipCollide -= 1
                
        if largeShipCollide_health <= 0:
            endGame("Your score is: " + str(score ),"Game Over ....")
            #music.play()
            break
            
        elif missileHit <= 0:
            endGame("Your score is: " + str(score ),'Game Over ....')
           # music.play()
            break
        elif smallShipCollide <= 0:
            endGame("Your score is: " + str(score ),'Game Over ....')
           # music.play()
            break
                  
        
        # listenting to key presses
        # control of the ship
        keys_pressed = pygame.key.get_pressed()
        

        if keys_pressed[pygame.K_a] and ship_r.x - 5 > 0: # move left
             ship_r.x -= 5
        if keys_pressed[pygame.K_d] and ship_r.x + 5 < 850: # move right
             ship_r.x += 5
        if keys_pressed[pygame.K_w] and ship_r.y - 5 > 380: # move up
             ship_r.y -= 5
        if keys_pressed[pygame.K_s] and ship_r.y + 5 < 450:# move reverse
             ship_r.y += 5
        #check for misile hits for the ship

        for e_ship in l_e_ship:
            e_ship.y += 2
            if e_ship.colliderect(ship_r):
                pygame.event.post(pygame.event.Event(collision))
                l_e_ship.remove(e_ship)
                target_hit.play()
            elif e_ship.y > HEIGHT:
                l_e_ship.remove(e_ship)
                
            for mis in missiles:
                if mis.colliderect(e_ship):

                    if e_ship in enemy_hit:
                        l_e_ship.remove(e_ship)
                        target_hit.play()
                        score += 10
                        
                    else:
                       enemy_hit.append(e_ship)
                       missiles.remove(mis)
                
        for space in enemy_l:

            if space.colliderect(ship_r):
                pygame.event.post(pygame.event.Event(small_ship_coll))
                enemy_l.remove(space)
            # speed of smaller enemy ship
            space.y += 4
            # check whether ship is beyond screen view and remove it from the list
            if space.y > HEIGHT:
                enemy_l.remove(space)
                
            # check for all ship missiles/bullets
            for missile_s in missiles:
                # speed of missiles
                missile_s.y -= 1
                #movement beyond screen
                if missile_s.y <= 0:
                    missiles.remove(missile_s)
                #collision with enemy small ship
                if missile_s.colliderect(space):
                    pygame.event.post(pygame.event.Event(enemy_missile_hit))
                    enemy_l.remove(space)
                    missiles.remove(missile_s)
                    score += 5
                    target_hit.play()
                # movement out of screen
                elif space in enemy_l  and space.y > HEIGHT:
                    enemy_l.remove(space)
            
        # check for every enemy missile/bullet
        for missi in missiles_e:
            missi.y +=8
            # A collision with ship
            if missi.colliderect(ship_r):
                pygame.event.post(pygame.event.Event(missile_hit))
                missiles_e.remove(missi)
                target_hit.play()
            # move beyond screen
            elif missi.y > HEIGHT:
                missiles_e.remove(missi)
            # missiles/bullets collision
            for s_bullet in missiles:
                if s_bullet.colliderect(missi):
                    missiles_e.remove(missi)
                    missiles.remove(s_bullet)
                    target_hit.play()

        
                

        gala_win.blit(space_image,(0,0))
        gala_win.blit(ship,(ship_r.x,ship_r.y))

        ship_health = health_font.render("Score: " + str(score ),1,(255,255,255))
        gala_win.blit(ship_health,(10,10))

        # Display small ships
        
        for spaceD in enemy_l: 
            gala_win.blit(enemy,(spaceD.x,spaceD.y))

         #  Display large ships   
        for large_ship in l_e_ship:
            gala_win.blit(enemy_ship_large,(large_ship.x,large_ship.y))
          ## Display mullets/missiles  
        for missileS in missiles:
            gala_win.blit(torpedo,(missileS))

        ## Display enemy bullets/missiles
        for missi in missiles_e:
            gala_win.blit(torpedo_e,(missi))
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
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Instructions', instructions)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.set_sound(engine, recursive=True)
    menu.mainloop(surface)
menuSelect()
