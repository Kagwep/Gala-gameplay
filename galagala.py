# Import the pygame module
import pygame
# Import random for random numbers
import random

# the constants for the screen width and height
WIDTH, HEIGHT = 900,500

#create screen
gala_win = pygame.display.set_mode(( WIDTH, HEIGHT ))

# change the titile of window screen
pygame.display.set_caption('Galagala D')

# Rate . frame per second
FPS = 30
# speed of missile/torpedo
speed = 5

# maximum number of enemy ships at any moment on screen
max_enemy = 10

#color red
red = (255,0,0)

missile_hit = pygame.USEREVENT + 1

# upload images to represent ships and torpedos/missiles
ship_image =  pygame.image.load("jet.png")
enemy_image =  pygame.image.load("enemy.png")
missile_image =  pygame.image.load("torpedo.png")

# Rotate the images to required orientation
ship=pygame.transform.rotate(ship_image ,90)
enemy=pygame.transform.rotate(enemy_image ,270)
torpedo =pygame.transform.rotate(missile_image,90)

# main class
def main():
    #rectangle for ship
    ship_r = pygame.Rect((450,450,300,440))
    #Only run when true
    run = True
    #lists for missile and enemy
    missiles = []
    missiles_e = []
    enemy_l = []
    # set time of playing
    clock = pygame.time.Clock()
 
    while run:
        if len(enemy_l) < max_enemy:
            enemy_r = pygame.Rect(random.randint(100,800),random.randint(0,50),random.randint(200,WIDTH),random.randint(0,100))
            enemy_l.append(enemy_r)
        #handling events
        for event in pygame.event.get():

          # quit when user closes window      
            if event.type == pygame.QUIT:
                run = False
         # firing to enemy
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    #create rect for missile/torpedo
                    missile = pygame.Rect(ship_r.x , ship_r.y,10,5)
                    missiles.append(missile)
        # missile/torpedo from enemy ship
        missile_e = pygame.Rect(enemy_r.x , enemy_r.y + enemy_r.height//2 - 2,10,5)
        missiles_e.append(missile_e)

                    
        
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
        for space in enemy_l:
            # speed of smaller enemy ship
            space.y += 4
            # check whether ship is beyond screen view and remove it from the list
            if space.y > HEIGHT:
                enemy_l.remove(space)

            for missile_s in missiles:
                # speed of missiles
                missile_s.y -= 6
                if missile_s.colliderect(space):
                    pygame.event.post(pygame.event.Event(missile_hit))
                    enemy_l.remove(space)
                    missiles.remove(missile_s)
                elif space in enemy_l  and space.y > HEIGHT:
                    enemy_l.remove(space)
                

        gala_win.fill((255,255,255))
        gala_win.blit(ship,(ship_r.x,ship_r.y))
        for spaceD in enemy_l:
            gala_win.blit(enemy,(spaceD.x,spaceD.y))
        for missileS in missiles:
            gala_win.blit(torpedo,(missileS))
            #pygame.draw.rect(gala_win,red,missileS)
        pygame.display.update()
        clock.tick(FPS)
        

    pygame.quit()

if __name__ == '__main__':
    main()
