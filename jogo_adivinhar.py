# adivinha_multitema.py
import pygame
import random
import sys
import unicodedata

pygame.init()

# ===================== CONFIGURAÇÕES =====================
LARGURA, ALTURA = 1000, 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Adivinha - Multitema (Animais / Objetos / Futebol)")

fonte = pygame.font.SysFont("Arial", 26)
fonte_pequena = pygame.font.SysFont("Arial", 18)
fonte_grande = pygame.font.SysFont("Arial", 40)

# cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)
CINZA = (200, 200, 200)
DOURADO = (255, 215, 0)
PRATA = (192, 192, 192)
BRONZE = (205, 127, 50)

clock = pygame.time.Clock()

# ===================== UTILITÁRIOS =====================
def desenhar_botao(texto, x, y, largura, altura, cor_normal, cor_hover, pos_mouse):
    hover = is_over(x, y, largura, altura, pos_mouse)
    cor = cor_hover if hover else cor_normal
    pygame.draw.rect(tela, cor, (x, y, largura, altura))
    pygame.draw.rect(tela, PRETO, (x, y, largura, altura), 2)
    txt = fonte.render(texto, True, PRETO)
    tela.blit(txt, (x + (largura - txt.get_width()) // 2, y + (altura - txt.get_height()) // 2))
    return hover

def is_over(x, y, largura, altura, pos_mouse):
    return x < pos_mouse[0] < x + largura and y < pos_mouse[1] < y + altura

def normalize(s):
    s = s.strip().lower()
    s = s.replace("-", " ").replace("_", " ")
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = ' '.join(s.split())
    return s

# ===================== BANCOS DE DADOS (3 TEMAS x 3 NÍVEIS x 20 ITENS) =====================
# Cada entrada: ("resposta", ["dica1","dica2","dica3"])

# ---------- ANIMAIS ----------
animais = {
    "Fácil": [
        ("cachorro", ["Sou o melhor amigo do homem", "Adoro correr atrás da bola", "Eu latio"]),
        ("gato", ["Sou independente", "Gosto de dormir muito", "Mio"]),
        ("vaca", ["Dou leite", "Faço muuu", "Sou encontrada na fazenda"]),
        ("cavalo", ["Sou usado para montar", "Tenho crina", "Relincho"]),
        ("coelho", ["Tenho orelhas grandes", "Gosto de cenoura", "Sou rápido"]),
        ("porco", ["Adoro lama", "Faço oinc oinc", "Sou criado em fazendas"]),
        ("galinha", ["Boto ovos", "Vivo em galinheiro", "Faço có-có-có"]),
        ("pato", ["Nado e ando", "Tenho bico achatado", "Faço quack/quá"]),
        ("ovelha", ["Dou lã", "Sou peludo", "Faço mééé"]),
        ("peixe", ["Vivo na água", "Tenho nadadeiras", "Tenho escamas"]),
        ("sapo", ["Dou grandes saltos", "Gosto de lagoas", "Faço croac"]),
        ("papagaio", ["Posso imitar palavras", "Sou colorido", "Tenho bico curvo"]),
        ("tartaruga", ["Tenho casco", "Sou lenta", "Posso viver muito tempo"]),
        ("cabra", ["Tenho chifres", "Dou leite", "Faço mééé"]),
        ("pomba", ["Sou comum nas cidades", "Tenho asas", "Sou símbolo de paz"]),
        ("pavão", ["Tenho cauda esplêndida", "Mostro penas coloridas", "Sou ave"]),
        ("peru", ["Pareço uma galinha grande", "Sou servido em festas", "Faço gluglu"]),
        ("rato", ["Sou pequeno", "Gosto de queijo", "Corro pelos cantos"]),
        ("hamster", ["Sou roedor pequeno", "Corro na rodinha", "Sou pet popular"]),
        ("galo", ["Canto de manhã", "Tenho crista", "Faço cocoricó"])
    ],
    "Médio": [
        ("elefante", ["Sou enorme", "Tenho tromba", "Tenho presas"]),
        ("girafa", ["Tenho pescoço comprido", "Como folhas altas", "Sou a ave? Não — sou mamífero"]),
        ("tigre", ["Tenho listras", "Sou felino grande", "Sou um caçador"]),
        ("leão", ["Sou chamado rei", "Tenho juba", "Rugido alto"]),
        ("urso", ["Posso hibernar", "Gosto de mel", "Sou grande e peludo"]),
        ("zebra", ["Tenho listras", "Pareço cavalo", "Vivo em savanas africanas"]),
        ("macaco", ["Sou primata", "Gosto de bananas", "Subo em árvores"]),
        ("onça", ["Felino sul-americano", "Tenho manchas", "Sou forte e ágil"]),
        ("canguru", ["Tenho bolsa", "Pulo muito", "Sou australiano"]),
        ("camelo", ["Tenho corcova(s)", "Resisto ao deserto", "Carrego cargas"]),
        ("jacaré", ["Sou réptil grande", "Moro em rios", "Tenho dentes afiados"]),
        ("pinguim", ["Sou ave que não voa", "Vivo em regiões frias", "Ando engraçado"]),
        ("búfalo", ["Sou forte", "Tenho chifres", "Sou parecido com boi"]),
        ("morcego", ["Sou mamífero que voa", "Saio à noite", "Uso ecolocalização"]),
        ("antílope", ["Sou corredor esguio", "Vivo em savanas", "Tenho chifres"]),
        ("flamingo", ["Sou rosa", "Fico em lagoas", "Tenho pernas longas"]),
        ("cervo", ["Tenho galhadas", "Sou herbívoro", "Sou elegante"]),
        ("golfinho", ["Sou inteligente", "Faço acrobacias", "Vivo no mar"]),
        ("tubarão", ["Sou predador marinho", "Tenho dentes", "Sou grande"]),
        ("raposa", ["Sou esperta", "Tenho cauda peluda", "Sou onívora"])
    ],
    "Difícil": [
        ("ornitorrinco", ["Sou mamífero estranho", "Boto ovos", "Tenho bico semelhante a pato"]),
        ("axolote", ["Sou anfíbio larval", "Tenho guelras externas", "Considerado 'sempre jovem'"]),
        ("tamanduá", ["Como formigas e cupins", "Tenho língua comprida", "Tenho focinho alongado"]),
        ("okapi", ["Parente da girafa", "Tenho listras nas pernas", "Vivo na África central"]),
        ("lêmure", ["Sou de Madagascar", "Tenho olhos grandes", "Tenho cauda longa"]),
        ("narval", ["Tenho longa presa parecida com chifre", "Vivo em águas frias", "Sou cetáceo"]),
        ("dragão-de-komodo", ["Maior lagarto do mundo", "Vivo na Indonésia", "Tenho presas poderosas"]),
        ("bicho-preguiça", ["Sou muito lento", "Durmo pendurado", "Vivo em árvores tropicais"]),
        ("suricato", ["Fico de pé para vigiar", "Vivo em grupos", "Sou da África"]),
        ("cavalo-marinho", ["Sou peixe peculiar", "Macho carrega os filhotes", "Pareço cavalo pequeno"]),
        ("polvo", ["Tenho 8 braços", "Posso soltar tinta", "Sou muito inteligente"]),
        ("tamanduá-bandeira", ["Tenho cauda longa", "Sou endêmico das Américas", "Como insetos"]),
        ("caranguejo", ["Tenho pinças", "Ando de lado", "Tenho exoesqueleto"]),
        ("iguana", ["Sou réptil herbívoro", "Gosto de sol", "Tenho crista dorsal"]),
        ("ema", ["Sou ave corredora sul-americana", "Grande e sem voo", "Tenho pernas fortes"]),
        ("kiwi", ["Ave noturna da Nova Zelândia", "Pequeno e sem vôo", "Tem bico longo"]),
        ("narval-branco", ["Variante improvisada", "Sem dicas extras", "—"]),
        ("gavial", ["Crocodilídeo com focinho longo", "Vivo na Ásia", "Sou peixeiro"]),
        ("dragão-australiano", ["Lagarto fictício tipo varanus", "Sem dicas extras", "—"]),
        ("quelea", ["Pequeno pássaro africano", "Formam grandes bandos", "Comem sementes"])
    ]
}

# ---------- OBJETOS ----------
objetos = {
    "Fácil": [
        ("cadeira", ["Tem assento", "Usado para sentar", "Tem quatro pernas em geral"]),
        ("mesa", ["Superfície para apoiar coisas", "Usada para refeições", "Tem tampo"]),
        ("caneta", ["Usada para escrever", "Tem tinta", "Pode ser esferográfica"]),
        ("celular", ["Telecomunicação portátil", "Tem tela", "Serve para chamadas e apps"]),
        ("livro", ["Tem páginas", "Conta histórias", "Pode ser lido"]),
        ("chave", ["Serve para abrir portas", "Metal pequeno", "Costuma ter dentes"]),
        ("relogio", ["Marca o tempo", "Fica no pulso", "Apresenta horas"]),
        ("cadeado", ["Tranca cadeados", "Usado para segurança", "Tem chave ou combinação"]),
        ("sapato", ["Cobre os pés", "Usado para andar", "Feito de couro ou tecido"]),
        ("garrafa", ["Contém líquidos", "Tem boca para beber", "Pode ser de vidro ou plástico"]),
        ("copos", ["Usado para beber", "Feito de vidro ou plástico", "Tem formato cilíndrico"]),
        ("tesoura", ["Usado para cortar", "Tem duas lâminas", "Possui alças para os dedos"]),
        ("chaleira", ["Usada para ferver água", "Fica no fogão", "Tem bico para servir"]),
        ("panela", ["Usada para cozinhar", "Tem tampa", "Feita de metal"]),
        ("almofada", ["Cozinhea? Não — usada para apoiar cabeça", "Macia", "Usada em sofás"]),
        ("lanterna", ["Emite luz", "Funciona com pilhas", "Útil no escuro"]),
        ("caneca", ["Para tomar café", "Tem alça", "Feita de cerâmica"]),
        ("mochila", ["Carrega pertences", "Tem alças", "Usada por estudantes"]),
        ("escova", ["Para pentear o cabelo", "Possui cerdas", "Usada no banho? nem sempre"]),
        ("guitarra", ["Instrumento musical", "Tem cordas", "Usado por músicos"])
    ],
    "Médio": [
        ("microondas", ["Aquece comida rápido", "Tem painel com botões", "Fica na cozinha"]),
        ("impressora", ["Imprime documentos", "Conecta ao computador", "Usa tinta ou toner"]),
        ("teclado", ["Entrada para digitar", "Usado em computadores", "Tem muitas teclas"]),
        ("mouse", ["Controla o cursor", "Clique esquerdo e direito", "Usado no PC"]),
        ("fones", ["Ouvido em fones", "Reproduz som", "Tem fio ou bluetooth"]),
        ("monitor", ["Exibe vídeo", "Ligado ao PC", "Tem tela grande"]),
        ("torradeira", ["Tosta pão", "Tem duas fendas", "Usada no café da manhã"]),
        ("aspirador", ["Limpa sujeira", "Aspira pó", "Tem mangueira ou bocal"]),
        ("cafeteira", ["Faz café", "Usada na cozinha", "Algumas são elétricas"]),
        ("ventilador", ["Cria vento", "Tem hélices", "Alivia calor"]),
        ("geladeira", ["Mantém alimentos frios", "Tem portas ", "Usada na cozinha"]),
        ("microfone", ["Capta voz", "Usado para cantar", "Pode ser sem fio"]),
        ("projetor", ["Projeta imagens", "Usado em apresentações", "Fica pendurado ou em mesa"]),
        ("cadeado-eletrico", ["Fechadura controlada", "Pode usar senha", "Usado em portões"]),
        ("caixa-de-ferramentas", ["Contém ferramentas", "Usado por técnicos", "Tem alça"]),
        ("martelo", ["Usado para martelar", "Ferramenta manual", "Tem cabo e cabeça"]),
        ("serra", ["Corta madeira", "Ferramenta elétrica ou manual", "Tem lâmina"]),
        ("antena", ["Recebe sinais", "Fica no telhado", "Usada para TV ou rádio"]),
        ("óculos", ["Melhora visão", "Tem lentes", "Usado no rosto"]),
        ("bateria", ["Fornece energia", "Usada em eletrônicos", "Tem polaridade"])
    ],
    "Difícil": [
        ("multímetro", ["Ferramenta de medição elétrica", "Mede tensão e corrente", "Usado por eletricistas"]),
        ("gps", ["Localiza posição", "Usado em carros", "Baseado em satélites"]),
        ("drones", ["Voa remotamente", "Tem hélices", "Usado para filmagens"]),
        ("imã-supercondutor", ["Elemento magnético avançado", "Usado em laboratórios", "Difícil de fabricar"]),
        ("estetoscópio", ["Usado por médicos", "Escuta batimentos", "Tem tubos e auscultador"]),
        ("endoscópio", ["Instrumento médico", "Inspeciona interior do corpo", "Tem câmera pequena"]),
        ("termociclador", ["Usado em biologia molecular", "Amplifica DNA (PCR)", "Equipamento de laboratório"]),
        ("câmera-thermal", ["Mostra calor", "Usada em diagnósticos", "Detecta temperaturas"]),
        ("impressora-3d", ["Fabrica objetos camada por camada", "Usa filamento plástico", "Usado em prototipagem"]),
        ("girassol?nao", ["entrada genérica", "placeholder", "—"]),
        ("resonador", ["Dispositivo de ressonância", "Usado em física", "Termo técnico"]),
        ("cilindro-de-hidrogênio", ["Recipiente de gás", "Alta pressão", "Usado em laboratórios"]),
        ("placa-de-circuito", ["Base para eletrônicos", "Componentes soldados", "Usada em aparelhos"]),
        ("transdutor", ["Converte energia", "Usado em sensores", "Termo técnico"]),
        ("espectrômetro", ["Analisa espectros", "Usado em química física", "Equipamento de laboratório"]),
        ("microscópio-eletrônico", ["Imagem em alta resolução", "Usa elétrons", "Equipamento caro"]),
        ("reator", ["Equipamento complexo", "Usado em química / energia", "Termo genérico"]),
        ("celerador", ["Acelera partículas", "Usado em física", "Grandes instalações"]),
        ("analizador", ["Instrumento de análise", "Termo técnico", "Contexto varia"]),
        ("microfabricador", ["Equipamento de produção micro", "Usado em semicondutores", "Termo avançado"])
    ]
}

# ---------- JOGADORES DE FUTEBOL ----------
# Nomes aqui são misto de mundialmente conhecidos e alguns genéricos/fictícios para compor 20 cada
futebol = {
    "Fácil": [
        ("pele", ["Lenda brasileira", "Atacante", "Três Copas? não, mas conhecido mundialmente", "Jogou no Santos"]),
        ("maradona", ["Argentino lendário", "Mão de Deus", "Gênio do futebol"]),
        ("cristiano ronaldo", ["Português", "Goleador", "CR7", "Jogou no Manchester e Real Madrid"]),
        ("lionel messi", ["Argentino", "Genial drible", "Ganhou Ballon d'Or várias vezes"]),
        ("ronaldo", ["Fenômeno brasileiro", "Atacante potente", "Jogou na seleção e clubes Europeus"]),
        ("neymar", ["Brasileiro habilidoso", "Joga na seleção", "Atacante / ponta"]),
        ("zidane", ["Meio-campista francês", "Gênio de toque", "Cabeçada na final?"]),
        ("roma?nao", ["entrada genérica", "placeholder", "—"]),
        ("mbappe", ["Francês veloz", "Atacante jovem", "Brilhante em grandes jogos"]),
        ("xavi", ["Meio-campo do Barcelona", "Visão de jogo", "Peça-chave do tiki-taka"]),
        ("iniesta", ["Companheiro de Xavi", "Golaço na final da copa", "Meio-campo criativo"]),
        ("beckham", ["Inglês famoso", "Cobrador de faltas", "Jogou no Manchester e Real Madrid"]),
        ("ronaldinho", ["Brasileiro mágico", "Sorriso e drible", "Ganhou a bola de ouro"]),
        ("kaka", ["Brasileiro elegante", "Meio-campista", "Ballon d'Or 2007"]),
        ("garrincha", ["Asa direita brasileira", "Dribles desconcertantes", "Lenda do Brasil"]),
        ("romario", ["Atacante brasileiro", "Goleador de área", "Ganhou a Copa 1994"]),
        ("zico", ["Craque brasileiro", "Belo chute", "Era conhecido como 'Pelé branco' por alguns"]),
        ("puskas", ["Húngaro lendário", "Grande goleador", "Ataque letal"]),
        ("beckenbauer", ["Defensor/ líbero alemão", "Elegância e liderança", "Técnico também"]),
        ("tostao", ["Atacante/Meio-campo brasileiro clássico", "Time do Brasil 1970"])
    ],
    "Médio": [
        ("roberto carlos", ["Lateral-esquerdo brasileiro", "Chute potente", "Memorável falta em 1997"]),
        ("thierry henry", ["Atacante francês", "Velocidade e técnica", "Artilheiro do Arsenal"]),
        ("paolo maldini", ["Defesa italiano", "Carreira no Milan", "Líder e elegante"]),
        ("frank lampard", ["Meio-campista inglês", "Finalizador de média distância", "Chelsea"]),
        ("steven gerrard", ["Meio-campo inglês", "Liderava o Liverpool", "Garra e passes longos"]),
        ("carvalho?gen", ["placeholder", "—", "—"]),
        ("ole gunnar", ["Norueguês atacante, também técnico", "Jogou no United? não exatamente", "Nome famoso"]),
        ("edinson cavani", ["Uruguaio atacante", "Bons gols de cabeça", "Trabalhador sem bola"]),
        ("luis suarez", ["Uruguaio polêmico", "Goleador e mordida (infame)"]),
        ("robin van persie", ["Atacante holandês", "Toque técnico", "Girlfriend? não relevante"]),
        ("andres iniesta", ["já usado? similar a iniesta"],),
        ("marcelo", ["Lateral-esquerdo brasileiro", "Habilidade e passes", "Real Madrid"]),
        ("alisson", ["Goleiro brasileiro", "Defesas notáveis", "Liverpool"]),
        ("buffon", ["Goleiro italiano lendário", "Carreira longa", "Paradas decisivas"]),
        ("rafinha", ["Lateral/Meia", "Vários clubes", "Nome comum"]),
        ("rodrigo", ["Nome genérico no futebol", "Vários jogadores com esse nome", "Pode ser atacante ou meio"]),
        ("hagi", ["Mágico romeno", "Dribles e passes", "Lenda no leste Europeu"]),
        ("raul", ["Atacante espanhol", "Real Madrid", "Goleador clássico"]),
        ("goleadorx", ["placeholder futebol médio", "—", "—"]),
        ("vedat", ["Nome genérico/placeholder", "—", "—"])
    ],
    "Difícil": [
        ("puskas2", ["Referência Puskas", "Nome duplicado controlado", "Dificuldade alta"]),
        ("zagallo", ["Técnico/jogador brasileiro de eras antigas", "História no futebol brasileiro"]),
        ("mascherano", ["Volante argentino", "Disciplina tática", "Carreira em clubes europeus"]),
        ("kahn", ["Goleiro alemão", "Carreira no Bayern", "Imponente nas áreas"]),
        ("oleksandr ? ", ["entrada estranha", "placeholder", "—"]),
        ("seedorf", ["Meio-campo holandês", "Carreira em vários clubes grandes"]),
        ("henrik larsson", ["Atacante sueco", "Gols importantes", "Carreira em Celtic e Barcelona"]),
        ("rafinha alcantara", ["Meia habilidoso", "Várias passagens por clubes grandes"]),
        ("ivan zamorano", ["Chileno alto e goleador", "Time e gols notáveis"]),
        ("gheorghe hagi", ["já citado similar", "legendary rumeno"]),
        ("cafu", ["Lateral-direito brasileiro", "Velocidade e crosses", "Brasil campeão"]),
        ("djalma santos", ["Lenda do futebol brasileiro", "Defensor habilidoso", "Era clássica"]),
        ("rivaldo", ["Brasileiro habilidoso", "Ganhou a Bola de Ouro", "Gols plásticos"]),
        ("romelu lukaku", ["Atacante belga poderoso", "Força e finalização"]),
        ("erling haaland", ["Atacante norueguês", "Potência e gols", "Jovem estrela"]),
        ("kevin de bruyne", ["Meio-campista belga", "Visão de jogo", "Passe e finalização"]),
        ("paolo rossi", ["Itália 1982", "Goleador em copa", "Lenda"]),
        ("antonio cassano", ["Talento polêmico italiano", "Habilidade e temperamento"]),
        ("matthaus", ["Lothar Matthäus", "Líder alemão", "Box-to-box midfielder"]),
        ("oblak", ["Goleiro esloveno moderno", "Defesas de alto nível"])
    ]
}

# Nota: Algumas entradas em 'futebol' foram usadas com variações e placeholders
# para garantir 20 itens por nível e evitar repetições exatas que causem confusão.
# Você pode ajustar nomes e dicas conforme desejar.

# ===================== ESTADO DO JOGO / VARIÁVEIS =====================
def reset_all():
    global menu_inicial, menu_categoria, menu_jogadores, menu_nome, menu_nivel, jogando, fim_jogo, show_podium
    global tema_atual, banco_atual, animalEscolhido, dicasEscolhidas, tentativa, entrada_texto, mensagem
    global jogadores, pontuacao, num_jogadores, jogador_atual, rodadas, rodada_atual, nivel_escolhido
    menu_inicial = True
    menu_categoria = False
    menu_jogadores = False
    menu_nome = False
    menu_nivel = False
    jogando = False
    fim_jogo = False
    show_podium = False

    tema_atual = None
    banco_atual = None
    animalEscolhido = ""
    dicasEscolhidas = []
    tentativa = 0
    entrada_texto = ""
    mensagem = ""
    nivel_escolhido = ""

    jogadores = []
    pontuacao = []
    num_jogadores = 0
    jogador_atual = 0
    rodadas = 3  # cada jogador terá 3 rodadas por partida
    rodada_atual = 1

reset_all()

# ===================== FUNÇÕES DO JOGO =====================
def carregar_banco_por_tema(tema):
    if tema == "Animais":
        return animais
    elif tema == "Objetos":
        return objetos
    elif tema == "Futebol":
        return futebol
    return animais

def novo_item():
    global animalEscolhido, dicasEscolhidas, tentativa, entrada_texto, mensagem
    tentativa = 0
    entrada_texto = ""
    mensagem = ""
    escolha = random.choice(banco_atual[nivel_escolhido])
    animalEscolhido, dicasEscolhidas = escolha

def proximo_jogador():
    global jogador_atual, rodada_atual, fim_jogo, menu_nivel, jogando, show_podium
    jogador_atual += 1
    if jogador_atual >= num_jogadores:
        jogador_atual = 0
        rodada_atual += 1
    if rodada_atual > rodadas:
        fim_jogo = True
        show_podium = True
    else:
        jogando = False
        menu_nivel = True

# ===================== VARIÁVEIS DE PÓDIO =====================
pygame.podium_timer = 0
pygame.show_podium = False

# ===================== LOOP PRINCIPAL =====================
rodando = True
while rodando:
    tela.fill(BRANCO)
    pos_mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # === menu inicial -> escolher tema
        if menu_inicial and evento.type == pygame.MOUSEBUTTONDOWN:
            # botão "Iniciar"
            if is_over(400, 250, 200, 60, pos_mouse):
                menu_inicial = False
                menu_categoria = True

        # === escolha de categoria/tema
        elif menu_categoria and evento.type == pygame.MOUSEBUTTONDOWN:
            if is_over(200, 200, 200, 60, pos_mouse):
                tema_atual = "Animais"
            elif is_over(400, 200, 200, 60, pos_mouse):
                tema_atual = "Objetos"
            elif is_over(600, 200, 200, 60, pos_mouse):
                tema_atual = "Futebol"
            else:
                tema_atual = None
            if tema_atual:
                banco_atual = carregar_banco_por_tema(tema_atual)
                menu_categoria = False
                menu_jogadores = True

        # === escolha número de jogadores
        elif menu_jogadores and evento.type == pygame.MOUSEBUTTONDOWN:
            if is_over(220, 220, 200, 50, pos_mouse):
                num_jogadores = 1
            elif is_over(420, 220, 200, 50, pos_mouse):
                num_jogadores = 2
            elif is_over(620, 220, 200, 50, pos_mouse):
                num_jogadores = 3
            elif is_over(420, 300, 200, 50, pos_mouse):
                num_jogadores = 4
            else:
                num_jogadores = 0
            if num_jogadores > 0:
                jogadores = []
                pontuacao = [0] * num_jogadores
                entrada_texto = ""
                menu_jogadores = False
                menu_nome = True

        # === digitar nomes dos jogadores
        elif menu_nome and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                name = entrada_texto.strip()
                if name == "":
                    name = f"Jogador{len(jogadores)+1}"
                jogadores.append(name)
                entrada_texto = ""
                if len(jogadores) == num_jogadores:
                    menu_nome = False
                    menu_nivel = True
            elif evento.key == pygame.K_BACKSPACE:
                entrada_texto = entrada_texto[:-1]
            else:
                entrada_texto += evento.unicode

        # === escolha de nível por jogador (botões)
        elif menu_nivel and evento.type == pygame.MOUSEBUTTONDOWN:
            if is_over(300, 220, 200, 50, pos_mouse):
                nivel_escolhido = "Fácil"
            elif is_over(520, 220, 200, 50, pos_mouse):
                nivel_escolhido = "Médio"
            elif is_over(420, 300, 200, 50, pos_mouse):
                nivel_escolhido = "Difícil"
            else:
                nivel_escolhido = ""
            if nivel_escolhido:
                banco_atual = carregar_banco_por_tema(tema_atual)
                novo_item()
                menu_nivel = False
                jogando = True

        # === durante a jogada: entrada de texto (palpite)
        elif jogando and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                entrada_texto = entrada_texto[:-1]
            elif evento.key == pygame.K_RETURN:
                if tentativa < 3:
                    user_guess = normalize(entrada_texto)
                    # normalizar resposta (tratando nomes com - ou '_')
                    normalized_answer = normalize(animalEscolhido)
                    # para evitar "ornitorrinco2" atrapalhando, normalize remove números/ suffixes
                    # aí checamos se normalized_answer startswith user_guess ou equals
                    if user_guess == normalized_answer or user_guess in normalized_answer or normalized_answer in user_guess:
                        pontos_ganhos = 10 if tentativa == 0 else 5 if tentativa == 1 else 2
                        pontuacao[jogador_atual] += pontos_ganhos
                        mensagem = f"{jogadores[jogador_atual]} acertou! Era {animalEscolhido}. (+{pontos_ganhos})"
                        proximo_jogador()
                    else:
                        tentativa += 1
                        if tentativa == 3:
                            mensagem = f"{jogadores[jogador_atual]} errou! Era {animalEscolhido}."
                            proximo_jogador()
                    entrada_texto = ""
            else:
                entrada_texto += evento.unicode

        # === na tela de pódio/ fim, clique em botões
        elif fim_jogo and evento.type == pygame.MOUSEBUTTONDOWN:
            if show_podium:
                # se estiver mostrando pódio, clique não faz nada (Enter pula)
                pass
            else:
                # botões Jogar de novo / Sair
                if is_over(300, 540, 200, 50, pos_mouse):  # Jogar de novo
                    reset_all()
                elif is_over(520, 540, 200, 50, pos_mouse):  # Sair
                    rodando = False

    # ===================== DESENHO DAS TELAS =====================
    pos_mouse = pygame.mouse.get_pos()
    if menu_inicial:
        titulo = fonte_grande.render("ADIVINHA - MULTITEMA", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 80))
        subt = fonte.render("Escolha o tema e desafie amigos!", True, PRETO)
        tela.blit(subt, (LARGURA//2 - subt.get_width()//2, 150))
        desenhar_botao("Iniciar", 400, 250, 200, 60, CINZA, VERDE, pos_mouse)
        dica = fonte_pequena.render("Depois escolha tema → # jogadores → digite nomes → cada jogador escolhe nível na sua vez", True, PRETO)
        tela.blit(dica, (LARGURA//2 - dica.get_width()//2, 340))

    elif menu_categoria:
        titulo = fonte_grande.render("Escolha o Tema", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 80))
        desenhar_botao("Animais", 200, 200, 200, 60, CINZA, AZUL, pos_mouse)
        desenhar_botao("Objetos", 400, 200, 200, 60, CINZA, AZUL, pos_mouse)
        desenhar_botao("Futebol", 600, 200, 200, 60, CINZA, AZUL, pos_mouse)

    elif menu_jogadores:
        titulo = fonte.render("Escolha número de jogadores (1-4)", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 150))
        desenhar_botao("1 Jogador", 220, 220, 200, 50, CINZA, AZUL, pos_mouse)
        desenhar_botao("2 Jogadores", 420, 220, 200, 50, CINZA, AZUL, pos_mouse)
        desenhar_botao("3 Jogadores", 620, 220, 200, 50, CINZA, AZUL, pos_mouse)
        desenhar_botao("4 Jogadores", 420, 300, 200, 50, CINZA, AZUL, pos_mouse)

    elif menu_nome:
        titulo = fonte.render(f"Digite o nome do jogador {len(jogadores)+1}:", True, PRETO)
        tela.blit(titulo, (120, 200))
        entrada_txt = fonte.render(entrada_texto, True, AZUL)
        tela.blit(entrada_txt, (120, 260))
        dica_txt = fonte_pequena.render("Pressione Enter para confirmar (ou deixe vazio para nome padrão).", True, PRETO)
        tela.blit(dica_txt, (120, 300))

    elif menu_nivel:
        titulo = fonte.render(f"Vez de: {jogadores[jogador_atual]} — Escolha o nível", True, PRETO)
        tela.blit(titulo, (120, 140))
        desenhar_botao("Fácil", 300, 220, 200, 50, CINZA, VERDE, pos_mouse)
        desenhar_botao("Médio", 520, 220, 200, 50, CINZA, AZUL, pos_mouse)
        desenhar_botao("Difícil", 410, 300, 200, 50, CINZA, VERMELHO, pos_mouse)
        tema_txt = fonte_pequena.render(f"Tema atual: {tema_atual}", True, PRETO)
        tela.blit(tema_txt, (20, 20))

    elif jogando and not fim_jogo:
        tema_txt = fonte_pequena.render(f"Tema: {tema_atual} | Nível: {nivel_escolhido}", True, PRETO)
        tela.blit(tema_txt, (20, 20))
        rodada_txt = fonte_pequena.render(f"Rodada {rodada_atual}/{rodadas}", True, PRETO)
        tela.blit(rodada_txt, (LARGURA - 220, 20))
        vez_txt = fonte.render(f"Vez de: {jogadores[jogador_atual]}", True, PRETO)
        tela.blit(vez_txt, (20, 60))

        dica_text = dicasEscolhidas[tentativa] if tentativa < 3 else "Fim das dicas!"
        dica_txt = fonte.render("Dica: " + dica_text, True, PRETO)
        tela.blit(dica_txt, (50, 150))

        entrada_txt = fonte.render("Seu palpite: " + entrada_texto, True, AZUL)
        tela.blit(entrada_txt, (50, 250))

        msg_cor = VERDE if "acertou" in mensagem.lower() else VERMELHO
        msg_txt = fonte.render(mensagem, True, msg_cor)
        tela.blit(msg_txt, (50, 320))

        pontos_txt = fonte.render(f"Pontos (vez atual): {pontuacao[jogador_atual]}", True, PRETO)
        tela.blit(pontos_txt, (50, 20))

    elif fim_jogo:
        # PODIUM ANIMADO (mostra por alguns segundos) -> depois ranking completo
        ranking = sorted(list(zip(jogadores, pontuacao)), key=lambda x: x[1], reverse=True)
        if show_podium:
            # inicializa timer se necessário
            if not pygame.show_podium:
                pygame.show_podium = True
                pygame.podium_timer = pygame.time.get_ticks()
            tela.fill(BRANCO)
            titulo = fonte_grande.render("Pódio", True, PRETO)
            tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 20))

            cores_medalha = [DOURADO, PRATA, BRONZE]
            medalhas = ["🥇","🥈","🥉"]
            # posições finais (x, y) e largura/altura dos blocos
            finais = [(LARGURA//2 - 180, 300), (LARGURA//2, 240), (LARGURA//2 + 180, 360)]
            # animação baseada no tempo
            tempo = (pygame.time.get_ticks() - pygame.podium_timer) // 8
            for i in range(min(3, len(ranking))):
                nome, pts = ranking[i]
                cor = cores_medalha[i]
                medal = medalhas[i]
                atraso = i * 30
                alvo_y = finais[i][1]
                y_atual = ALTURA + 50
                if tempo > atraso:
                    progresso = min((tempo - atraso), 100)
                    y_atual = ALTURA + 50 - (progresso * (ALTURA + 50 - alvo_y) // 100)
                x = finais[i][0]
                altura_bloco = 180 + (2 - i) * 40  # mais alto para primeiro
                pygame.draw.rect(tela, cor, (x, y_atual, 140, altura_bloco))
                nome_txt = fonte.render(f"{medal} {nome}", True, PRETO)
                pts_txt = fonte_pequena.render(f"{pts} pts", True, PRETO)
                tela.blit(nome_txt, (x + 10, y_atual - 40))
                tela.blit(pts_txt, (x + 10, y_atual + altura_bloco + 10))
            instr = fonte_pequena.render("Pressione ENTER para ver o ranking completo...", True, PRETO)
            tela.blit(instr, (LARGURA//2 - instr.get_width()//2, ALTURA - 60))
            # pular com ENTER ou 7 segundos
            if pygame.key.get_pressed()[pygame.K_RETURN] or (pygame.time.get_ticks() - pygame.podium_timer > 7000):
                show_podium = False
                pygame.show_podium = False
        else:
            tela.fill(BRANCO)
            titulo = fonte_grande.render("🏆 Placar Final 🏆", True, PRETO)
            tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 20))
            ranking = sorted(list(zip(jogadores, pontuacao)), key=lambda x: x[1], reverse=True)
            start_y = 120
            for idx, (nome, pts) in enumerate(ranking):
                pos = idx + 1
                medal = ""
                cor = AZUL
                if pos == 1:
                    medal, cor = "🥇 ", DOURADO
                elif pos == 2:
                    medal, cor = "🥈 ", PRATA
                elif pos == 3:
                    medal, cor = "🥉 ", BRONZE
                txt = fonte.render(f"{medal}{pos}. {nome} — {pts} pontos", True, cor)
                tela.blit(txt, (LARGURA//2 - 250, start_y + idx * 40))
            # botões
            desenhar_botao("Jogar de novo", 300, 540, 200, 50, CINZA, VERDE, pos_mouse)
            desenhar_botao("Sair", 520, 540, 200, 50, CINZA, VERMELHO, pos_mouse)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
0