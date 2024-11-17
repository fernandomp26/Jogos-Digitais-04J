import pygame
import random
import time

# Configurações básicas
pygame.init()
largura_tela, altura_tela = 600, 600  # Aumenta o tamanho da tela
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
tam_quadrado = 80  # Tamanho dos quadrados do grid

# Carregar imagens de fundo e personagem em diferentes direções
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

# Inicializar o personagem para frente
current_character = character_front

# Carregar ícone de vida e aumentar para 60x60 pixels
vida_icon = pygame.image.load('./assets/heart.png')
vida_icon = pygame.transform.scale(vida_icon, (60, 60))

# Calcular o deslocamento para centralizar o personagem dentro de um quadrado
character_offset_x = (tam_quadrado - character_front.get_width()) // 2
character_offset_y = (tam_quadrado - character_front.get_height()) // 2

# Função para calcular a posição centralizada do grid
def calcular_offset_centralizado(linhas, colunas, tam_quadrado):
    offset_x = (largura_tela - (colunas * tam_quadrado)) // 2
    offset_y = (altura_tela - (linhas * tam_quadrado)) // 2
    return offset_x, offset_y

# Função para desenhar o grid centralizado
def desenhar_grid(linhas, offset_x, offset_y):
    for y in range(linhas):
        for x in range(colunas):
            pygame.draw.rect(
                tela, verde,
                (offset_x + x * tam_quadrado, offset_y + y * tam_quadrado, tam_quadrado, tam_quadrado), 1
            )

# Função para atualizar as posições do grid com base nas linhas e colunas atuais
def atualizar_grid_posicoes(linhas):
    return [(x, y) for y in range(linhas) for x in range(colunas)]

# Função para criar um caminho contínuo no grid
def gerar_caminho_continuo(tamanho, grid_posicoes):
    caminho = [random.choice(grid_posicoes)]
    while len(caminho) < tamanho:
        x, y = caminho[-1]
        vizinhos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        vizinhos = [v for v in vizinhos if v in grid_posicoes and v not in caminho]
        if vizinhos:
            caminho.append(random.choice(vizinhos))
        else:
            caminho = [random.choice(grid_posicoes)]  # Reinicia se não houver vizinhos disponíveis
    return caminho

# Função para mostrar o caminho para o jogador
def mostrar_caminho(caminho, offset_x, offset_y):
    for posicao in caminho:
        pygame.draw.rect(
            tela, azul,
            (offset_x + posicao[0] * tam_quadrado, offset_y + posicao[1] * tam_quadrado, tam_quadrado, tam_quadrado)
        )
        pygame.display.flip()
        time.sleep(0.5)  # Tempo para memorizar cada quadrado
        tela.blit(background_image, (0, 0))  # Redesenha o fundo
        desenhar_grid(linhas, offset_x, offset_y)
    pygame.display.flip()

# Função para desenhar o HUD com as vidas
def desenhar_hud(fase, vidas):
    # Desenhar fase
    fonte_fase = pygame.font.SysFont(None, 36)
    texto_fase = fonte_fase.render(f"Fase: {fase}", True, branco)
    tela.blit(texto_fase, (10, 10))
    
    # Desenhar vidas com ícones de coração aumentados
    for i in range(vidas):
        tela.blit(vida_icon, (largura_tela - (i + 1) * 65, 10))  # Espaçamento ajustado para corações maiores

# Função para exibir a tela de reinício com opções de S/N
def mostrar_tela_reinicio():
    tela.fill(preto)
    mensagem = "Você perdeu todas as vidas. Deseja recomeçar?"
    texto = pygame.font.SysFont(None, 36).render(mensagem, True, branco)
    tela.blit(texto, (largura_tela // 10, altura_tela // 2 - 30))
    
    # Opções S/N para o jogador
    texto_sim = pygame.font.SysFont(None, 36).render("S - Sim", True, branco)
    texto_nao = pygame.font.SysFont(None, 36).render("N - Não", True, branco)
    tela.blit(texto_sim, (largura_tela // 10, altura_tela // 2 + 10))
    tela.blit(texto_nao, (largura_tela // 10, altura_tela // 2 + 50))
    
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Reiniciar o jogo
                    return True
                elif event.key == pygame.K_n:  # Sair do jogo
                    return False

# Função para reiniciar o jogo
def reiniciar_jogo():
    global fase, vidas, linhas, grid_posicoes, offset_x, offset_y, caminho, posicao_personagem, caminho_jogador
    fase = 1
    vidas = 3
    linhas = linhas_iniciais
    grid_posicoes = atualizar_grid_posicoes(linhas)
    offset_x, offset_y = calcular_offset_centralizado(linhas, colunas, tam_quadrado)
    caminho = gerar_caminho_continuo(fase + 2, grid_posicoes)  # Gerar um novo caminho
    posicao_personagem = caminho[0]
    caminho_jogador = [posicao_personagem]
    mostrar_caminho(caminho, offset_x, offset_y)

# Parâmetros do jogo
fase = 1
linhas = linhas_iniciais
vidas = 3  # Vidas iniciais
grid_posicoes = atualizar_grid_posicoes(linhas)
offset_x, offset_y = calcular_offset_centralizado(linhas, colunas, tam_quadrado)
caminho = gerar_caminho_continuo(fase + 2, grid_posicoes)  # Caminho inicial com dificuldade crescente

# Posição inicial do personagem
posicao_personagem = caminho[0]
caminho_jogador = [posicao_personagem]

# Loop principal
jogando = True
mostrar_caminho(caminho, offset_x, offset_y)  # Mostra o caminho no início

while jogando:
    tela.blit(background_image, (0, 0))  # Desenha o fundo
    desenhar_grid(linhas, offset_x, offset_y)

    # Exibir HUD com fase e vidas
    desenhar_hud(fase, vidas)

    # Desenha o personagem centralizado no quadrado atual
    tela.blit(
        current_character,
        (offset_x + posicao_personagem[0] * tam_quadrado + character_offset_x,
         offset_y + posicao_personagem[1] * tam_quadrado + character_offset_y)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False
        elif event.type == pygame.KEYDOWN:
            # Movimentos do jogador e atualização da direção do personagem
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

            # Verifica se o movimento é correto no caminho
            if len(caminho_jogador) < len(caminho) and nova_posicao == caminho[len(caminho_jogador)]:
                posicao_personagem = nova_posicao
                caminho_jogador.append(posicao_personagem)
            else:
                # Se o jogador erra o caminho, perde uma vida
                vidas -= 1
                if vidas == 0:
                    # Tela de reinício
                    if mostrar_tela_reinicio():
                        reiniciar_jogo()
                    else:
                        jogando = False
                else:
                    # Mensagem de tentativa perdida
                    tela.fill(preto)
                    mensagem = "Você errou"
                    texto = pygame.font.SysFont(None, 55).render(mensagem, True, vermelho)
                    tela.blit(texto, (largura_tela // 4, altura_tela // 2))
                    pygame.display.flip()
                    time.sleep(2)
                # Reinicia a posição inicial para tentar novamente a fase
                caminho_jogador = [caminho[0]]
                posicao_personagem = caminho[0]
                mostrar_caminho(caminho, offset_x, offset_y)

            # Verifica se o jogador completou o caminho com sucesso
            if len(caminho_jogador) == len(caminho):
                tela.fill(preto)
                mensagem = "Você venceu"
                texto = pygame.font.SysFont(None, 55).render(mensagem, True, branco)
                tela.blit(texto, (largura_tela // 4, altura_tela // 2))
                pygame.display.flip()
                time.sleep(2)
                fase += 1
                vidas = 3  # Reseta as vidas ao passar de fase

                # A cada 5 fases, aumenta o tamanho do grid
                if fase % 5 == 1 and fase > 1:
                    linhas += 1
                    grid_posicoes = atualizar_grid_posicoes(linhas)
                    offset_x, offset_y = calcular_offset_centralizado(linhas, colunas, tam_quadrado)

                caminho = gerar_caminho_continuo(fase + 2, grid_posicoes)  # Caminho mais difícil
                posicao_personagem = caminho[0]
                caminho_jogador = [posicao_personagem]
                mostrar_caminho(caminho, offset_x, offset_y)

    pygame.display.flip()

pygame.quit()
