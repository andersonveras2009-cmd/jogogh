
import pygame
import sys

pygame.init()
pygame.display.set_caption("Calculadora de Troco")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 120, 250)
CINZA_ESCURO = (160, 160, 160)

# Tela
tela = pygame.display.set_mode((420, 350))
fonte = pygame.font.Font(None, 36)

# Variáveis
valor_total = ""
valor_pago = ""
troco = ""
campo_ativo = "total"
mensagem_erro = ""

# Função desenhar texto
def desenhar_texto(texto, x, y, cor=PRETO):
    tela.blit(fonte.render(texto, True, cor), (x, y))

# Função botão
def botao(texto, x, y, largura, altura, cor_normal, cor_hover, acao=None):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    cor = cor_hover if (x < mouse[0] < x + largura and y < mouse[1] < y + altura) else cor_normal
    pygame.draw.rect(tela, cor, (x, y, largura, altura), border_radius=10)
    desenhar_texto(texto, x + 10, y + 10)

    if clique[0] == 1 and x < mouse[0] < x + largura and y < mouse[1] < y + altura:
        if acao:
            acao()
# Funções principais
def calcular_troco():
    global troco, mensagem_erro
    try:
        total = float(valor_total.replace(',', '.'))
        pago = float(valor_pago.replace(',', '.'))
        troco_valor = pago - total
        troco = f"R$ {troco_valor:.2f}"
        mensagem_erro = ""
    except:
        troco = ""
        mensagem_erro = "Erro: digite valores válidos!"

def limpar_campos():
    global valor_total, valor_pago, troco, mensagem_erro
    valor_total = ""
    valor_pago = ""
    troco = ""
    mensagem_erro = ""

# Loop principal
rodando = True
while rodando:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            if 220 < x < 370 and 35 < y < 75:
                campo_ativo = "total"
            elif 220 < x < 370 and 95 < y < 135:
                campo_ativo = "pago"

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False

            elif evento.key == pygame.K_BACKSPACE:
                if campo_ativo == "total":
                    valor_total = valor_total[:-1]
                else:
                    valor_pago = valor_pago[:-1]

            elif evento.unicode.isdigit() or evento.unicode in [',', '.']:
                if campo_ativo == "total":
                    valor_total += evento.unicode
                else:
                    valor_pago += evento.unicode

    # Desenhar interface
    desenhar_texto("Valor Total (R$):", 20, 40)
    pygame.draw.rect(tela, CINZA if campo_ativo == "total" else CINZA_ESCURO, (220, 35, 150, 40), border_radius=8)
    desenhar_texto(valor_total, 230, 45)

    desenhar_texto("Valor Pago (R$):", 20, 100)
    pygame.draw.rect(tela, CINZA if campo_ativo == "pago" else CINZA_ESCURO, (220, 95, 150, 40), border_radius=8)
    desenhar_texto(valor_pago, 230, 105)

    # Botões
    botao("Calcular Troco", 40, 170, 150, 50, AZUL, VERDE, calcular_troco)
    botao("Limpar", 220, 170, 150, 50, CINZA_ESCURO, CINZA, limpar_campos)

    # Resultado
    if troco:
        desenhar_texto(f"Troco: {troco}", 40, 250, VERDE)
    elif mensagem_erro:
        desenhar_texto(mensagem_erro, 40, 250, VERMELHO)

    pygame.display.flip()
