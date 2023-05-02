########################################################################
###                          BACKUP                                  ###
########################################################################
import pygame
import time
import os
import random
WIDTH ,HEIGHT = 1280,720
FPS=60

WHITE = (255,255,255)
GREEN=(0,255,0)
BLACK = (0,0,0)
#initialize
pygame.init()
pygame.mixer.get_init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("CapyFight")
clock=pygame.time.Clock()
#background
####   FRAMES #####
bg_frame=0
refresh = pygame.USEREVENT + 1
pygame.time.set_timer(refresh,100)
################################################################
jumping = False
DASH_CHANGE=0

recover = pygame.USEREVENT + 2
pygame.time.set_timer(recover,3000)#recover 10 hp every 3 secs
#SOUND EFFECTS
dash_sound=pygame.mixer.Sound("slideslidebaby.wav")
catbomb_sound = pygame.mixer.Sound("Bomb.mp3")
oraoraora_sound = pygame.mixer.Sound("NEWCutORA.mp3")
lightning_sound = pygame.mixer.Sound("Electricity.mp3")
jumping_sound=pygame.mixer.Sound("yahoo.mp3")
pygame.mixer.Sound.set_volume(dash_sound,0.2)
pygame.mixer.Sound.set_volume(catbomb_sound,0.05)
pygame.mixer.Sound.set_volume(oraoraora_sound,0.2)
pygame.mixer.Sound.set_volume(jumping_sound,0.05)
### MISTSAKE (1) ###
pygame.mixer.music.load("BATTLE.mp3")
pygame.mixer.music.set_volume(0.2)
################################################################

#position
X_POSITION = 250#initial position
Y_POSITION = 590#initial position
FACING = 1  #  player's FACING
Hog_facing = -1

# score on screen
font_name = os.path.join("font.ttf")

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)#True = anti-alias
    text_rect = text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
def new_small_rock():#recreate rock 
    r=Rock()
    all_sprites.add(r)
    rocks.add(r)
def draw_health(surf, hp, x, y):#HP
    if hp < 0:
        hp = 0
    BAR_LENGTH=200
    BAR_HEIGHT=10
    fill =(hp/200)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)#inside 
    pygame.draw.rect(surf, WHITE, outline_rect, 2)#border

def draw_init():#初始畫面
    screen.fill(BLACK)
    image = pygame.image.load("capybara.png")
    screen.blit(image,(WIDTH/2,HEIGHT/2))
    draw_text(screen, 'CapyFight', 64, WIDTH/2,HEIGHT/4)
    draw_text(screen, '[<- -> move Capy]  [SPACE or W for jump]  [LSHIFT, J , K , L for attack]', 22 , WIDTH/2 , HEIGHT/2)
    draw_text(screen, 'press any button', 18 , WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:#鬆開
                waiting = False
                return False

#----------------------------------------------------------------
#Player
class Player(pygame.sprite.Sprite):#the capy 
    global X_POSITION,Y_POSITION
    def  __init__(self):
        pygame.sprite.Sprite. __init__(self)
        self.image=pygame.image.load("capyR.png")
        self.rect=self.image.get_rect(center=(X_POSITION,Y_POSITION))
        #self.rect.bottom=HEIGHT-40
        self.speedx = 15
        self.speedy = -30
        self.previous = X_POSITION
        self.health = 200
    def update(self):
        global FACING
        key_pressed=pygame.key.get_pressed()
        #keyboard movement
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.rect.x+=self.speedx
            self.image=pygame.image.load("capyR.png")
            FACING=1
        if key_pressed[pygame.K_LEFT]or key_pressed[pygame.K_a]:
            self.rect.x-=self.speedx
            self.image=pygame.image.load("capyL.png")
            FACING=-1
### MISTSAKE (2) ###  #JUMPING
        global jumping
        gravity=1
        if key_pressed[pygame.K_SPACE]or key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            jumping_sound.play()
            jumping = True
        if jumping:
            self.rect.y+=self.speedy
            self.speedy+=gravity
            if self.speedy>30:
                jumping = False
                self.speedy=-30
        
################################################################
        #----------------------------------------------------------------  
        if self.rect.bottom>=HEIGHT:self.rect.bottom=HEIGHT
        if self.rect.right>WIDTH:self.rect.right=WIDTH
        if self.rect.left<0:self.rect.left=0
    
    def dash(self):
        dash = Dash(self.rect.centerx,self.rect.bottom)
        all_sprites.add(dash)
        dash_sound.play()
        attack.add(dash)
    def bomb(self):
        CatBomb = Bomb(self.rect.centerx,self.rect.centery)
        all_sprites.add(CatBomb)
        catbomb_sound.play()
        bomb.add(CatBomb)
    def oraoraora(self):
        if FACING == 1:
            oraora = ORA(self.rect.right,self.rect.bottom-100)
        else:
            oraora = ORA(self.rect.left,self.rect.bottom-100)
        all_sprites.add(oraora)
        oraoraora_sound.play()
        attack.add(oraora)
    def LIGHTNING(self):
        Thunder = lightning(self.rect.x+150*FACING,self.rect.top-50)
        all_sprites.add(Thunder)
        attack.add(Thunder)
class Dash(pygame.sprite.Sprite):###PRESS LSHIFT
    global FACING
    def __init__(self,x,y):
        pygame.sprite.Sprite. __init__(self)
        if FACING==1:
            self.image=pygame.image.load("capydashR.png")
        else:
            self.image=pygame.image.load('capydashL.png')
        self.rect=self.image.get_rect()
        self.rect.centerx = x
        self.previous = x
        self.rect.bottom = y+70
        self.speedx = 20*FACING
    def update(self):
        global DASH_CHANGE
        self.rect.x+=self.speedx
        
        if self.rect.right<0 or self.rect.left>WIDTH:self.kill()  
class Bomb(pygame.sprite.Sprite):###PRESS E
    global FACING
    def __init__(self,x,y):
        pygame.sprite.Sprite. __init__(self)
        self.image=pygame.image.load("catbomb.gif")
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect=self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y      
        self.speedx = 15*FACING
        self.speedy=-20
    def update(self):
        height = 20
        vel = height
        
        gravity = 1
        exploded = 0 #disappear after exploded
        self.rect.x+=self.speedx
        if vel>=-height:
            self.rect.y+=self.speedy
            self.speedy+=gravity
            vel-=gravity
        if vel<-height:vel=5
        if self.rect.right<0 or self.rect.left>WIDTH:self.kill()  
class ORA(pygame.sprite.Sprite):###PRESS Q
    def __init__(self,x,y):
        global FACING 
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join(f"oraora{FACING}","frame_0_delay-0.05s.gif")))
        self.sprites.append(pygame.image.load(os.path.join(f"oraora{FACING}","frame_1_delay-0.05s.gif")))
        self.sprites.append(pygame.image.load(os.path.join(f"oraora{FACING}","frame_2_delay-0.05s.gif")))
        self.sprites.append(pygame.image.load(os.path.join(f"oraora{FACING}","frame_3_delay-0.05s.gif")))
        self.sprites.append(pygame.image.load(os.path.join(f"oraora{FACING}","frame_4_delay-0.05s.gif")))
        self.sprites.append(pygame.image.load(os.path.join(f"oraora{FACING}","frame_5_delay-0.05s.gif")))
        self.current_sprite=0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx = x-50*FACING
        self.rect.bottom = y
    def update(self):
        self.current_sprite +=0.35
        if self.current_sprite >=len(self.sprites):
            self.kill()
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
class lightning(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning0.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning1.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning2.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning3.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning4.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning5.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning6.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning7.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning8.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning9.png")))        
        self.sprites.append(pygame.image.load(os.path.join("CutLightning","Cutlightning10.png"))) 
        self.current_sprite= 0
        self.image=self.sprites[self.current_sprite]
        
        self.rect= self.image.get_rect()
        self.rect.centerx=x
        self.rect.top = y
    def update(self):
        
        if self.current_sprite>=5:
            self.current_sprite+=0.6
        else:
            self.current_sprite+=0.4
        if self.current_sprite >=len(self.sprites):
            self.kill()
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]    
        #self.image = pygame.transform.scale(self.image,(450,600))
#ENEMY
class Rock(pygame.sprite.Sprite):#Rocks from right
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("rock5.png")
        self.image = pygame.transform.scale(self.image,(50,40))
        self.rect = self.image.get_rect()
        #a = random.randrange(-100,-20)
        b = random.randrange(1400,2000)
        self.rect.x =b
        self.rect.y = random.randrange(300,620)  
        self.speedx = random.randrange(-5,-1) 
    def update(self):
        self.rect.x += self.speedx
        if self.rect.left<0:
            b = random.randrange(1400,2000)
            self.rect.x =b
            self.rect.y = random.randrange(300,590)  
            self.speedx = random.randrange(-5,-1)            
class Fast_Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("THERock2.png")
        self.rect = self.image.get_rect()
        b = random.randrange(1300,3000)  
        self.rect.x = b
        self.rect.centery = 630
        self.speedx = random.randrange(15,20)
    def update(self):
        self.rect.x-=self.speedx 
        if self.rect.left<0:
            b = random.randrange(1300,1800)  
            self.rect.x = b
            self.rect.centery = 630
            self.speedx = random.randrange(3,20)        
#all sprite
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
attack = pygame.sprite.Group()
bomb=pygame.sprite.Group()
fastrock = Fast_Rock()
THEROCK = pygame.sprite.Group()
player =  Player()
all_sprites.add(player)
all_sprites.add(fastrock)
THEROCK.add(fastrock)
for i in range(20):
    r=Rock()
    all_sprites.add(r)
    rocks.add(r)
SCORE = 0  ##分數
pygame.mixer.music.play(-1)
#game loop
show_init = True
running = True

while running:
    if show_init:
        close = draw_init() 
        if close:
            break
        show_init = False
     
    clock.tick(FPS)#max frames per second
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:running = False
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LSHIFT:
               player.dash()
            if event.key==pygame.K_k:
                player.bomb()
            if event.key==pygame.K_l:
                player.oraoraora()
            if event.key==pygame.K_j:
                player.LIGHTNING()      
        elif event.type == refresh:bg_frame+=1  
        elif event.type == recover:
            if player.health<190:
                player.health+=10
    if bg_frame>=7:bg_frame = 0
    
    #update
    all_sprites.update()
    ###   COLLISION   ###
    hits = pygame.sprite.groupcollide(rocks,attack,True,False)#rocks(dis) and attack(appear)
    for hit in hits:
        SCORE += 10### get 10 points
        if player.health<100:
            player.health+=5
        new_small_rock()
    hitss = pygame.sprite.groupcollide(rocks,bomb,True,True)#rocks(dis) and bomb(dis)
    for hit in hitss:
        SCORE +=20###get 20 points
        new_small_rock()
        if player.health<150:
            player.health+=10
    hitsss = pygame.sprite.spritecollide(player,rocks,True)#player and rocks
    for hit in hitsss:
        new_small_rock()
        player.health -=5  #PLAYER HP
        if player.health<=0:
            running = False
    hitssss = pygame.sprite.spritecollide(player,THEROCK,True)#player and fastrock
    for hit in hitssss:
        fastrock = Fast_Rock()
        all_sprites.add(fastrock)
        THEROCK.add(fastrock)
        player.health -=15
        if player.health<=0:
            running = False
    ################################################################
    #the screen 
    ###  SOLUTION (3)  ###
    BG_img = pygame.image.load(os.path.join("background",f"frame_{bg_frame}_delay-0.1s.gif")).convert()
    BG_img = pygame.transform.scale(BG_img,(WIDTH,HEIGHT))
    ################################################################
    screen.fill(WHITE)
    screen.blit(BG_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(SCORE), 18 , WIDTH/2, 10)
    draw_health(screen, player.health, 5, 10)
    pygame.display.update()
pygame.quit()




