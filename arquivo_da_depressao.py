"""
Jogo Marvel - Giovanna Alves, Giulia Castro e Pedro Célia
"""
import pygame
import random
from os import path
from config_depressao import img_dir, WIDTH, HEIGHT, BLACK, FPS, WHITE, GREY, INITIAL_BLOCKS, TILE_SIZE, SPEED_X, SPEED_Y, GRAVITY, JUMP_SIZE, GROUND, STILL, JUMPING, FALLING

# Nome do jogo
pygame.display.set_caption("Avengers the game")

class Tile(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, tile_img, x, y):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
        # Define a imagem do tile.
        self.image = tile_img
        self.image.set_colorkey(WHITE)
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Posiciona o tile
        self.rect.x = x
        self.rect.y = y
        self.speedx = 0             
    def update(self):
        self.rect.x += self.speedx

class Player(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, player_img):     
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self) 
        # Carregando a imagem de fundo.
        self.state = STILL
        self.image = player_img
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (200,175))
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 3
        self.rect.bottom = HEIGHT + 30
        # Velocidade
        self.speedx = 0
        self.speedy = 0
        # Melhora a colis�o estabelecendo um raio de um circulo
        self.radius = 25
    def update(self):
        self.speedy += GRAVITY
        if self.speedy > 0:
            self.state = FALLING
        self.rect.y +=self.speedy
        if self.rect.bottom > GROUND:
            self.rect.bottom = GROUND
            self.speedy = 0
            self.state = STILL

    def jump(self):
        # S� pode pular se ainda n�o estiver pulando ou caindo
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING             

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
        self.speedy = 0       
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Sorteia um lugar inicial em x
        self.px = 1052
        # Sorteia um lugar inicial em y
        self.rect.x = 1052
        self.rect.y = HEIGHT - 170          
        # Melhora a colis�o estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy                   

class Bullet(pygame.sprite.Sprite):  
    # Construtor da classe.
    def __init__(self, x, y,direction, bullet_img):    
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        # Carregando a imagem de fundo.
        self.image = bullet_img
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()         
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y + 40
        self.rect.centerx = x + 10 
        self.speedx = 20   
        self.speedy=-20
        self.direction=direction
    def update(self):
        if self.direction ==0:
            self.rect.x -= self.speedx
        if self.direction==1:
            self.rect.y+=self.speedy
        if self.direction==2:
            self.rect.x += self.speedx
        # Se o tiro passar do inicio da tela, morre.
        if self.rect.centerx < 0:
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
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(Homem, "Stance_Iron_Man.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(Thanos, "Stance_Thanos.png")).convert()
    assets["bullet_img1"] = pygame.image.load(path.join(Homem, "Propulsor2.png")).convert()
#    assets["bullet_img2"] = pygame.image.load(path.join(Homem,"Propulsor.png")).convert()
    assets["background"] = pygame.image.load(path.join(fundo, 'houses31.png')).convert()
    assets["block_img"] = pygame.image.load(path.join(img_dir, 'Dano_Ultron.png')).convert()
    return assets

def game_screen(screen):
    assets = load_assets(img_dir)
    clock = pygame.time.Clock()
    background = assets["background"]
    background_rect = background.get_rect()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Avengers the Game")
    player = Player(assets["player_img"])
# Cria um grupo de todos os sprites e adiciona a nave.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
#Cria um gupo de plataforma
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
    # Cria blocos espalhados em posi��es aleat�rias do mapa
    for i in range(INITIAL_BLOCKS):
        block_x = random.randint(0, WIDTH)
        block_y = random.randint(0, int(HEIGHT * 0.25))
        block = Tile(assets["block_img"], block_x, block_y)
        world_sprites.add(block)
        # Adiciona tambem no grupo de todos os sprites para serem atualizados e desenhados
        all_sprites.add(block)

    PLAYING = 0
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
            # Verifica se houve colis�o entre o player e o meteoro ou com bola de ferro
            hits = pygame.sprite.spritecollide(player, mobs, False)
            ht=pygame.sprite.spritecollide(player, world_sprites, False)            
            if hits or ht:
               state = DONE
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_LEFT:
                    player.speedx -= SPEED_X
                elif event.key == pygame.K_RIGHT:
                    player.speedx += SPEED_X
                elif event.key == pygame.K_DOWN:
                    player.speedy -= SPEED_Y
                elif event.key == ord('d'):
                    bullet = Bullet(player.rect.centerx, player.rect.top,2,assets["bullet_img"])
                    all_sprites.add(bullet)
                    bullets.add(bullet)      
                elif event.key == ord('w'):
                    bullet = Bullet(player.rect.centerx, player.rect.top,1,assets["bullet_img"])
                    all_sprites.add(bullet)
                    bullets.add(bullet)          
                elif event.key == ord('a'):
                    bullet = Bullet(player.rect.centerx, player.rect.top,0,assets["bullet_img"])
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
                # Destr�i o bloco e cria um novo no final da tela
                block.kill()
                block_x = random.randint(WIDTH, int(WIDTH * 1.5))
                block_y = random.randint(0, int(HEIGHT * 0.75))
                new_block = Tile(assets["block_img"], block_x, block_y)
                all_sprites.add(new_block)
                world_sprites.add(new_block)
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)      
        # Desenha o fundo e uma c�pia para a direita. Assumimos que a imagem selecionada ocupa pelo menos o tamanho da janela.
        # Al�m disso, ela deve ser c�clica, ou seja, o lado esquerdo deve ser continua��o do direito.
        screen.blit(background, background_rect)        
        # Desenhamos a imagem novamente, mas deslocada em x.
        background_rect2 = background_rect.copy()
        if background_rect.left > 0:
            # Precisamos desenhar o fundo � esquerda
            background_rect2.x -= background_rect2.width
        else:
            # Precisamos desenhar o fundo � direita
            background_rect2.x += background_rect2.width
        #A cada loop, redesenha o fundo e os sprites
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

pygame.init()
pygame.mixer.init()