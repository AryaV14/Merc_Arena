import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 200
screen_width = 640
screen_height = 440 + bottom_panel


screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Merc Arena')


#images
#bg image
background = pygame.image.load('images/background/bg_img_Medium.jpeg').convert_alpha()
bottom = pygame.image.load('images/bottompanel/panel.jpeg').convert_alpha()

def draw_img():
    screen.blit(background, (0,0))
def draw_panel():
    screen.blit(bottom, (0,screen_height - bottom_panel))
    
    
class Fighter():
    def __init__(self,x,y,name, max_hp,strength,potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        img = pygame.image.load(f'images/{self.name}/Idle/0.png')
        self.image = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)
    
merc = Fighter(180, 260, 'merc', 30, 10 ,3)
enemy1 = Fighter(400, 270, 'enemy', 20, 6, 1)
enemy2 = Fighter(520, 270, 'enemy', 20, 6, 1)

enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)


run = True
while run:
    
    
    
    clock.tick(fps)
    draw_img()
    draw_panel()
    merc.draw()
    for e in enemy_list:
        e.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
            
pygame.quit()
    