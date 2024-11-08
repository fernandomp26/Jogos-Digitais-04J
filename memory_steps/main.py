import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela e das células
screen_width = 800
screen_height = 600
cell_size = 70  # Tamanho de cada célula
cell_spacing = 20  # Espaçamento entre as células
columns = 3  # Número de células por linha
rows = screen_height // (cell_size + cell_spacing)  # Número de células ajustado para espaçamento

# Configura a tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Caminho Correto - Pygame')

# Cores
green = (0, 255, 0)  # Cor do caminho correto no início
gray = (169, 169, 169)  # Cor para ocultar o caminho após o tempo de memorização

# Carrega a imagem de fundo principal
background = pygame.image.load("./background/background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Carrega as imagens do personagem
person_front = pygame.image.load("./person/person_front.png")
person_front = pygame.transform.scale(person_front, (cell_size, cell_size))

# Posição inicial do personagem (na parte inferior da tela, fora do grid, centralizado na coluna do meio)
x, y = screen_width // 2 - cell_size // 2, screen_height - cell_size - 20
current_image = person_front  # Imagem inicial

# Centraliza o grid horizontalmente
start_x = (screen_width - (columns * cell_size + (columns - 1) * cell_spacing)) // 2

# Define os três caminhos possíveis, cada um com um conjunto fixo de posições
path1 = [(start_x, screen_height - (i * (cell_size + cell_spacing))) for i in range(1, 6, 2)]
path2 = [(start_x + cell_size + cell_spacing, screen_height - (i * (cell_size + cell_spacing))) for i in range(2, 6, 2)]
path3 = [(start_x + 2 * (cell_size + cell_spacing), screen_height - (i * (cell_size + cell_spacing))) for i in range(1, 6, 2)]

# Combina todos os caminhos para memorização
all_paths = path1 + path2 + path3

# Controle do jogo
game_active = False
win = False
lose = False
show_path = True  # Mostra os caminhos no início

# Fonte para mensagens
font = pygame.font.Font(None, 74)

# Função para desenhar o grid com os caminhos em verde
def draw_grid(show_correct_path=False):
    for row in range(rows):
        for col in range(columns):
            x_pos = start_x + col * (cell_size + cell_spacing)
            y_pos = row * (cell_size + cell_spacing)
            # Mostra os caminhos possíveis em verde no início, depois todos em cinza
            color = green if show_correct_path and (x_pos, y_pos) in all_paths else gray
            pygame.draw.rect(screen, color, (x_pos, y_pos, cell_size, cell_size))

# Loop principal
running = True
show_timer = 5000  # Tempo para mostrar os caminhos corretos (5 segundos)
start_ticks = pygame.time.get_ticks()  # Marca o tempo inicial

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detecta o pressionamento de teclas
        if event.type == pygame.KEYDOWN and game_active and not win and not lose:
            if event.key == pygame.K_UP:
                y -= cell_size + cell_spacing
            elif event.key == pygame.K_LEFT:
                x -= cell_size + cell_spacing
            elif event.key == pygame.K_RIGHT:
                x += cell_size + cell_spacing

            # Limita o movimento para dentro do grid
            x = max(start_x, min(x, start_x + (columns - 1) * (cell_size + cell_spacing)))
            y = max(0, min(y, (rows - 1) * (cell_size + cell_spacing)))

            # Verifica se a posição atual está no caminho correto
            player_pos = (x, y)
            if player_pos in all_paths:
                if player_pos == all_paths[-1]:  # Chegou ao final do caminho
                    win = True
                    game_active = False
            else:
                lose = True
                game_active = False

    # Desenha o fundo principal
    screen.blit(background, (0, 0))

    # Mostra o caminho correto por um tempo e depois oculta
    if show_path:
        draw_grid(show_correct_path=True)
        if pygame.time.get_ticks() - start_ticks > show_timer:  # Oculta o caminho após o tempo
            show_path = False
            game_active = True
    else:
        draw_grid(show_correct_path=False)

    # Desenha o personagem na tela
    screen.blit(current_image, (x, y))

    # Mostra mensagem de vitória ou derrota
    if win:
        message = font.render("Você venceu!", True, green)
        screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2))
    elif lose:
        message = font.render("Você perdeu!", True, (255, 0, 0))
        screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2))

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()
