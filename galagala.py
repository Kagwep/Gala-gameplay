# Import the pygame module
import pygame
# Import random for random numbers
import random

pygame.font.init()
pygame.mixer.init()
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



#missile_hit_sound = pygame.mixer.Sound()
missile_fire = pygame.mixer.Sound('missile.mp3')
torpedo_fire = pygame.mixer.Sound('torpedo.mp3')
target_hit = pygame.mixer.Sound('explosion.mp3')

health_font = pygame.font.SysFont('comicsans',40)

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

# main class
def main():
    #rectangle for ship
    ship_r = pygame.Rect((450,450,30,44))
    #Only run when true
   
    #lists for missile and enemy
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
    l_e_ship = []
   
    # set time of playing
    clock = pygame.time.Clock()
    run = True
    while run:
        if len(enemy_l) < max_enemy:
            enemy_r = pygame.Rect(random.randint(100,800),random.randint(0,50),random.randint(20,40),random.randint(20,40))
            enemy_l.append(enemy_r)
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
            break
            
        elif missileHit <= 0:
            break
        elif smallShipCollide <= 0:
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

            for missile_s in missiles:
                # speed of missiles
                missile_s.y -= 1
                if missile_s.y <= 0:
                    missiles.remove(missile_s)
                if missile_s.colliderect(space):
                    pygame.event.post(pygame.event.Event(enemy_missile_hit))
                    enemy_l.remove(space)
                    missiles.remove(missile_s)
                    target_hit.play()
                elif space in enemy_l  and space.y > HEIGHT:
                    enemy_l.remove(space)
            

        for missi in missiles_e:
            missi.y +=8
            if missi.colliderect(ship_r):
                pygame.event.post(pygame.event.Event(missile_hit))
                missiles_e.remove(missi)
            elif missi.y > HEIGHT:
                missiles_e.remove(missi)
            for s_bullet in missiles:
                if s_bullet.colliderect(missi):
                    missiles_e.remove(missi)
                    missiles.remove(s_bullet)
                    target_hit.play()

        
                

        gala_win.blit(space_image,(0,0))
        gala_win.blit(ship,(ship_r.x,ship_r.y))

        ship_health = health_font.render("Health: ",1,(255,255,255))

        gala_win.blit(ship_health,(WIDTH - ship_health.get_width()-10,10))
        
        for spaceD in enemy_l: 
            gala_win.blit(enemy,(spaceD.x,spaceD.y))
            
        for large_ship in l_e_ship:
            gala_win.blit(enemy_ship_large,(large_ship.x,large_ship.y))
            
        for missileS in missiles:
            gala_win.blit(torpedo,(missileS))

        for missi in missiles_e:
            gala_win.blit(torpedo_e,(missi))
            #pygame.draw.rect(gala_win,red,missileS)
        pygame.display.update()
        clock.tick(FPS)
        

    main()

if __name__ == '__main__':
    main()
