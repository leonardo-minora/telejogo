# exemplo de modifiação direto no codespace
import pygame

# movendo a bola
def bola_mover(bola, velocidade, delta, jogadores):
    # usa a função move inplace
    bola.move_ip(velocidade * delta, 0)
    # checa por colisão com os jogadores
    colisao = bola.collidelist(jogadores)
    if colisao >= 0:
        velocidade = -velocidade
    return velocidade


# contabilização de gols
def gol(bola, gols_esquerda, gols_direita, margem_esquerda, margem_direita,
        largura, velocidade):
    if bola.left <= margem_esquerda:
        bola.move_ip(largura // 2, 0)
        gols_direita += 1
        velocidade = -(velocidade)
    elif bola.right >= margem_direita:
        bola.move_ip(-(largura // 2), 0)
        gols_esquerda += 1
        velocidade = -(velocidade)
    return [gols_esquerda, gols_direita, velocidade]


# Função para fazer a movimentação dos jogadores
def mover_jogador(tecla, jogador, velocidade_y, delta_de_tempo, altura_tela):
    if tecla == pygame.K_UP:
        jogador.move_ip(0, -(velocidade_y * delta_de_tempo))
        if jogador.top <= 0:
            jogador.move_ip(0, -jogador.top)
    elif tecla == pygame.K_DOWN:
        jogador.move_ip(0, velocidade_y * delta_de_tempo)
        if jogador.bottom >= altura_tela:
            delta_y = altura_tela - jogador.bottom
            jogador.move_ip(0, delta_y)


# escrever o texto no topo da janela
def escreve(texto, tela, cor, largura):
    fonte_name = pygame.font.get_default_font()
    fonte = pygame.font.Font(fonte_name, 32)
    texto = fonte.render(texto, True, cor)
    texto_retangulo = texto.get_rect()
    texto_retangulo.center = (largura // 2, 20)
    tela.blit(texto, texto_retangulo)


# função para apresentar tela inicial
def abrir_tela_de_entrada(tela, largura, altura):
    # configurando imagem
    tamanho = (largura, altura)
    imagem_original = pygame.image.load('sprites/campo.jpg').convert()
    imagem = pygame.transform.scale(imagem_original, tamanho)

    # mostrando imagem
    tela.blit(imagem, (0, 0))

    # configurando texto
    escreve('Pressionar espaço para iniciar o jogo…', tela, PRETO, largura)

    #atualizando tela
    pygame.display.flip()
    sair_tela_entrada = False
    while not sair_tela_entrada:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            sair_tela_entrada = event.key == pygame.K_SPACE
    return imagem


# Contantes das cores utilizadsas no jogo
PRETO = pygame.Color(0, 0, 0)
BRANCO = pygame.Color(255, 255, 255)
VERMELHO = (255, 0, 0)

tela_altura = 480
tela_largura = 640

# cria tela gráfica do jogo
pygame.init()
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption('INFOWEB - Tele jogo')

# cria o Rect para a bola
bola = pygame.Rect(300, 230, 20, 20)
velocidade_x = 0.1

# cria o Rect para os jogadores
velocidade_jogador_esquerda_y = 0.5
velocidade_jogador_direta_y = 0.5
gols_esquerda = 0
gols_direita = 0
jogador_esquerda = pygame.Rect(15, 210, 20, 60)
jogador_direita = pygame.Rect(607, 210, 20, 60)

jogadores = [jogador_esquerda, jogador_direita]

# apresenta tela de entrada
campo = abrir_tela_de_entrada(tela, tela_largura, tela_altura)

# Loop principal do jogo
clock = pygame.time.Clock()
while True:
    delta_de_tempo = clock.tick(30)

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            mover_jogador(pygame.K_UP, jogador_esquerda,
                          velocidade_jogador_esquerda_y, delta_de_tempo,
                          tela_altura)
        elif event.key == pygame.K_s:
            mover_jogador(pygame.K_DOWN, jogador_esquerda,
                          velocidade_jogador_esquerda_y, delta_de_tempo,
                          tela_altura)
        if event.key == pygame.K_UP:
            mover_jogador(pygame.K_UP, jogador_direita,
                          velocidade_jogador_direta_y, delta_de_tempo,
                          tela_altura)
        elif event.key == pygame.K_DOWN:
            mover_jogador(pygame.K_DOWN, jogador_direita,
                          velocidade_jogador_direta_y, delta_de_tempo,
                          tela_altura)

    # mover a bola
    velocidade_x = bola_mover(bola, velocidade_x, delta_de_tempo, jogadores)
    # contabilizar gols
    gols_esquerda, gols_direita, velocidade_x = gol(bola, gols_esquerda,
                                                    gols_direita, 0,
                                                    tela_largura, tela_largura,
                                                    velocidade_x)

    # coloca o campo na tela
    tela.blit(campo, (0, 0))

    # coloca o placar na tela
    escreve(f'Esquera {gols_esquerda} X {gols_direita} Direita', tela, BRANCO,
            tela_largura)

    # desenha o quadrado usando o Rect
    pygame.draw.rect(tela, BRANCO, bola)

    # desenha os jogadores
    for jogador in jogadores:
        pygame.draw.rect(tela, BRANCO, jogador)

    pygame.display.flip()
