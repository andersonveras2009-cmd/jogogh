"""
App em Pygame: Relógio completo (digital + analógico + alarme + cronômetro + temporizador)
- Menu principal com 5 opções
- Relógio digital
- Relógio analógico com ponteiros estilizados
- Alarme (usuário define hora:minuto)
- Cronômetro (iniciar/pausar/resetar)
- Temporizador (definir minutos/segundos e contagem regressiva)
- Sons externos (ex: alarme.wav, beep.wav) devem estar na mesma pasta

Requisitos: pygame
Instalação: pip install pygame
Salvar como: pygames_clock_app.py
Executar: python pygames_clock_app.py
"""

import pygame
import sys
import math
from datetime import datetime, timedelta

# Inicialização
pygame.init()
pygame.mixer.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Relógio - Pygame')
CLOCK = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 30, 30)
BLUE = (40, 120, 200)
GREEN = (30, 200, 30)

# Sons externos
try:
    ALARM_SOUND = pygame.mixer.Sound("alarme.wav")
    BEEP_SOUND = pygame.mixer.Sound("beep.wav")
except Exception:
    ALARM_SOUND = None
    BEEP_SOUND = None

# Fonte
def load_font(size=24):
    return pygame.font.SysFont(None, size)

# Desenha texto
def draw_text(surface, text, size, pos, color=WHITE, center=True):
    font = load_font(size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(rendered, rect)

# Gradiente de fundo
def draw_gradient(surface, top_color, bottom_color):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1-ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1-ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1-ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

# Menu

def main_menu():
    selected = 0
    options = ['Relógio Digital', 'Relógio Analógico', 'Alarme', 'Cronômetro', 'Temporizador', 'Sair']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return selected

        draw_gradient(SCREEN, (10, 10, 30), (30, 30, 90))
        draw_text(SCREEN, 'Relógio Pygame', 64, (WIDTH//2, HEIGHT//6))
        for i, opt in enumerate(options):
            color = GREEN if i == selected else WHITE
            draw_text(SCREEN, opt, 36, (WIDTH//2, HEIGHT//2 + i*50), color)
        draw_text(SCREEN, 'Use ↑ ↓ e ENTER para selecionar', 20, (WIDTH//2, HEIGHT - 40))

        pygame.display.flip()
        CLOCK.tick(FPS)

# Relógio Digital
def digital_clock_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        now = datetime.now()
        draw_gradient(SCREEN, (0, 0, 40), (0, 40, 120))
        draw_text(SCREEN, 'Relógio Digital', 36, (WIDTH//2, 60))
        draw_text(SCREEN, now.strftime('%H:%M:%S'), 90, (WIDTH//2, HEIGHT//2))
        draw_text(SCREEN, now.strftime('%A, %d %B %Y'), 28, (WIDTH//2, HEIGHT//2 + 80))
        draw_text(SCREEN, 'ESC para voltar', 20, (WIDTH//2, HEIGHT - 30))
        pygame.display.flip()
        CLOCK.tick(FPS)

# Conversão polar
def polar_to_cartesian(center, length, angle_deg):
    angle_rad = math.radians(angle_deg - 90)
    x = center[0] + length * math.cos(angle_rad)
    y = center[1] + length * math.sin(angle_rad)
    return (int(x), int(y))

# Relógio Analógico
def analog_clock_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        now = datetime.now()
        h, m, s = now.hour % 12, now.minute, now.second
        micro = now.microsecond
        s_ang = (s + micro/1_000_000)*6
        m_ang = (m + s/60)*6
        h_ang = (h + m/60)*30

        draw_gradient(SCREEN, (10, 10, 30), (50, 50, 100))
        draw_text(SCREEN, 'Relógio Analógico', 36, (WIDTH//2, 40))

        pygame.draw.circle(SCREEN, WHITE, CENTER, RADIUS, 6)
        pygame.draw.circle(SCREEN, BLACK, CENTER, RADIUS-6)

        for hr in range(12):
            ang = hr*30
            start = polar_to_cartesian(CENTER, RADIUS-10, ang)
            end = polar_to_cartesian(CENTER, RADIUS-30, ang)
            pygame.draw.line(SCREEN, WHITE, start, end, 4)

        pygame.draw.line(SCREEN, BLUE, CENTER, polar_to_cartesian(CENTER, RADIUS*0.5, h_ang), 8)
        pygame.draw.line(SCREEN, GREEN, CENTER, polar_to_cartesian(CENTER, RADIUS*0.75, m_ang), 6)
        pygame.draw.line(SCREEN, RED, CENTER, polar_to_cartesian(CENTER, RADIUS*0.9, s_ang), 2)

        pygame.draw.circle(SCREEN, WHITE, CENTER, 8)
        pygame.draw.circle(SCREEN, BLACK, CENTER, 5)

        draw_text(SCREEN, now.strftime('%H:%M:%S'), 28, (WIDTH//2, HEIGHT - 40))
        draw_text(SCREEN, 'ESC para voltar', 20, (WIDTH//2, HEIGHT - 20))
        pygame.display.flip()
        CLOCK.tick(FPS)

# Alarme
def alarm_loop():
    hour, minute = 7, 0
    setting = True
    alarm_active = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if ALARM_SOUND:
                        ALARM_SOUND.stop()
                    return
                if setting:
                    if event.key == pygame.K_UP:
                        minute = (minute + 1) % 60
                    if event.key == pygame.K_DOWN:
                        minute = (minute - 1) % 60
                    if event.key == pygame.K_RIGHT:
                        hour = (hour + 1) % 24
                    if event.key == pygame.K_LEFT:
                        hour = (hour - 1) % 24
                    if event.key == pygame.K_RETURN:
                        setting = False

        draw_gradient(SCREEN, (30, 0, 0), (80, 0, 0))
        draw_text(SCREEN, 'Alarme', 48, (WIDTH//2, 60))

        if setting:
            draw_text(SCREEN, f'Defina Hora: {hour:02d}:{minute:02d}', 40, (WIDTH//2, HEIGHT//2))
            draw_text(SCREEN, 'Setas ← → hora | ↑ ↓ minuto | ENTER confirma | ESC volta', 20, (WIDTH//2, HEIGHT - 40))
        else:
            now = datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if now >= alarm_time and not alarm_active:
                alarm_active = True
                if ALARM_SOUND:
                    ALARM_SOUND.play(-1)  # Loop infinito até ESC

            draw_text(SCREEN, f'Alarme definido: {hour:02d}:{minute:02d}', 40, (WIDTH//2, HEIGHT//2))
            if alarm_active:
                draw_text(SCREEN, '⏰ TOCANDO! Pressione ESC para sair', 30, (WIDTH//2, HEIGHT//2 + 60), RED)

        pygame.display.flip()
        CLOCK.tick(FPS)

# Cronômetro
def stopwatch_loop():
    start_time = None
    running = False
    elapsed = timedelta(0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    if not running:
                        start_time = datetime.now() - elapsed
                        running = True
                    else:
                        elapsed = datetime.now() - start_time
                        running = False
                if event.key == pygame.K_r:
                    elapsed = timedelta(0)
                    start_time = None
                    running = False

        if running:
            elapsed = datetime.now() - start_time

        draw_gradient(SCREEN, (0, 30, 0), (0, 80, 0))
        draw_text(SCREEN, 'Cronômetro', 48, (WIDTH//2, 60))
        draw_text(SCREEN, str(elapsed).split('.')[0], 64, (WIDTH//2, HEIGHT//2))
        draw_text(SCREEN, 'SPACE Inicia/Pausa | R Reseta | ESC Volta', 24, (WIDTH//2, HEIGHT - 40))

        pygame.display.flip()
        CLOCK.tick(FPS)

# Temporizador
def timer_loop():
    minutes, seconds = 0, 10
    setting = True
    running = False
    end_time = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if ALARM_SOUND:
                        ALARM_SOUND.stop()
                    return
                if setting:
                    if event.key == pygame.K_UP:
                        seconds = (seconds + 1) % 60
                    if event.key == pygame.K_DOWN:
                        seconds = (seconds - 1) % 60
                    if event.key == pygame.K_RIGHT:
                        minutes = (minutes + 1) % 60
                    if event.key == pygame.K_LEFT:
                        minutes = (minutes - 1) % 60
                    if event.key == pygame.K_RETURN:
                        setting = False
                        running = True
                        end_time = datetime.now() + timedelta(minutes=minutes, seconds=seconds)

        draw_gradient(SCREEN, (30, 30, 0), (80, 80, 0))
        draw_text(SCREEN, 'Temporizador', 48, (WIDTH//2, 60))

        if setting:
            draw_text(SCREEN, f'Defina: {minutes:02d}:{seconds:02d}', 40, (WIDTH//2, HEIGHT//2))
            draw_text(SCREEN, '← → Minutos | ↑ ↓ Segundos | ENTER Confirma | ESC Volta', 20, (WIDTH//2, HEIGHT - 40))
        else:
            remaining = end_time - datetime.now()
            if remaining.total_seconds() <= 0:
                draw_text(SCREEN, '⏰ TEMPO ESGOTADO!', 40, (WIDTH//2, HEIGHT//2), RED)
                if ALARM_SOUND:
                    ALARM_SOUND.play(-1)  # Loop até sair
            else:
                draw_text(SCREEN, str(remaining).split('.')[0], 64, (WIDTH//2, HEIGHT//2))

        pygame.display.flip()
        CLOCK.tick(FPS)

# Main Loop
def main():
    while True:
        choice = main_menu()
        if choice == 0:
            digital_clock_loop()
        elif choice == 1:
            analog_clock_loop()
        elif choice == 2:
            alarm_loop()
        elif choice == 3:
            stopwatch_loop()
        elif choice == 4:
            timer_loop()
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
