import pygame
import random
import sys

pygame.init()

# ---------------- CONFIGURAÇÕES ----------------
LARGURA, ALTURA = 900, 700
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Bingo 2 Jogadores")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (100, 150, 255)
VERDE = (0, 200, 0)
VERMELHO = (255, 0, 0)
CINZA = (230, 230, 230)
CINZA_ESCURO = (180, 180, 180)

# Fontes
FONTE = pygame.font.SysFont("arial", 36)
FONTE_PEQUENA = pygame.font.SysFont("arial", 24)
FONTE_TITULO = pygame.font.SysFont("arial", 60, bold=True)

# ---------------- FUNÇÕES DE JOGO ----------------
def criar_cartela():
    numeros = list(range(1, 76))
    random.shuffle(numeros)
    cartela = []
    for i in range(5):
        linha = []
        for j in range(5):
            if i == 2 and j == 2:
                linha.append("★")
            else:
                linha.append(numeros.pop())
        cartela.append(linha)
    return cartela


def desenhar_cartela(cartela, marcados, x_inicio, y_inicio, titulo):
    tam = 80
    pygame.draw.rect(TELA, CINZA, (x_inicio - 10, y_inicio - 60, tam * 5 + 20, tam * 5 + 100), border_radius=10)
    titulo_texto = FONTE.render(titulo, True, AZUL)
    TELA.blit(titulo_texto, (x_inicio + 60, y_inicio - 50))
    for i in range(5):
        for j in range(5):
            x = x_inicio + j * tam
            y = y_inicio + i * tam
            pygame.draw.rect(TELA, PRETO, (x, y, tam, tam), 2)
            valor = str(cartela[i][j])
            if valor in marcados or valor == "★":
                cor = VERDE
            else:
                cor = PRETO
            texto = FONTE_PEQUENA.render(valor, True, cor)
            TELA.blit(texto, (x + 30, y + 25))


def verificar_bingo(cartela, marcados):
    for linha in cartela:
        if all(str(n) in marcados or n == "★" for n in linha):
            return True
    for c in range(5):
        if all(str(cartela[l][c]) in marcados or cartela[l][c] == "★" for l in range(5)):
            return True
    if all(str(cartela[i][i]) in marcados or cartela[i][i] == "★" for i in range(5)):
        return True
    if all(str(cartela[i][4 - i]) in marcados or cartela[i][4 - i] == "★" for i in range(5)):
        return True
    return False


# ---------------- FUNÇÃO PRINCIPAL ----------------
def jogo():
    cartela1 = criar_cartela()
    cartela2 = criar_cartela()
    marcados = set()
    todos_numeros = list(range(1, 76))
    random.shuffle(todos_numeros)
    proximo_numero = None
    ganhador = None
    relogio = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and ganhador is None:
                    if todos_numeros:
                        proximo_numero = todos_numeros.pop()
                        marcados.add(str(proximo_numero))
                    else:
                        proximo_numero = "Fim"

                if evento.key == pygame.K_r:
                    return "menu"

        TELA.fill(BRANCO)
        desenhar_cartela(cartela1, marcados, 100, 120, "Jogador 1")
        desenhar_cartela(cartela2, marcados, 500, 120, "Jogador 2")

        if proximo_numero:
            texto_num = FONTE.render(f"Número: {proximo_numero}", True, VERMELHO)
            TELA.blit(texto_num, (LARGURA//2 - texto_num.get_width()//2, 600))

        if ganhador is None:
            if verificar_bingo(cartela1, marcados):
                ganhador = "Jogador 1"
            elif verificar_bingo(cartela2, marcados):
                ganhador = "Jogador 2"

        if ganhador:
            texto_vitoria = FONTE.render(f"{ganhador} fez BINGO!", True, VERDE)
            TELA.blit(texto_vitoria, (LARGURA//2 - texto_vitoria.get_width()//2, 550))

        pygame.display.update()
        relogio.tick(30)


# ---------------- TELA DE MENU ----------------
def menu():
    relogio = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Botão Jogar
                if 350 <= mx <= 550 and 300 <= my <= 360:
                    return "jogar"
                # Botão Sair
                if 350 <= mx <= 550 and 400 <= my <= 460:
                    pygame.quit()
                    sys.exit()

        # Fundo
        TELA.fill(BRANCO)
        titulo = FONTE_TITULO.render("🎲 BINGO 🎲", True, AZUL)
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 150))

        # Botões
        mx, my = pygame.mouse.get_pos()
        jogar_cor = CINZA_ESCURO if 350 <= mx <= 550 and 300 <= my <= 360 else CINZA
        sair_cor = CINZA_ESCURO if 350 <= mx <= 550 and 400 <= my <= 460 else CINZA

        pygame.draw.rect(TELA, jogar_cor, (350, 300, 200, 60), border_radius=15)
        pygame.draw.rect(TELA, sair_cor, (350, 400, 200, 60), border_radius=15)

        jogar_txt = FONTE.render("JOGAR", True, PRETO)
        sair_txt = FONTE.render("SAIR", True, PRETO)
        TELA.blit(jogar_txt, (LARGURA//2 - jogar_txt.get_width()//2, 310))
        TELA.blit(sair_txt, (LARGURA//2 - sair_txt.get_width()//2, 410))

        pygame.display.update()
        relogio.tick(30)


# ---------------- LOOP PRINCIPAL ----------------
while True:
    acao = menu()
    if acao == "jogar":
        resultado = jogo()
        if resultado == "menu":
            continue