

import pygame
import random
from time import sleep as wait

# Inicialização
pygame.init()

# Constantes
LARGURA_TELA = 800
ALTURA_TELA = 800
TAMANHO_BLOCO = 50
FPS = 8

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Sons
som_comendo = pygame.mixer.Sound('./src/sounds/eating.wav')
som_gameover = pygame.mixer.Sound('./src/sounds/gameover.wav')
som_sucesso = pygame.mixer.Sound('./src/sounds/sucess.wav')

# Tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo da Cobra")

# Imagens
img1 = pygame.image.load('./src/img/skin1.png').convert_alpha()
img2 = pygame.image.load('./src/img/skin2.png').convert_alpha()
img3 = pygame.image.load('./src/img/skin3.png').convert_alpha()
img4 = pygame.image.load('./src/img/skin4.png').convert_alpha()
img_apple = pygame.image.load('./src/img/apple.png').convert_alpha()



class Cobra:
    def __init__(self, skin):
        self.corpo = [[LARGURA_TELA // 2, ALTURA_TELA // 2]]
        self.direcao = "DIREITA"
        self.imagem = pygame.transform.scale(skin, (TAMANHO_BLOCO, TAMANHO_BLOCO))

    def mover(self, comida_pos):
        x, y = self.corpo[0]
        if self.direcao == "DIREITA":
            x += TAMANHO_BLOCO
        elif self.direcao == "ESQUERDA":
            x -= TAMANHO_BLOCO
        elif self.direcao == "CIMA":
            y -= TAMANHO_BLOCO
        elif self.direcao == "BAIXO":
            y += TAMANHO_BLOCO

        nova_cabeca = [x, y]
        self.corpo.insert(0, nova_cabeca)

        if nova_cabeca != comida_pos:
            self.corpo.pop()

    def desenhar(self, tela):
        for segmento in self.corpo:
            tela.blit(self.imagem, (segmento[0], segmento[1]))

    def colidiu_com_borda(self):
        x, y = self.corpo[0]
        return x < 0 or x >= LARGURA_TELA or y < 0 or y >= ALTURA_TELA

    def colidiu_com_corpo(self):
        return self.corpo[0] in self.corpo[1:]

    def set_direcao(self, nova_direcao):
        # Impede reversão imediata
        opostos = {"DIREITA": "ESQUERDA", "ESQUERDA": "DIREITA", "CIMA": "BAIXO", "BAIXO": "CIMA"}
        if nova_direcao != opostos.get(self.direcao):
            self.direcao = nova_direcao

    def resetar(self, skin):
        self.__init__(skin)

class Comida:
    def __init__(self):
        self.imagem = pygame.transform.scale(img_apple, (TAMANHO_BLOCO, TAMANHO_BLOCO))
        self.posicao = self.gerar_posicao()

    def gerar_posicao(self):
        x = random.randrange(0, LARGURA_TELA, TAMANHO_BLOCO)
        y = random.randrange(0, ALTURA_TELA, TAMANHO_BLOCO)
        return [x, y]

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.posicao[0], self.posicao[1]))

class JogoCobrinha:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.estado = "start_menu"
        self.skins = [img1, img2, img3, img4]
        self.skin_selecionada = img1
        self.imagem_skin_menu = pygame.transform.scale(self.skin_selecionada, (TAMANHO_BLOCO, TAMANHO_BLOCO))
        self.cobra = Cobra(self.skin_selecionada)
        self.comida = Comida()
        self.pontuacao = 0

    def desenhar_menu(self):
        tela.fill(PRETO)
        fonte = pygame.font.SysFont('arial', 40)
        title = fonte.render('Jogo da Cobrinha', True, BRANCO)
        start = fonte.render('Pressione espaço para começar', True, BRANCO)
        skin_txt = fonte.render('Pressione 1, 2, 3 ou 4 para selecionar a skin', True, BRANCO)

        tela.blit(title, (LARGURA_TELA/2 - title.get_width()/2, ALTURA_TELA/2 - 350))
        tela.blit(skin_txt, (LARGURA_TELA/2 - skin_txt.get_width()/2, ALTURA_TELA/2 + 200))
        tela.blit(start, (LARGURA_TELA/2 - start.get_width()/2, ALTURA_TELA/2 + 300))
        tela.blit(self.imagem_skin_menu, (LARGURA_TELA / 2 - TAMANHO_BLOCO / 2, ALTURA_TELA / 2 - 50))
        pygame.display.update()

    def exibir_pontuacao(self):
        fonte = pygame.font.Font(None, 40)
        texto = fonte.render(f"Pontuação: {self.pontuacao}", True, BRANCO)
        tela.blit(texto, (5, 5))

    def resetar_jogo(self):
        self.cobra.resetar(self.skin_selecionada)
        self.comida = Comida()
        self.pontuacao = 0

    def loop(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if evento.type == pygame.KEYDOWN:
                    if self.estado == "start_menu":
                        if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            index = int(evento.key) - pygame.K_1
                            self.skin_selecionada = self.skins[index]
                            self.imagem_skin_menu = pygame.transform.scale(self.skin_selecionada, (TAMANHO_BLOCO, TAMANHO_BLOCO))
                        elif evento.key == pygame.K_SPACE:
                            som_sucesso.play()
                            self.estado = "game"
                            self.resetar_jogo()

                    elif self.estado == "game":
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

if __name__ == "__main__":
    jogo = JogoCobrinha()
    jogo.loop()
