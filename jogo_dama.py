import pygame
import sys
import random

# -------------------- CONFIGURAÇÕES GERAIS --------------------
LARGURA, ALTURA = 600, 600
LINHAS, COLUNAS = 8, 8
TAMANHO_QUADRADO = LARGURA // COLUNAS

# Cores suaves e contrastantes
COR_TABULEIRO_ESCURO = (176, 135, 90)
COR_TABULEIRO_CLARO = (240, 220, 200)
COR_PECA_VERMELHA = (220, 70, 70)
COR_PECA_BRANCA = (240, 240, 240)
COR_DESTAQUE = (80, 190, 80)
COR_FUNDO_TEXTO = (240, 240, 240)
COR_TEXTO = (20, 20, 20)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA + 80))
pygame.display.set_caption("Jogo de Damas - Versão Simples")
fonte = pygame.font.SysFont("Arial", 28, bold=True)

# -------------------- CLASSE DAS PEÇAS --------------------
class Peca:
    def __init__(self, linha, coluna, cor):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor
        self.rei = False
        self.atualizar_pos()

    def atualizar_pos(self):
        self.x = self.coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
        self.y = self.linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2

    def tornar_rei(self):
        self.rei = True

    def desenhar(self, tela):
        raio = TAMANHO_QUADRADO // 2 - 10
        pygame.draw.circle(tela, self.cor, (self.x, self.y), raio)
        if self.rei:
            pygame.draw.circle(tela, (255, 215, 0), (self.x, self.y), raio // 2, 4)

# -------------------- CLASSE DO TABULEIRO --------------------
class Tabuleiro:
    def __init__(self):
        self.tabuleiro = []
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        for linha in range(LINHAS):
            self.tabuleiro.append([])
            for coluna in range(COLUNAS):
                if (linha + coluna) % 2 == 1:
                    if linha < 3:
                        self.tabuleiro[linha].append(Peca(linha, coluna, COR_PECA_BRANCA))
                    elif linha > 4:
                        self.tabuleiro[linha].append(Peca(linha, coluna, COR_PECA_VERMELHA))
                    else:
                        self.tabuleiro[linha].append(0)
                else:
                    self.tabuleiro[linha].append(0)

    def desenhar_tabuleiro(self, tela):
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                cor = COR_TABULEIRO_CLARO if (linha + coluna) % 2 == 0 else COR_TABULEIRO_ESCURO
                pygame.draw.rect(
                    tela,
                    cor,
                    (coluna * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO)
                )

    def desenhar(self, tela):
        self.desenhar_tabuleiro(tela)
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peca = self.tabuleiro[linha][coluna]
                if peca != 0:
                    peca.desenhar(tela)

    def get_peca(self, linha, coluna):
        if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:
            return self.tabuleiro[linha][coluna]
        return None

    def mover(self, peca, linha, coluna):
        self.tabuleiro[peca.linha][peca.coluna] = 0
        self.tabuleiro[linha][coluna] = peca
        peca.linha, peca.coluna = linha, coluna
        peca.atualizar_pos()
        # promover a rei
        if peca.cor == COR_PECA_VERMELHA and linha == 0:
            peca.tornar_rei()
        elif peca.cor == COR_PECA_BRANCA and linha == LINHAS - 1:
            peca.tornar_rei()

    def remover(self, pecas):
        for p in pecas:
            self.tabuleiro[p.linha][p.coluna] = 0

    def movimentos_validos(self, peca):
        movimentos = {}
        direcoes = []
        if peca.cor == COR_PECA_VERMELHA or peca.rei:
            direcoes += [(-1, -1), (-1, 1)]
        if peca.cor == COR_PECA_BRANCA or peca.rei:
            direcoes += [(1, -1), (1, 1)]
        for dr, dc in direcoes:
            nova_linha, nova_coluna = peca.linha + dr, peca.coluna + dc
            if 0 <= nova_linha < LINHAS and 0 <= nova_coluna < COLUNAS:
                destino = self.tabuleiro[nova_linha][nova_coluna]
                if destino == 0:
                    movimentos[(nova_linha, nova_coluna)] = []
                elif destino.cor != peca.cor:
                    pular_linha, pular_coluna = nova_linha + dr, nova_coluna + dc
                    if 0 <= pular_linha < LINHAS and 0 <= pular_coluna < COLUNAS:
                        if self.tabuleiro[pular_linha][pular_coluna] == 0:
                            movimentos[(pular_linha, pular_coluna)] = [destino]
        return movimentos

# -------------------- IA SIMPLES --------------------
def jogada_ia(tabuleiro):
    opcoes = []
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            peca = tabuleiro.get_peca(linha, coluna)
            if peca != 0 and peca.cor == COR_PECA_BRANCA:
                moves = tabuleiro.movimentos_validos(peca)
                if moves:
                    opcoes.append((peca, moves))
    if not opcoes:
        return
    peca, moves = random.choice(opcoes)
    destino = random.choice(list(moves.keys()))
    capturadas = moves[destino]
    tabuleiro.mover(peca, destino[0], destino[1])
    if capturadas:
        tabuleiro.remover(capturadas)

# -------------------- INTERFACE --------------------
def desenhar_texto(tela, texto):
    pygame.draw.rect(tela, COR_FUNDO_TEXTO, (0, ALTURA, LARGURA, 80))
    texto_render = fonte.render(texto, True, COR_TEXTO)
    tela.blit(texto_render, (20, ALTURA + 20))

# -------------------- LOOP PRINCIPAL --------------------
def main():
    tabuleiro = Tabuleiro()
    turno = COR_PECA_VERMELHA
    selecionada = None
    movimentos = {}
    jogando_contra_pc = True
    rodando = True

    while rodando:
        tela.fill((0, 0, 0))
        tabuleiro.desenhar(tela)
        desenhar_texto(tela, "Sua vez!" if turno == COR_PECA_VERMELHA else "Computador jogando...")

        # Turno do computador
        if jogando_contra_pc and turno == COR_PECA_BRANCA:
            pygame.time.wait(700)
            jogada_ia(tabuleiro)
            turno = COR_PECA_VERMELHA

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and turno == COR_PECA_VERMELHA:
                x, y = pygame.mouse.get_pos()
                if y < ALTURA: # evita clicar na área de texto
                    linha = y // TAMANHO_QUADRADO
                    coluna = x // TAMANHO_QUADRADO
                    if selecionada:
                        if (linha, coluna) in movimentos:
                            capturadas = movimentos[(linha, coluna)]
                            tabuleiro.mover(selecionada, linha, coluna)
                            if capturadas:
                                tabuleiro.remover(capturadas)
                            selecionada = None
                            movimentos = {}
                            turno = COR_PECA_BRANCA
                        else:
                            selecionada = None
                            movimentos = {}
                    else:
                        peca = tabuleiro.get_peca(linha, coluna)
                        if peca != 0 and peca.cor == turno:
                            selecionada = peca
                            movimentos = tabuleiro.movimentos_validos(peca)

        # Mostra os movimentos possíveis
        if selecionada:
            for (r, c) in movimentos.keys():
                pygame.draw.circle(
                    tela,
                    COR_DESTAQUE,
                    (c * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, r * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2),
                    12
                )

        pygame.display.flip()

# -------------------- EXECUTAR --------------------
if __name__ == "__main__":
    main()  