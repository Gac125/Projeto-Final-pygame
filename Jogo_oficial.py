# -*- coding: utf-8 -*-
"""
Jogo Marvel - Giovanna Alves, Giulia Castro e Pedro Célia
"""
import pygame
import random
import time
from os import path

vec = pygame.math.Vector2

# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'Avengers anime')
#fundo = path.join(path.dirname(__file__), 'Backgrounds')

# Dados gerais do jogo.
WIDTH = 1000 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

#Propriedades do Player
PLAYER_ACC=0.5
PLAYER_FRICTION=-0.1

class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, manager):     
        pygame.sprite.Sprite.__init__(self) 
        self.image = player_img
        self.manager = manager
        self.image = pygame.transform.scale(player_img, (200,175))
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        # Velocidade
        self.pos=vec(WIDTH/2, HEIGHT/2)
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 25
    
    def update(self):
        self.acc = vec(0,0)
        keys=pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]:
            self.acc.x=-PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x=PLAYER_ACC
        #Coloca atrito no movimento
        self.acc += self.vel*PLAYER_FRICTION
        #Equações do movimento
        self.vel += self.acc        
        self.pos += self.vel+0.5*self.acc       
        self.rect.center=self.pos     
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top > HEIGHT :
            self.rect.top = HEIGHT
        if self.rect.bottom < HEIGHT:
            self.rect.bottom = HEIGHT

class Mob(pygame.sprite.Sprite): 
    # Construtor da classe.
    def __init__(self, mob_img, manager):      
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager       
        self.image = pygame.transform.scale(mob_img, (50, 38))                
        self.image.set_colorkey(WHITE)       
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 9)       
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Sorteia um lugar inicial em x
        self.px = random.randrange(WIDTH - self.rect.width)
        # Sorteia um lugar inicial em y
        self.py = random.randrange(-100, -40)       
        self.rect.x = self.px - self.manager.px
        self.rect.y = self.py - self.manager.py               
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)    
    def update(self):
        self.px += self.speedx
        self.py += self.speedy    
        self.rect.x = self.px - self.manager.px
        self.rect.y = self.py - self.manager.py             
        # Se o meteoro passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 9)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img):    
        pygame.sprite.Sprite.__init__(self)      
        self.image = bullet_img    
        self.image.set_colorkey(BLACK)     
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()     
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y+60
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx   
        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()
            
# Manager do jogo         
class GameManager:
    def __init__(self):
        self.px = 0
        self.py = 0

def load_assets(img_dir):
    Homem = path.join(img_dir, 'Iron Man')
    Thanos = path.join(img_dir, 'Thanos')
    fundo = path.join(path.dirname(__file__), 'Backgrounds')
#    tela_I = path.join(path.dirname(__file__), 'Backgrounds')
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(Homem, "Stance_Iron_Man.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(Thanos, "Stance_Thanos.png")).convert()
    assets["bullet_img"] = pygame.image.load(path.join(Homem, "Propulsor2.png")).convert()
    assets["background"] = pygame.image.load(path.join(fundo, 'houses31.png')).convert()
#    assets["title"] = pygame.image.load(path.join(tela_I, 'Tela_inicio.png')).convert()
    return assets

#

class platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Cria um gupo de plataforma

#

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Avengers the Game")

assets = load_assets(img_dir)

clock = pygame.time.Clock()

background = assets["background"]

manager = GameManager()

player = Player(assets["player_img"], manager)

# Cria um grupo de todos os sprites e adiciona o mob.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

platforms = pygame.sprite.Group()
pl = platform(0, HEIGHT - 25, WIDTH, 100)
all_sprites.add(pl)


# Cria um grupo só do thanos
mobs = pygame.sprite.Group()

# Cria um grupo para tiros
bullets = pygame.sprite.Group()

# Cria 8 meteoros e adiciona no grupo thanos
for i in range(8):
    m = Mob(assets["mob_img"], manager)
    all_sprites.add(m)
    mobs.add(m)

try:   
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update() 
        # Verifica se houve colisão entre propulsor e Thanos
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            m = Mob(assets["mob_img"], manager) 
            all_sprites.add(m)
            mobs.add(m)     
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        background_rect = background.get_rect()
        background_rect.x = -manager.px
        background_rect.y = -manager.py
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()