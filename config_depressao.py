from os import path


#Dados do jogo 
img_dir = path.join(path.dirname(__file__), 'Avengers anime')
snd_dir = path.join(path.dirname(__file__), 'snd')
fnt_dir = path.join(path.dirname(__file__), 'font')

WIDTH = 1052 # Largura da tela
HEIGHT = 650 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

INIT = 0
GAME = 1
QUIT = 2

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