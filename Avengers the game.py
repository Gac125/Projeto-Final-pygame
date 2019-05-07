# -*- coding: utf-8 -*-
"""
Jogo Marvel - Giovanna Alves, Giulia Castro e Pedro Célia
"""
import pygame
import random
import time
from os import path

try:
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                if event.key == pygame.K_UP:
                    player.speedx = 8
                if event.key == pygame.K_DOWN:
                    player.speedx = -8
                    
             if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                if event.key == pygame.K_UP:
                    player.key = 0
                if event.key == pygame.K_DOWN:
                    player.key = 0
            all_sprites.update()