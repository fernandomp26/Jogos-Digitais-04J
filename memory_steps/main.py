import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Movimento Controlado com Pygame')

# Carrega as imagens do personagem
person_front = pygame.image.load("./person/person_front.png")
person_left = pygame.image.load("./person/person_left.png")
person_right = pygame.image.load("./person/person_right.png")
person_back = pygame.image.load("./person/person_back.png")

# Redimensiona as imagens do personagem para 70x70 pixels
person_front = pygame.transform.scale(person_front, (70, 70))
person_left = pygame.transform.scale(person_left, (70, 70))
person_right = pygame.transform.scale(person_right, (70, 70))
person_back = pygame.transform.scale(person_back, (70, 70))

# Carrega a imagem de fundo
background = pygame.image.load("./background/background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))  # Redimensiona para caber na tela

# Posição inicial do personagem
x, y = 375, screen_height - 100
current_image = person_front  # Imagem inicial

# Define as variáveis de movimento e direção
moving = False
direction = None

# Definindo a grade de caminhos e o caminho certo
cell_size = 70  # Tamanho de cada quadrado
grid_width = screen_width // cell_size  # Quantidade de quadrados por linha
grid_height = screen_height // cell_size  # Quantidade de quadrados por coluna

# Gera o caminho correto de forma aleatória
correct_path = [(random.randint(0, grid_width - 1), i) for i in range(grid_height)]
path_index = 0

# Controle do jogo
game_active = False  # O jogo começa com o caminho sendo mostrado
win = False
lose = False

# Fonte para as mensagens de vitória e derrota
font = pygame.font.Font(None, 74)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detecta o pressionamento de teclas
        if event.type == pygame.KEYDOWN and game_active and not moving:
            if event.key == pygame.K_UP:
                current_image = person_back
                direction = (0, -cell_size)
                moving = True
            elif event.key == pygame.K_DOWN:
                current_image = person_front
                direction = (0, cell_size)
                moving = True
            elif event.key == pygame.K_LEFT:
                current_image = person_left
                direction = (-cell_size, 0)
                moving = True
            elif event.key == pygame.K_RIGHT:
                current_image = person_right
                direction = (cell_size, 0)
                moving = True

    # Se o personagem estiver se movendo, atualiza a posição
    if moving:
        x += direction[0]
        y += direction[1]
        moving = False  # Para o movimento após o deslocamento

        # Verifica se a posição está no caminho correto
        player_pos = (x // cell_size, y // cell_size)
        if player_pos == correct_path[path_index]:  # Caminho correto
            path_index += 1
            if path_index == len(correct_path):  # Chegou ao final do caminho
                win = True
                game_active = False
        else:  # Caminho incorreto
            lose = True
            game_active = False

    # Desenha o fundo
    screen.blit(background, (0, 0))

    # Mostra o caminho correto se o jogo ainda não começou
    if not game_active and not win and not lose:
        for pos in correct_path:
            pygame.draw.rect(screen, (0, 255, 0), (pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(2000)  # Mostra o caminho por 2 segundos
        game_active = True

    # Desenha o personagem na tela
    screen.blit(current_image, (x, y))

    # Mostra mensagem de vitória ou derrota
    if win:
        message = font.render("Você venceu!", True, (0, 255, 0))
        screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2))
    elif lose:
        message = font.render("Você perdeu!", True, (255, 0, 0))
        screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2))

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()
