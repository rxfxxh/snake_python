import pygame
from classeCobra import Cobra
from classeComida import Comida
import random
from time import sleep as wait

# Inicialização da biblioteca Pygame
pygame.init()

# Constantes
LARGURA_TELA = 800  # Largura da tela
ALTURA_TELA = 800   # Altura da tela
TAMANHO_BLOCO = 50  # Tamanho de cada bloco (parte da cobra e da comida)
FPS = 8             # Taxa de quadros por segundo (velocidade do jogo)

# Definição das cores
PRETO = (0, 0, 0)     # Cor preta
BRANCO = (255, 255, 255)  # Cor branca

# Sons
som_comendo = pygame.mixer.Sound('./src/sounds/eating.wav')  # Som quando a cobra come a comida
som_gameover = pygame.mixer.Sound('./src/sounds/gameover.wav')  # Som de game over
som_sucesso = pygame.mixer.Sound('./src/sounds/sucess.wav')  # Som de sucesso ao iniciar o jogo

# Carregando as imagens das skins e da maçã
img1 = pygame.image.load('./src/img/skin1.png').convert_alpha()
img2 = pygame.image.load('./src/img/skin2.png').convert_alpha()
img3 = pygame.image.load('./src/img/skin3.png').convert_alpha()
img4 = pygame.image.load('./src/img/skin4.png').convert_alpha()


# Tela de exibição
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))  # Criando a tela
pygame.display.set_caption("Jogo da Cobrinha")  # Título da janela



# Classe principal do jogo
class JogoCobrinha:
    def __init__(self):
        self.clock = pygame.time.Clock()  # Controla a taxa de quadros por segundo
        self.estado = "start_menu"  # Estado inicial (menu)
        self.skins = [img1, img2, img3, img4]  # Lista de skins para a cobra
        self.skin_selecionada = img1  # Skin inicial da cobra
        self.imagem_skin_menu = pygame.transform.scale(self.skin_selecionada, (TAMANHO_BLOCO, TAMANHO_BLOCO))  # Imagem da skin para o menu
        self.cobra = Cobra(self.skin_selecionada)  # Inicializa a cobra com a skin selecionada
        self.comida = Comida()  # Inicializa a comida
        self.pontuacao = 0  # Pontuação inicial

    def desenhar_menu(self):
        # Desenha o menu de início do jogo
        tela.fill(PRETO)  # Limpa a tela com a cor preta
        fonte = pygame.font.SysFont('arial', 40)  # Fonte para o texto
        title = fonte.render('Jogo da Cobrinha', True, BRANCO)  # Texto do título
        start = fonte.render('Pressione espaço para começar', True, BRANCO)  # Texto para começar
        skin_txt = fonte.render('Pressione 1, 2, 3 ou 4 para selecionar a skin', True, BRANCO)  # Texto para escolher a skin

        tela.blit(title, (LARGURA_TELA/2 - title.get_width()/2, ALTURA_TELA/2 - 350))  # Desenha o título na tela
        tela.blit(skin_txt, (LARGURA_TELA/2 - skin_txt.get_width()/2, ALTURA_TELA/2 + 200))  # Desenha a instrução de skin
        tela.blit(start, (LARGURA_TELA/2 - start.get_width()/2, ALTURA_TELA/2 + 300))  # Desenha a instrução de começar
        tela.blit(self.imagem_skin_menu, (LARGURA_TELA / 2 - TAMANHO_BLOCO / 2, ALTURA_TELA / 2 - 50))  # Desenha a skin selecionada
        pygame.display.update()  # Atualiza a tela

    def exibir_pontuacao(self):
        # Exibe a pontuação na tela
        fonte = pygame.font.Font(None, 40)
        texto = fonte.render(f"Pontuação: {self.pontuacao}", True, BRANCO)
        tela.blit(texto, (5, 5))  # Desenha a pontuação no canto superior esquerdo

    def resetar_jogo(self):
        # Reseta o jogo para o estado inicial
        self.cobra.resetar(self.skin_selecionada)
        self.comida = Comida()
        self.pontuacao = 0

    def loop(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Encerra o jogo se a janela for fechada

                if evento.type == pygame.KEYDOWN:
                    if self.estado == "start_menu":
                        # Mudança de skin no menu
                        if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            index = int(evento.key) - pygame.K_1
                            self.skin_selecionada = self.skins[index]
                            self.imagem_skin_menu = pygame.transform.scale(self.skin_selecionada, (TAMANHO_BLOCO, TAMANHO_BLOCO))
                        elif evento.key == pygame.K_SPACE:
                            som_sucesso.play()  # Som de sucesso ao iniciar o jogo
                            self.estado = "game"  # Muda o estado para o jogo
                            self.resetar_jogo()

                    elif self.estado == "game":
                        # Movimenta a cobra dependendo da tecla pressionada

                        if evento.key in [pygame.K_LEFT, pygame.K_a]:
                            self.cobra.set_direcao("ESQUERDA")
                        elif evento.key in [pygame.K_RIGHT, pygame.K_d]:
                            self.cobra.set_direcao("DIREITA")
                        elif evento.key in [pygame.K_UP, pygame.K_w]:
                            self.cobra.set_direcao("CIMA")
                        elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                            self.cobra.set_direcao("BAIXO")

            if self.estado == "start_menu":
                self.desenhar_menu()

            elif self.estado == "game":
                self.cobra.mover(self.comida.posicao)

                if self.cobra.colidiu_com_borda() or self.cobra.colidiu_com_corpo():
                    som_gameover.play()
                    wait(2)
                    pygame.quit()
                    exit()

                if self.cobra.corpo[0] == self.comida.posicao:
                    som_comendo.play()
                    self.comida.posicao = self.comida.gerar_posicao()
                    self.pontuacao += 1

                tela.fill(PRETO)
                self.cobra.desenhar(tela)
                self.comida.desenhar(tela)
                self.exibir_pontuacao()
                pygame.display.flip()
                self.clock.tick(FPS)
