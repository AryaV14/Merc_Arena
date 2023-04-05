import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 200
screen_width = 640
screen_height = 440 + bottom_panel


screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Merc Arena')

current_fighter = 1  #1=merc 2=enemy1 3=enemy2
total_fighters = 3
action_cooldown = 0  
action_wait_time = 90
attack =False
potion =False
clicked =False

font = pygame.font.SysFont('Roboto', 26)

red=(255,0,0)
green=(0,255,0)
#images
#bg image
background = pygame.image.load('images/background/bg_img_Medium.jpeg').convert_alpha()
bottom = pygame.image.load('images/bottompanel/panel.jpeg').convert_alpha()
sword = pygame.image.load('images/icons/sword.png').convert_alpha()



#function to add text to panel since text cannot be directly written on to the pygame window
def draw_text(text,font,text_color,x,y):
    img = font.render(text,True,text_color)
    screen.blit(img,(x,y))


#blit method - for placing the image on to the screen
def draw_img():
    screen.blit(background, (0,0))
def draw_panel():
    screen.blit(bottom, (0,screen_height - bottom_panel))
    draw_text(f'{merc.name} HP: {merc.hp}',font, red,100,screen_height-bottom_panel +10)
    for count, i in enumerate(enemy_list):
        draw_text(f'{i.name} HP: {i.hp}',font, red,400,(screen_height-bottom_panel +10)+count*60)
        
    
    
class Fighter():
    def __init__(self,x,y,name, max_hp,strength,potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = [] #each action and its frames
        self.frame_index = 0
        self.action = 0 # 0: idle 1: attack 2: hurt 3: dead
        self.update_time = pygame.time.get_ticks()
        
        #Idle
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'images/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        #Attack
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f'images/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        #Hurt
        temp_list = []
        for i in range(2):
            img = pygame.image.load(f'images/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        
        #Death
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'images/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()
     
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    #update healthbar on each attack
    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        if target.hp < 1:
            target.hp = 0
            target.alive = False
                
       
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
        
        
        
        
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x=x
        self.y=y
        self.hp=hp
        self.max_hp=max_hp
        
    def draw(self,hp):
        self.hp=hp
        ratio=self.hp/self.max_hp
        pygame.draw.rect(screen, red, (self.x,self.y,150,20))
        pygame.draw.rect(screen, green, (self.x,self.y, 150*ratio,20))
        
        
        
        
     
#instances of class fighter
merc = Fighter(180, 260, 'merc', 30, 10 ,3)
enemy1 = Fighter(400, 270, 'enemy', 20, 6, 1)
enemy2 = Fighter(520, 270, 'enemy', 20, 6, 1)

enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)

merc_healthbar =HealthBar(100,screen_height-bottom_panel+40,merc.hp,merc.max_hp)
enemy1_healthbar =HealthBar(400,screen_height-bottom_panel+40,enemy1.hp,enemy1.max_hp)
enemy2_healthbar =HealthBar(400,screen_height-bottom_panel+100,enemy2.hp,enemy2.max_hp)


potion_button = button.Button(screen, 100, screen_height - button +70, potion, 64, 64)
#game
run = True
while run:
    
    
    
    clock.tick(fps)
    draw_img()
    draw_panel()
    merc_healthbar.draw(merc.hp)
    enemy1_healthbar.draw(enemy1.hp)
    enemy2_healthbar.draw(enemy2.hp)
    merc.update()
    merc.draw()
    for e in enemy_list:
        e.update()
        e.draw()
        
    
    attack =False
    potion =False
    target = None
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, enemy in enumerate(enemy_list):
        if enemy.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            screen.blit(sword,pos)
            if clicked == True:
                attack = True
                target = enemy_list[count]
                
            
    if merc.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                if attack == True and target != None:
                    merc.attack(target)
                    current_fighter += 1
                    action_cooldown = 0
                
    for count, enemy in enumerate(enemy_list):
        if current_fighter == 2 + count:
            if enemy.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    enemy.attack(merc)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter += 1
    if current_fighter > total_fighters:
        current_fighter = 1
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else: 
            clicked = False
    pygame.display.update()
            
pygame.quit()
    
