import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Movimento Controlado com Pygame')

# Carrega as imagens do personagem
person_front = pygame.image.load("person_front.png")
person_left = pygame.image.load("person_left.png")
person_right = pygame.image.load("person_right.png")
person_back = pygame.image.load("person_back.png")

# Redimensiona as imagens do personagem para 50x50 pixels
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

# Estados de movimento
moving = False
direction = None

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detecta o pressionamento de teclas
        if event.type == pygame.KEYDOWN and not moving:
            if event.key == pygame.K_UP:
                current_image = person_back
                direction = (0, -70)
                moving = True
            elif event.key == pygame.K_DOWN:
                current_image = person_front
                direction = (0, 70)
                moving = True
            elif event.key == pygame.K_LEFT:
                current_image = person_left
                direction = (-70, 0)
                moving = True
            elif event.key == pygame.K_RIGHT:
                current_image = person_right
                direction = (70, 0)
                moving = True

    # Se o boneco estiver se movendo, atualiza a posição
    if moving:
        x += direction[0]
        y += direction[1]
        moving = False  # Para o movimento após 1 pixel

    # Desenha o fundo
    screen.blit(background, (0, 0))

    # Desenha a imagem atual do personagem na tela
    screen.blit(current_image, (x, y))

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()
