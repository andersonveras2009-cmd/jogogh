# mente_brilhante.py
from flask import Flask, render_template_string, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "mente_brilhante_secret"

# ===================== QUESTÕES =====================

questoes = [
    # ----------- BIOLOGIA (100) -----------
    {"pergunta":"Qual é a função do cloroplasto nas células vegetais?",
     "opcoes":["Produzir energia","Fotossíntese","Armazenar água","Transportar seiva"],"resposta":1},
    {"pergunta":"Qual é a principal função do sistema circulatório?",
     "opcoes":["Transporte de substâncias","Produção de hormônios","Movimento","Defesa do organismo"],"resposta":0},
    {"pergunta":"O que os linfócitos fazem no corpo humano?",
     "opcoes":["Transportam oxigênio","Produzem anticorpos","Produzem energia","Auxiliam na digestão"],"resposta":1},
    {"pergunta":"Qual é a função da hemoglobina?",
     "opcoes":["Transportar oxigênio","Produzir energia","Digestão de proteínas","Formar coágulos"],"resposta":0},
    {"pergunta":"Qual é a função dos rins?",
     "opcoes":["Filtrar o sangue","Produzir hormônios","Transportar oxigênio","Controlar temperatura"],"resposta":0},
    {"pergunta":"Qual é a função do fígado?",
     "opcoes":["Produzir bile","Filtrar sangue","Armazenar oxigênio","Produzir insulina"],"resposta":0},
    {"pergunta":"Qual é a função da medula espinhal?",
     "opcoes":["Transmitir impulsos nervosos","Produzir hormônios","Armazenar nutrientes","Filtrar sangue"],"resposta":0},
    {"pergunta":"Qual a função dos pulmões?",
     "opcoes":["Troca gasosa","Produzir hormônios","Filtrar sangue","Transportar nutrientes"],"resposta":0},
    {"pergunta":"Qual é a principal função do sistema digestório?",
     "opcoes":["Digestão e absorção de nutrientes","Produção de hormônios","Transporte de oxigênio","Defesa do organismo"],"resposta":0},
    {"pergunta":"Qual hormônio regula a glicemia?",
     "opcoes":["Insulina","Adrenalina","Cortisol","Tiroxina"],"resposta":0},
    {"pergunta":"Qual é a função dos ribossomos?",
     "opcoes":["Síntese de proteínas","Produção de energia","Armazenamento de lipídios","Filtração"],"resposta":0},
    {"pergunta":"Qual é a função do sistema esquelético?",
     "opcoes":["Sustentação e proteção","Produção de energia","Digestão de alimentos","Transporte de oxigênio"],"resposta":0},
    {"pergunta":"Qual é a função do sistema muscular?",
     "opcoes":["Movimentação","Defesa do organismo","Digestão","Filtração"],"resposta":0},
    {"pergunta":"Qual é a função do sistema nervoso?",
     "opcoes":["Controle e coordenação","Produção de hormônios","Digestão","Transporte de oxigênio"],"resposta":0},
    {"pergunta":"Qual é a função do sistema excretor?",
     "opcoes":["Eliminação de resíduos","Produção de energia","Digestão","Movimentação"],"resposta":0},
    {"pergunta":"O que é fotossíntese?",
     "opcoes":["Produção de energia pela luz solar","Respiração celular","Fermentação","Transpiração"],"resposta":0},
    {"pergunta":"Qual é a função do estômago?",
     "opcoes":["Digestão química dos alimentos","Produção de hormônios","Armazenamento de sangue","Filtração"],"resposta":0},
    {"pergunta":"Qual é a função do intestino delgado?",
     "opcoes":["Absorção de nutrientes","Digestão mecânica","Filtração de sangue","Produção de hormônios"],"resposta":0},
    {"pergunta":"Qual é a função do intestino grosso?",
     "opcoes":["Absorção de água","Absorção de proteínas","Digestão de lipídios","Produção de enzimas"],"resposta":0},
    {"pergunta":"Qual é a função do coração?",
     "opcoes":["Bombear sangue","Produzir hormônios","Filtrar sangue","Digestão"],"resposta":0},
    {"pergunta":"Qual é a função dos alvéolos pulmonares?",
     "opcoes":["Troca gasosa","Produção de hormônios","Digestão","Filtração"],"resposta":0},
    {"pergunta":"Qual é a função do pâncreas?",
     "opcoes":["Produzir insulina e enzimas digestivas","Produzir hormônios sexuais","Transportar oxigênio","Filtrar sangue"],"resposta":0},
    {"pergunta":"O que é o DNA?",
     "opcoes":["Material genético","Proteína","Lipídio","Açúcar"],"resposta":0},
    {"pergunta":"O que é o RNA?",
     "opcoes":["Molécula que ajuda na síntese de proteínas","Material genético","Lipídio","Açúcar"],"resposta":0},
    {"pergunta":"Qual é a função da mitocôndria?",
     "opcoes":["Produzir energia (ATP)","Síntese de proteínas","Armazenar água","Transportar nutrientes"],"resposta":0},
    {"pergunta":"Qual é a função do complexo de Golgi?",
     "opcoes":["Processar e empacotar proteínas","Produzir energia","Filtrar sangue","Armazenar água"],"resposta":0},
    {"pergunta":"O que são enzimas?",
     "opcoes":["Proteínas que aceleram reações químicas","Ácidos nucleicos","Lipídios","Vitaminas"],"resposta":0},
    {"pergunta":"O que são hormônios?",
     "opcoes":["Mensageiros químicos do corpo","Vitaminas","Lipídios","Ácidos nucleicos"],"resposta":0},
    {"pergunta":"O que é a osmose?",
     "opcoes":["Movimento de água através da membrana","Síntese de proteínas","Produção de energia","Digestão"],"resposta":0},
    {"pergunta":"O que são vacúolos?",
     "opcoes":["Armazenam substâncias nas células","Produzem energia","Síntese de proteínas","Filtração"],"resposta":0},
    {"pergunta":"O que é difusão?",
     "opcoes":["Movimento de moléculas do mais concentrado para o menos concentrado","Produção de energia","Síntese de proteínas","Digestão"],"resposta":0},
    {"pergunta":"O que é transpiração?",
     "opcoes":["Perda de água pelas plantas","Produção de energia","Síntese de proteínas","Filtração"],"resposta":0},
    {"pergunta":"Qual é a função dos estômatos?",
     "opcoes":["Troca gasosa nas folhas","Produção de hormônios","Digestão","Filtração"],"resposta":0},
    {"pergunta":"O que é homeostase?",
     "opcoes":["Equilíbrio do ambiente interno do corpo","Produção de energia","Digestão","Transporte de oxigênio"],"resposta":0},
    {"pergunta":"O que é fototropismo?",
     "opcoes":["Crescimento das plantas em direção à luz","Movimento muscular","Transpiração","Produção de energia"],"resposta":0},
    {"pergunta":"O que são protozoários?",
     "opcoes":["Organismos unicelulares","Plantas","Fungos","Animais"],"resposta":0},
    {"pergunta":"O que são fungos?",
     "opcoes":["Organismos heterótrofos com parede celular de quitina","Plantas","Bactérias","Protozoários"],"resposta":0},
    {"pergunta":"O que são bactérias?",
     "opcoes":["Organismos unicelulares procariontes","Plantas","Fungos","Protozoários"],"resposta":0},
    {"pergunta":"O que são algas?",
     "opcoes":["Organismos fotossintéticos aquáticos","Plantas terrestres","Animais","Fungos"],"resposta":0},
    {"pergunta":"O que é ecossistema?",
     "opcoes":["Conjunto de seres vivos e ambiente","Apenas animais","Apenas plantas","Apenas microorganismos"],"resposta":0},
    {"pergunta":"O que é cadeia alimentar?",
     "opcoes":["Sequência de transferência de energia","Transporte de oxigênio","Produção de hormônios","Filtração"],"resposta":0},
    {"pergunta":"O que são produtores?",
     "opcoes":["Seres que produzem seu próprio alimento","Consumidores","Decompositores","Predadores"],"resposta":0},
    {"pergunta":"O que são consumidores?",
     "opcoes":["Seres que se alimentam de outros organismos","Produtores","Decompositores","Predadores"],"resposta":0},
    {"pergunta":"O que são decompositores?",
     "opcoes":["Seres que decompõem matéria orgânica","Produtores","Consumidores","Predadores"],"resposta":0},
    {"pergunta":"O que é fotofosforilação?",
     "opcoes":["Produção de ATP usando luz solar","Digestão de proteínas","Produção de hormônios","Filtração"],"resposta":0},
    {"pergunta":"O que é respiração celular?",
     "opcoes":["Produção de energia através de glicose","Produção de hormônios","Digestão","Filtração"],"resposta":0},
    {"pergunta":"O que é glicólise?",
     "opcoes":["Quebra da glicose para produzir ATP","Produção de hormônios","Digestão","Filtração"],"resposta":0},
    {"pergunta":"O que são lipídios?",
     "opcoes":["Moléculas energéticas e estruturais","Proteínas","Carboidratos","Ácidos nucleicos"],"resposta":0},
    {"pergunta":"O que são carboidratos?",
     "opcoes":["Moléculas de energia rápida","Proteínas","Lipídios","Ácidos nucleicos"],"resposta":0},
    {"pergunta":"O que são proteínas?",
     "opcoes":["Moléculas estruturais e funcionais","Lipídios","Carboidratos","Ácidos nucleicos"],"resposta":0},
    {"pergunta":"O que são ácidos nucleicos?",
     "opcoes":["DNA e RNA","Proteínas","Lipídios","Carboidratos"],"resposta":0},
    {"pergunta":"O que é clorofila?",
     "opcoes":["Pigmento verde da fotossíntese","Hormônio","Enzima digestiva","Proteína muscular"],"resposta":0},
    {"pergunta":"O que é estroma do cloroplasto?",
     "opcoes":["Região fluida onde ocorre a síntese de carboidratos","Produção de energia","Digestão","Filtração"],"resposta":0},
    {"pergunta":"O que é tilacoide?",
     "opcoes":["Membrana onde ocorre fotofosforilação","Produção de hormônios","Digestão","Filtração"],"resposta":0},

    # ----------- QUÍMICA (100) -----------
    {"pergunta":"Qual é a fórmula do bicarbonato de sódio?",
     "opcoes":["NaHCO3","NaCl","KCl","CaCO3"],"resposta":0},
    {"pergunta":"Qual é a fórmula do ácido clorídrico?",
     "opcoes":["HCl","H2SO4","HNO3","NaOH"],"resposta":0},
    {"pergunta":"Qual é a fórmula do ácido nítrico?",
     "opcoes":["HNO3","H2SO4","HCl","NaOH"],"resposta":0},
    {"pergunta":"Qual é a unidade de massa atômica?",
     "opcoes":["u","g","mol","L"],"resposta":0},
    {"pergunta":"Qual é a principal função de um catalisador?",
     "opcoes":["Acelerar uma reação química","Diminuir a temperatura","Produzir energia","Inibir reação"],"resposta":0},
    {"pergunta":"Qual a carga de um próton?",
     "opcoes":["Positiva","Negativa","Neutra","Depende do átomo"],"resposta":0},
    {"pergunta":"Qual a função de um ácido?",
     "opcoes":["Doar prótons","Receber prótons","Doar elétrons","Receber elétrons"],"resposta":0},
    {"pergunta":"Qual a função de uma base?",
     "opcoes":["Receber prótons","Doar prótons","Doar elétrons","Receber elétrons"],"resposta":0},
    {"pergunta":"O que é uma solução saturada?",
     "opcoes":["Não pode dissolver mais soluto","Pode dissolver mais soluto","Não tem solvente","Não tem soluto"],"resposta":0},
    {"pergunta":"O que é uma solução insaturada?",
     "opcoes":["Pode dissolver mais soluto","Não pode dissolver mais soluto","Não tem solvente","Não tem soluto"],"resposta":0},
    {"pergunta":"Qual gás é liberado na reação do ácido clorídrico com metal?",
     "opcoes":["H2","O2","CO2","N2"],"resposta":0},
    {"pergunta":"O que é oxidação?",
     "opcoes":["Perda de elétrons","Ganho de elétrons","Perda de prótons","Ganho de prótons"],"resposta":0},
    {"pergunta":"O que é redução?",
     "opcoes":["Ganho de elétrons","Perda de elétrons","Ganho de prótons","Perda de prótons"],"resposta":0},
    {"pergunta":"Qual é o número de oxidação do oxigênio na água?",
     "opcoes":["-2","0","+1","+2"],"resposta":0},
    {"pergunta":"Qual é o número de oxidação do hidrogênio na água?",
     "opcoes":["+1","0","-1","+2"],"resposta":0},
    {"pergunta":"O que é eletrólito?",
     "opcoes":["Substância que conduz corrente elétrica","Substância que não conduz","Ácido forte","Base fraca"],"resposta":0},
    {"pergunta":"O que é pH?",
     "opcoes":["Medida de acidez ou alcalinidade","Temperatura","Massa molar","Concentração"],"resposta":0},
    {"pergunta":"Qual é a cor do papel de tornassol em solução básica?",
     "opcoes":["Azul","Vermelho","Amarelo","Verde"],"resposta":0},
    {"pergunta":"Qual é a cor do papel de tornassol em solução ácida?",
     "opcoes":["Vermelho","Azul","Amarelo","Verde"],"resposta":0},
    {"pergunta":"O que é uma reação endotérmica?",
     "opcoes":["Absorve calor","Libera calor","Produz gás","Libera luz"],"resposta":0},
    {"pergunta":"O que é uma reação exotérmica?",
     "opcoes":["Libera calor","Absorve calor","Produz gás","Libera luz"],"resposta":0},
    {"pergunta":"O que é uma reação de neutralização?",
     "opcoes":["Ácido + Base → Sal + Água","Ácido + Metal → Sal + H2","Base + Metal → Sal","Ácido + Sal → Água"],"resposta":0},
    {"pergunta":"Qual é a fórmula do etanol?",
     "opcoes":["C2H5OH","CH4","C2H6","C2H4O"],"resposta":0},
    {"pergunta":"Qual é a fórmula do metanol?",
     "opcoes":["CH3OH","CH4","C2H5OH","C2H6"],"resposta":0},
    {"pergunta":"Qual gás é produzido na fermentação alcoólica?",
     "opcoes":["CO2","O2","H2","N2"],"resposta":0},
    {"pergunta":"O que é densidade?",
     "opcoes":["Massa/Volume","Massa","Volume","Temperatura"],"resposta":0},
    {"pergunta":"O que é massa molar?",
     "opcoes":["Massa de 1 mol de substância","Massa total","Volume","Concentração"],"resposta":0},
    {"pergunta":"O que é mol?",
     "opcoes":["Quantidade de substância","Massa","Volume","Concentração"],"resposta":0},
    {"pergunta":"O que é reação de combustão?",
     "opcoes":["Reage com oxigênio liberando energia","Reage com água","Reage com ácido","Reage com base"],"resposta":0},
    {"pergunta":"O que é reação de síntese?",
     "opcoes":["Formação de um composto","Separação de um composto","Oxidação","Redução"],"resposta":0},
    {"pergunta":"O que é reação de decomposição?",
     "opcoes":["Separação de um composto","Formação de um composto","Oxidação","Redução"],"resposta":0},
    {"pergunta":"O que é reação de deslocamento simples?",
     "opcoes":["Um elemento substitui outro","Dois elementos trocam","Formação de sal","Oxidação"],"resposta":0},
    {"pergunta":"O que é reação de dupla troca?",
     "opcoes":["Troca de íons entre dois compostos","Formação de gás","Oxidação","Redução"],"resposta":0},
    {"pergunta":"O que é eletronegatividade?",
     "opcoes":["Capacidade de atrair elétrons","Perda de prótons","Ganho de elétrons","Produção de calor"],"resposta":0},
    {"pergunta":"O que é energia de ionização?",
     "opcoes":["Energia para remover um elétron","Energia de ligação","Calor de combustão","Produção de luz"],"resposta":0},
    {"pergunta":"Qual metal é mais reativo, sódio ou ouro?",
     "opcoes":["Sódio","Ouro","Igual","Depende"],"resposta":0},
    {"pergunta":"Qual é a principal propriedade dos gases nobres?",
     "opcoes":["Baixa reatividade","Alta reatividade","Condutividade","Densidade"],"resposta":0},
    {"pergunta":"Qual é o gás presente em extintores?",
     "opcoes":["CO2","O2","N2","H2"],"resposta":0},
    {"pergunta":"Qual é a unidade de pressão?",
     "opcoes":["Pa","atm","mmHg","Todas"],"resposta":3},
    {"pergunta":"Qual é a unidade de volume?",
     "opcoes":["L","m3","cm3","Todas"],"resposta":3},
    {"pergunta":"O que é solubilidade?",
     "opcoes":["Capacidade de dissolver em um solvente","Produção de calor","Geração de energia","Oxidação"],"resposta":0},
    {"pergunta":"O que é concentração?",
     "opcoes":["Quantidade de soluto por volume de solução","Massa","Volume","Pressão"],"resposta":0},
    {"pergunta":"O que é uma mistura homogênea?",
     "opcoes":["Composição uniforme","Composição variável","Reação química","Separação de fases"],"resposta":0},
    {"pergunta":"O que é uma mistura heterogênea?",
     "opcoes":["Composição não uniforme","Composição uniforme","Reação química","Solução"],"resposta":0},
    {"pergunta":"O que é destilação?",
     "opcoes":["Separação por ponto de ebulição","Filtração","Evaporação","Decantação"],"resposta":0},
    {"pergunta":"O que é filtração?",
     "opcoes":["Separação sólido-líquido","Separação gasosa","Reação química","Evaporação"],"resposta":0},
    {"pergunta":"O que é decantação?",
     "opcoes":["Separação por densidade","Separação química","Oxidação","Redução"],"resposta":0},
    {"pergunta":"O que é evaporação?",
     "opcoes":["Transformação líquido-gás","Separação sólido-líquido","Reação química","Oxidação"],"resposta":0},
    {"pergunta":"O que é fusão?",
     "opcoes":["Sólido-líquido","Líquido-gás","Gás-sólido","Oxidação"],"resposta":0},
    {"pergunta":"O que é solidificação?",
     "opcoes":["Líquido-sólido","Sólido-líquido","Líquido-gás","Gás-líquido"],"resposta":0},
    {"pergunta":"O que é condensação?",
     "opcoes":["Gás-líquido","Líquido-gás","Sólido-líquido","Gás-sólido"],"resposta":0},
    {"pergunta":"O que é sublimação?",
     "opcoes":["Sólido-gás","Líquido-sólido","Gás-líquido","Líquido-gás"],"resposta":0},
    {"pergunta":"O que é ponto de ebulição?",
     "opcoes":["Temperatura que líquido vira gás","Temperatura que sólido vira líquido","Temperatura que líquido congela","Temperatura que gás se condensa"],"resposta":0},
    {"pergunta":"O que é ponto de fusão?",
     "opcoes":["Temperatura que sólido vira líquido","Temperatura que líquido vira gás","Temperatura que líquido congela","Temperatura que gás se condensa"],"resposta":0},
]

# ===================== ROTAS =====================
@app.route("/")
def index():
    session.clear()
    return render_template_string("""
    <h1>Bem-vindo ao Site de Estudos - Mente Brilhante</h1>
    <a href="{{ url_for('questao') }}">Começar Quiz</a>
    """)

@app.route("/questao", methods=["GET","POST"])
def questao():
    if "acertos" not in session:
        session["acertos"] = 0
        session["respondidas"] = 0
        session["ordem"] = random.sample(range(len(questoes)), len(questoes))
    
    respondidas = session["respondidas"]
    if respondidas >= len(questoes):
        return redirect(url_for("resultado"))
    
    q_index = session["ordem"][respondidas]
    q = questoes[q_index]

    if request.method == "POST":
        escolha = int(request.form["opcao"])
        if escolha == q["resposta"]:
            session["acertos"] += 1
        session["respondidas"] += 1
        return redirect(url_for("questao"))

    return render_template_string("""
    <h2>Questão {{ respondidas + 1 }} de {{ total }}</h2>
    <p>{{ pergunta }}</p>
    <form method="post">
       {% for opcao in opcoes %}
      <input type="radio" name="opcao" value="{{ loop.index0 }}" required> {{ opcao }}<br>
      {% endfor %}
    """, pergunta=q["pergunta"], opcoes=q["opcoes"], respondidas=respondidas, total=len(questoes))

@app.route("/resultado")
def resultado():
    acertos = session.get("acertos",0)
    total = len(questoes)
    return render_template_string("""
    <h1>Resultado Final</h1>
    <p>Você acertou {{ acertos }} de {{ total }} questões.</p>
    <a href="{{ url_for('index') }}">Recomeçar</a>
    """, acertos=acertos, total=total)

# ===================== RODAR =====================
if __name__ == "__main__":
    app.run(debug=True)
