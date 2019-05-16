# Importando as bibliotecas necessárias.
import pygame
import random
import time

from os import path

from config_depressao import WIDTH, HEIGHT, INIT, GAME, QUIT
from init_avengers import init_avengers
import arquivo_da_depressao 

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Avengers the game")

# Comando para evitar travamentos.
try:
    state = INIT
    while state != QUIT:
        if state == INIT:
            state = init_avengers(screen)
        elif state == GAME:
            state = arquivo_da_depressao(screen)
        else:
            state = QUIT
finally:
    pygame.quit()
