import pygame
import random
import time

# Configurações básicas
pygame.init()
largura_tela, altura_tela = 600, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo de Memorização")

# Cores
verde = (34, 139, 34)
preto = (0, 0, 0)
branco = (255, 255, 255)
azul = (0, 0, 255)
vermelho = (255, 0, 0)

# Configurações iniciais do grid
linhas_iniciais, colunas = 3, 4
tam_quadrado = 80

# Carregar imagens
background_image = pygame.image.load('./background/background.jpg')
background_image = pygame.transform.scale(background_image, (largura_tela, altura_tela))
character_front = pygame.image.load('./person/person_front.png')
character_front = pygame.transform.scale(character_front, (tam_quadrado - 20, tam_quadrado - 20))
character_back = pygame.image.load('./person/person_back.png')
character_back = pygame.transform.scale(character_back, (tam_quadrado - 20, tam_quadrado - 20))
character_left = pygame.image.load('./person/person_left.png')
character_left = pygame.transform.scale(character_left, (tam_quadrado - 20, tam_quadrado - 20))
character_right = pygame.image.load('./person/person_right.png')
character_right = pygame.transform.scale(character_right, (tam_quadrado - 20, tam_quadrado - 20))
vida_icon = pygame.image.load('./assets/heart.png')
vida_icon = pygame.transform.scale(vida_icon, (60, 60))

current_character = character_front
character_offset_x = (tam_quadrado - character_front.get_width()) // 2
character_offset_y = (tam_quadrado - character_front.get_height()) // 2

# Funções auxiliares
def calcular_offset_centralizado(linhas, colunas, tam_quadrado):
    offset_x = (largura_tela - (colunas * tam_quadrado)) // 2
    offset_y = (altura_tela - (linhas * tam_quadrado)) // 2
    return offset_x, offset_y

def desenhar_grid(linhas, offset_x, offset_y):
    for y in range(linhas):
        for x in range(colunas):
            pygame.draw.rect(
                tela, verde,
                (offset_x + x * tam_quadrado, offset_y + y * tam_quadrado, tam_quadrado, tam_quadrado), 1
            )

def atualizar_grid_posicoes(linhas):
    return [(x, y) for y in range(linhas) for x in range(colunas)]

def gerar_caminho_continuo(tamanho, grid_posicoes):
    caminho = [random.choice(grid_posicoes)]
    while len(caminho) < tamanho:
        x, y = caminho[-1]
        vizinhos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        vizinhos = [v for v in vizinhos if v in grid_posicoes and v not in caminho]
        if vizinhos:
            caminho.append(random.choice(vizinhos))
        else:
            caminho = [random.choice(grid_posicoes)]
    return caminho

def mostrar_caminho(caminho, offset_x, offset_y):
    for posicao in caminho:
        pygame.draw.rect(
            tela, azul,
            (offset_x + posicao[0] * tam_quadrado, offset_y + posicao[1] * tam_quadrado, tam_quadrado, tam_quadrado)
        )
        pygame.display.flip()
        time.sleep(0.5)
        tela.blit(background_image, (0, 0))
        desenhar_grid(linhas, offset_x, offset_y)
    pygame.display.flip()

def desenhar_hud(fase, vidas):
    fonte_fase = pygame.font.SysFont(None, 36)
    texto_fase = fonte_fase.render(f"Fase: {fase}", True, branco)
    tela.blit(texto_fase, (10, 10))
    for i in range(vidas):
        tela.blit(vida_icon, (largura_tela - (i + 1) * 65, 10))

def reiniciar_jogo():
    global fase, vidas, linhas, grid_posicoes, offset_x, offset_y, caminho, posicao_personagem, caminho_jogador
    fase = 1
    vidas = 3
    linhas = linhas_iniciais
    grid_posicoes = atualizar_grid_posicoes(linhas)
    offset_x, offset_y = calcular_offset_centralizado(linhas, colunas, tam_quadrado)
    caminho = gerar_caminho_continuo(fase + 1, grid_posicoes)
    posicao_personagem = caminho[0]
    caminho_jogador = [posicao_personagem]
    mostrar_caminho(caminho, offset_x, offset_y)

def iniciar_jogo():
    global grid_posicoes, offset_x, offset_y, caminho, posicao_personagem, caminho_jogador
    grid_posicoes = atualizar_grid_posicoes(linhas)
    offset_x, offset_y = calcular_offset_centralizado(linhas, colunas, tam_quadrado)
    caminho = gerar_caminho_continuo(fase + 1, grid_posicoes)
    posicao_personagem = caminho[0]
    caminho_jogador = [posicao_personagem]
    mostrar_caminho(caminho, offset_x, offset_y)

def exibir_mensagem(mensagem, cor):
    tela.fill(preto)
    fonte = pygame.font.SysFont(None, 55)
    texto = fonte.render(mensagem, True, cor)
    tela.blit(texto, (largura_tela // 4, altura_tela // 2))
    pygame.display.flip()
    time.sleep(2)

def menu_principal():
    tela.fill(preto)
    fonte_menu = pygame.font.SysFont(None, 48)
    opcoes = ["1. Iniciar Jogo", "2. Reiniciar Jogo", "3. Sair"]
    for i, opcao in enumerate(opcoes):
        texto = fonte_menu.render(opcao, True, branco)
        tela.blit(texto, (largura_tela // 4, altura_tela // 3 + i * 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                elif event.key == pygame.K_2:
                    return "restart"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    quit()

def menu_game_over():
    tela.fill(preto)
    fonte_menu = pygame.font.SysFont(None, 48)
    opcoes = ["1. Reiniciar Jogo", "2. Sair"]
    for i, opcao in enumerate(opcoes):
        texto = fonte_menu.render(opcao, True, branco)
        tela.blit(texto, (largura_tela // 4, altura_tela // 3 + i * 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "restart"
                elif event.key == pygame.K_2:
                    pygame.quit()
                    quit()

# Parâmetros do jogo
fase = 1
linhas = linhas_iniciais
vidas = 3

while True:
    acao = menu_principal()
    if acao == "start":
        reiniciar_jogo()
        jogando = True
    elif acao == "restart":
        reiniciar_jogo()
        jogando = True

    while jogando:
        tela.blit(background_image, (0, 0))
        desenhar_grid(linhas, offset_x, offset_y)
        desenhar_hud(fase, vidas)

        tela.blit(
            current_character,
            (offset_x + posicao_personagem[0] * tam_quadrado + character_offset_x,
             offset_y + posicao_personagem[1] * tam_quadrado + character_offset_y)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                nova_posicao = list(posicao_personagem)
                if event.key == pygame.K_UP:
                    nova_posicao[1] -= 1
                    current_character = character_back
                elif event.key == pygame.K_DOWN:
                    nova_posicao[1] += 1
                    current_character = character_front
                elif event.key == pygame.K_LEFT:
                    nova_posicao[0] -= 1
                    current_character = character_left
                elif event.key == pygame.K_RIGHT:
                    nova_posicao[0] += 1
                    current_character = character_right

                nova_posicao = tuple(nova_posicao)

                if len(caminho_jogador) < len(caminho) and nova_posicao == caminho[len(caminho_jogador)]:
                    posicao_personagem = nova_posicao
                    caminho_jogador.append(posicao_personagem)
                else:
                    vidas -= 1
                    exibir_mensagem("Você perdeu", vermelho)
                    if vidas == 0:
                        acao = menu_game_over()
                        if acao == "restart":
                            reiniciar_jogo()
                            jogando = True
                        else:
                            pygame.quit()
                            quit()
                    else:
                        caminho_jogador = [caminho[0]]
                        posicao_personagem = caminho[0]
                        mostrar_caminho(caminho, offset_x, offset_y)

                if len(caminho_jogador) == len(caminho):
                    exibir_mensagem("Você venceu", branco)
                    fase += 1
                    vidas = 3
                    linhas += 1 if fase % 5 == 0 else 0
                    grid_posicoes = atualizar_grid_posicoes(linhas)
                    offset_x, offset_y = calcular_offset_centralizado(linhas, colunas, tam_quadrado)
                    caminho = gerar_caminho_continuo(fase + 1, grid_posicoes)
                    posicao_personagem = caminho[0]
                    caminho_jogador = [posicao_personagem]
                    mostrar_caminho(caminho, offset_x, offset_y)

        pygame.display.flip()
