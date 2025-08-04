import pygame
import random
import os #importar para caminhos de arquivo
from time import sleep as wait

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA_TELA = 800
ALTURA_TELA = 800
TAMANHO_BLOCO = 50 # Tamanho de cada segmento da cobra e da comida
FPS = 10 # Velocidade do jogo (frames por segundo)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Sons

som_comendo = pygame.mixer.Sound('./sounds/eating.wav')
som_gameover = pygame.mixer.Sound('./sounds/gameover.wav')
som_sucesso = pygame.mixer.Sound('./sounds/sucess.wav')

# Cria a tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo da Cobra")

relogio = pygame.time.Clock()



# Carregamento do estilo da Cobra 
#Caminho da imagem
CAMINHO_IMAGEM_COBRA = './img/a.png'
imagem_cobra = None 
img1 = pygame.image.load(CAMINHO_IMAGEM_COBRA).convert_alpha()
imagem_cobra = pygame.transform.scale(img1, (TAMANHO_BLOCO, TAMANHO_BLOCO))

imagem_maca = None
img2 = pygame.image.load('./img/apple.png').convert_alpha()
imagem_maca = pygame.transform.scale(img2, (TAMANHO_BLOCO, TAMANHO_BLOCO))
# Função para carregar e escalar a imagem da cobra

def desenhar_cobra(cobra):
    # Desenha cada segmento da cobra na tela
    for segmento in cobra:
        tela.blit(imagem_cobra, (segmento[0], segmento[1]))

def mover_cobra(cobra, direcao, comida):
    """
    Atualiza a posição da cobra com base na direção.
    Verifica se a cobra comeu a comida para determinar se ela deve crescer.
    """
    x_cabeca, y_cabeca = cobra[0]

    if direcao == "DIREITA":
        x_cabeca += TAMANHO_BLOCO
    elif direcao == "ESQUERDA":
        x_cabeca -= TAMANHO_BLOCO
    elif direcao == "CIMA":
        y_cabeca -= TAMANHO_BLOCO
    elif direcao == "BAIXO":
        y_cabeca += TAMANHO_BLOCO

    nova_cabeca = [x_cabeca, y_cabeca]
    cobra.insert(0, nova_cabeca) # Adiciona a nova cabeça

    # Se a cabeça não está na mesma posição da comida, remove o último segmento
    # Isso faz a cobra se mover e crescer apenas quando come
    if not (nova_cabeca[0] == comida[0] and nova_cabeca[1] == comida[1]):
        cobra.pop()
    
    return cobra

def gerar_comida():
    """Gera uma nova posição aleatória para a comida na grade."""
    x = random.randrange(0, LARGURA_TELA - TAMANHO_BLOCO, TAMANHO_BLOCO)
    y = random.randrange(0, ALTURA_TELA - TAMANHO_BLOCO, TAMANHO_BLOCO)
    return [x, y]

def desenhar_comida(comida):
    tela.blit(imagem_maca, (comida[0], comida[1]))

def exibir_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30) # Fonte padrão, tamanho 30
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontuacao, (5, 5))

def desenhar_menu():
    tela.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Jogo da Cobrinha', True, (255, 255, 255))
    start_button = font.render('Pressione espaço para começar', True, (255, 255, 255))
    tela.blit(title, (LARGURA_TELA/2 - title.get_width()/2, ALTURA_TELA/2 - title.get_height()/2))
    tela.blit(start_button, (LARGURA_TELA/2 - start_button.get_width()/2, ALTURA_TELA/2 +300 + start_button.get_height()/2))
    pygame.display.update()


def jogo():
    # O estado inicial do jogo é o menu
    game_state = "start_menu"

    # Essas variáveis precisam ser criadas fora do loop para não serem resetadas
    # a cada ciclo. Elas serão inicializadas de fato quando o jogo começar.
    cobra = [[LARGURA_TELA / 2, ALTURA_TELA / 2]]
    direcao = "DIREITA"
    comida = gerar_comida()
    pontuacao = 0

    while True:
        # AQUI É O LOOP PRINCIPAL. Ele roda o tempo todo.
        # Ele verifica todos os eventos (como cliques e teclas)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # Se o jogo estiver no menu e o usuário apertar a tecla Espaço...
            if game_state == "start_menu":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    som_sucesso.play()
                    game_state = "game"
                    # Resetamos as variáveis do jogo para começar de novo
                    cobra = [[LARGURA_TELA / 2, ALTURA_TELA / 2]]
                    direcao = "DIREITA"
                    comida = gerar_comida()
                    pontuacao = 0
            
            # Se o jogo estiver em andamento, verifica os comandos da cobra
            elif game_state == "game":
                if evento.type == pygame.KEYDOWN:
                    if (evento.key == pygame.K_LEFT or evento.key == pygame.K_a) and direcao != "DIREITA":
                        direcao = "ESQUERDA"
                    elif (evento.key == pygame.K_RIGHT or evento.key == pygame.K_d) and direcao != "ESQUERDA":
                        direcao = "DIREITA"
                    elif (evento.key == pygame.K_UP or evento.key == pygame.K_w) and direcao != "BAIXO":
                        direcao = "CIMA"
                    elif (evento.key == pygame.K_DOWN or evento.key == pygame.K_s) and direcao != "CIMA":
                        direcao = "BAIXO"

        # desenha e atualiza a tela, dependendo do estado atual
        if game_state == "start_menu":
            desenhar_menu()
        
        elif game_state == "game":
            # Toda a lógica do jogo ta aqui
            cobra = mover_cobra(cobra, direcao, comida)

            # Colisão com as bordas
            if cobra[0][0] >= LARGURA_TELA or cobra[0][0] < 0 or \
            cobra[0][1] >= ALTURA_TELA or cobra[0][1] < 0:
                som_gameover.play()
                wait(2)
                pygame.quit()
                exit()

            # Colisão com o próprio corpo
            for segmento in cobra[1:]:
                if cobra[0][0] == segmento[0] and cobra[0][1] == segmento[1]:
                    som_gameover.play()
                    wait(2)
                    pygame.quit()
                    exit()

            # Colisão com a comida
            if cobra[0][0] == comida[0] and cobra[0][1] == comida[1]:
                som_comendo.play()
                comida = gerar_comida()
                pontuacao += 1

            # Desenha e atualiza a tela do jogo
            tela.fill(PRETO)
            desenhar_cobra(cobra)
            desenhar_comida(comida)
            exibir_pontuacao(pontuacao)
            pygame.display.flip()
            relogio.tick(FPS)

# Inicia o jogo
if __name__ == "__main__":
    jogo()
