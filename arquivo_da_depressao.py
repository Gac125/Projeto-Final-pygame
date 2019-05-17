# -*- coding: utf-8 -*-
"""
Jogo Marvel - Giovanna Alves, Giulia Castro e Pedro Célia
"""
import pygame
import random
import time
from os import path
from config_depressao import img_dir, snd_dir, fnt_dir, WIDTH, HEIGHT, BLACK, YELLOW, RED, FPS, QUIT, WHITE, GREY


screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Avengers the game")

vec=pygame.math.Vector2
#Propriedades do Player
PLAYER_ACC=0.5
PLAYER_FRICTION=-0.1

class Player(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, player_img, manager):     
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self) 
        # Carregando a imagem de fundo.
        self.image = player_img
        self.manager = manager
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (200,175))
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 3
        self.rect.bottom = HEIGHT - 10
        # Velocidade
        self.pos=vec(WIDTH/2, HEIGHT/2)
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 25

    def update(self):
        Velocidade = False
        if Velocidade:
            self.acc = vec(0,0.5)
        if not Velocidade:
            self.acc = vec(0,0)
        keys=pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]:
            self.acc.x=-PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x=PLAYER_ACC
        
        self.acc += self.vel*PLAYER_FRICTION
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
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager       
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (200, 160))                
        # Deixando transparente.
        self.image.set_colorkey(WHITE)       
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(-3, 3)
  #      self.speedy = random.randrange(2, 9)
        self.speedy = 0       
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Sorteia um lugar inicial em x
        self.px = 1052
        # Sorteia um lugar inicial em y
#        self.py = random.randrange(-100, -40) 
        self.py = HEIGHT - 170
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
  #      if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
  #          self.rect.x = random.randrange(WIDTH - self.rect.width)
  #          self.rect.y = random.randrange(-100, -40)
  #          self.speedx = random.randrange(-3, 3)
  #          self.speedy = random.randrange(2, 9)
      

class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, x, y, bullet_img):    
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)      
        # Carregando a imagem de fundo.
        self.image = bullet_img    
        # Deixando transparente.
        self.image.set_colorkey(BLACK)     
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()     
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y+60
        self.rect.centerx = x
      #  self.vel = vec(10,0)
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()


class platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

          
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

def game_screen(screen):

    assets = load_assets(img_dir)

    clock = pygame.time.Clock()

    background = assets["background"]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Avengers the Game")

    manager = GameManager()

    player = Player(assets["player_img"], manager)

# Cria um grupo de todos os sprites e adiciona a nave.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

#Cria um gupo de plataforma
    platforms = pygame.sprite.Group()
    pl = platform(0, HEIGHT - 25, WIDTH, 100)
    all_sprites.add(pl)

# Cria um grupo só do thanos
    mobs = pygame.sprite.Group()

# Cria um grupo para tiros
    bullets = pygame.sprite.Group()

# Cria 8 meteoros e adiciona no grupo thanos
    for i in range(10):
        m = Mob(assets["mob_img"], manager)
        all_sprites.add(m)
        mobs.add(m)

#try:  

#    running = True

#    def update(self):
#     self.all.sprites.update()
#     hits = pygame.sprite.spritecollide(self.player,self.platforms,False)
#     if hits:
#       self.player.pos.y = hits[0].rect.top
#        self.player.vel.y = 0


    PLAYING = 0
    EXPLODING = 1
    DONE = 2

    state = PLAYING
    while state != DONE:
    #while running:

        clock.tick(FPS)

        if state == PLAYING:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_LEFT:
#                    player.acc.x = -8
                    if event.key == pygame.K_RIGHT:
                        player.acc.x = 8
                    if event.key == pygame.K_UP:
                        player.speedy = -50
#                if event.key == pygame.K_DOWN:
#                    player.speedy = 50
                    if event.key == pygame.K_SPACE:
                        bullet = Bullet(player.rect.centerx, player.rect.top, assets["bullet_img"])
                        all_sprites.add(bullet)
                        bullets.add(bullet)        
#            if event.type == pygame.KEYUP:
#                if event.key == pygame.K_LEFT:
#                   player.acc.x = 0
#                if event.key == pygame.K_RIGHT:
#                    player.acc.x = 0
#                if event.key == pygame.K_UP:
#                    player.speedy = 0

        all_sprites.update()


        if state == PLAYING:    

         # Verifica se houve colisão entre propulsor e Thanos
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
                m = Mob(assets["mob_img"], manager)
                v = Mob(assets["mob_img"], manager)
                all_sprites.add(m)
                all_sprites.add(v)
                mobs.add(m)
                mobs.add(v)

        # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
            if hits:
                # Toca o som da colisão
               time.sleep(1) # Precisa esperar senão fecha
               state = DONE
        #Verifica se houve colisão entre a plataforma e o player
    #    hits = pygame.sprite.spritecollide(player,platform,True,True)
    #    for hit in hits:
    #       Velocidade = True
            # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        background_rect = background.get_rect()
        background_rect.x = -manager.px
        background_rect.y = -manager.py
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return QUIT
        
#finally:
    
#    pygame.quit()
    
    
    
    
    
