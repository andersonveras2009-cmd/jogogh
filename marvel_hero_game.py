import pygame
import random
import os

# Inicialização
pygame.init()

# Tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Marvel Heroes no Espaço")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Fonte e Clock
fonte = pygame.font.SysFont("arial", 30)
clock = pygame.time.Clock()

# Caminho da pasta de imagens
CAMINHO_IMAGENS = "imagens"

# Heróis disponíveis (10)
HERÓIS = {
    "Homem de Ferro": {"arquivo": "homem_ferro.png"},
    "Capitão América": {"arquivo": "capitao_america.png"},
    "Thor": {"arquivo": "thor.png"},
    "Hulk": {"arquivo": "hulk.png"},
    "Viúva Negra": {"arquivo": "viuva_negra.png"},
    "Gavião Arqueiro": {"arquivo": "gaviao_arqueiro.png"},
    "Pantera Negra": {"arquivo": "pantera_negra.png"},
    "Homem-Aranha": {"arquivo": "homem_aranha.png"},
    "Doutor Estranho": {"arquivo": "doutor_estranho.png"},
    "falção": {"arquivo": "falcao.png"},
}

# Carregar imagens dos heróis
for heroi in HERÓIS.values():
    caminho = os.path.join(CAMINHO_IMAGENS, heroi["arquivo"])
    heroi["imagem"] = pygame.image.load(caminho).convert_alpha()
    heroi["imagem"] = pygame.transform.scale(heroi["imagem"], (50, 50))

# Vilões disponíveis
VILOES = [
    "thanos.png",
    "ultron.png",
    "loki.png"
]

# Carregar imagens dos vilões
IMAGENS_VILOES = []
for arquivo in VILOES:
    caminho = os.path.join(CAMINHO_IMAGENS, arquivo)
    imagem = pygame.image.load(caminho).convert_alpha()
    imagem = pygame.transform.scale(imagem, (50, 50))
    IMAGENS_VILOES.append(imagem)

# Carregar fundo do espaço
fundo_espaco = pygame.image.load(os.path.join(CAMINHO_IMAGENS, "espaco.png")).convert()
fundo_espaco = pygame.transform.scale(fundo_espaco, (LARGURA, ALTURA))

# Classe do Herói
class Heroi(pygame.sprite.Sprite):
    def __init__(self, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.left = 50
        self.rect.centery = ALTURA // 2
        self.velocidade = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTURA:
            self.rect.y += self.velocidade

    def atirar(self):
        tiro = Tiro(self.rect.right, self.rect.centery)
        tiros.add(tiro)
        todos_sprites.add(tiro)

# Classe dos inimigos (vilões)
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(IMAGENS_VILOES)
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA
        self.rect.y = random.randint(0, ALTURA - self.rect.height)
        self.velocidade = random.randint(4, 8)

    def update(self):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()

# Classe dos tiros
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BRANCO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade = 10

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.left > LARGURA:
            self.kill()

# Tela de escolha de herói
def escolher_heroi():
    escolhendo = True
    while escolhendo:
        tela.blit(fundo_espaco, (0, 0))
        texto = fonte.render("Escolha seu herói (1-0):", True, BRANCO)
        tela.blit(texto, (LARGURA // 2 - 150, 50))

        for i, (nome, dados) in enumerate(HERÓIS.items()):
            img = dados["imagem"]
            linha = i // 5
            coluna = i % 5
            x = 100 + coluna * 130
            y = 150 + linha * 150
            tela.blit(img, (x, y))
            tecla = str(i + 1) if i < 9 else "0"
            nome_texto = fonte.render(f"{tecla}. {nome}", True, BRANCO)
            tela.blit(nome_texto, (x - 20, y + 60))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in [
                    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0
                ]:
                    if evento.key == pygame.K_0:
                        index = 9
                    else:
                        index = int(evento.unicode) - 1
                    nome_heroi = list(HERÓIS.keys())[index]
                    return HERÓIS[nome_heroi]["imagem"]

# ---------- Início do Jogo ----------
imagem_heroi_escolhido = escolher_heroi()

heroi = Heroi(imagem_heroi_escolhido)
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()
todos_sprites.add(heroi)

pontos = 0
jogando = True
spawn_inimigo_evento = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_inimigo_evento, 1500)

# Loop principal
while jogando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                heroi.atirar()
        if evento.type == spawn_inimigo_evento:
            inimigo = Inimigo()
            inimigos.add(inimigo)
            todos_sprites.add(inimigo)

    # Atualizar
    todos_sprites.update()
    tiros.update()

    # Colisões
    hits = pygame.sprite.groupcollide(inimigos, tiros, True, True)
    pontos += len(hits)

    if pygame.sprite.spritecollideany(heroi, inimigos):
        jogando = False

    # Desenhar
    tela.blit(fundo_espaco, (0, 0))  # Fundo espacial
    todos_sprites.draw(tela)
    tiros.draw(tela)

    texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))

    pygame.display.flip()

# Fim de jogo
tela.blit(fundo_espaco, (0, 0))
texto_game_over = fonte.render("GAME OVER", True, VERMELHO)
texto_final = fonte.render(f"Pontuação final: {pontos}", True, BRANCO)
tela.blit(texto_game_over, (LARGURA // 2 - 80, ALTURA // 2 - 40))
tela.blit(texto_final, (LARGURA // 2 - 100, ALTURA // 2 + 10))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
