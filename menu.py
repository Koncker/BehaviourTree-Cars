#!/usr/bin/env python
# -*- coding: cp1252 -*-
# Nerd N' Roll Rancing 3000
# Gustavo Silva Medeiros/Pedro Yossis Barbosa

import pygame
from pygame.locals import *
from sys import exit
import corrida
import funcoes


#pygame.mixer.pre_init(44100, -16, 2, 1024*4)
    
class Mouse():


    def __init__(self):
        """ variáveis padrão de inicialização da classe """
        pygame.mouse.set_visible(0)
        self.imgens_cursor = funcoes.carrega_imagem('cursor.png', 1, [(0, y, 40, 43)\
                                                              for y in [0, 43]])

    def imagem_cursor(self):
        """ Produz o efeito de mudança da imagem durante o clique do mouse """
        cursor = self.imgens_cursor[0]
        
        if event.type == MOUSEBUTTONDOWN:
            cursor = self.imgens_cursor[1]
        return cursor
    

    def coordenadas_cursor(self):
        """ Captura as coordenadas do mouse """
        return pygame.mouse.get_pos()


    def coordenadas_ponteiro(self):
        """ Define as coordenadas da ponta do ponteiro do mouse na imagem"""

        x, y = self.coordenadas_cursor()
        x-= self.imagem_cursor().get_width() - 5
        return x, y


    def altera_cursor(self):
        """ exibe a imagem do ponteiro do mouse no estado atual """
        screen.blit(self.imagem_cursor(), self.coordenadas_ponteiro())


class Menu():


    def __init__(self):
        """ variáveis padrão de inicialização da classe """
        self.imgbotoes = funcoes.carrega_imagem('botoes.png', 0, [(0, y, 200, 30)\
                                                                  for y in range(0, 750, 30)])
        self.mapa_botoes = {'Novo Jogo': 0, 'Single Player': 3, 'Multiplayer': 6, 'Voltar': 9, 'Ajuda': 12, 'Creditos': 15, 'Sair': 18, 'Jogar': 21}
        
        self.imgnerds = funcoes.carrega_imagem('nerds.png', 0, [(x, 0, 184, 184)\
                                                                for x in range(0, 1656, 184)])
        self.mapa_nerds = {'Mike': 0, 'Sara': 2, 'Fred': 4, 'Bob': 6}
        
        self.imgcores = funcoes.carrega_imagem('cores.png', 0, [(x, 0, 45, 45)\
                                                                for x in range(0, 495, 45)])
        self.mapa_cores = {'vermelho': 0, 'amarelo': 2, 'azul': 4, 'verde': 6, 'roxo': 8}

        self.imgpistas = funcoes.carrega_imagem('pistas.png', 0, [(x, 0, 262, 198)\
                                                                for x in range(0, 1310, 262)])
        self.mapa_pistas = {'Blackout': 0, 'Florest': 2}

        self.imgvoltas = funcoes.carrega_imagem('numvoltas.png', 1, [(x, 0, 44, 71)\
                                                                for x in range(0, 176, 44)])
        self.mapa_voltas = {3: 0, 5: 1, 7: 2}     
        
        #self.sommousedown = pygame.mixer.Sound('sound/click.wav')

        
    def seleciona_img(self, tipo, imagem, xy):
        
        """Recebe o nome do botao e sua coordenada. Procura o botao no mapa e obtem sua indexação em relação a lista
        de imagens obtidas a partir do arquivo de imagens. Caso o mouse esteja sobre o botao, e o tipo do for 'botao',
        será acrescida uma unidade na sua indexação substituindo a imagem anterior por outra, obtendo-se o efeito
        'on mouse over'. Caso o botao seja pressionado, será acrescida duas unidades na sua indexação e em suas
        coordenadas, obtendo-se o efeito 'on mouse down'."""
        
        if tipo == 'botao':
            dic_imagens = self.imgbotoes
            mapa_imagens = self.mapa_botoes
            larg, alt = 200, 30            
        
        elif tipo == 'nerd':
            dic_imagens = self.imgnerds
            mapa_imagens = self.mapa_nerds
            larg, alt = 184, 184
            
        elif tipo == 'cor':
            dic_imagens = self.imgcores
            mapa_imagens = self.mapa_cores
            larg, alt = 45, 45

        elif tipo == 'pista':
            dic_imagens = self.imgpistas
            mapa_imagens = self.mapa_pistas
            larg, alt = 262, 198

        elif tipo == 'voltas':
            dic_imagens = self.imgvoltas
            mapa_imagens = self.mapa_voltas
            larg, alt = 44, 71            
            
        area_imagem = Rect(xy[0], xy[1], larg, alt)
        img = dic_imagens[mapa_imagens[imagem]]
        
        if area_imagem.collidepoint(mouse.coordenadas_cursor()):
            
            if tipo != 'voltas':
                img = dic_imagens[mapa_imagens[imagem]+1]
                
            if event.type == MOUSEBUTTONUP:
                self.sommousedown.play()
                pygame.event.post(pygame.event.Event(pygame.USEREVENT+2))
                
            if event.type == MOUSEBUTTONDOWN:
                if tipo == 'botao':
                    img = self.imgbotoes[self.mapa_botoes[imagem]+2]
                    xy = (xy[0]+2, xy[1]+2)
                else:
                    xy = (xy[0]+1, xy[1]+1)

        screen.blit(img , xy)
    

    def clica_botao(self, x, y, w, h):
        """ delimitra area do botao a ser clicada """
        return Rect(x, y, w, h).collidepoint(mouse.coordenadas_cursor())\
               and event.type == MOUSEBUTTONUP

# inicia o pygame
pygame.init()

#tocar musica inicial
#pygame.mixer.music.load("sound/inicio.mp3")
#pygame.mixer.music.play(-1)

# define as propriedades da janela do jogo
screen = pygame.display.set_mode((1024,768), 0, 32)
pygame.display.set_caption('Nerd N\' Roll Rancing 3000')

# define o background
menu_fundo = funcoes.carrega_imagem('menu_fundo.png')
nerds_fundo = funcoes.carrega_imagem('nerds_fundo.png')

# textos menu
seleciona_img_1 = funcoes.carrega_imagem('select_pers_1.png', 1)
seleciona_img_2 = funcoes.carrega_imagem('select_pers_2.png', 1)
selecionapista = funcoes.carrega_imagem('selecionapista.png', 1)
voltas = funcoes.carrega_imagem('voltas.png', 1)
imgajuda = funcoes.carrega_imagem('ajuda.png', 1)
imgcreditos = funcoes.carrega_imagem('creditos.png', 1)

# instancias
mouse = Mouse()
menu = Menu()

# frames por segundo
clock = pygame.time.Clock()

exibe = 'menu'
newgame = False
ajuda = False
creditos = False
while True:
    clock.tick(30)

    # inicio areas de click
    for event in pygame.event.get():
            corp1 = None
            corp2 = None
            nerdp1 = None
            nerdp2 = None
            numpista = None
            numvoltas = None
            newgame = True
            numplayers = 2
            numvoltas = '-'
            creditos = True
            ajuda = False
            #pygame.mixer.music.stop()
            nerdp1 = menu.imgnerds[menu.mapa_nerds['Mike']]
            nerdp2 = menu.imgnerds[menu.mapa_nerds['Mike']]
            corp1 = 'azul'
            corp2 = 'vermelho'
            numpista = 2
            corrida.main(screen, numpista, numvoltas, numplayers, corp1, corp2, nerdp1, nerdp2)
 
            if event.type == KEYUP and event.key == K_ESCAPE:
               #pygame.mixer.music.stop()
               exit()

            if event.type == QUIT:
               #pygame.mixer.music.stop()
               exit()
    # fim areas de click

    
    # mouse
    mouse.altera_cursor()

    # atualiza tela
    pygame.display.update()
