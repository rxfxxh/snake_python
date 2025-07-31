import pygame
import random
import os #importar para caminhos de arquivo

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA_TELA = 800
ALTURA_TELA = 800
TAMANHO_BLOCO = 40 # Tamanho de cada segmento da cobra e da comida
FPS = 10 # Velocidade do jogo (frames por segundo)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

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
    fonte = pygame.font.Font(None, 25) # Fonte padrão, tamanho 25
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontuacao, (5, 5))

def jogo():
    # Carrega a imagem da cobra no início do jogo
    cobra = [[LARGURA_TELA / 2, ALTURA_TELA / 2]] # Posição inicial da cobra (cabeça)
    direcao = "DIREITA" # Direção inicial da cobra
    comida = gerar_comida() # Gera a primeira comida
    pontuacao = 0
    jogo_acabou = False

    while not jogo_acabou:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_acabou = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and direcao != "DIREITA" or (evento.key == pygame.K_a and direcao != "DIREITA"):
                    direcao = "ESQUERDA"
                elif evento.key == pygame.K_RIGHT and direcao != "ESQUERDA" or (evento.key == pygame.K_d and direcao != "ESQUERDA"):
                    direcao = "DIREITA"
                elif evento.key == pygame.K_UP and direcao != "BAIXO" or (evento.key == pygame.K_w and direcao != "BAIXO"):
                    direcao = "CIMA"
                elif evento.key == pygame.K_DOWN and direcao != "CIMA" or (evento.key == pygame.K_s and direcao != "CIMA"):
                    direcao = "BAIXO"

        cobra = mover_cobra(cobra, direcao, comida) # Passa a comida para a função de movimento


        # Colisão com as bordas da tela
        if cobra[0][0] >= LARGURA_TELA or cobra[0][0] < 0 or \
           cobra[0][1] >= ALTURA_TELA or cobra[0][1] < 0:
            jogo_acabou = True

        # Colisão com o próprio corpo
        # Percorre todos os segmentos da cobra, exceto a cabeça (o primeiro elemento)
        for segmento in cobra[1:]: 
            if cobra[0][0] == segmento[0] and cobra[0][1] == segmento[1]:
                jogo_acabou = True

        # Colisão com a comida
        if cobra[0][0] == comida[0] and cobra[0][1] == comida[1]:
            comida = gerar_comida() # Gera nova comida
            pontuacao += 1 # Aumenta a pontuação

        tela.fill(PRETO) # Limpa a tela com o fundo preto
        desenhar_cobra(cobra) # Desenha a cobra atualizada
        desenhar_comida(comida) # Desenha a comida
        exibir_pontuacao(pontuacao) # Exibe a pontuação

        pygame.display.flip() # Atualiza toda a tela para mostrar o que foi desenhado
        relogio.tick(FPS) # Controla a velocidade do jogo

    pygame.quit() # Desinicializa todos os módulos Pygame
    quit() # Sai do Python

# Inicia o jogo
if __name__ == "__main__":
    jogo()
