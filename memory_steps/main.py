import pygame
import random
import time

# Configurações básicas
pygame.init()
largura_tela, altura_tela = 600, 700  # Altura aumentada para incluir o menu fixo
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

def redimensionar_imagem(imagem, tam_quadrado):
    largura_original, altura_original = imagem.get_size()
    escala = min((tam_quadrado - 10) / largura_original, (tam_quadrado - 10) / altura_original)
    nova_largura = int(largura_original * escala)
    nova_altura = int(altura_original * escala)
    return pygame.transform.scale(imagem, (nova_largura, nova_altura))

character_front = pygame.image.load('./person/masculino/frente_masculino.png')
character_back = pygame.image.load('./person/masculino/costas_masculino.png')
character_left = pygame.image.load('./person/masculino/lado_esquerdo_masculino.png')
character_right = pygame.image.load('./person/masculino/lado_direito_masculino.png')
# Redimensionar as imagens do personagem proporcionalmente
character_front = redimensionar_imagem(character_front, tam_quadrado)
character_back = redimensionar_imagem(character_back, tam_quadrado)
character_left = redimensionar_imagem(character_left, tam_quadrado)
character_right = redimensionar_imagem(character_right, tam_quadrado)

vida_icon = pygame.image.load('./assets/heart.png')
vida_icon = pygame.transform.scale(vida_icon, (40, 40))

current_character = character_front
character_offset_x = (tam_quadrado - character_front.get_width()) // 2
character_offset_y = (tam_quadrado - character_front.get_height()) // 2

background_image = pygame.image.load('./background/background.jpg')
background_image = pygame.transform.scale(background_image, (largura_tela, altura_tela - 100))

# Funções auxiliares
def calcular_offset_centralizado(linhas, colunas, tam_quadrado):
    offset_x = (largura_tela - (colunas * tam_quadrado)) // 2
    offset_y = ((altura_tela - 100) - (linhas * tam_quadrado)) // 2
    return offset_x, offset_y

def desenhar_grid(linhas, offset_x, offset_y):
    for y in range(linhas):
        for x in range(colunas):
            pygame.draw.rect(
                tela, preto,
                (offset_x + x * tam_quadrado, offset_y + y * tam_quadrado, tam_quadrado, tam_quadrado), 3
            )

def atualizar_grid_posicoes(linhas):
    return [(x, y) for y in range(linhas) for x in range(colunas)]

def gerar_caminho_continuo(tamanho, grid_posicoes):
    caminho = [random.choice(grid_posicoes)]
    while len(caminho) < tamanho:
        x, y = caminho[-1]
        vizinhos = [(x+1, y), (x-1, y), (x, y+1), (x-1, y)]
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
        desenhar_grid(len(caminho), offset_x, offset_y)
    pygame.display.flip()

def desenhar_hud(fase, vidas):
    fonte = pygame.font.SysFont(None, 36)
    texto_fase = fonte.render(f"Fase: {fase}", True, branco, preto)
    tela.blit(texto_fase, (10, 10))
    for i in range(vidas):
        tela.blit(vida_icon, (largura_tela - (i + 1) * 50, 10))

def desenhar_menu():
    """
    Desenha o menu fixo na parte inferior da tela com as opções "R - Reiniciar" e "Q - Sair".
    """
    fonte = pygame.font.SysFont(None, 36)
    pygame.draw.rect(tela, preto, (0, altura_tela - 100, largura_tela, 100))
    texto_reiniciar = fonte.render("R - Reiniciar", True, branco)
    texto_sair = fonte.render("Q - Sair", True, branco)
    tela.blit(texto_reiniciar, (10, altura_tela - 60))
    tela.blit(texto_sair, (300, altura_tela - 60))

def exibir_mensagem(mensagem, cor):
    """
    Exibe uma mensagem no centro da tela com o fundo completamente preto.
    """
    tela.fill(preto)
    fonte = pygame.font.SysFont(None, 55)
    texto = fonte.render(mensagem, True, cor)
    tela.blit(texto, (largura_tela // 4, altura_tela // 2))
    pygame.display.flip()
    time.sleep(2)

def exibir_menu_game_over():
    """
    Exibe o menu de Game Over com as opções "Reiniciar Jogo" ou "Sair do Jogo".
    """
    while True:
        tela.fill(preto)
        fonte = pygame.font.SysFont(None, 48)
        texto_reiniciar = fonte.render("1. Reiniciar Jogo", True, branco)
        texto_sair = fonte.render("2. Sair do Jogo", True, branco)
        tela.blit(texto_reiniciar, (largura_tela // 4, altura_tela // 3))
        tela.blit(texto_sair, (largura_tela // 4, altura_tela // 3 + 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "restart"
                elif event.key == pygame.K_2:
                    return "exit"

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

# Parâmetros do jogo
fase = 1
linhas = linhas_iniciais
vidas = 3
grid_posicoes = atualizar_grid_posicoes(linhas)
offset_x, offset_y = calcular_offset_centralizado(linhas, colunas, tam_quadrado)
caminho = gerar_caminho_continuo(fase + 1, grid_posicoes)
posicao_personagem = caminho[0]
caminho_jogador = [posicao_personagem]

# Exibir o caminho antes de iniciar o loop principal
mostrar_caminho(caminho, offset_x, offset_y)

# Loop principal
jogando = True
while jogando:
    tela.fill(preto)
    tela.blit(background_image, (0, 0))
    desenhar_grid(linhas, offset_x, offset_y)
    desenhar_hud(fase, vidas)
    desenhar_menu()

    tela.blit(
        current_character,
        (offset_x + posicao_personagem[0] * tam_quadrado + character_offset_x,
         offset_y + posicao_personagem[1] * tam_quadrado + character_offset_y)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reiniciar o jogo
                exibir_mensagem("Reiniciando o jogo...", branco)
                reiniciar_jogo()
            elif event.key == pygame.K_q:  # Sair do jogo
                jogando = False
            elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
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
                        escolha = exibir_menu_game_over()
                        if escolha == "restart":
                            exibir_mensagem("Reiniciando o jogo...", branco)
                            reiniciar_jogo()
                        else:
                            jogando = False
                    else:
                        caminho_jogador = [caminho[0]]
                        posicao_personagem = caminho[0]
                        mostrar_caminho(caminho, offset_x, offset_y)

                if len(caminho_jogador) == len(caminho):
                    if fase == 0:
                        exibir_mensagem("Parabéns, você zerou o jogo!", branco)
                        jogando = False
                        break
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

pygame.quit()
