# -*- coding: utf-8 -*-
"""
Jogo Marvel - Giovanna Alves, Giulia Castro e Pedro Célia
"""
import pygame
import random
import time
from os import path
from config_depressao import img_dir, snd_dir, fnt_dir, WIDTH, HEIGHT, BLACK, YELLOW, RED, FPS, QUIT, WHITE, GREY

INITIAL_BLOCKS = 10
TILE_SIZE = 80
SPEED_X = 10
SPEED_Y = -5

# Define a aceleração da gravidade
GRAVITY = 2
# Define a velocidade inicial no pulo
JUMP_SIZE = 30
# Define a altura do chão
GROUND = HEIGHT * 6.2 // 6

# Define estados possíveis do jogador
STILL = 0
JUMPING = 1
FALLING = 2


screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Avengers the game")

BLOCK = 0
EMPTY = -1

MAP = [
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY],
    [BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK],
    [EMPTY, EMPTY, BLOCK, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, BLOCK, BLOCK, BLOCK],
    [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
    [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
]


class Tile(pygame.sprite.Sprite):
    # Construtor da classe.
    # Construtor da classe.
    def __init__(self, tile_img, row, column):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o tile
        self.rect.x = TILE_SIZE * column
        self.rect.y = TILE_SIZE * row

class Player(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, player_img, row, column,  blocks):     
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self) 
        # Carregando a imagem de fundo.
        self.state = STILL

        self.image = player_img
#        self.manager = manager
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (200,175))
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        self.blocks = blocks

        self.rect.x = column * TILE_SIZE
        self.rect.bottom = row * TILE_SIZE
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 3
        self.rect.bottom = HEIGHT + 30
        # Velocidade
        self.speedx = 0
        self.speedy = 0
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 25

    def update(self):
        self.speedy += GRAVITY

        if self.speedy > 0:
            self.state = FALLING
        self.rect.y +=self.speedy

        collisions = pygame.sprite.spritecollide(self, self.blocks, False)

        for collision in collisions:
        # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = STILL
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = STILL

            if self.rect.bottom > GROUND:
                self.rect.bottom = GROUND
                self.speedy = 0
                self.state = STILL

        for collision in collisions:
        # Estava indo para a direita
            if self.speedx > 0:
               self.rect.right = collision.rect.left
        # Estava indo para a esquerda
            elif self.speedx < 0:
               self.rect.left = collision.rect.right


    def jump(self):
        # Só pode pular se ainda não estiver pulando ou caindo
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING 
 #       keys=pygame.key.get_pressed() 
 #       if keys[pygame.K_LEFT]:
 #           self.acc.x=-PLAYER_ACC
 #       if keys[pygame.K_RIGHT]:
 #           self.acc.x=PLAYER_ACC
 #       if keys[pygame.K_UP]:
 #           self.acc.y = PLAYER_JUMP
            

class Mob(pygame.sprite.Sprite): 
    # Construtor da classe.
    def __init__(self, mob_img):      
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)      
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
        self.rect.x = 1052
        self.rect.y = HEIGHT - 170          
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy              
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
    assets["block_img"] = pygame.image.load(path.join(img_dir, 'block.png')).convert()
    assets["player_attack"] = pygame.image.load(path.join(Homem, "Ataque propulsor.png")).convert()
#    assets["title"] = pygame.image.load(path.join(tela_I, 'Tela_inicio.png')).convert()
    return assets

def game_screen(screen):

    assets = load_assets(img_dir)

    clock = pygame.time.Clock()

    background = assets["background"]

    background_rect = background.get_rect()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Avengers the Game")

    blocks = pygame.sprite.Group()
 #   manager = GameManager()

    player = Player(assets["player_img"], blocks)

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
    for i in range(20):
        m = Mob(assets["mob_img"])
        all_sprites.add(m)
        mobs.add(m)


    world_sprites = pygame.sprite.Group()
    # Cria blocos espalhados em posições aleatórias do mapa
   # for i in range(INITIAL_BLOCKS):
    #    block_x = random.randint(0, WIDTH)
    #    block_y = random.randint(0, int(HEIGHT * 0.25))
    #    block_y = HEIGHT - 30
    #    block = Tile(assets["block_img"], block_x, block_y)
    #    world_sprites.add(block)
        # Adiciona também no grupo de todos os sprites para serem atualizados e desenhados
    #    all_sprites.add(block)

    for row in range(len(MAP)):
        for column in range(len(MAP[row])):
            tile_type = MAP[row][column]
            if tile_type == BLOCK:
                tile = Tile(assets[tile_type], row, column)
                all_sprites.add(tile)
                blocks.add(tile)


#try:  

#    running = True


    PLAYING = 0
    EXPLODING = 1
    DONE = 2

    state = PLAYING
    while state != DONE:
    #while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE

            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
                all_sprites.add(m)
                mobs.add(m)
            # Verifica se houve colisão entre o player e o meteoro ou com bola de ferro
            hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
            ht=pygame.sprite.spritecollide(player, world_sprites, False, pygame.sprite.collide_circle)            

            if hits: #or ht:
               state = DONE
            if ht: 
                player.rect.centerx = ht[0].rect.top
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_LEFT:
                    player.speedx -= SPEED_X
                elif event.key == pygame.K_RIGHT:
                    player.speedx += SPEED_X
                elif event.key == pygame.K_DOWN:
                    player.speedy -= SPEED_Y
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top, assets["bullet_img"])
                    all_sprites.add(bullet)
                    bullets.add(bullet)                   
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_LEFT:
                    player.speedx += SPEED_X
                elif event.key == pygame.K_RIGHT:
                    player.speedx -= SPEED_X
                elif event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_DOWN:
                    player.speedy = 0           

        for block in world_sprites:
            block.speedx = -player.speedx   
            
        all_sprites.update()

        background_rect.x -= player.speedx
        # Se o fundo saiu da janela, faz ele voltar para dentro.Verifica se o fundo saiu para a esquerda
        if background_rect.right < 0:
            background_rect.x += background_rect.width            
        # Verifica se o fundo saiu para a direita
        if background_rect.left >= WIDTH:
            background_rect.x -= background_rect.width      
        for block in world_sprites:
            if block.rect.right < 0:
                # Destrói o bloco e cria um novo no final da tela
                block.kill()
                block_x = random.randint(WIDTH, int(WIDTH * 1.5))
                block_y = random.randint(0, int(HEIGHT * 0.75))
                new_block = Tile(assets["block_img"], block_x, block_y)
                all_sprites.add(new_block)
                world_sprites.add(new_block)
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)      
        # Desenha o fundo e uma cópia para a direita. Assumimos que a imagem selecionada ocupa pelo menos o tamanho da janela.
        # Além disso, ela deve ser cíclica, ou seja, o lado esquerdo deve ser continuação do direito.
        screen.blit(background, background_rect)        
        # Desenhamos a imagem novamente, mas deslocada em x.
        background_rect2 = background_rect.copy()
        if background_rect.left > 0:
            # Precisamos desenhar o fundo à esquerda
            background_rect2.x -= background_rect2.width
        else:
            # Precisamos desenhar o fundo à direita
            background_rect2.x += background_rect2.width
            

        #Verifica se houve colisão entre a plataforma e o player

             #A cada loop, redesenha o fundo e os sprites
      
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

pygame.init()
pygame.mixer.init()
#finally:
    
#    pygame.quit()