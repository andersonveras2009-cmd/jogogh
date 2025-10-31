import pygame
import random
import sys

# Inicialização
pygame.init()

# Tela
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario com Seleção de Personagem")
clock = pygame.time.Clock()
FPS = 60

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonte
font = pygame.font.SysFont(None, 36)

# Personagens disponíveis
characters = {
    "Mario": "mario.png",
    "Luigi": "luigi.png",
    "dragão": "dragão.png",
    "Yoshi": "yoshi.png"
}

# Tamanho do personagem
player_width = 50
player_height = 60

# Seleção de personagem
def select_character():
    selected = None
    buttons = []

    # Carregar imagens em miniatura
    thumbnails = {}
    for i, (name, img_file) in enumerate(characters.items()):
        try:
            img = pygame.image.load(img_file)
            img = pygame.transform.scale(img, (player_width, player_height))
            thumbnails[name] = img
        except pygame.error:
            print(f"Erro ao carregar {img_file}")
            pygame.quit()
            sys.exit()

        # Botões (retângulos clicáveis)
        x = 100 + i * 150
        y = HEIGHT // 2
        rect = pygame.Rect(x, y, player_width, player_height)
        buttons.append((name, rect))

    while selected is None:
        screen.fill(WHITE)
        title = font.render("Escolha seu personagem", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 150, 50))

        for name, rect in buttons:
            pygame.draw.rect(screen, GRAY, rect, border_radius=10)
            screen.blit(thumbnails[name], (rect.x, rect.y - 10))
            label = font.render(name, True, BLACK)
            screen.blit(label, (rect.x - 10, rect.y + 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for name, rect in buttons:
                    if rect.collidepoint(mouse_pos):
                        selected = name

        clock.tick(FPS)

    return thumbnails[selected]  # retorna a imagem do personagem

# Inicia com a escolha do personagem
player_image = select_character()

# Variáveis do jogador
player_x = 100
player_y = HEIGHT - player_height - 50
player_vel_y = 0
gravity = 0.8
jump_force = -15
on_ground = True
double_jump_used = False
run_speed = 5

# Obstáculos
obstacles = []
obstacle_timer = 0
obstacle_interval = 1500
obstacle_speed = 5

# Fogo
fireballs = []
fireball_speed = 10
fireball_cooldown = 300
last_fire_time = 0

# Pontuação
score = 0
start_ticks = pygame.time.get_ticks()

# Jogo principal
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Correr
    is_running = keys[pygame.K_LSHIFT]
    player_speed = run_speed * 2 if is_running else run_speed

    # Pulo e pulo duplo
    if keys[pygame.K_SPACE]:
        if on_ground:
            player_vel_y = jump_force
            on_ground = False
            double_jump_used = False
        elif not double_jump_used:
            player_vel_y = jump_force
            double_jump_used = True

    # Bola de fogo
    if keys[pygame.K_f]:
        if current_time - last_fire_time > fireball_cooldown:
            fireball = pygame.Rect(player_x + player_width, player_y + player_height // 2 - 5, 10, 10)
            fireballs.append(fireball)
            last_fire_time = current_time

    # Gravidade
    player_vel_y += gravity
    player_y += player_vel_y

    if player_y >= HEIGHT - player_height - 50:
        player_y = HEIGHT - player_height - 50
        player_vel_y = 0
        on_ground = True
        double_jump_used = False

    # Obstáculos
    if current_time - obstacle_timer > obstacle_interval:
        obstacle_timer = current_time
        height = random.randint(40, 80)
        obs = pygame.Rect(WIDTH, HEIGHT - height - 50, 40, height)
        obstacles.append(obs)

    for obs in obstacles[:]:
        obs.x -= obstacle_speed
        if obs.x < -50:
            obstacles.remove(obs)

    # Fogo
    for fb in fireballs[:]:
        fb.x += fireball_speed
        if fb.x > WIDTH:
            fireballs.remove(fb)

    for fb in fireballs[:]:
        for obs in obstacles[:]:
            if fb.colliderect(obs):
                if fb in fireballs:
                    fireballs.remove(fb)
                if obs in obstacles:
                    obstacles.remove(obs)
                break

    # Colisão com obstáculo
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obs in obstacles:
        if player_rect.colliderect(obs):
            game_over_text = font.render("Game Over! Pontuação: " + str(score), True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

    # Desenho
    screen.blit(player_image, (player_x, player_y))

    for obs in obstacles:
        pygame.draw.rect(screen, GREEN, obs)

    for fb in fireballs:
        pygame.draw.rect(screen, RED, fb)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 50, WIDTH, 50))

    score = (pygame.time.get_ticks() - start_ticks) // 1000
    score_text = font.render("Pontuação: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()

    