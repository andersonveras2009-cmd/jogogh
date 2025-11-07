import pygame, sys, random, time, os, wave, struct, math
from gtts import gTTS

pygame.init()
pygame.mixer.init()

# ==================== CONFIGURAÇÕES GERAIS ====================
LARGURA, ALTURA = 800, 600
COR_LARANJA = (255, 102, 0)
COR_BRANCO = (255, 255, 255)
COR_PRETO = (0, 0, 0)
COR_CINZA = (230, 230, 230)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Shopee Simulador")
fonte = pygame.font.SysFont("arial", 24)

# ==================== FUNÇÕES DE SOM ====================
def gerar_som_caixa(nome_arquivo="sons/compra.wav"):
    """Gera um som curto tipo caixa registradora."""
    os.makedirs("sons", exist_ok=True)
    freq = 440.0
    duracao = 0.25
    amostragem = 44100
    nframes = int(duracao * amostragem)
    wav = wave.open(nome_arquivo, 'w')
    wav.setparams((1, 2, amostragem, nframes, 'NONE', 'not compressed'))
    for i in range(nframes):
        valor = int(32767.0 * math.sin(2.0 * math.pi * freq * i / amostragem))
        data = struct.pack('<h', valor)
        wav.writeframesraw(data)
    wav.close()

if not os.path.exists("sons/compra.wav"):
    gerar_som_caixa()

# Carrega sons
som_compra = pygame.mixer.Sound("sons/compra.wav")
voz_compra = pygame.mixer.Sound("sons/voz_compra.wav") if os.path.exists("sons/voz_compra.wav") else None

# ==================== CLASSES ====================
class Produto:
    def __init__(self, nome, preco, imagem):
        self.nome = nome
        self.preco = preco
        self.imagem = pygame.image.load(imagem)
        self.imagem = pygame.transform.scale(self.imagem, (100, 100))

# ==================== DADOS DO JOGO ====================
saldo = 100
produtos = []
for i in range(1, 11):
    nome = f"Produto {i}"
    preco = random.randint(10, 60)
    img = f"imagens/produto{i}.png"
    if not os.path.exists(img):
        pygame.Surface((100, 100)).fill(COR_CINZA)
        os.makedirs("imagens", exist_ok=True)
        superficie = pygame.Surface((100, 100))
        superficie.fill(COR_CINZA)
        pygame.image.save(superficie, img)
    produtos.append(Produto(nome, preco, img))

pedidos = [] # cada pedido: {'produto':nome, 'status':str, 'tempo':time.time()}

# ==================== FUNÇÕES GRÁFICAS ====================
def desenhar_texto(txt, x, y, cor=COR_PRETO, centralizado=False):
    render = fonte.render(txt, True, cor)
    rect = render.get_rect()
    if centralizado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    tela.blit(render, rect)

def botao(texto, x, y, w, h, cor, cor_hover):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()[0]
    cor_final = cor_hover if (x < mouse[0] < x + w and y < mouse[1] < y + h) else cor
    pygame.draw.rect(tela, cor_final, (x, y, w, h), border_radius=12)
    desenhar_texto(texto, x + w // 2, y + h // 2 - 10, COR_BRANCO, True)
    return clique and x < mouse[0] < x + w and y < mouse[1] < y + h

# ==================== TELAS ====================
def menu_principal():
    while True:
        tela.fill(COR_LARANJA)
        desenhar_texto("Shopee Simulador", LARGURA//2, 100, COR_BRANCO, True)
        if botao("Iniciar", 320, 200, 160, 60, COR_PRETO, (50,50,50)):
            tela_loja()
        if botao("Pedidos", 320, 300, 160, 60, COR_PRETO, (50,50,50)):
            tela_pedidos()
        if botao("Sair", 320, 400, 160, 60, COR_PRETO, (50,50,50)):
            pygame.quit(); sys.exit()
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

def tela_loja():
    global saldo
    clock = pygame.time.Clock()
    while True:
        tela.fill(COR_CINZA)
        desenhar_texto(f"Saldo: R$ {saldo}", 20, 20, COR_PRETO)
        desenhar_texto("Clique em um produto para comprar", LARGURA//2, 60, COR_PRETO, True)

        # Mostra produtos
        for i, p in enumerate(produtos):
            x = 80 + (i % 5) * 140
            y = 120 + (i // 5) * 200
            tela.blit(p.imagem, (x, y))
            desenhar_texto(p.nome, x, y + 110)
            desenhar_texto(f"R$ {p.preco}", x, y + 130)
            if botao("Comprar", x, y + 160, 100, 35, COR_LARANJA, (255,128,0)):
                if saldo >= p.preco:
                    saldo -= p.preco
                    som_compra.play()
                    if voz_compra:
                        pygame.time.delay(200)
                        voz_compra.play()
                    pedidos.append({
                        "produto": p.nome,
                        "status": "Pagando",
                        "tempo": time.time()
                    })
                else:
                    print("Saldo insuficiente!")

        # Botão voltar
        if botao("Voltar", 650, 520, 120, 50, COR_PRETO, (50,50,50)):
            return

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(30)

# --- Parte 2 (entregas e barra de progresso) continua abaixo ---
# ==================== TELA DE PEDIDOS (Parte 2) ====================
def tela_pedidos():
    clock = pygame.time.Clock()
    while True:
        tela.fill(COR_BRANCO)
        desenhar_texto("Seus Pedidos", LARGURA//2, 40, COR_LARANJA, True)

        # Atualiza status automaticamente
        tempo_atual = time.time()
        for pedido in pedidos:
            tempo_passado = tempo_atual - pedido["tempo"]
            if pedido["status"] == "Pagando" and tempo_passado > 10:
                pedido["status"] = "A caminho"
                pedido["tempo"] = tempo_atual
            elif pedido["status"] == "A caminho" and tempo_passado > 10:
                pedido["status"] = "Entregue"

        # Exibe cada pedido com barra de progresso
        for i, pedido in enumerate(pedidos):
            y = 100 + i * 80
            pygame.draw.rect(tela, COR_CINZA, (60, y, 680, 60), border_radius=12)
            desenhar_texto(pedido["produto"], 80, y + 10)
            desenhar_texto(pedido["status"], 80, y + 30, COR_LARANJA)

            # Barra de progresso
            barra_x = 300
            barra_y = y + 20
            barra_largura = 400
            barra_altura = 20
            pygame.draw.rect(tela, (200, 200, 200), (barra_x, barra_y, barra_largura, barra_altura), border_radius=10)

            progresso = 0
            if pedido["status"] == "Pagando":
                progresso = (time.time() - pedido["tempo"]) / 10 * 0.33
            elif pedido["status"] == "A caminho":
                progresso = 0.33 + (time.time() - pedido["tempo"]) / 10 * 0.67
            elif pedido["status"] == "Entregue":
                progresso = 1.0

            progresso = min(1.0, progresso)
            pygame.draw.rect(tela, COR_LARANJA,
                             (barra_x, barra_y, int(barra_largura * progresso), barra_altura), border_radius=10)

        # Botão voltar
        if botao("Voltar", 650, 520, 120, 50, COR_PRETO, (50, 50, 50)):
            return

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(30)


# ==================== INICIAR O JOGO ====================
if __name__ == "__main__":
    menu_principal()