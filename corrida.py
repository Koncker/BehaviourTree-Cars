#!/usr/bin/env python
# -*- coding: cp1252 -*-
# Nerd N' Roll Rancing 3000
# Gustavo Silva Medeiros/Pedro Yossis Barbosa

import os
import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from vector import Vector
from sys import exit
from math import *
import funcoes
import random
import math
from BehaviourTree import *

def main(screen, num_pista, num_voltas, players, corp1, corp2=None, nerdp1=None, nerdp2=None):
    """ Função de inicialização da corrida. Recebe parametros de configuração do módulo menu.py. Quando esta função é executada, a corrida é iniciada na tela principal. """
    #sortear musica
    #musicas = {1: "sound/music01.mp3", 2: "sound/music02.mp3", 3: "sound/music03.mp3"}
    #num_musica = random.randint(1, 3)
    #pygame.mixer.pre_init(44100, -16, 2, 1024*4)

    tam_tela_x = 1024
    tam_tela_y = 768
    tam_tela = (tam_tela_x, tam_tela_y)
    
    PI = math.pi

    fps = 30 # frames por segundo

    carList = []

    vermelho = (255, 0, 0, 255)
    vermelho_escuro = (128, 0, 0, 255)
    laranja = (255, 128, 0, 255)
    marrom = (128, 64, 0, 255)
    branco = (255, 255, 255, 255)
    cinza_claro = (192, 192, 192, 255)
    verde = (0, 255, 0, 255)
    verde_escuro = (0, 128, 0, 255)
    azul_piscina = (0, 128, 255, 255)
    azul_bebe = (128, 255, 255, 255)
    amarelo = (255, 255, 0, 255)
    amarelo_escuro = (128, 128, 0, 255)
    preto = (0, 0, 0, 255)
    azul = (0, 0, 255, 255)

    colors = {(255, 0, 0, 255):"vermelho",(128, 0, 0, 255):"vermelho_escuro", (255, 128, 0, 255):"laranja",
              (128, 64, 0, 255):"castanho",(255, 255, 255, 255):"branco",(192, 192, 192, 255):"cinzento claro",
              (0, 255, 0, 255):"verde",(0, 128, 0, 255):"verde escuro",(0, 128, 255, 255):"azul piscina",
              (128, 255, 255, 255):"azul bebe",(255, 255, 0, 255):"amarelo",(128, 128, 0, 255):"amarelo escuro",
              (0, 0, 0, 255):"preto",(0, 0, 255, 255):"azul"}



    pontos = [(860,630),(880,120),(120,180),(684,344),(120,546)]
    delta = 05;


    def escreve_tela(texto, cor, tamanho, posicao):
        """ função utilizada por diversas partes do código que exibe na tela os dados recebidos como parâmetro """
        fonte = pygame.font.Font(None, tamanho)
        screen.blit(fonte.render(texto,  3, cor), posicao)
        

    def tecla(botao, player):
        """ mapa dos comandos da corrida """
        botao_map = {'acelerador': [K_UP, K_w], 'freio': [K_DOWN, K_s],\
                     'esquerda': [K_LEFT, K_a], 'direita': [K_RIGHT, K_d],\
                     'atira': [K_RCTRL, K_LCTRL]}
        if player == 1:
            return botao_map[botao][0]
        return botao_map[botao][1]


    class Display():

        def __init__(self, player):
            """ variáveis padrão de inicialização da classe """
            self.tamanho_fonte = 25
            self.total_laps = num_voltas
            
            self.track = pista
            
            if player is 1:
                self.name = 'Nerd 1'
                self.carro_player = carrop1
                self.pos_name = (5, 5)
                self.pos_balas = (5, 25)
                self.pos_speed = (5, 65)
                self.pos_laps = (5, 85)
                self.pos_life = (5, 45)
                self.pos_ultima_volta = (5, 105)
                self.pos_melhor_volta = (5, 125)
                self.posicao = (5, 145)
                self.direcao = (5, 165)
                self.sensor = (5, 185)
            else:
                self.name = 'Nerd 2'
                self.carro_player = carrop2
                self.pos_name = (5, 625)
                self.pos_balas = (5, 645)
                self.pos_speed = (5, 685)
                self.pos_laps = (5, 705)
                self.pos_life = (5, 665)
                self.pos_ultima_volta = (5, 725)
                self.pos_melhor_volta = (5, 745)
                self.posicao = (5, 145)
                self.direcao = (5, 165)
                self.sensor = (5, 185)


        def exibe_display(self):
            """ exibe as informações atuais referentes ao player (vida, velocidade, tiros, etc) """
            municao = 'Munição: ' + str(self.carro_player.municao)
            vida = 'Vida: ' + str(self.carro_player.life)
            velocidade = 'Velocidade: ' + str(self.carro_player.velocidade_carro / 5)
            voltas = 'Voltas: ' + str(self.carro_player.voltas+1) + '/' + str(self.total_laps)
            ultima_volta = 'Ultima Volta: ' + str(self.carro_player.ultima_volta)
            melhor_volta = 'Melhor Volta: ' + str(self.carro_player.melhor_volta)
            localizacao = 'Posicao: (' + str(int(self.carro_player.posicao.x))+","+str(int(self.carro_player.posicao.y))+")"
            direcao = 'Direccao: (' + str(int(self.carro_player.rotacao))+","+str(int(self.carro_player.get_orientation()))+")   "+ self.carro_player.identify_color()
            car1_sensor = "Red "+ str(self.carro_player.identify_color_point2(self.carro_player.left)) + "   center " + \
                          str(self.carro_player.identify_color_point2(self.carro_player.center)) + "   right " + str(self.carro_player.identify_color_point2(self.carro_player.right))
            escreve_tela(self.name, vermelho, self.tamanho_fonte, self.pos_name)
            escreve_tela(municao, branco, self.tamanho_fonte, self.pos_balas)
            escreve_tela(vida, branco, self.tamanho_fonte, self.pos_life)
            escreve_tela(velocidade, branco, self.tamanho_fonte, self.pos_speed)
            escreve_tela(voltas, branco, self.tamanho_fonte, self.pos_laps)      
            escreve_tela(ultima_volta, branco, self.tamanho_fonte, self.pos_ultima_volta)
           # escreve_tela(melhor_volta, branco, self.tamanho_fonte, self.pos_melhor_volta)
           # escreve_tela(localizacao, branco, self.tamanho_fonte, self.posicao)
           # escreve_tela(direcao, branco, self.tamanho_fonte, self.direcao)
           # escreve_tela(car1_sensor, branco, self.tamanho_fonte, self.sensor)

            
    class Pista():

        
        def __init__(self, pista):
            """ variáveis padrão de inicialização da classe """
            self.imgpista = funcoes.carrega_imagem('pista' + str(pista) + '.png')
            self.imgmapa_cores = funcoes.carrega_imagem('pista_mapa' + str(pista) + '.png')
            self.num_voltas = num_voltas
        
            # largada
            self.tempo_largada = 0
            self.largada = False
            self.tamanho_fonte = 100
            if num_pista is 1:
                self.posicaop1 = Vector(565, 135)
                self.posicaop2 = Vector(465, 165)
                self.rotacao = 90.
            elif num_pista is 2:
                self.posicaop1 = Vector(565, 630)
                self.posicaop2 = Vector(465, 670)
                self.rotacao = 90.

            # arvores
            self.arvores = funcoes.carrega_imagem('pista_arvores' + str(pista) + '.png', 1)

        def conta_tempo_largada(self, tf, ti, numero):
            """ o nome já diz tudo """
            #if tf > self.tempo_largada >= ti:
            #    escreve_tela(numero, branco, self.tamanho_fonte, (500, 334))
            pass

        def larga(self):
            """ exibe na tela a mensagem de largada e permite a movimentação dos carros (self.largada) """
            if self.tempo_largada < fps*10:
                self.tempo_largada+=1
                
            for i in range(1, 6):
                self.conta_tempo_largada(fps*i + fps, fps*i, "%d" % (6 - i))

            if fps*7 > self.tempo_largada >= fps*6:
#                escreve_tela('ROCK AND ROLL!!!', branco, self.tamanho_fonte, (200, 334))
                self.largada = True
                

        def carrega_mapa_cores(self):
            """ carrega o mapa de cores da pista responsável pelo controle de colisões de obstáculos """
            screen.blit(self.imgmapa_cores, (0,0))


        def carrega_pista(self):
            """ carrega a imagem da pista escolhida pelo usuário que fica em cima da imagem do mapa de cores """
            screen.blit(self.imgpista, (0,0))


        def mostra_arvores(self):
            """ carrega a imagem das árvores """
            screen.blit(self.arvores, (0, 0))


    class Carro(Sprite):
        def __init__(self, player, cor, *grupos):
            """ variáveis padrão de inicialização da classe """
            Sprite.__init__ ( self , *grupos )
            
			# list with cars
            carList.append(self)

            # teclas
            self.acelerador, self.freio = tecla('acelerador', player), tecla('freio', player)
            self.esquerda, self.direita = tecla('esquerda', player), tecla('direita', player)
            self.atira = tecla('atira', player)
            
            # cor do carro
            self.imgscar = funcoes.carrega_imagem('cars.png', 1, [(x, 0, 34, 60) for x in range(0, 477, 34)])
            self.cor_carro_map = {'vermelho': 0, 'amarelo': 3, 'azul': 6, 'verde': 9, 'roxo': 12}
            self.cor = cor
            self.imgcar = self.imgscar[self.cor_carro_map[self.cor]]
            
            # velocidade/deslocamento/acelera
            self.velocidade_carro = 0
            self.velocidade_max = 400.
            self.rotacao = pista.rotacao
            self.velocidade_rotacao = 90. # graus por segundo
            self.direcao_rotacao = 0

            # posicao inicial dos carros na pista e antes de uma batida
            if player is 1:
                self.posicao = pista.posicaop1
            else:
                self.posicao = pista.posicaop2
            self.pos_antes_batida = self.posicao.copy()
            
            self.nextpoint = 0

            self.left = (0,0)
            self.right = (0,0)
            self.center = (0,0)
            self.sensorimg = funcoes.carrega_imagem('point.png', 1)
            self.opponentSensor = (0,0)
                
            # conta voltas
            self.checks = 0
            self.voltas = 0
            self.melhor_volta = "-"
            self.ultima_volta = "-"
            self.cronometro = pygame.time.Clock()

            self.last = (0,0)
            self.count=0

            # life
            self.life = 500
            #self.somexplosao = pygame.mixer.Sound('sound/explode.wav')
            self.imgsexplosao = funcoes.carrega_imagem('explosion.png', 1, [(x, 0, 50, 50) for x in range(0, 400, 50)])
            self.imgexplosao = self.imgsexplosao[0]
            self.explode = False
            self.conta_tempo_morte = fps * 5

            # retangulo do sprite
            self.rect =  Rect(self.posicao.x - self.imgcar.get_width()/2, self.posicao.y - self.imgcar.get_height()/2,\
                        self.imgcar.get_width(), self.imgcar.get_height())


            self.municao = 5
            self.otherCar = None

            #Definição do comportamento
            self.mybehaviour = self.defineBehaviour()

        def setOtherCar(self,other):
			self.otherCar = other

        def identify_color(self):
            """identifica as cores de uma posição"""
            color = pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1])))
            if color in [preto,azul]:
                return "pista"
            elif color in [branco]:
                return "meta"
            else: 
                return "outra"

        def identify_color_point(self,point):
            """identifica as cores de uma posição"""
            color = pista.imgmapa_cores.get_at(point)
            if color in [preto,azul]:
                return "pista"
            elif color in [branco]:
                return "meta"
            elif color in [branco]:
                return "meta"
            else:
                return "outra"

        def identify_color_point2(self,point):
            """identifica as cores de uma posição"""
            col = tuple(pista.imgmapa_cores.get_at(point))
            if col in colors.keys():
                return colors[col]
            else:
                return "unknown"

        def isOpponent(self, carrop1):
            if self == carrop1:
                return True
            else: 
                return False


        def muda_textura(self, pressed_key):
            """ muda a imagem do carro de acordo com as ações durante o jogo (acelera, freia, ré, explosão) """
            self.imgcar = self.imgscar[self.cor_carro_map[self.cor]]
            if pressed_key[self.freio]:
                if self.velocidade_carro > 0:
                    self.imgcar = self.imgscar[self.cor_carro_map[self.cor]+1]
                elif self.velocidade_carro < 0:
                    self.imgcar = self.imgscar[self.cor_carro_map[self.cor]+2]
                    
            if self.life <= 0:
                self.imgcar = self.imgexplosao
            

        def colide(self):
            """ detecta a colisão do carro com os extremos da tela e com os obstáculos da pista """
            x, y = (int (self.posicao[0]),int(self.posicao[1]))
            
            if x <= 10:
                x = 10
            elif x >= tam_tela_x - 10:
                x = tam_tela_x - 10
                
            if y <= 10:
                y = 10
            elif y >= tam_tela_y - 10:
                y = tam_tela_y - 10
                
            if pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) == laranja:
                #self.sombatida.play()
                y-= 2
            elif pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) == marrom:
                #self.sombatida.play()
                y+= 2
            elif pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) == vermelho:
                #self.sombatida.play()
                x-= 2
            elif pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) == vermelho_escuro:
                #self.sombatida.play()
                x+= 2
                
            if pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) in [laranja, marrom,\
                                                             vermelho, vermelho_escuro]:
                self.perde_velocidade(50, -25)
                self.perde_life(10)
     
            self.posicao = Vector(x, y)



        def pista(self,sensor):
            return pista.imgmapa_cores.get_at(self.safety_belt(sensor)) in [preto, branco, azul_piscina, azul, verde,  azul_bebe, verde_escuro]

        def perde_life(self, dano):
            """ decrementa a vida do carro """
            if self.life > 0 and self.conta_tempo_morte == fps * 5:
                self.life-= dano


        def morre(self, grupo):
            """ realiza o efeito de explosão do carro e muda o seu estado atual """
            if self.life <= 0 or fps * 2 >= self.conta_tempo_morte >= 0:
                grupo.remove(self)
                

                if fps * 5 >= self.conta_tempo_morte >= (fps * 5) - 5:
                    self.imgexplosao = self.imgsexplosao[0]
                    #self.somexplosao.play()
                    
                elif (fps * 5) - 5 >= self.conta_tempo_morte >= (fps * 5) - 10:
                    self.imgexplosao = self.imgsexplosao[1]
                    
                elif (fps * 5) - 10 >= self.conta_tempo_morte >= (fps * 5) - 15:
                    self.imgexplosao = self.imgsexplosao[2]

                elif (fps * 5) - 15 >= self.conta_tempo_morte >= (fps * 5) - 20:
                    self.imgexplosao = self.imgsexplosao[3]

                elif (fps * 5) - 20 >= self.conta_tempo_morte >= (fps * 5) - 25:
                    self.imgexplosao = self.imgsexplosao[4]

                elif (fps * 5) - 25 >= self.conta_tempo_morte >= (fps * 5) - 30:
                    self.imgexplosao = self.imgsexplosao[5]

                elif (fps * 5) - 30 >= self.conta_tempo_morte >= (fps * 5) - 35:
                    self.imgexplosao = self.imgsexplosao[6]
                    self.velocidade_carro = 0
                    while(True):
                        p = (random.randint(10,tam_tela_x-10),random.randint(10,tam_tela_y-10))
                        if self.pista(p):
                            self.posicao.x = p[0]
                            self.posicao.y = p[1]
                            print self.cor,p
                            break


                if self.life <= 0:
                    self.explode = True
                    
                if self.conta_tempo_morte > 0:
                    self.conta_tempo_morte-= 1
                    
                if self.conta_tempo_morte <= fps * 2:
                    self.add(grupo)
                    self.life = 500
                    self.explode = False
                    if self.conta_tempo_morte <= 0:
                        self.conta_tempo_morte = fps * 5


                
        def perde_velocidade(self, limite, limite_re):
            """ controla a velocidade do carro """
            if self.velocidade_carro > limite:
                self.velocidade_carro-= 50
            elif -600 < self.velocidade_carro < limite_re:
                self.velocidade_carro+= 35


        def pisa_brita(self):
            """ determina as ações do carro quando este pisa na brita """
            if pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) not in [preto, branco,azul_bebe,\
                                                                 verde, azul, amarelo_escuro]:
                self.perde_velocidade(300, -80)


        def pisa_agua(self):
            """ determina as ações do carro quando este pisa na agua """
            if pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) == azul and self.velocidade_carro > 200:
                self.perde_life(5)
                self.direcao_rotacao = random.randint(-1,1)
                self.velocidade_carro -= 25


        def pisa_atalho(self):
            """ determina as ações do carro quando este passa pelo atalho """
            if pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) == amarelo_escuro:
                self.perde_velocidade(100, -80)
                self.perde_life(20)

        def get_orientation(self):
            """conversão em radianos -pi a pi"""
            if  self.rotacao < 90:
                return (self.rotacao - 90)/180 * PI
            elif 90 <= self.rotacao <= 270 :
                return (self.rotacao - 90)/180 * PI
            else:
                return (self.rotacao - 360)/180 * PI - PI/2

        def safety_belt(self,point):
             return (point[0] if point[0] > 0 and point[0] < tam_tela_x else 0 if point[0] < 0 else tam_tela_x-1,
                     point[1] if point[1] > 0 and point[1] < tam_tela_y else 0 if point[1] < 0 else tam_tela_y-1)

        def refresh_sensors(self,display):
            alfa = self.rotacao * PI /180
            slide = 20 * PI / 180

            delta = 60 /fabs(self.velocidade_max/(self.velocidade_carro+1)) + 40
            deltacenter = 40/fabs(self.velocidade_max/(self.velocidade_carro+1)) + 30
            self.left = (int(self.posicao.x + delta * sin(alfa + slide)-3), int(self.posicao.y + delta * cos(alfa + slide)-3))
            self.right = (int(self.posicao.x + delta * sin(alfa - slide)-3), int(self.posicao.y + delta * cos(alfa - slide)-3))
            self.center = (int(self.posicao.x + (deltacenter) * sin(alfa)-3), int(self.posicao.y + (deltacenter) * cos(alfa)-3))
            self.opponentSensor = (int(self.posicao.x + (deltacenter + 100) * sin(alfa)-3), int(self.posicao.y + (deltacenter + 100) * cos(alfa)-3))

            self.left = self.safety_belt(self.left)
            self.right = self.safety_belt(self.right)
            self.center = self.safety_belt(self.center)
            self.opponentSensor = self.safety_belt(self.opponentSensor)

            if display:
                screen.blit(self.sensorimg, self.left)
                screen.blit(self.sensorimg, self.right)
                screen.blit(self.sensorimg, self.center)
                screen.blit(self.sensorimg, self.opponentSensor)
            
        def run_behaviour(self):

            self.refresh_sensors(True)

            self.velocidade_rotacao = max(math.fabs(self.velocidade_carro/2),45)

            self.direcao_rotacao = 0
            if not self.pista_left() :
                self.direcao_rotacao = -1
                self.trava()

            elif not self.pista_right() :
                self.direcao_rotacao = 1
                self.trava()

            if not self.pista_center()  :
                self.trava()
            else:
                self.acelera()

#
#  Definição da BehaviourTree
#

        #Define o comportamento do carro sobre a forma de uma behaviourTree
        def defineBehaviour(self):
            return Sequence(Atomic(self.update),
                             Selector(
                                Sequence(Inverter(Atomic(self.pista_left)),
                                        Atomic(self.rotRight),
                                        Atomic(self.trava)),
                                Sequence(Inverter(Atomic(self.pista_right)),
                                        Atomic(self.rotLeft),
                                        Atomic(self.trava)),
                                Atomic(self.succeed)
                             ),
                             Selector(
                                 Sequence(Atomic(self.pista_center),
                                          Atomic(self.acelera)
                                 ),
                                 Atomic(self.trava)
                             ),
                             RandomSelector(
                                Sequence(Atomic(self.found_you),
                                   Atomic(self.shoot)
                                   ),
								Atomic(self.succeed)
                             )
                    )

        #
        # Definição das funções correspondentes à ações atomicas
        #
        def update(self):
            self.refresh_sensors(True)
            self.velocidade_rotacao = max(math.fabs(self.velocidade_carro/2),45)
            self.direcao_rotacao = 0
            return True

        # Acções
        def rotLeft(self):
            self.direcao_rotacao = 1
            return True

        def rotRight(self):
            self.direcao_rotacao = -1
            return True

        def acelera(self):
            """ controla a aceleração do carro de acordo com seu estado"""
            if self.velocidade_carro < self.velocidade_max:
                self.velocidade_carro+= 5
            return True

        def trava(self):
            """ controla a aceleração do carro de acordo com seu estado"""
            if self.velocidade_carro > -10:
                self.velocidade_carro -= 10
            return True

        def found_you(self):
			if self.otherCar == None:
				return False
			if (self.opponentSensor[0] < self.otherCar.posicao[0] + 50 and self.opponentSensor[0] > self.otherCar.posicao[0] - 50
			and self.opponentSensor[1] < self.otherCar.posicao[1] + 50 and self.opponentSensor[1] > self.otherCar.posicao[1] - 50):
				return True
			
        def shoot(self):
			if self == carrop1 :
				self.atirar(time_passed_seconds, grupo_tiros1)
				return True
			elif self == carrop2 :
				self.atirar(time_passed_seconds, grupo_tiros2)
				return True
			

    #Sensores
        def pista_left(self):
            return self.pista(self.left)

        def pista_right(self):
            return self.pista(self.right)

        def pista_center(self):
            return self.pista(self.center)

        def succeed(self):
            return True

        #
        # Fim das acoes atomicas
        #

        def seek_behaviour(self):
            """implementa o comportamento de seek"""
            x, y = (int (self.posicao[0]),int(self.posicao[1]))
            nx,ny = tuple(pontos[self.nextpoint])
            rot = self.rotacao
            direction = pontos[self.nextpoint]-self.posicao
            
                
        def rotaciona_carro(self, pressed_key):
            """ rotaciona o carro(estado) de acordo com a ação realizada pelo usuário """
            self.direcao_rotacao = 0.
            x, y = (int (self.posicao[0]),int(self.posicao[1]))
             
            if self.velocidade_carro != 0:
                if self.velocidade_carro < 0:
                    if pressed_key[self.esquerda]:
                        self.direcao_rotacao = -1
                    elif pressed_key[self.direita]:
                        self.direcao_rotacao = +1
                else:
                    if pressed_key[self.esquerda]:
                        self.direcao_rotacao = +1
                    elif pressed_key[self.direita]:
                        self.direcao_rotacao = -1


        def rotaciona_imgcarro(self):
            """ rotaciona a imagem do carro de acordo com a ação realizadaa pelo usuário """
            self.imgcar = pygame.transform.rotate(self.imgcar, self.rotacao)
            self.w, self.h = self.imgcar.get_size()
            desenha_carro = Vector(self.posicao.x - self.w/2, self.posicao.y - self.h/2)
            screen.blit(self.imgcar, desenha_carro)
            

        def movimenta(self, time_passed_seconds):
            """ responsável pela movimentação geral (baseada em vetores) do carro """
            self.direcao_movimento = +(self.velocidade_carro/1000.)
            self.rotacao += self.direcao_rotacao * self.velocidade_rotacao * time_passed_seconds
            if self.rotacao >= 360:
               self.rotacao = self.rotacao - 360
            elif self.rotacao < 0:
               self.rotacao = 360 + self.rotacao
            heading_x = sin(self.rotacao*pi/180.0)
            heading_y = cos(self.rotacao*pi/180.0)
            heading = Vector(heading_x, heading_y)
            heading *= self.direcao_movimento
            self.posicao += heading * self.velocidade_max * time_passed_seconds
            if self.posicao.x > tam_tela_x-5:
                self.posicao.x = tam_tela_x-5
            elif self.posicao.x < 5:
                self.posicao.x = 5
            if self.posicao.y > tam_tela_y-5:
                self.posicao.y = tam_tela_y-5
            elif self.posicao.y < 5:
                self.posicao.y = 5

            

        def atualiza_rect(self):
            """ atualiza a representação do carro (retângulo) de acordo com a sua posição atual """
            self.rect = Rect(self.posicao.x - self.imgcar.get_width()/2, self.posicao.y - \
                              self.imgcar.get_height()/2, self.imgcar.get_width(), self.imgcar.get_height())
            

        def testa_batida(self, outro, grupo):
            """ verifica batidas entre os carros e produz o os efeitos de movimento de colisão """
            self.atualiza_rect()
            outro.atualiza_rect()
        
            x, y = (int (self.posicao[0]),int(self.posicao[1]))
            x1, y1 = tuple(self.pos_antes_batida)
            if outro in pygame.sprite.spritecollide(self, grupo, False):
                #self.sombatida.play()
                x, y = x1, y1
                if (45 <= self.rotacao <= 135 and 45 <= outro.rotacao <= 135) or\
                   (225 < self.rotacao < 315 and 225 < outro.rotacao < 315) or \
                   (135 < self.rotacao <= 225 and 135 < outro.rotacao <= 225) or\
                   ((315 < self.rotacao < 360 or 0 < self.rotacao < 45) and\
                    (315 < outro.rotacao < 360 or 0 < outro.rotacao < 45)):
                    
                    outro.velocidade_carro += self.velocidade_carro/3
                    outro.velocidade_carro -= outro.velocidade_carro % 10
                    self.velocidade_carro -= self.velocidade_carro/2
                    self.velocidade_carro -= self.velocidade_carro % 10
                    
                elif (225 < self.rotacao < 315 and 45 <= outro.rotacao <= 135) or\
                   (45 <= self.rotacao <= 135 and 225 < outro.rotacao < 315) or \
                   (135 < self.rotacao <= 225 and (315 < outro.rotacao < 360 or \
                    0 < outro.rotacao < 45)) or ((315 < self.rotacao < 360 \
                    or 0 < self.rotacao < 45) and 135 < outro.rotacao <= 225):

                    outro.velocidade_carro -= self.velocidade_carro/3
                    outro.velocidade_carro -= outro.velocidade_carro % 10
                    self.velocidade_carro -= self.velocidade_carro/2
                    self.velocidade_carro -= self.velocidade_carro % 10
                    
                elif ((self.velocidade_carro > 0 and 45 < self.rotacao < 135) or \
                      (self.velocidade_carro < 0 and 225 < self.rotacao < 315)) and\
                      (135 < outro.rotacao <= 225 or (315 < outro.rotacao < 360 or 0 < outro.rotacao < 45)):
                    
                      self.velocidade = self.velocidade_carro/4
                      outro.posicao.x += 2
                      
                elif ((self.velocidade_carro < 0 and 45 < self.rotacao < 135) or \
                      (self.velocidade_carro > 0 and 225 < self.rotacao < 315)) and  \
                      (135 < outro.rotacao <= 225 or (315 < outro.rotacao < 360 or 0 < outro.rotacao < 45)):
                    
                      self.velocidade = self.velocidade_carro/4
                      outro.posicao.x -= 2

                elif ((135 < self.rotacao < 225 and self.velocidade_carro > 0) or \
                      ((315 < self.rotacao < 360 or 0 < self.rotacao < 45) and \
                       self.velocidade_carro < 0)) and  (45 <= outro.rotacao <= 135 or 225 < outro.rotacao < 315):
                    
                      self.velocidade = self.velocidade_carro/4
                      outro.posicao.y -= 2

                elif ((315 < self.rotacao < 360 or 0 < self.rotacao < 45) and \
                      self.velocidade_carro > 0 or (135 < self.rotacao < 225 and \
                      self.velocidade_carro < 0)) and (45 <= outro.rotacao <= 135 or 225 < outro.rotacao < 315):

                      self.velocidade = self.velocidade_carro/4
                      outro.posicao.y += 2

                elif self.rect.collidepoint(outro.posicao):
                    self.perde_life(500)

                self.perde_life(5)
                
            else:
                self.pos_antes_batida = self.posicao

            self.posicao = Vector(x, y)


        def atirar(self, time_passed_seconds, grupo_tiros1):
            """ ações do carro quando o comando de tiro é acionado """
            #self.somtiro.play()
            tiro = Tiro(self, grupo_tiros1)
            self.municao -= 1
        

        def movimenta_tiro(self, time_passed_seconds, grupo_tiros1):
            """ atualiza a posição do tiro a medida que os frames são atualizados """
            for tiro in grupo_tiros1:
                tiro.movimenta(self, time_passed_seconds)
                screen.blit(tiro.imgtiro, tiro.posicao)
                tiro.atualiza_rect()
                if tiro.posicao.x <= 10 or tiro.posicao.x >= 1014 or tiro.posicao.y <= 10 or tiro.posicao.y >= 758:
                    grupo_tiros1.remove(tiro)
                    

        def testa_atingido(self, grupo_tiros2):
            """ verifica se o carro foi atingido por um tiro e atualiza os atributos do carro ao ser atingido pelo tiro """
            if pygame.sprite.spritecollide(self, grupo_tiros2, True):
                self.perde_life(200)
                if pressed_key[self.esquerda]:
                    self.direcao_rotacao = +10
                elif pressed_key[self.direita]:
                    self.direcao_rotacao = -10
                else:
                    self.rotacao += 30


        def completa_volta(self, pista):
            """ verifica se o carro completou volta de forma correta (checkpoints) """
            if pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) in [azul_bebe, azul_piscina]:
                self.checks = 1
            elif pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) in [verde, verde_escuro]\
                 and self.checks is 1:
                self.checks = 2
            elif pista.imgmapa_cores.get_at((int (self.posicao[0]),int(self.posicao[1]))) in [branco, cinza_claro]\
                 and self.checks is 2:
                
                self.ultima_volta_mil = self.cronometro.tick(fps)
                self.ultima_volta = self.ultima_volta_mil / 1000.0

                if self.melhor_volta == "-":
                    self.melhor_volta = self.ultima_volta

                if self.ultima_volta < self.melhor_volta:
                    self.melhor_volta = self.ultima_volta
                
                self.voltas+= 1
                self.checks = 0
                self.municao+= 5
                if self.voltas == pista.num_voltas:
                    return True


        def acoes(self, grupo, grupo_tiros1, grupo_tiros2):
            """ metoto responsável por atualizar todas as ações do carro """
            self.colide()
            self.muda_textura(pressed_key)

            self.run_behaviour()

            self.mybehaviour.run()

            self.rotaciona_imgcarro()
            self.pisa_agua()
            self.pisa_brita()
            self.pisa_atalho()
            self.movimenta(time_passed_seconds)
            self.movimenta_tiro(time_passed_seconds, grupo_tiros1)
            self.testa_atingido(grupo_tiros2)
            self.morre(grupo)
                

    class Tiro(Sprite):
        
        def __init__(self, player, *grupos):
            """ variáveis padrão de inicialização da classe """
            Sprite.__init__ ( self , *grupos )
            self.posicao = player.posicao.copy()
            self.rotacao = player.rotacao
            self.imgtiro = funcoes.carrega_imagem('tiro.png', 1)
            self.imgtiro = pygame.transform.rotate(self.imgtiro, self.rotacao)
            self.velocidade = 300
            self.rect = Rect(self.posicao.x - self.imgtiro.get_width()/2, self.posicao.y - self.imgtiro.get_height()/2,\
                        self.imgtiro.get_width(), self.imgtiro.get_height())
            

        def movimenta(self, carro, time_passed_seconds):
            """ posiciona o tiro de acordo com a posição do carro no momento de acionamento do tiro"""
            heading_x = sin(self.rotacao*pi/180.0)
            heading_y = cos(self.rotacao*pi/180.0)
            heading = Vector(heading_x, heading_y)
            self.posicao += heading * self.velocidade * time_passed_seconds
            

        def atualiza_rect(self):
            """ atualiza a representação do tiro (retângulo) de acordo com a sua posição atual """
            self.rect = Rect(self.posicao.x - self.imgtiro.get_width()/2, self.posicao.y - self.imgtiro.get_height()/2,\
                            self.imgtiro.get_width(), self.imgtiro.get_height()) 

    pygame.init()
    
    #tocar musica selecionada
    #pygame.mixer.music.load(musicas[num_musica]
    #pygame.mixer.music.play(-1)
    
    #instanciação dos objetos da corrida
    pista = Pista(num_pista)
    carrop1 = Carro(1, corp1)
    displayp1 = Display(1)
    grupo1 = pygame.sprite.GroupSingle(carrop1)
    grupo_tiros1 = pygame.sprite.Group()
    if players > 1:
        carrop2 = Carro(2, corp2)
        carrop2.velocidade_max +=50
        displayp2 = Display(2)
        grupo2 = pygame.sprite.GroupSingle(carrop2)
        carrop1.setOtherCar(carrop2)
        carrop2.setOtherCar(carrop1)
    #grupo de tiros de cada carro. Ele eh independente do numero de players 
    grupo_tiros1 = pygame.sprite.Group()
    grupo_tiros2 = pygame.sprite.Group()
    clock = pygame.time.Clock()
    
    sairmenu = False
    
    while True:
        
        time_passed = clock.tick(fps)
        time_passed_seconds = time_passed / 1000.0

        displayp1.exibe_display()
        if players > 1:
            displayp2.exibe_display()
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                #pygame.mixer.music.stop()
                exit()
            if event.type == KEYUP and event.key == K_ESCAPE:
                #pygame.mixer.music.stop()
                sairmenu = True
            #if pista.tempo_largada >= fps*10:
#            if carrop1.isOnTarget(carrop2,carrop1.opponentSensor):
#                carrop1.atirar(time_passed_seconds, grupo_tiros1)

#            if carrop2.isOnTarget(carrop1, carrop2.opponentSensor):
#                carrop2.atirar(time_passed_seconds, grupo_tiros2)
                #if event.type == KEYDOWN:
                #    if event.key == K_RCTRL and carrop1.municao > 0 and carrop1 in grupo1:

                #    if players > 1:§
                #        if event.key == K_LCTRL and carrop2.municao > 0 and carrop2 in grupo2:
         

                            
        pressed_key = pygame.key.get_pressed()
        
        pista.carrega_mapa_cores()
        pista.carrega_pista()
        
        carrop1.acoes(grupo1, grupo_tiros1, grupo_tiros2)
            
        if players > 1:
            carrop2.acoes(grupo2, grupo_tiros2, grupo_tiros1)
                
            #colisao entre os carros
            carrop1.testa_batida(carrop2, grupo2)
            carrop2.testa_batida(carrop1, grupo1)
            
        pista.mostra_arvores()
        pista.larga()
        
        if carrop1.completa_volta(pista):
            foto_nerd = nerdp1
            break
        if players > 1:
            if carrop2.completa_volta(pista):
                foto_nerd = nerdp2
                break

        if sairmenu:
            break
        
    if not sairmenu:

        displayp1.exibe_display()
        if players > 1:
            displayp2.exibe_display()
            
        pygame.display.update()
        
        #pygame.mixer.music.stop()
        #somwin = pygame.mixer.Sound('sound/winrace.wav')
        screen.blit(funcoes.carrega_imagem('congratulations.png', 1), (0, 0))
        screen.blit(foto_nerd, (425, 242))
        #somwin.play()
        pygame.display.update()

        while True:
            stop = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    #pygame.mixer.music.stop()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        stop = True
            if stop:
                #pygame.mixer.music.stop()
                #pygame.mixer.music.load("sound/inicio.mp3")
                #pygame.mixer.music.play(-1)
                break

    #pygame.mixer.music.stop()
    #pygame.mixer.music.load("sound/inicio.mp3")
    #pygame.mixer.music.play(-1)
    
