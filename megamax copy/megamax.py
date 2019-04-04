################################
#   EXPERIMENTAL GAME ENGINE   #
#    Designed - Max Provolt    #
#   Assistance - Adam Wolfe    #
#                              #
# This engine is meant to test #
#   the potential of sprites   #
# in python, utilizing classes.#
# This is by no means finished,#
#    and will be subject to    #
#   rigorous modification and  #
#           addendum.          #
################################

################################
#       CURRENT PROJECTS       #
#    Fixing the collisions     #
#    function so that side     #
#  collisions can be properly  #
#     detected while still     #
#  maintaining all other built #
#        functionality.        #
################################


import pygame, os, math

class Entity(pygame.sprite.Sprite):

    def stop_xVel(self): #simple function stopping the x velocity.

        self.xVel = 0

    def stop_yVel(self): #simple function stopping the y velocity.

        self.yVel = 0

    def stop_vel(self): #simple function calling stop_xVel() and stop_yVel() to stop all movement.

        self.stop_xVel()
        self.stop_yVel()
    
    def update_position(self): #function that adds the calculated change of position by other functions to the actual position of the sprite.

        self.rect.x += self.xVel
        self.rect.y += self.yVel

    def store_position(self):

        self.prev_xPos = self.rect.x
        self.prev_yPos = self.rect.y

    def is_colliding(self): #Checks if you are contacting an edge of the screen, and stops your xVel if so.
    
        if self.rect.x <= 0:
            self.rect.x = 0
            self.stop_xVel()
        if self.rect.x >= screen_width - self.character_width:
            self.rect.x = screen_width - self.character_width
            self.stop_xVel()

    def is_falling(self): #Checks 3 things : 1. if you are above the window, stop your velocity and set it to one.
                        #                  2. if you are below the window, stop your velocity and set it to ground level.
                        #                  3. if you are between, add self.gravity to the velocity. This creates a parabolic trajectory, since
                        #                     it will repeat every frame until it hits the ground.
        if self.rect.y <= 0:
            self.stop_yVel()
            self.rect.y = 1
            self.onground = False

        if self.rect.y > 0 and self.rect.y < screen_height:
            self.yVel += self.gravity

        if self.rect.y >= screen_height - self.character_height:
            self.stop_yVel()
            self.rect.y = screen_height - self.character_height
            self.onground = True
            self.damaged = False

    def find_dist(self): #simple function that finds the total distance traveled along the x axis. An absolute value is taken of the velocity,
                       #since that is how far the object travels every frame.
        self.dist += abs(self.xVel)

    def find_direction(self):

        if self.xVel > 0:
            self.direction_right = True
        if self.xVel < 0:
            self.direction_right = False



class Player(Entity): # A controllable character. The main character, as well as multiplayer characters.

    def __init__(self, xPos, yPos, character_width, character_height, player, file, rof): #Initialize the sprite's assets and functions. Runs once,
        pygame.sprite.Sprite.__init__(self)
    

        #Size
        self.character_width = character_width
        self.character_height = character_height

        #Appearance
        self.color = (255, 255, 255)
        self.file = file

        #Surface ***
        self.image = pygame.Surface([self.character_width, self.character_height])
        self.image_name = directory + self.file + "idle_right.png"

        #Rect ***
        self.rect = self.image.get_rect()

        #Position of the Sprite
        self.rect.x = xPos
        self.rect.y = yPos
        self.dist = 0

        #Velocity of the Sprite
        self.xVel = 0
        self.yVel = 0
        self.gravity = 1
        self.speed = 5
        self.jump_height = 20

        #Shooting
        self.shoot_cooldown = 0
        self.rof = rof

        #Player Type
        self.player = player

        #Booleans
        self.onground = True
        self.direction_right = False
        self.damaged = False

        #Sounds
        self.loaded_sound = ""

    def sprite_render(self): #function that uses remainders to determine which image to render onto the sprite at any given point in time.
                           #it also uses whether the velocity is positive or negative to determine which direction the image should be
        if (self.dist + 50) % 50 >= 0 and (self.dist + 50) % 50 < 10: #displayed to be going.
            if self.direction_right == False: # if the object is moving left
                self.image_name = directory + self.file + "move_left_1.png"
            elif self.direction_right == True: # if the object is moving right
                self.image_name = directory + self.file + "move_right_1.png"
        
        if (self.dist + 50) % 50 >= 10 and (self.dist + 50) % 50 < 20:
            if self.direction_right == False:
                self.image_name = directory + self.file + "move_left_2.png"
            elif self.direction_right == True:
                self.image_name = directory + self.file + "move_right_2.png"

        if (self.dist + 50) % 50 >= 20 and (self.dist + 50) % 50 < 30:
            if self.direction_right == False:
                self.image_name = directory + self.file + "move_left_3.png"
            elif self.direction_right == True:
                self.image_name = directory + self.file + "move_right_3.png"

        if (self.dist + 50) % 50 >= 30 and (self.dist + 50) % 50 < 40:
            if self.direction_right == False:
                self.image_name = directory + self.file + "move_left_4.png"
            elif self.direction_right == True:
                self.image_name = directory + self.file + "move_right_4.png"

        if (self.dist + 50) % 50 >= 40 and (self.dist + 50) % 50 < 50:
            if self.direction_right == False:
                self.image_name = directory + self.file + "move_left_5.png"
            elif self.direction_right == True:
                self.image_name = directory + self.file + "move_right_5.png"

        if self.xVel == 0:
      
            if self.direction_right == False:
                self.image_name = directory + self.file + "idle_left.png"
            elif self.direction_right == True:
                self.image_name = directory + self.file + "idle_right.png"
        
            self.dist = 0

        if not self.onground:

            if self.direction_right == False:
                self.image_name = directory + self.file + "jump_left.png"
            elif self.direction_right == True:
                self.image_name = directory + self.file + "jump_right.png"

            self.dist = 0

        if self.damaged:

            if self.direction_right == False:
                self.image_name = directory + self.file + "damage_left.png"
            if self.direction_right == True:
                self.image_name = directory + self.file + "damage_right.png"

        #Load Image
        self.image = pygame.transform.scale((pygame.image.load(self.image_name)), (self.character_width, self.character_height))
        
    def movements(self):

        if not self.damaged:

            if self.player == "P1":
                if self.keys[pygame.K_RIGHT]:
                    self.xVel = self.speed
                if self.keys[pygame.K_LEFT]:
                    self.xVel = -1 * self.speed
                if self.keys[pygame.K_UP] and self.onground:
                    self.yVel = -1 * self.jump_height
                    self.onground = False
                if not self.keys[pygame.K_RIGHT] and not self.keys[pygame.K_LEFT]:
                    self.xVel = 0

            if self.player == "P2":
                if self.keys[pygame.K_d]:
                    self.xVel = self.speed
                if self.keys[pygame.K_a]:
                    self.xVel = -1 * self.speed
                if self.keys[pygame.K_w] and self.onground:
                    self.yVel = -1 * self.jump_height
                    self.onground = False
                if not self.keys[pygame.K_d] and not self.keys[pygame.K_a]:
                    self.xVel = 0

    def shoot(self):

        if not self.damaged:

            if self.keys[pygame.K_SPACE] and self.player == "P1" and self.shoot_cooldown <= total_frames:

                if self.direction_right == True:
                    bullet = Bullet((self.rect.x + self.character_width), (self.rect.y + ((1/3) * self.character_height)), 30, 15, 15, self.player, "megaman_bullet/")
                if self.direction_right == False:
                    bullet = Bullet((self.rect.x - 15), (self.rect.y + ((1/3) * self.character_height)), -30, 15, 15, self.player, "megaman_bullet/")

                projectiles.add(bullet)
                allSprites.add(bullet)
                self.shoot_cooldown = total_frames + self.rof

        if self.keys[pygame.K_LSHIFT] and self.player == "P2" and total_frames >= self.shoot_cooldown:

            if self.direction_right == True:
                bullet = Bullet((self.rect.x + self.character_width), (self.rect.y + ((1/3) * self.character_height)), 30, 15, 15, self.player, "megaman_bullet/")
            if self.direction_right == False:
                bullet = Bullet((self.rect.x - 15), (self.rect.y + ((1/3) * self.character_height)), -30, 15, 15, self.player, "megaman_bullet/")

            projectiles.add(bullet)
            allSprites.add(bullet)
            self.shoot_cooldown = total_frames + self.rof
          
    def events(self):

        self.keys = pygame.key.get_pressed()

        self.movements()
        self.shoot()

    def update(self):
    
        self.events()
        self.store_position()
        self.update_position()
        self.is_falling()
        self.is_colliding()
        self.find_dist()
        self.find_direction()
        self.sprite_render()



class Bullet(Entity):

    def __init__(self, xPos, yPos, xVel, character_width, character_height, player, file): #Initialize the sprite's assets and functions. Runs once,
        pygame.sprite.Sprite.__init__(self)                                             #Without needing to be called.

        #Size
        self.character_width = character_width
        self.character_height = character_height

        #Appearance
        self.color = (255, 255, 255)
        self.file = file

        #Surface ***
        self.image = pygame.Surface([self.character_width, self.character_height])
        self.image_name = directory + self.file + "bullet.png"

        #Rect ***
        self.rect = self.image.get_rect()

        #Position of the Sprite
        self.rect.x = xPos
        self.rect.y = yPos
        self.dist = 0
        self.is_hit = False

        #Velocity of the Sprite
        self.xVel = xVel

        #Player associated with the bullet
        self.player = player

        #Booleans
        self.direction_right = None

      # Bullet() functions :
      # 1. Is created when Player() shoots
      # 2. Created at a specified position relative to the player
      # 3. Travels in the direction the player was aiming
      # 4. Has an animation of travel
      # 5. position, x velocity, file
    
    def update_position(self): #function that adds the calculated change of position by other functions to the actual position of the sprite.
  
        self.rect.x += self.xVel

    def find_direction(self):

        if self.xVel >= 0:
            self.direction_right = True
      
        if self.xVel <= 0:
            self.direction_right = False

    def sprite_render(self):
    
        self.image_name = directory + self.file + "bullet.png"
        self.image = pygame.transform.scale((pygame.image.load(self.image_name)), (self.character_width, self.character_height))

    def is_kill(self):

        if self.rect.x < -(self.character_height) or self.rect.x > screen_width:
            self.kill()

    def update(self):
        self.sprite_render()
        self.update_position()
        self.find_direction()
        self.is_kill()



class Tile(Entity):

    def __init__(self, xPos, yPos, character_width, character_height, file):

        pygame.sprite.Sprite.__init__(self)

        #Size
        self.character_width = character_width
        self.character_height = character_height

        #Appearance
        self.color = (255, 255, 255)
        self.file = file

        #Surface ***
        self.image = pygame.Surface([self.character_width, self.character_height])
        self.image_name = directory + self.file + "wall.png"

        #Rect ***
        self.rect = self.image.get_rect()

        #Position of the Sprite
        self.rect.x = xPos
        self.rect.y = yPos

    def sprite_render(self):

        self.image = pygame.transform.scale((pygame.image.load(self.image_name)), (self.character_width, self.character_height))

    def update(self):

        self.sprite_render()



def collisions():

    is_x = None
    is_y = None

    for player in players:
        for projectile in projectiles:
            if pygame.sprite.collide_rect(player, projectile) and projectile.player != player.player:

                if not player.damaged:

                    if projectile.direction_right:

                        player.xVel = 3
                        player.direction_right = True

                    if not projectile.direction_right:

                        player.xVel = -3
                        player.direction_right = False

                    projectile.kill()
                    player.damaged = True
                    player.yVel = -5

    for player in players:
        for tile in tiles:

            test_tile = Tile(player.prev_xPos, player.prev_yPos, player.character_width, player.character_height, "tile_wall_gray/")

            top = Tile(tile.rect.x, tile.rect.y, tile.character_width, 1, "tile_wall_gray/")
            left = Tile(tile.rect.x, tile.rect.y, 1, tile.character_height, "tile_wall_gray/")
            right = Tile((tile.rect.x + tile.character_width - 1), tile.rect.y, tile.character_height, 1, "tile_wall_gray/")
            bottom = Tile((tile.rect.x + tile.character_height), (tile.rect.y - 1), tile.character_width, 1, "tile_wall_gray/")

            if pygame.sprite.collide_rect(player, tile):

                if abs((player.rect.y + player.character_height) - tile.rect.y) < abs(player.rect.y - tile.rect.y):

                    player.rect.y = tile.rect.y - player.character_height + 1
                    player.stop_yVel()
                    player.onground = True

            if abs((player.rect.y + player.character_height) - tile.rect.y) > abs(player.rect.y - tile.rect.y):

                player.rect.y = tile.rect.y + tile.character_height + 1
                player.stop_yVel()

################### | CODE CURRENTLY EXPERIMENTING WITH | ####################
#                  \/                                   \/
##        if pygame.sprite.collide_rect(player, top) or pygame.sprite.collide_rect(player, bottom):
##
##          if pygame.sprite.collide_rect(player, top):
##            player.rect.y = tile.rect.y - player.character_height
##            player.onground = True
##
##          if pygame.sprite.collide_rect(player, bottom):
##            player.rect.y = tile.rect.y + tile.character_height
##          player.stop_yVel()

###############################################################################

            else:

                if pygame.sprite.collide_rect(test_tile, tile):

                    player.onground = False

            test_tile.kill()
            top.kill()
            bottom.kill()
            left.kill()
            right.kill()
      


    for tile in tiles:
        for projectile in projectiles:
            if pygame.sprite.collide_rect(projectile, tile):

                projectile.kill()

def update_all():

    allSprites.update()
    collisions()
  



#constants
screen_width = 1000 #
screen_height = 500 #change these if needed until better solution arises
bg_color = (255, 255, 255)
screen = pygame.display.set_mode([screen_width, screen_height])
directory = os.path.dirname(os.path.realpath("megamax.py")) + "/"
end_shell = False
total_frames = 0

#MAC directory - "/Users/maximilian.provolt/Desktop/Code/Python/megamax/"
#PI directory - "/home/pi/Desktop/Python/megamax/"

pygame.init()

pygame.display.set_caption("|<>| MEGAMAX |<>|")

#clock
fps = 40
clock = pygame.time.Clock()

#groups
allSprites = pygame.sprite.Group()
players = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
tiles = pygame.sprite.Group()

#sprites
player1 = Player(screen_width * 0.25, screen_height * .5, 50, 50,  "P1", "megaman/", 5)
player2 = Player(screen_width * 0.25, screen_height * .5, 50, 50,  "P2", "megaman/", 5)
tile = Tile(450, 300, 200, 5, "tile_wall_gray/")
tile1 = Tile(200, 100, 200, 5, "tile_wall_gray/")
tile2 = Tile(400, 200, 200, 5, "tile_wall_gray/")

allSprites.add(player1)
allSprites.add(player2)
allSprites.add(tile)
allSprites.add(tile1)
allSprites.add(tile2)
players.add(player1)
players.add(player2)
tiles.add(tile)
tiles.add(tile1)
tiles.add(tile2)

while not end_shell:

  #Event Handling
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            end_shell = True

  #Clear the Screen
    screen.fill(bg_color)

  #Updates
    update_all()

  #Drawing
    allSprites.draw(screen)

  #Next frame
    total_frames += 1
  
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
