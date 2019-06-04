# -*- coding: utf-8 -*-
import pygame
import random
from os import path
from config_depressao import img_dir, fnt_dir, snd_dir, WIDTH, HEIGHT, BLACK, FPS, WHITE, RED, YELLOW, INITIAL_BLOCKS, TILE_SIZE, SPEED_X, SPEED_Y, GRAVITY, JUMP_SIZE, GROUND, STILL, JUMPING, FALLING, FALLING_BURACO

class Tile(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, tile_img, x, y):
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
        pygame.sprite.Sprite.__init__(self)
        # Aumenta o tamanho do tile.
        buraco_img = pygame.transform.scale(buraco_img, (50, 130))
        # Define a imagem do tile.
        self.image = buraco_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Posiciona o tile
        self.rect.x = 800
        self.rect.y = HEIGHT - 50
        self.speedx = 0    
    def update(self):
        self.rect.x += self.speedx    

class Player(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, player_img):     
        pygame.sprite.Sprite.__init__(self) 
        # Carregando a imagem de fundo.
        self.state = STILL
        self.image = player_img
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (200,150))
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        #Criando uma máscara para o Player
        self.mask = pygame.mask.from_surface(self.image)
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 3
        self.rect.bottom = HEIGHT 
        # Velocidade
        self.speedx = 0
        self.speedy = 0
    def update(self):
        self.speedy += GRAVITY
        # Atualiza o estado para caindo
        if self.speedy > 0 and self.state!= FALLING_BURACO:
            self.state = FALLING
        self.rect.y += self.speedy
        if self.state != FALLING_BURACO:
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
        pygame.sprite.Sprite.__init__(self)      
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (200, 160))                
        # Deixando transparente.
        self.image.set_colorkey(WHITE)       
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(1, 3)
        self.speedy = 0       
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        # Lugar inicial em x
        self.px = 1052
        # Lugar inicial em y
        self.rect.x = 1052
        self.rect.y = HEIGHT - 170     
    #Método que atualiza a posição do Thanos 
    def update(self):
        self.rect.x -= self.speedx    

class Mob2(pygame.sprite.Sprite):   
    # Construtor da classe.
    def __init__(self, mob2_img):        
        pygame.sprite.Sprite.__init__(self)        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob2_img, (20, 38))        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)     
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()     
        # Sorteia um lugar inicial em x
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 9)       
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)       
    # Metodo que atualiza a posição do laser
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy        
        # Se o laser passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 9)            
            
class Mob3(pygame.sprite.Sprite): 
    # Construtor da classe.
    def __init__(self, mob3_img):      
        pygame.sprite.Sprite.__init__(self)      
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob3_img, (200, 160))                
        # Deixando transparente.
        self.image.set_colorkey(WHITE)       
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(1, 3)
        self.speedy = 0       
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        #Lugar inicial em X
        self.rect.x = - 40
        # Lugar inicial em y
        self.rect.y = HEIGHT - 170            
    def update(self):
        self.rect.x += self.speedx  

class Bullet(pygame.sprite.Sprite):  
    # Construtor da classe.
    def __init__(self, x, y,direction, bullet_img):    
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
    assets["tiro_img"] = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
    assets["loki_img"] = pygame.image.load(path.join(img_dir, 'Stance_Loki.png')).convert()
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    assets["tira_vida"] = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav'))
    assets["destroi_mob"] = pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav'))
    assets["tiro_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
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
# Cria um grupo de todos os sprites e adiciona o Homem de Ferro.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
# Cria um grupo dos inimigos
    mobs = pygame.sprite.Group()
# Cria um grupo para tiros
    bullets = pygame.sprite.Group()
# Cria um grupo para os buracos
    buracos = pygame.sprite.Group()
# Carrega os sons do jogo
    pygame.mixer.music.set_volume(0.4)
    tira_vidasnd = assets["tira_vida"]
    destroi_mobsnd = assets["destroi_mob"]
    tiro_snd = assets["tiro_sound"]
# Cria 1 thanos e adiciona no grupo dos inimigos
    for i in range(1):
        m = Mob(assets["mob_img"])
        all_sprites.add(m)
        mobs.add(m)
    world_sprites = pygame.sprite.Group() 
    # Cria ultrons espalhados em posições aleatórias do mapa
    for i in range(INITIAL_BLOCKS):
        block_x = random.randint(0, WIDTH)
        block_y = random.randint(0, int(HEIGHT * 0.25))
        block = Tile(assets["block_img"], block_x, block_y)
        world_sprites.add(block)
        # Adiciona tambem no grupo de todos os sprites para serem atualizados e desenhados
        all_sprites.add(block)
# Cria 5 lasers e adiciona no grupo dos inimigos
    for a in range(5):
        t = Mob2(assets["tiro_img"])
        all_sprites.add(t)
        mobs.add(t)
# Cria 2 lokis e adiciona no grupo dos inimigos
    for q in range(2):
        l = Mob3(assets["loki_img"])
        all_sprites.add(l)
        mobs.add(l)
        
    # Define os estados possíveis do jogo       
    PLAYING = 0
    DONE = 1 
    score = 0
    lives = 3   
    # Define estado atual
    state = PLAYING
    # Começa a contar o tempo
    tempo = pygame.time.get_ticks()
    while state != DONE:      
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = DONE       
         # Verifica se houve colisão entre propulsor e os inimigos
            hits = pygame.sprite.groupcollide(mobs, bullets, True, False)
            ht = pygame.sprite.groupcollide(world_sprites, bullets, True, False)
            for hit in hits: 
            # O Thanos é destruido depois recriado
                destroi_mobsnd.play()
                t = Mob(assets["mob_img"])
                all_sprites.add(t)
                mobs.add(t)
                score += 100
            for hit in ht: # Pode haver mais de um
            # O ultron é destruido e aumenta os pontos do player
                score += 100
                destroi_mobsnd.play()
                u = Tile(assets["block_img"], block_x, block_y)
                all_sprites.add(u)
                world_sprites.add(u)
#                u2 = Tile(assets["block_img"], block_y, block_x)
#                all_sprites.add(u2)
#                world_sprites.add(u2)
                score += 100
            # Verifica se houve colisão entre o player e os inimigos ou com os ultrons
            hits = pygame.sprite.spritecollide(player, mobs, False)              
            ht=pygame.sprite.spritecollide(player, world_sprites, True)
            #Tira vida do Player caso haja colisão
            if hits or ht:
                tira_vidasnd.play()
                lives -= 1                  
            if lives == 0:
                state = DONE
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
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
                    tiro_snd.play()
                elif event.key == ord('w'):
                    bullet = Bullet(player.rect.centerx, player.rect.top,1,assets["bullet_img3"])
                    all_sprites.add(bullet)
                    bullets.add(bullet)    
                    tiro_snd.play()
                elif event.key == ord('a'):
                    bullet = Bullet(player.rect.centerx, player.rect.top,0,assets["bullet_img2"])
                    all_sprites.add(bullet)
                    bullets.add(bullet) 
                    tiro_snd.play()
                elif event.key == pygame.K_LEFT:
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
        #Faz os buracos aparecerem a cada 7 segundos
        if now - tempo > 7000:
            buraco=Platform(assets["buraco_img"])
            all_sprites.add(buraco)
            buracos.add(buraco)
            tempo=pygame.time.get_ticks()
        #Verifica colisão com o buraco    
        caiu=pygame.sprite.spritecollide(player, buracos, False, pygame.sprite.collide_rect)
        if caiu:
            player.state = FALLING_BURACO
            delay = pygame.time.get_ticks()
            if delay >= 2000:            
                state = DONE
        # Atualiza a acao de cad a sprite. O grupo chama o método update() de cada Sprite dentre dele.
        all_sprites.update()
        # Atualiza a posição da imagem de fundo.
        background_rect.x -= player.speedx
        #Faz os buracos andarem conforme o fundo
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
                # Destrói o ultron e cria um novo no final da tela
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
            # Desenha o fundo à esquerda
            background_rect2.x -= background_rect2.width
        else:
            # Desenha o fundo à direita
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

