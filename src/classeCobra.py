
import pygame
from time import sleep as wait

# Constantes
LARGURA_TELA = 800  # Largura da tela
ALTURA_TELA = 800   # Altura da tela
TAMANHO_BLOCO = 50  # Tamanho de cada bloco (parte da cobra e da comida)
FPS = 8             # Taxa de quadros por segundo (velocidade do jogo)

# Definição das cores
PRETO = (0, 0, 0)     # Cor preta
BRANCO = (255, 255, 255)  # Cor branca

# Classe que representa a cobra
# VITOR ---------------------------------------------
class Cobra:
    def __init__(self, skin):
        self.corpo = [[LARGURA_TELA // 2, ALTURA_TELA // 2]]  # Começo da cobra no centro da tela
        self.direcao = "DIREITA"  # Direção inicial da cobra
        self.imagem = pygame.transform.scale(skin, (TAMANHO_BLOCO, TAMANHO_BLOCO))  # Definindo o tamanho da imagem da cobra

    def mover(self, comida_pos):
        x, y = self.corpo[0]  # Posição da cabeça da cobra
        if self.direcao == "DIREITA":
            x += TAMANHO_BLOCO
        elif self.direcao == "ESQUERDA":
            x -= TAMANHO_BLOCO
        elif self.direcao == "CIMA":
            y -= TAMANHO_BLOCO
        elif self.direcao == "BAIXO":
            y += TAMANHO_BLOCO

        nova_cabeca = [x, y]  # Nova posição da cabeça da cobra
        self.corpo.insert(0, nova_cabeca)  # Adiciona a nova cabeça à frente

        # Se não comeu a comida, remove a última parte do corpo (a cauda)
        if nova_cabeca != comida_pos:
            self.corpo.pop()

    def desenhar(self, tela):
        # Desenha cada segmento do corpo da cobra na tela
        for segmento in self.corpo:
            tela.blit(self.imagem, (segmento[0], segmento[1]))

        # JÚLIO ---------------------------------------------
    
    def colidiu_com_borda(self):
        # Verifica se a cabeça da cobra bateu na borda da tela
        x, y = self.corpo[0]
        return x < 0 or x >= LARGURA_TELA or y < 0 or y >= ALTURA_TELA

    def colidiu_com_corpo(self):
        # Verifica se a cabeça da cobra bateu em algum segmento do seu corpo
        return self.corpo[0] in self.corpo[1:]

    def set_direcao(self, nova_direcao):
        # Impede que a cobra se mova para a direção oposta imediatamente
        opostos = {"DIREITA": "ESQUERDA", "ESQUERDA": "DIREITA", "CIMA": "BAIXO", "BAIXO": "CIMA"}
        if nova_direcao != opostos.get(self.direcao):
            self.direcao = nova_direcao

    def resetar(self, skin):
        # Reseta a cobra para a posição inicial
        self.__init__(skin)

