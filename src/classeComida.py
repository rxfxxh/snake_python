import pygame
import random
from time import sleep as wait


# Constantes
LARGURA_TELA = 800  # Largura da tela
ALTURA_TELA = 800   # Altura da tela
TAMANHO_BLOCO = 50  # Tamanho de cada bloco (parte da cobra e da comida)
FPS = 8             # Taxa de quadros por segundo (velocidade do jogo)

# Definição das cores
PRETO = (0, 0, 0)     # Cor preta
BRANCO = (255, 255, 255)  # Cor branca

# Inicialização da biblioteca Pygame
pygame.init()
# Tela de exibição
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))  # Criando a tela
pygame.display.set_caption("Jogo da Cobrinha")  # Título da janela

img_apple = pygame.image.load('./img/apple.png').convert_alpha()

# LEONARDO ---------------------------------------------
# Classe que representa a comida (maçã)
class Comida:
    def __init__(self):
        self.imagem = pygame.transform.scale(img_apple, (TAMANHO_BLOCO, TAMANHO_BLOCO))  # Definindo o tamanho da imagem da comida
        self.posicao = self.gerar_posicao()  # Gera uma nova posição para a comida

    def gerar_posicao(self):
        # Gera uma posição aleatória para a comida dentro dos limites da tela
        x = random.randrange(0, LARGURA_TELA, TAMANHO_BLOCO)
        y = random.randrange(0, ALTURA_TELA, TAMANHO_BLOCO)
        return [x, y]

    def desenhar(self, tela):
        # Desenha a comida na tela
        tela.blit(self.imagem, (self.posicao[0], self.posicao[1]))
