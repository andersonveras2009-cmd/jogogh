from PIL import Image, ImageDraw, ImageFont
import random, os

# =============================================
# Shopee Simulador - Geração de Imagens Fictícias
# =============================================

# Cria a pasta imagens se não existir
os.makedirs("imagens", exist_ok=True)

# Lista de produtos fictícios
nomes = [
    "Celular X10", "Tênis Turbo", "Relógio Fit", "Fone Bass",
    "Mochila Max", "Câmera Zoom", "Teclado Pro", "Mouse Gamer",
    "Smartwatch Z", "Controle XR"
]

# Cores diferentes
cores = [
    (255, 165, 0), (0, 150, 255), (60, 200, 80), (255, 100, 100),
    (150, 80, 255), (255, 210, 0), (0, 200, 180), (200, 100, 255),
    (255, 150, 50), (100, 255, 180)
]

# Tenta carregar a fonte Arial, se não tiver usa a padrão
try:
    fonte = ImageFont.truetype("arial.ttf", 20)
except:
    fonte = ImageFont.load_default()

for i, nome in enumerate(nomes, start=1):
    img = Image.new("RGB", (150, 150), cores[i - 1])
    draw = ImageDraw.Draw(img)

    # Centraliza o texto na imagem
    w, h = draw.textsize(nome, font=fonte)
    draw.text(((150 - w) / 2, (150 - h) / 2), nome, fill="white", font=fonte)

    # Salva a imagem
    caminho = f"imagens/produto{i}.png"
    img.save(caminho)
    print(f"✅ Gerado: {caminho}")

print("\nTodas as 10 imagens foram criadas com sucesso!")