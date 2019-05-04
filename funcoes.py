#!/usr/bin/env python
# -*- coding: cp1252 -*-
# Nerd N' Roll Rancing 3000
# Gustavo Silva Medeiros/Pedro Yossis Barbosa

import os
import pygame
from pygame.locals import *

def carrega_imagem(arquivo, transparencia=None, imagens=None):
    """
    Carrega as imagens. Quando recebe apenas o arquivo, abre ele e retorna a
    imagem. Quando recebe uma lista de retangulos em 'imagens', extrai pedacos da
    imagem e retorna uma lista com esses pedaços. Quando recebe '1' como valor em
    transparencia, captura a cor do pixel da coordenada (0, 0) e deixa ela trasnparente.
    """
    arquivo = os.path.join('img', arquivo)
    image = pygame.image.load(arquivo)
    
    if imagens is None:
        if transparencia is 1:
            return image.convert_alpha()
            
        return image.convert()
    else:
        imgs = []
        for img_area in imagens:
            img = pygame.Surface(Rect(img_area).size).convert()
            img.blit(image, (0, 0), img_area)
            if transparencia is 1:
                colorkey = img.get_at((0,0))
                img.set_colorkey(colorkey, RLEACCEL)
            imgs.append(img)
        return imgs
