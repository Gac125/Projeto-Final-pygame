# -*- coding: utf-8 -*-
import pygame
import random
from os import path
from config_depressao import img_dir, TITULO, fnt_dir, WIDTH, HEIGHT, BLACK, FPS, WHITE, GREY, RED, YELLOW, INITIAL_BLOCKS, TILE_SIZE, SPEED_X, SPEED_Y, GRAVITY, JUMP_SIZE, GROUND, STILL, JUMPING, FALLING


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

class Platform(pygame.sprite.Sprite):
    def __init__(self, buraco_img):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        # Aumenta o tamanho do tile.
        buraco_img = pygame.transform.scale(buraco_img, (150, 130))
        # Define a imagem do tile.
        self.image = buraco_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Posiciona o tile
        self.rect.x = 1200
        self.rect.y = GROUND
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
        self.rect.bottom = HEIGHT 
        # Velocidade
        self.speedx = 0
        self.speedy = 0
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 25
    def update(self):
        self.speedy += GRAVITY
        # Atualiza o estado para caindo
        if self.speedy > 0:
            self.state = FALLING
        self.rect.y += self.speedy
        # Se bater no chão, para de cair
        if self.rect.bottom > GROUND:
            # Reposiciona para a posição do chão
            self.rect.bottom = GROUND
            # Para de cair
            self.speedy = 0
            # Atualiza o estado para parado
            self.state = STILL
    # Método que faz o personagem pular
    def jump(self):
        # Só pode pular se ainda não estiver pulando ou caindo
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
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * 1 / 2)    
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
#
#class platform(pygame.sprite.Sprite):
#    def __init__(self, x, y, w, h):
#        pygame.sprite.Sprite.__init__(self)
#        self.image = pygame.Surface((w, h))
#        self.image.fill(GREY)
#        self.rect = self.image.get_rect()
#        self.rect.x = x
#        self.rect.y = y

def load_assets(img_dir):
    Homem = path.join(img_dir, 'Iron Man')
    Thanos = path.join(img_dir, 'Thanos')
    fundo = path.join(path.dirname(__file__), 'Backgrounds')
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(Homem, "Stance_Iron_Man.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(Thanos, "Stance_Thanos.png")).convert()
    assets["bullet_img1"] = pygame.image.load(path.join(Homem, "Propulsor2.png")).convert()
    assets["bullet_img2"] = pygame.image.load(path.join(img_dir,"Propulsor.png")).convert()
    assets["bullet_img3"] = pygame.image.load(path.join(img_dir,"Propulsor3.png")).convert()
    assets["background"] = pygame.image.load(path.join(fundo, 'houses31.png')).convert()
    assets["block_img"] = pygame.image.load(path.join(img_dir, 'Dano_Ultron.png')).convert()
    assets["buraco_img"] = pygame.image.load(path.join(img_dir, 'Buraco.png')).convert()
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    return assets


def game_screen(screen):
    assets = load_assets(img_dir)
    clock = pygame.time.Clock()
    background = assets["background"]
    background_rect = background.get_rect()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Avengers the Game")
    player = Player(assets["player_img"])
    score_font = assets["score_font"]
# Cria um grupo de todos os sprites e adiciona a nave.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
#Cria um gupo de plataforma
#    pl = platform(0, HEIGHT - 25, WIDTH, 100)
#    all_sprites.add(pl)
# Cria um grupo sÃ³ do thanos
    mobs = pygame.sprite.Group()
# Cria um grupo para tiros
    bullets = pygame.sprite.Group()
# Cria buracos com o passar do tempo
    buracos = pygame.sprite.Group()
# Cria 8 meteoros e adiciona no grupo thanos
    for i in range(1):
        m = Mob(assets["mob_img"])
        all_sprites.add(m)
        mobs.add(m)
    world_sprites = pygame.sprite.Group() 
    # Cria blocos espalhados em posições aleatórias do mapa
    for i in range(INITIAL_BLOCKS):
        block_x = random.randint(0, WIDTH)
        block_y = random.randint(0, int(HEIGHT * 0.25))
        block = Tile(assets["block_img"], block_x, block_y)
        world_sprites.add(block)
        # Adiciona tambem no grupo de todos os sprites para serem atualizados e desenhados
        all_sprites.add(block)

    PLAYING = 0
    DONE = 1
    
    score = 0
    lives = 3
    #Define estado atual
    state = PLAYING
    tempo = pygame.time.get_ticks()
    while state != DONE:      
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = DONE       
         # Verifica se houve colisão entre propulsor e o meteoro
            hits = pygame.sprite.groupcollide(mobs, bullets, True, False)
            for hit in hits: # Pode haver mais de um
            # O meteoro e destruido dps recriado
                m = Mob(assets["mob_img"])
                all_sprites.add(m)
                mobs.add(m)
                score += 100
            # Verifica se houve colisão entre o player e o meteoro ou com bola de ferro
            hits = pygame.sprite.spritecollide(player, mobs, False)
                
            #ht=pygame.sprite.spritecollide(player, world_sprites, False, pygame.sprite.collide_circle)
            ht=pygame.sprite.spritecollide(player, world_sprites, True)
            if hits or ht:
                lives -= 1  
                print("perdeu vida {0}".format(lives))
            if lives == 0:
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
                    bullet = Bullet(player.rect.centerx, player.rect.top,2,assets["bullet_img1"])
                    all_sprites.add(bullet)
                    bullets.add(bullet)      
                elif event.key == ord('w'):
                    bullet = Bullet(player.rect.centerx, player.rect.top,1,assets["bullet_img3"])
                    all_sprites.add(bullet)
                    bullets.add(bullet)          
                elif event.key == ord('a'):
                    bullet = Bullet(player.rect.centerx, player.rect.top,0,assets["bullet_img2"])
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
        # Depois de processar os eventos, como o jogador vai ficar parado, o fundo e os objetos no mundo devem se mover 
        #com a velocidade do personagem no sentido oposto.
        for block in world_sprites:
            block.speedx = -player.speedx        
        now=pygame.time.get_ticks()
        if now - tempo > 7000:
            buraco=Platform(assets["buraco_img"])
            all_sprites.add(buraco)
            buracos.add(buraco)
            tempo=pygame.time.get_ticks()
            
        caiu=pygame.sprite.spritecollide(player, buracos, False)
        if caiu:
            lives -= 1                
            if lives == 0:
                state = DONE
        # Atualiza a acao de cad a sprite. O grupo chama o método update() de cada Sprite dentre dele.
        all_sprites.update()
        # Atualiza a posição da imagem de fundo.
        background_rect.x -= player.speedx
        for b in buracos:
            b.speedx=(-1)*player.speedx
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
            
        screen.blit(background, background_rect2)
        all_sprites.draw(screen) 
        
        text_surface = score_font.render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        screen.blit(text_surface, text_rect)
        
        text_surface = score_font.render(chr(9829) * lives, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()

