# -*- coding: utf-8 -*-
"""
ÁRVORE DO BRUNO (v3) — o que o pedido de desculpa libera.
Executado (exec) por gerar_parte2.py, depois de vida_hotel.py. Usa f, n, pens, sis, item, op, cena, C, _inserir_opcao.

Linhas:
  1. Clínica -> barulhos -> Homem Lagarto (luta 1 perdida) -> hall -> esquecer ou caçar -> luta 2 -> biblioteca
  2. Homem Invisível (10 fragmentos) -> Arthur
  3. Senhor Pálido (livro de 5 noites)
  4. Caminho A (Jehan)  |  Caminho B (Enola -> Jonathan ou Mavis -> Arthur -> sala de música -> estoque)
  5. Baile (portão: caminho A ou B concluído + Homem Invisível concluído)
"""

MEDICAS = [("amanda", "Amanda"), ("rafaela", "Rafaela")]

def por_medica(prefixo):
    """condicional: manda para <prefixo>_amanda ou <prefixo>_rafaela, conforme a médica que ajudou."""
    cena(prefixo, None, tipo="condicional",
         dados={"flag": "medica", "casos": {"amanda": prefixo + "_amanda", "rafaela": prefixo + "_rafaela"},
                "padrao": prefixo + "_amanda", "raiz": True})

# =====================================================================
# LINHA 1A — A clínica avisa: um paciente fugiu
# =====================================================================
por_medica("lag_clinica")
for m, M in MEDICAS:
    gentil = (m == "amanda")
    cena("lag_clinica_" + m, [
        "A clínica está silenciosa. Na maca onde você ficou, os lençóis foram trocados, e há um armário aberto, com frascos fora do lugar.",
        f(m, "Thiago! Eu ia mesmo te procurar. Como estão as dores?" if gentil else "Você voltou. Ótimo. Estava esperando que voltasse sozinho. Como estão as dores?"),
        f("thiago", "Voltam à noite. No ombro, no peito. Às vezes parece que está queimando."),
        "Ela examina o curativo com cuidado e troca a gaze. Depois separa dois frascos e uma caixinha de comprimidos.",
        f(m, "Tome isto quando a dor apertar. Não é um milagre, mas ajuda." ),
        item("remedios"),
        "Quando você já ia sair, ela segura a porta com a mão e baixa a voz.",
        f(m, "Preciso te avisar de uma coisa. Um paciente fugiu da clínica ontem à noite. Ele é... um funcionário daqui. Está doente, e não sabe o que faz quando a crise vem."),
        f("thiago", "Fugiu? Para onde?"),
        f(m, "Se eu soubesse, não estaria te contando no corredor. Tome cuidado. Se ouvir barulho estranho à noite, não vá ver sozinho."),
        pens("Mais uma coisa para não fazer sozinho neste hotel."),
    ], destino_auto="hub_corredores",
       chegada={"flags": {"lag_clinica_feito": True, "lag_estado": "aviso"}, "barras": {"sanidade": -4, "vida": 3},
                "itens": [], "tirar_marcadores_texto": [{"area": "corredores", "texto": "Voltar à clínica (as dores)"}],
                "marcadores": [{"area": "suite14", "texto": "Esteja no quarto à noite"}], "tempo": 20,
                "relacoes": {m: {"afeto": 3}}},
       dados={"raiz": True}, fundo="clinica")

_inserir_opcao("hub_corredores", op("lag_clinica_op", "Voltar à clínica por causa das dores", "lag_clinica",
    se=[{"flag": "elisabeta_desculpou"}, {"flag": "lag_clinica_feito", "diferente": True}]))

# =====================================================================
# LINHA 1B — Barulhos no corredor (à noite, depois da janta)
# =====================================================================
cena("lag_barulho", [
    "A janta terminou há pouco. Você volta para a suíte 14 com o estômago quente e a cabeça cheia. Mal gira a chave quando um som atravessa a porta.",
    "Algo arranha o chão, longe, no fundo do corredor. Depois um resmungo baixo, quase um choro, e um corpo pesado batendo na parede.",
    pens("O paciente que fugiu. Ela disse para não ir sozinho."),
    pens("Mas e se ele estiver machucado?"),
], opcoes=[
    op("lag_seguir", "Abrir a porta e seguir o barulho", "lag_corredor", efeitos={"barras": {"suspeita": 5}, "tempo": 4}),
    op("lag_ignorar", "Trancar a porta e ignorar", "lag_ignorou"),
], dados={"raiz": True}, fundo="suite14")

_inserir_opcao("suite_base", op("lag_barulho_op", "Escutar o barulho que vem do corredor", "lag_barulho",
    se=[{"flag": "lag_estado", "valor": "aviso"}, {"flag": "@hora", "min": 19, "max": 21}]))

cena("lag_ignorou", [
    "Você encosta a testa na porta, respira fundo e deixa o barulho para lá. Tranca duas vezes. Os sons duram quase uma hora e param de repente.",
    "Você dorme mal. Pela manhã, o corredor está vazio. Nenhum sinal de nada.",
    sis("Você não seguiu o barulho. O paciente não volta a aparecer, e a história dele não terá continuação nesta partida."),
], destino_auto="hub_suite14",
   chegada={"ate": "07:00", "sono": True, "barras": {"cansaco": 100, "sanidade": 10, "vida": 5},
            "flags": {"lag_estado": "ignorou", "lugar": "suite14"},
            "tirar_marcadores_texto": [{"area": "suite14", "texto": "Esteja no quarto à noite"}]},
   dados={"raiz": True}, fundo="suite14")

cena("lag_corredor", [
    "O corredor está iluminado só pelas lâmpadas de emergência, vermelhas e tremidas. O som vem do fim da ala, onde uma armadura caiu, espalhada pelo tapete.",
    "Atrás dela, encolhido no escuro, há um homem de uniforme rasgado. Ele tem a cabeça entre os braços e treme.",
    f("thiago", "Ei. Você está bem? Eu... vim ajudar."),
    "Ele levanta o rosto devagar. A pele do pescoço e da bochecha está coberta de escamas verde-acinzentadas, e os olhos são duas fendas amarelas.",
    f("lagarto", "Vá embora. Por favor. Eu... não consigo... segurar..."),
    "A voz se parte em um chiado. A mão dele, de unhas curvas e escamas finas, agarra o tapete e rasga um pedaço.",
    "Quando ele se levanta, já não é mais o mesmo homem. Ele ruge e avança.",
], destino_auto="lag_luta1", chegada={"barras": {"sanidade": -8}, "conhece": []}, dados={"raiz": True}, fundo="corredor")

cena("lag_luta1", None, tipo="combate", dados={"raiz": True, "combate": {
    "inimigo": {"nome": "Homem Lagarto", "retrato": "lagarto", "vida": 120, "dano": [9, 14]},
    "intro": "O Homem Lagarto avança, mais rápido e mais forte do que qualquer coisa que você já enfrentou.",
    "roteiro": "derrota", "rodadas_derrota": 3, "piso": 12,
    "vitoria": "lag_derrotado", "derrota": "lag_derrotado"}}, fundo="corredor")

cena("lag_derrotado", [
    "Um golpe no peito tira o ar de você. Outro, nas costas. O tapete vem ao seu encontro, e o corredor se apaga em manchas vermelhas.",
    "Você ouve um rugido, depois passos pesados se afastando. Depois só o seu próprio coração, muito devagar.",
    sis("Você perdeu a luta. Era uma luta que você não podia vencer."),
], destino_auto="lag_cuidado",
   chegada={"barras": {"sanidade": -10}, "tempo": 20}, dados={"raiz": True}, fundo="corredor")

por_medica("lag_cuidado")
for m, M in MEDICAS:
    cena("lag_cuidado_" + m, [
        "Você acorda no chão, no fundo do corredor, com o rosto colado ao tapete. Tudo dói, mas o mundo está de volta.",
        "Alguém afasta o seu cabelo da testa. Jehan, de camisa amassada e sem o colete, está agachado ao seu lado. Atrás dele, " + M + " abre uma maleta de primeiros socorros.",
        f("jehan", "Não se mexa. Você é teimoso, hein? Eu avisei."),
        f(m, "Respire devagar. Costelas machucadas, mas nada quebrado. Você tem muita sorte."),
        f("thiago", "Era... um homem. Com escamas. Ele me atacou."),
        f("jehan", "Fale baixo. Amanhã você conta direito. Agora, cama."),
        "Os dois levam você até a suíte. " + M + " faz um curativo novo e deixa um copo de água na mesinha. Jehan fica na porta até você fechar os olhos.",
    ], destino_auto="lag_hall",
       chegada={"ate": "07:10", "sono": True, "barras": {"vida": 20, "cansaco": 60, "sanidade": 5},
                "relacoes": {"jehan": {"afeto": 4}, m: {"afeto": 4}},
                "flags": {"lag_estado": "lutou", "lugar": "hall"},
                "tirar_marcadores_texto": [{"area": "suite14", "texto": "Esteja no quarto à noite"}]},
       dados={"raiz": True}, fundo="suite14")

# =====================================================================
# LINHA 1C — Manhã seguinte: o hall, Mavis e Jonathan
# =====================================================================
cena("lag_hall", [
    "Na manhã seguinte, antes do café, você desce ao hall, ainda dolorido. Mavis e Jonathan estão juntos, perto do balcão, conferindo uma lista.",
    f("mavis", "Thiago? Você está horrível. O que aconteceu?"),
    "Você conta tudo: o barulho, a armadura caída, o homem de escamas, a luta que você perdeu em três golpes.",
    f("jonathan", "Escamas? Thiago, o hotel é antigo. Tem cano que range e tapete que se mexe. Você bateu em algum lugar."),
    f("mavis", "Jonathan! Ele está machucado de verdade. Isso não é pouca coisa."),
    f("jonathan", "Não disse que não está. Só digo que o cansaço prega peças. Ele está há dias dormindo mal."),
    "Mavis olha para você, preocupada. Jonathan olha para o relógio.",
    pens("Eu sei o que eu vi. Mas e se eles estiverem certos?"),
], opcoes=[
    op("lag_esquecer1", "“Talvez vocês tenham razão. Foi cansaço.”", "lag_esquece",
       efeitos={"relacoes": {"mavis": {"afeto": 6}, "jehan": {"afeto": 4}, "jonathan": {"afeto": 2}}}),
    op("lag_cacar1", "“Eu sei o que vi. Vou descobrir o que é.”", "lag_cacar",
       efeitos={"relacoes": {"jonathan": {"afeto": -5}, "mavis": {"afeto": -2}}}),
], dados={"raiz": True}, fundo="hall")

cena("lag_esquece", [
    "Você respira fundo e dá de ombros, com um sorriso torto.",
    f("thiago", "Deve ter sido isso. Eu preciso dormir mais."),
    f("mavis", "Descansa hoje, tá? Eu aviso o Jehan para pegar leve no bar. Ele se preocupa com você."),
    "Jonathan assente, aliviado. Mavis aperta o seu braço com carinho.",
    sis("Você decidiu deixar o assunto para lá. Sua relação com Mavis e com Jehan aumentou."),
], destino_auto="hub_hall",
   chegada={"flags": {"lag_estado": "esqueceu", "lugar": "hall"}, "barras": {"sanidade": 3}, "tempo": 10},
   dados={"raiz": True}, fundo="hall")

cena("lag_cacar", [
    "Jonathan solta uma risada curta, sem humor. Mavis fica em silêncio, e o silêncio pesa mais.",
    f("mavis", "Tudo bem. Mas tome cuidado. Por favor."),
    f("jonathan", "Quando você encontrar uma lagartixa, me conte."),
    "Eles se afastam. Você sabe que algo no tom de Jonathan não era só ironia.",
    sis("Você decidiu caçar o Homem Lagarto. Durante o dia, procure nos corredores. À noite, fale com Jehan no bar."),
], destino_auto="hub_hall",
   chegada={"flags": {"lag_estado": "cacando", "lugar": "hall"}, "tempo": 10,
            "marcadores": [{"area": "bar", "texto": "Contar tudo a Jehan (à noite)"}]},
   dados={"raiz": True}, fundo="hall")

_inserir_opcao("hub_corredores", op("lag_procura_op", "Procurar sinais do Homem Lagarto", "lag_procura",
    se=[{"flag": "lag_estado", "valor": "cacando"}, {"flag": "@hora", "min": 7, "max": 18}]))

cena("lag_procura", None, tipo="sorteio", dados={"raiz": True, "opcoes": ["lag_procura_1", "lag_procura_2", "lag_procura_3"]})
cena("lag_procura_1", [
    "Você percorre o corredor devagar, atento. Um rasgo no tapete. Uma armadura que alguém recolocou no lugar, com pressa.",
    "Ao longe, um som de arranhão, que some quando você se aproxima.",
], destino_auto="hub_corredores", chegada={"tempo": 12, "barras": {"sanidade": -1}}, dados={"raiz": True}, fundo="corredor_dia")
cena("lag_procura_2", [
    "Você encosta a orelha em algumas portas. Só silêncio, e um perfume de lavanda numa delas.",
    "Do último quarto do corredor vem um resmungo baixo. Mas quando você bate, ninguém responde.",
], destino_auto="hub_corredores", chegada={"tempo": 12, "barras": {"sanidade": -1}}, dados={"raiz": True}, fundo="corredor_dia")
cena("lag_procura_3", [
    "Há um risco de unhas na madeira de uma porta, a uns dois palmos do chão. Você passa o dedo sobre a marca, e ela está fria, seca, recente.",
    "Quando olha para trás, o corredor está vazio. Mas você tem a sensação de que alguém acabou de sair.",
], destino_auto="hub_corredores", chegada={"tempo": 12, "barras": {"sanidade": -1}}, dados={"raiz": True}, fundo="corredor_dia")

# =====================================================================
# LINHA 1D — No bar: Jehan aconselha esquecer; Thiago decide
# =====================================================================
cena("lag_bar", [
    "O bar está quase vazio. Jehan enxuga um copo, e quando vê o seu rosto, deixa o pano no balcão.",
    f("jehan", "Fale. Você tem cara de quem está carregando uma pedra."),
    "Você conta tudo de novo: os arranhões, o homem escamado, a luta perdida e a risada seca de Jonathan.",
    f("jehan", "Eu ouvi pela Mavis. E vou te dizer o que eu diria a qualquer hóspede: esqueça isso. Vá para o quarto e durma."),
    f("jehan", "Esse tipo de gente... esse tipo de doença... não é coisa para um humano caçar."),
    f("thiago", "Humano. É sempre assim que você me chama quando está preocupado."),
    "Ele ri sem vontade e passa a mão pelo cabelo.",
], opcoes=[
    op("lag_esquecer2", "“Você tem razão. Vou esquecer.”", "lag_esquece2",
       efeitos={"relacoes": {"mavis": {"afeto": 6}, "jehan": {"afeto": 6}}}),
    op("lag_cacar2", "“Não consigo. Eu vou atrás dele.”", "lag_noite_caca",
       efeitos={"relacoes": {"jehan": {"afeto": 2}}}),
], dados={"raiz": True}, fundo="bar")

_inserir_opcao("bar_base", op("lag_bar_op", "Contar tudo a Jehan sobre o Homem Lagarto", "lag_bar",
    se=[{"flag": "lag_estado", "valor": "cacando"}, {"flag": "@hora", "min": 19, "max": 21}]))

cena("lag_esquece2", [
    f("thiago", "Tem razão. Eu vou esquecer isso."),
    f("jehan", "Esse é o meu rapaz. Bebe isso e dorme. Eu aviso a Mavis que você está bem."),
    "Ele serve um copo de leite morno, para sua surpresa, e sorri de lado.",
    sis("Você desistiu de caçar o Homem Lagarto. Sua relação com Mavis e com Jehan aumentou."),
], destino_auto="bar_base",
   chegada={"flags": {"lag_estado": "esqueceu"}, "barras": {"sanidade": 4}, "tirar_marcadores_texto": [{"area": "bar", "texto": "Contar tudo a Jehan (à noite)"}], "tempo": 15},
   dados={"raiz": True}, fundo="bar")

cena("lag_noite_caca", [
    "Jehan fica em silêncio por um longo tempo. Depois tira o avental, dobra com cuidado e o põe sobre o balcão.",
    f("jehan", "Eu sabia que você ia dizer isso. Então não vai sozinho."),
    f("jehan", "Eu vou chamar a médica. Ela conhece esse paciente melhor do que ninguém. Esperem no corredor leste, depois da meia-noite."),
    "Você sai do bar com o coração batendo no ritmo de um relógio. O hotel parece prender a respiração.",
], destino_auto="lag_corredor2",
   chegada={"ate": "23:40", "tirar_marcadores_texto": [{"area": "bar", "texto": "Contar tudo a Jehan (à noite)"}], "barras": {"suspeita": 5}},
   dados={"raiz": True}, fundo="bar")

por_medica("lag_corredor2")
for m, M in MEDICAS:
    cena("lag_corredor2_" + m, [
        "O corredor leste está escuro, e as lâmpadas de emergência dão ao tapete a cor de ferrugem. " + M + " espera encostada numa armadura, com uma seringa numa mão e uma lanterna na outra.",
        f(m, "Jehan me contou. Você é corajoso ou teimoso, ainda não decidi."),
        f("thiago", "Os dois, normalmente."),
        f(m, "Ele se chama Heitor. Trabalhava na lavanderia. A crise começa em dias de lua cheia, e ele perde o controle. Se eu chegar perto, talvez a voz dele me reconheça."),
        f("jehan", "E se não reconhecer, você é o primeiro a levar."),
        "Um arranhão no fim do corredor. Um chiado. Uma sombra comprida se estica sobre a parede.",
        "O Homem Lagarto aparece. Desta vez, você tem as mãos livres e um motivo.",
    ], destino_auto="lag_luta2", dados={"raiz": True}, fundo="corredor")

cena("lag_luta2", None, tipo="combate", dados={"raiz": True, "combate": {
    "inimigo": {"nome": "Homem Lagarto", "retrato": "lagarto", "vida": 70, "dano": [7, 11]},
    "intro": "O Homem Lagarto ruge. Desta vez, você não está sozinho.",
    "roteiro": "livre", "piso": 8,
    "vitoria": "lag_vitoria", "derrota": "lag_derrota2"}}, fundo="corredor")

por_medica("lag_vitoria")
for m, M in MEDICAS:
    cena("lag_vitoria_" + m, [
        "O último golpe encontra o ombro dele. O Homem Lagarto cai de joelhos, a respiração falhando. As escamas recuam do rosto, e ele volta a ser um homem muito magro, de olhos fundos, chorando.",
        f("lagarto_calmo", "Desculpa... desculpa... eu não queria..."),
        M + " passa por você, ajoelha-se e encosta a seringa no braço dele, com uma delicadeza que você não esperava.",
        f(m, "Está tudo bem, Heitor. Já passou. Eu estou aqui."),
        "Ele afunda numa respiração lenta. Dois funcionários da clínica surgem do fundo do corredor, com uma maca, e o levam sem dizer uma palavra.",
        f(m, "Você... enfrentou ele sozinho? Quer dizer, quase sozinho." if m == "amanda" else "Você é mais resistente do que parece, Thiago. Isso foi... impressionante."),
        "Ela desvia o olhar um segundo mais tarde do que devia, e as bochechas dela ficam um pouco rosadas.",
        f("jehan", "Chega de heroísmo por hoje. Toma, bebe isso. Vai te ajudar a dormir. E esquece. É só um homem doente."),
        "Ele leva você até a suíte e põe um frasquinho na sua mão. Você bebe e adormece sem lembrar de ter deitado.",
        sis("Você venceu o Homem Lagarto. A relação com " + M + " subiu, e algo mais começou a se mover. Uma nova pista foi liberada na biblioteca."),
    ], destino_auto="hub_suite14",
       chegada={"ate": "07:00", "sono": True, "barras": {"vida": 20, "cansaco": 70, "sanidade": 8},
                "relacoes": {m: {"afeto": 10, "nivel": 1}, "jehan": {"afeto": 4}},
                "ligacao": {m: "romance"},
                "conhece": ["lagarto"],
                "flags": {"lag_estado": "venceu", "lugar": "suite14", "lag_biblioteca": True},
                "marcadores": [{"area": "biblioteca", "texto": "Pesquisar o Homem Lagarto"}]},
       dados={"raiz": True}, fundo="corredor")

cena("lag_derrota2", [
    "Você cai de costas, sem ar. O Homem Lagarto ergue as garras para o golpe final.",
    "Então a voz de alguém corta o corredor, firme e baixa. Ele hesita. A seringa encontra o pescoço dele, e o rugido se desfaz num gemido.",
    "Você ouve o corpo dele bater no chão. Depois só a respiração de três pessoas, e a de um quarto homem, que vai se acalmando.",
    f("jehan", "Eu falei que você ia apanhar. Levanta. Hoje não."),
    sis("Você foi salvo por Jehan e pela médica. O Homem Lagarto foi levado de volta à clínica."),
], destino_auto="hub_suite14",
   chegada={"ate": "07:00", "sono": True, "barras": {"vida": 15, "cansaco": 60, "sanidade": -5},
            "flags": {"lag_estado": "resgatado", "lugar": "suite14", "lag_biblioteca": True},
            "marcadores": [{"area": "biblioteca", "texto": "Pesquisar o Homem Lagarto"}]},
   dados={"raiz": True}, fundo="corredor")

# --- biblioteca: o que é o Homem Lagarto? ---
cena("lag_biblio", [
    "Na biblioteca, Enola aponta sem perguntar duas estantes: uma de folclore, outra de medicina antiga. O olhar dela diz que ela sabe por que você está ali.",
    "No primeiro livro, uma lenda: um homem que, nas noites de lua cheia, vira lagarto. Pele em escamas, olhos de fenda, uma fome que ninguém explica. Um castigo, dizem, por ter roubado o que não devia.",
    "No segundo, um tratado de 1890: uma doença rara da pele que a deixa grossa, escamosa, esverdeada. Os pacientes eram isolados. Alguns, diz o autor, perdiam a razão.",
    pens("Lenda ou doença? As escamas estavam mesmo na pele. Mas aqueles olhos..."),
    pens("Ou então... não era nada disso. Alienígena, talvez. Lagartos do espaço, num hotel perdido na estrada."),
    "Você ri sozinho. Enola, ao longe, não ri.",
], opcoes=[
    op("lag_t1", "Concluir que é uma doença", "lag_biblio_fim", efeitos={"flags": {"lag_teoria": "doenca"}}),
    op("lag_t2", "Concluir que é uma lenda de verdade", "lag_biblio_fim", efeitos={"flags": {"lag_teoria": "lenda"}}),
    op("lag_t3", "Não concluir nada. Anotar as duas hipóteses.", "lag_biblio_fim", efeitos={"flags": {"lag_teoria": "duvida"}}),
], dados={"raiz": True}, fundo="biblioteca")

cena("lag_biblio_fim", [
    "Você fecha os livros e devolve às estantes. A dúvida fica com você, mais pesada que os dois volumes juntos.",
    sis("Missão concluída: <b>O Que Era o Homem Lagarto</b>."),
], destino_auto="biblioteca_base",
   chegada={"flags": {"lag_biblio": "concluida"}, "barras": {"sanidade": 3}, "tempo": 40,
            "tirar_marcadores_texto": [{"area": "biblioteca", "texto": "Pesquisar o Homem Lagarto"}]},
   dados={"raiz": True}, fundo="biblioteca")

_inserir_opcao("biblioteca_base", op("lag_biblio_op", "Pesquisar o Homem Lagarto nas estantes", "lag_biblio",
    se=[{"flag": "lag_biblioteca", "valor": True}, {"flag": "lag_biblio", "diferente": "concluida"}]))

# =====================================================================
# LINHA 2 — Homem Invisível: 10 fragmentos, conversa com Arthur
# =====================================================================
cena("inv2_arthur", [
    "Arthur acena para você da mesa de sempre. Há papéis espalhados por todo canto, cada um com uma data e uma anotação.",
    f("arthur", "Eu contei. Dez ocorrências suas, só nestes dias. Dez vezes que algo mexeu nas suas coisas, riu perto de você, fechou uma porta. Sempre em horários e lugares que se repetem."),
    n("Ele pausa e olha para o seu ombro enfaixado. “Depois do que aconteceu com você, eu não posso mais chamar isso de coincidência.”", se={"flag": "lag_estado", "valor": "venceu"}),
    n("Ele pausa e olha para o seu ombro enfaixado. “Depois do que aconteceu com você, eu não posso mais chamar isso de coincidência.”", se={"flag": "lag_estado", "valor": "lutou"}),
    n("Ele pausa e olha para os seus olhos, que continuam fundos. “Depois do que aconteceu na sala de música, eu não posso mais chamar isso de coincidência.”", se=[{"flag": "lag_estado", "diferente": "venceu"}, {"flag": "lag_estado", "diferente": "lutou"}]),
    f("thiago", "Eu estava errado, Arthur. Você tinha razão. Tem alguém, ou algo, que não quer ser visto. E está se divertindo."),
    f("arthur", "Então somos dois que acreditam. Vamos fazer o seguinte: nada de contar ao Jehan. Ele sabe de tudo e não fala nada. Eu confio mais no Jonathan para isso."),
    f("thiago", "Jonathan? Ele riu de mim no hall."),
    f("arthur", "Eu sei. Mas ele organiza o baile, e o baile reúne todo mundo. Se o responsável existe, vai estar lá. Eu quero ver a cara dele."),
    f("thiago", "No baile, então. Nós dois vamos conversar com o Jonathan."),
    "Arthur sorri, de verdade pela primeira vez, e guarda os papéis na pasta.",
    sis("Missão concluída: <b>Um Passo Mais Perto do Homem Invisível</b>."),
    sis("O Baile da Fundação está liberado: vá ao salão de festas quando estiver pronto.", se={"flag": "@baile"}, ao={"marcadores": [{"area": "salao_festas", "texto": "Baile da Fundação"}]}),
], destino_auto="biblioteca_base",
   chegada={"flags": {"inv2_estado": "concluida"}, "relacoes": {"arthur": {"afeto": 8}}, "barras": {"sanidade": 4}, "tempo": 25,
            "tirar_marcadores_texto": [{"area": "biblioteca", "texto": "Arthur tem novidades"}]},
   dados={"raiz": True}, fundo="biblioteca")

_inserir_opcao("biblioteca_base", op("inv2_op", "Arthur chama você: ele contou as ocorrências", "inv2_arthur",
    se=[{"flag": "elisabeta_desculpou"}, {"flag": "arthur_estado", "valor": "concluido"},
        {"flag": "fragmentos", "min": 10}, {"flag": "inv2_estado", "diferente": "concluida"}]))

# =====================================================================
# LINHA 3 — Senhor Pálido: o livro de magia (5 noites)
# =====================================================================
cena("pal_conversa", [
    "O Senhor Pálido está na mesma mesa afastada, de abajur verde. Dessa vez, o livro que ele lê é outro: capa de couro escuro, letras douradas, uma fita vermelha no meio.",
    f("nosferatu", "Thiago. Fico contente que tenha voltado. Raramente alguém volta."),
    f("thiago", "O senhor lê muito."),
    f("nosferatu", "Leio magia. Não a dos palcos. A outra, que dá trabalho e não perdoa quem erra. É um hábito antigo."),
    f("nosferatu", "Você me parece interessante. Perdoe a franqueza. Os humanos que passam por aqui costumam ter medo de tudo, e você parece ter medo só do que merece."),
    f("thiago", "Eu tenho medo de muita coisa."),
    f("nosferatu", "Tem. Mas escolhe com cuidado. É raro."),
    "Ele empurra o livro na sua direção, com as pontas dos dedos.",
    f("nosferatu", "Leve este para o quarto. Leia à noite, antes de dormir, uma parte por vez. Não corra. O livro cobra o tempo de quem o lê."),
    f("thiago", "Cobra como?"),
    f("nosferatu", "O sono, em geral. Cinco noites, se você tiver paciência. Depois me conte o que entendeu."),
    item("livro_palido"),
    "Ele fecha os olhos, como quem encerra a conversa, e some entre as estantes antes que você consiga falar de novo.",
    sis("Missão: <b>O Livro do Senhor Pálido</b>. Leia o livro no quarto, antes de dormir. Cada noite de leitura recupera menos descanso."),
], destino_auto="biblioteca_base",
   chegada={"flags": {"pal_estado": "livro", "livro_n": 0}, "relacoes": {"nosferatu": {"afeto": 6}}, "barras": {"sanidade": 2}, "tempo": 15,
            "marcadores": [{"area": "suite14", "texto": "Ler o livro (5 noites)"}],
            "tirar_marcadores_texto": [{"area": "biblioteca", "texto": "O Senhor Pálido"}]},
   dados={"raiz": True}, fundo="biblioteca")

_inserir_opcao("biblioteca_base", op("pal_op", "Aproximar-se do Senhor Pálido, que lê na mesa afastada", "pal_conversa",
    se=[{"flag": "elisabeta_desculpou"}, {"flag": "conv_biblio", "valor": True}, {"flag": "pal_estado", "diferente": "livro"},
        {"flag": "pal_estado", "diferente": "concluido"}, {"flag": "baile_inicio", "diferente": True}]))

# leitura: um capítulo por noite
LIVRO = [
    ["A primeira noite: o livro começa pelo silêncio. Não há feitiço nas primeiras páginas. Só um aviso: “Toda magia tem preço, e o preço se paga em tempo.”",
     "Você lê até os olhos arderem. Antes de dormir, a letra parece se mover de leve, como se respirasse."],
    ["A segunda noite fala de nomes. Quem sabe o nome de uma coisa tem um pedaço dela. Você anota três nomes e se arrepende de uma das anotações.",
     "Ao fechar o livro, um dos nomes escritos no caderno já não está lá."],
    ["A terceira noite é sobre símbolos. Círculos, traços, sinais de fechadura. O livro avisa que alguns desenhos só funcionam em certas horas.",
     "Você copia um, com a mão tremendo, e o abajur pisca duas vezes."],
    ["A quarta noite é a mais pesada. Fala do que acontece com quem usa magia sem cuidado: o corpo se acostuma com o frio, a memória se solta, a sombra se desprende.",
     "Você não consegue dormir logo. Fica escutando o hotel respirar."],
    ["A quinta noite explica por que o livro cobra o sono: a magia que se lê precisa ser sonhada para ficar. Quando você fecha a última página, a sua cabeça está estranhamente clara.",
     "Você entende, por um segundo, o que o Senhor Pálido queria dizer."],
]
cena("livro_ler", None, tipo="condicional",
     dados={"flag": "livro_n", "casos": {str(i): f"livro_n{i+1}" for i in range(5)}, "padrao": "livro_n5", "raiz": True})
for i, linhas in enumerate(LIVRO, 1):
    ultimo = (i == 5)
    narr = list(linhas)
    if ultimo:
        narr.append(sis("Você aprendeu <b>Noções de Magia</b>. Volte a falar com o Senhor Pálido, se ele ainda estiver por aí."))
    ef = {"ate": "07:00", "sono": True, "barras": {"cansaco": 50, "sanidade": 4, "vida": 3},
          "somar": {"livro_n": 1}, "flags": {"lugar": "suite14"}, "relacoes": {"nosferatu": {"afeto": 1}}}
    if ultimo:
        ef["habilidades"] = ["nocoes_magia"]
        ef["flags"]["pal_estado"] = "concluido"
        ef["tirar_marcadores_texto"] = [{"area": "suite14", "texto": "Ler o livro (5 noites)"}]
        ef["barras"]["sanidade"] = 8
    cena(f"livro_n{i}", narr, destino_auto="hub_suite14", chegada=ef, dados={"raiz": True}, fundo="suite14")

for faixa in ({"min": 19}, {"max": 5}):
    _inserir_opcao("suite_base", op("livro_op_" + ("noite" if "min" in faixa else "madrugada"),
        "Ler o livro do Senhor Pálido antes de dormir", "livro_ler",
        se=[{"flag": "pal_estado", "valor": "livro"}, dict({"flag": "@hora"}, **faixa)], requisitos={"itens": ["livro_palido"]}))

cena("pal_fim", [
    "O Senhor Pálido ainda está na mesa. Ele ergue os olhos assim que você se aproxima.",
    f("nosferatu", "Terminou. Dá para perceber. Você está mais calado."),
    f("thiago", "Entendi parte. Não sei se quero entender o resto."),
    f("nosferatu", "É a resposta certa. Guarde o livro, ele é seu agora. E, quando quiser conversar sobre o que leu, saiba que raramente estarei de passagem."),
    "Ele sorri de lado, só com a boca, e volta a ler.",
    sis("Missão concluída: <b>O Livro do Senhor Pálido</b>."),
], destino_auto="biblioteca_base",
   chegada={"flags": {"pal_fim": True}, "relacoes": {"nosferatu": {"afeto": 8}}, "barras": {"sanidade": 3}, "tempo": 12},
   dados={"raiz": True}, fundo="biblioteca")

_inserir_opcao("biblioteca_base", op("pal_fim_op", "Contar ao Senhor Pálido que terminou o livro", "pal_fim",
    se=[{"flag": "pal_estado", "valor": "concluido"}, {"flag": "pal_fim", "diferente": True}, {"flag": "baile_inicio", "diferente": True}]))

# =====================================================================
# CAMINHO A — Jehan conta a história do hotel
# =====================================================================
cena("a_jehan", [
    "O bar está quase vazio. Jehan sorri de leve quando você se senta no balcão, e já desliza o copo de sempre.",
    f("jehan", "Você tem cara de quem quer perguntar uma coisa grande. Tente começar pelo pedacinho."),
    f("thiago", "A mulher do piano pediu desculpas. Ela se chama Elisabeta. Eu queria entender quem ela era."),
    n("Ele para de enxugar o copo. “Depois do Homem Lagarto, eu devo muita explicação a você. Mais do que devo a qualquer hóspede.”", se={"flag": "lag_estado", "valor": "venceu"}),
    n("Ele para de enxugar o copo. “Depois do que você viu no corredor, eu devo muita explicação a você.”", se={"flag": "lag_estado", "valor": "lutou"}),
    n("Ele para de enxugar o copo e demora a falar.", se=[{"flag": "lag_estado", "diferente": "venceu"}, {"flag": "lag_estado", "diferente": "lutou"}]),
    f("jehan", "Eu não conto essa história no balcão. A biblioteca está vazia a esta hora. Vem."),
], destino_auto="a_biblioteca",
   chegada={"flags": {"caminho_escolhido": True, "caminho": "A"}, "relacoes": {"jehan": {"afeto": 3}}, "tempo": 10,
            "tirar_marcadores_texto": [{"area": "bar", "texto": "Conversar com Jehan (à noite)"}, {"area": "biblioteca", "texto": "Investigar a história de Elisabeta"}]},
   dados={"raiz": True}, fundo="bar")

_inserir_opcao("bar_base", op("a_jehan_op", "Perguntar a Jehan sobre a mulher do piano", "a_jehan",
    se=[{"flag": "elisabeta_desculpou"}, {"flag": "caminho_escolhido", "diferente": True}, {"flag": "@hora", "min": 19, "max": 21}]))

cena("a_biblioteca", [
    "A biblioteca está iluminada só por duas lâmpadas verdes. Enola está atrás do balcão, com a coruja no ombro, e franze o rosto assim que vê Jehan entrar com você.",
    f("enola", "Senhor Jehan. Isto é uma biblioteca, não um confessionário."),
    f("jehan", "Eu sei. Eu só preciso de uma mesa."),
    f("enola", "Aquilo que o senhor vai contar não deveria ser contado. Mas a casa tem regras que o senhor conhece melhor do que eu."),
    "Ela volta a arrumar livros, de costas, em um silêncio que corta. Você sente que acaba de gastar um pouco da simpatia dela.",
    "Jehan escolhe a mesa mais afastada, olha em volta, e baixa a voz.",
    f("jehan", "O hotel é mais velho do que parece. Antes de ter esse nome, era uma casa de campo de uma família que organizava saraus. Eles recebiam gente de toda parte. Músicos, poetas, forasteiros."),
    f("jehan", "Numa dessas noites, chegou uma pianista. Ninguém sabia de onde. Ela tocou por três horas e ninguém conseguiu aplaudir, de tanto que a música prendia."),
    f("jehan", "Dizem que o dono da casa nunca mais foi o mesmo. Que ela ficou. Que ainda toca. Que a música nunca termina."),
    f("thiago", "Mas ela é filha... não, mãe da Mavis. É o que a Mavis disse. E a esposa do fundador morreu há anos."),
    "Jehan sorri, mas o sorriso não chega aos olhos.",
    f("jehan", "Eu contei o que eu sei. O resto são versões. Tem versão em que ela é a esposa. Tem versão em que não. Se você quer a versão da Mavis, pergunte a ela. Quem sabe, no Baile."),
    f("jehan", "Mas pergunte devagar. Algumas perguntas são feridas que cicatrizaram mal."),
], destino_auto="a_fim",
   chegada={"relacoes": {"enola": {"afeto": -6}, "jehan": {"afeto": 6}}, "barras": {"sanidade": -3}, "tempo": 45}, dados={"raiz": True}, fundo="biblioteca")

cena("a_fim", [
    "Jehan fecha o caderno de pensamentos que não escreveu e acompanha você até a porta da suíte.",
    f("jehan", "Tome cuidado com o que faz com isso. Quando as pessoas aqui sabem demais, começam a procurar demais."),
    pens("A história tinha buracos. Mas os buracos têm formato. Talvez o formato diga mais do que a história."),
    sis("Missão concluída: <b>Os Contos de Jehan</b> (Caminho A). No Baile, você poderá conversar com Mavis sobre a mãe dela."),
    sis("O Baile da Fundação está liberado: vá ao salão de festas quando estiver pronto.", se={"flag": "@baile"}, ao={"marcadores": [{"area": "salao_festas", "texto": "Baile da Fundação"}]}),
], destino_auto="hub_suite14",
   chegada={"flags": {"pos_estado": "concluido", "caminho_fim": "A", "baile_mavis_a": True, "lugar": "suite14"}, "tempo": 15},
   dados={"raiz": True}, fundo="suite14")

# =====================================================================
# CAMINHO B — Enola, Jonathan ou Mavis, Arthur, sala de música, estoque
# =====================================================================
cena("b_enola", [
    "Você chega à biblioteca com uma pergunta guardada no bolso. Enola está atrás do balcão, com a coruja no ombro e um livro aberto.",
    f("thiago", "Enola, eu queria perguntar uma coisa. Sobre a mulher do quadro, no hall. A esposa do fundador."),
    "O livro cai da mão dela e bate na mesa com um estalo seco. A coruja arregala os olhos.",
    f("enola", "Por que o senhor pergunta sobre essa mulher?"),
], opcoes=[
    op("b_curioso", "“Curiosidade. O retrato me chamou a atenção.”", "b_enola2", efeitos={"flags": {"b_vi": False}}),
    op("b_vi", "“Eu a vi. Tocando piano, na sala de música.”", "b_enola2", efeitos={"flags": {"b_vi": True}, "barras": {"suspeita": 3}}),
], dados={"raiz": True}, fundo="biblioteca")

_inserir_opcao("biblioteca_base", op("b_enola_op", "Perguntar a Enola sobre a mulher do quadro", "b_enola",
    se=[{"flag": "elisabeta_desculpou"}, {"flag": "caminho_escolhido", "diferente": True}, {"flag": "@hora", "min": 8, "max": 18}]))

cena("b_enola2", [
    n("Enola dá um passo atrás. “O senhor não deveria. Quem vê aquela mulher, não esquece. E quem esquece, às vezes, é melhor.”", se={"flag": "b_vi", "valor": True}),
    n("Ela aperta os lábios. “Curiosidade é como a fome, senhor Thiago. Dá a impressão de que se resolve comendo.”", se={"flag": "b_vi", "diferente": True}),
    f("enola", "Aquilo que está nos livros foi escrito por quem não viu o que aconteceu. Eu vi. E tenho razões para preferir que essa história durma."),
    f("thiago", "Mas ela me procurou. Ela pediu desculpas. Eu quero saber por quê."),
    "Enola olha para a coruja, como quem pede opinião, e a coruja, claro, não responde.",
    f("enola", "O senhor é teimoso. Eu aprendi a não discutir com gente teimosa. Segunda prateleira à esquerda, atrás do mapa. Um livro de capa cinza, sem título."),
    f("enola", "Eu não vou ajudar a ler. Também não vou impedir."),
    item("livro_elisabeta"),
], destino_auto="b_leitura",
   chegada={"flags": {"caminho_escolhido": True, "caminho": "B"}, "relacoes": {"enola": {"afeto": -6}}, "tempo": 12,
            "tirar_marcadores_texto": [{"area": "biblioteca", "texto": "Investigar a história de Elisabeta"}, {"area": "bar", "texto": "Conversar com Jehan (à noite)"}]},
   dados={"raiz": True}, fundo="biblioteca")

cena("b_leitura", [
    "Você leva o livro cinza para uma mesa no fundo e lê por horas, até a luz amarelar nas janelas.",
    "É uma crônica da casa antiga: um sarau, uma pianista, um casamento com o dono da casa, uma morte que ninguém descreve. Os parágrafos mais importantes foram riscados com tinta preta.",
    "Mas sobram detalhes. Um nome, Elisabeta. Uma filha adotiva. Um retrato pintado dois dias antes da morte.",
    pens("Mavis disse que aquela mulher era a mãe dela. Mas a esposa do fundador morreu há tantos anos que Mavis, pelo rosto, nem deveria ter conhecido."),
    pens("Ou ela conheceu. E eu não sei de quanto tempo estamos falando."),
    "Você junta o que já ouviu antes: a risada de Jonathan, o silêncio de Jehan, o rosto assustado de Elisabeta no quadro. Nada fecha. Tudo se parece.",
    "Alguém precisa explicar isso. Duas pessoas conhecem o assunto de verdade.",
], opcoes=[
    op("b_jon", "Ir atrás de Jonathan, no refeitório", "b_jonathan"),
    op("b_mav", "Ir atrás de Mavis, nos corredores", "b_mavis"),
], chegada={"barras": {"sanidade": -4}, "tempo": 90}, dados={"raiz": True}, fundo="biblioteca")

cena("b_jonathan", [
    "Jonathan está sentado numa mesa do refeitório, conferindo uma lista. Quando vê o livro cinza nas suas mãos, o lápis para no ar.",
    f("thiago", "Jonathan, tem alguma coisa errada nessa história. A esposa do fundador, a Mavis, a Elisabeta. Eu queria que você me explicasse."),
    "Ele fecha a lista, devagar, e olha em volta antes de responder.",
    f("jonathan", "Você é esperto. Mais esperto do que eu imaginei quando te dei a lista de convites."),
    f("jonathan", "Eu posso te explicar. Mas essa explicação tem um preço, Thiago. Você teria que ficar do meu lado no que vier depois do Baile."),
    f("thiago", "Do seu lado em quê?"),
    f("jonathan", "Você vai entender. Quando entender, vai agradecer."),
], opcoes=[
    op("b_jon_sim", "“Estou com você.”", "b_jon_fim", efeitos={"flags": {"b_lado": "jonathan", "jon_aliado": True}, "relacoes": {"jonathan": {"afeto": 10}}}),
    op("b_jon_nao", "“Preciso pensar. Não aceito nada às cegas.”", "b_jon_fim", efeitos={"flags": {"b_lado": "jonathan", "jon_aliado": False}, "relacoes": {"jonathan": {"afeto": -2}}}),
], dados={"raiz": True}, fundo="refeitorio")

cena("b_jon_fim", [
    "Jonathan sorri e dá um tapinha na sua mão sobre a mesa.",
    f("jonathan", "Pense. Você tem até o Baile. A história de Elisabeta é mais feia do que o livro conta. E vai ficar mais feia, se você continuar fuçando sozinho."),
    "Quando ele se levanta, deixa na mesa um guardanapo dobrado. Dentro, escrito à pressa: “Pergunte ao Arthur sobre as cartas.”",
    pens("Ele me mandou para o Arthur. Será por quê?"),
], destino_auto="b_arthur_ponte", chegada={"tempo": 10, "barras": {"suspeita": 3}}, dados={"raiz": True}, fundo="refeitorio")

cena("b_mavis", [
    "Você encontra Mavis ajeitando guirlandas num corredor. Ela sorri ao vê-lo, mas o sorriso some quando repara no livro cinza.",
    f("thiago", "Mavis, desculpa. Eu preciso perguntar. A mulher do quadro, a esposa do fundador, você disse que era sua mãe. Isso não bate com o que está no livro."),
    "Ela desce da escada, devagar, e o silêncio entre vocês dura mais do que deveria.",
    f("mavis", "Você leu isso. Sem me perguntar. Atrás de mim."),
    f("thiago", "Eu... achei que você não ia querer falar."),
    f("mavis", "Você achou. Então não perguntou. Minha mãe não é um tema para livros, Thiago. É a minha mãe."),
    "Os olhos dela brilham, e ela se vira para esconder.",
    f("mavis", "Eu preciso trabalhar."),
], destino_auto="b_arthur_ponte",
   chegada={"flags": {"b_lado": "mavis"}, "relacoes": {"mavis": {"afeto": -10}}, "barras": {"sanidade": -6}, "tempo": 12},
   dados={"raiz": True}, fundo="corredor")

cena("b_arthur_ponte", [
    "Você sabe que não vai conseguir lidar com isso sozinho. Um nome vem à cabeça: Arthur. Ele passa as tardes lendo a história do hotel, e talvez já tenha chegado a esse ponto.",
    sis("Uma nova pista: fale com <b>Arthur</b> na biblioteca.", se={"flag": "arthur_estado", "valor": "concluido"}),
    sis("Arthur ainda não está disponível. Continue explorando o hotel: quando acontecerem mais coisas estranhas, ele vai procurar você.", se={"flag": "arthur_estado", "diferente": "concluido"}),
], destino_auto="hub_corredores",
   chegada={"flags": {"b_arthur_aberto": True, "lugar": "corredores"}, "marcadores": [{"area": "biblioteca", "texto": "Contar a Arthur"}]},
   dados={"raiz": True}, fundo="corredor")

cena("b_arthur", [
    "Arthur ergue os olhos quando você se aproxima com o livro cinza. Os óculos escorregam, e ele os empurra de volta.",
    f("arthur", "Você achou. Eu procurei esse livro por três semanas."),
    f("thiago", "A Enola me deu. Disse que não ia ajudar a ler, nem impedir."),
    f("arthur", "Ela ajuda mais do que parece."),
    n("“O Homem Invisível já fez de tudo para me atrapalhar enquanto eu lia,” você conta. Arthur concorda, sem surpresa: “As ocorrências estão ligadas. Eu tenho mapas.”", se={"flag": "fragmentos", "min": 8}),
    n("Você conta o que o Homem Lagarto fez, e Arthur anota tudo, num ritmo que mal o deixa respirar.", se={"flag": "lag_estado", "valor": "venceu"}),
    n("Você conta o que o Homem Lagarto fez, e Arthur anota tudo, num ritmo que mal o deixa respirar.", se={"flag": "lag_estado", "valor": "lutou"}),
    f("arthur", "Eu quero ver a sala de música com meus olhos. Hoje à noite, depois da meia-noite. Eu bato na sua porta."),
    f("thiago", "É proibido sair depois das dez."),
    f("arthur", "Eu sei. Mas é a única hora em que ela toca de verdade."),
    sis("Arthur vai bater na sua porta à noite. Quando você dormir, ele chamará."),
], destino_auto="biblioteca_base",
   chegada={"flags": {"b_noite": True}, "relacoes": {"arthur": {"afeto": 6}}, "tempo": 20,
            "tirar_marcadores_texto": [{"area": "biblioteca", "texto": "Contar a Arthur"}]},
   dados={"raiz": True}, fundo="biblioteca")

_inserir_opcao("biblioteca_base", op("b_arthur_op", "Mostrar o livro cinza a Arthur", "b_arthur",
    se=[{"flag": "b_arthur_aberto", "valor": True}, {"flag": "b_noite", "diferente": True}, {"flag": "arthur_estado", "valor": "concluido"}]))

# o portão do sono: se a noite do Arthur está marcada, ele bate na porta
cena("dormir_gate3", None, tipo="condicional",
     dados={"flag": "b_noite", "casos": {"true": "b_bate_hora"}, "padrao": "dormiu", "raiz": True})
# se Thiago só vai dormir depois da meia-noite, Arthur bate pouco depois (não no dia seguinte)
cena("b_bate_hora", None, tipo="condicional",
     dados={"flag": "@hora", "casos": {str(h): "b_bate_madrugada" for h in range(0, 6)}, "padrao": "b_bate", "raiz": True})
for c in C:
    if c["id"] == "dormir_gate2":
        c["dados"]["padrao"] = "dormir_gate3"

cena("b_bate", [
    "Algo desperta você no meio da noite. Pouco depois da meia-noite, o corredor é um poço escuro.",
    "Duas batidas leves na porta. Depois uma. Depois, baixinho:",
    f("arthur", "Thiago. Sou eu. Vamos."),
    "Arthur está do outro lado, de casaco, com uma lanterna pequena e os óculos tortos. Ele tem o rosto de quem não dormiu.",
    f("arthur", "Pode vir, tem uma regra para andar à noite: não faça barulho e não olhe para as armaduras."),
], destino_auto="b_musica",
   chegada={"ate": "00:20", "sono": True, "barras": {"cansaco": 30}, "flags": {"b_noite": False, "lugar": "corredores"}}, dados={"raiz": True}, fundo="suite14")

cena("b_bate_madrugada", [
    "Algo desperta você no meio da noite. Pouco depois da meia-noite, o corredor é um poço escuro.",
    "Duas batidas leves na porta. Depois uma. Depois, baixinho:",
    f("arthur", "Thiago. Sou eu. Vamos."),
    "Arthur está do outro lado, de casaco, com uma lanterna pequena e os óculos tortos. Ele tem o rosto de quem não dormiu.",
    f("arthur", "Pode vir, tem uma regra para andar à noite: não faça barulho e não olhe para as armaduras."),
], destino_auto="b_musica",
   chegada={"tempo": 25, "sono": True, "barras": {"cansaco": 20}, "flags": {"b_noite": False, "lugar": "corredores"}}, dados={"raiz": True}, fundo="suite14")

cena("b_musica", [
    "A sala de música está banhada de lua. No piano, sentada de costas, Elisabeta toca uma melodia lenta, que desmancha no meio.",
    "Arthur segura o seu braço e faz sinal de silêncio. Os dois ficam parados na porta, até ela parar de tocar.",
    f("elisabeta", "Vocês vieram. Eu senti."),
    "Ela se vira devagar. Está pálida, de olhos baixos, o vestido branco fora de lugar.",
    f("thiago", "Elisabeta. Eu li o livro. Eu quero entender. Quem era você? O que você era para a Mavis?"),
    f("elisabeta", "Para a Mavis eu era... eu era..."),
    "A palavra não vem. Ela leva a mão ao pescoço, como se procurasse algo que está lá e não está.",
    f("arthur", "O seu nome está num retrato no hall. Há uma data. Dois dias depois, o registro acaba."),
    f("elisabeta", "Não. Não. Dois dias depois. Ninguém registra o que dói."),
    "O piano toca uma nota grave, sozinho. A lâmpada do corredor estala. O rosto dela cai e se repuxa, o cinza sobe pelo pescoço.",
    f("mulher_piano_medo", "NÃO ME PERGUNTEM ISSO."),
    "As teclas explodem em uma dissonância. A porta atrás de vocês bate. O vidro de uma vitrine se parte.",
    f("arthur", "Corre! AGORA!"),
], destino_auto="b_fuga",
   chegada={"barras": {"sanidade": -12, "vida": -10}, "flags": {"confronto_eli": True}, "tempo": 12},
   dados={"raiz": True}, fundo="sala_musica")

cena("b_fuga", [
    "Vocês correm. O corredor é um túnel de vermelho. O piano segue atrás, uma nota por passo, como um cachorro seguindo o cheiro.",
    "Arthur puxa você por uma porta lateral, desce uma escada de serviço e fecha o ferrolho de uma porta de ferro: o estoque.",
    "Dentro, o cheiro de poeira e de papel velho. Caixas empilhadas até o teto, armaduras desmontadas, um espelho coberto por um lençol.",
    "Vocês se agacham atrás de uma pilha de baús. Do outro lado da porta, passos leves. Uma respiração. Algo roça no ferro.",
    "Ela fica ali um longo tempo. Depois, a música se afasta, devagar, nota por nota.",
], destino_auto="b_estoque", chegada={"tempo": 15}, dados={"raiz": True}, fundo="estoque")

cena("b_estoque", [
    "Arthur senta no chão e tira os óculos. As mãos dele tremem.",
    f("arthur", "Ela não é um fantasma, Thiago. Não do jeito que a gente imagina. É uma memória que ficou presa e perdeu a saída."),
    f("thiago", "Ela não queria nos machucar. Quase."),
    f("arthur", "Quase é a palavra mais perigosa que existe."),
    "Vocês ficam ali até o céu clarear por uma fresta no alto. Arthur se levanta primeiro e ajuda você.",
    f("arthur", "Eu volto para a biblioteca. Vou ler o livro de novo. Ela falou de um colar. E tem alguém que sabe muito sobre isso: Jonathan."),
    pens("Jonathan. Outra vez."),
    sis("Missão concluída: <b>A Sala de Música</b> (Caminho B). Arthur e você têm algo em comum agora: um segredo."),
    sis("O Baile da Fundação está liberado: vá ao salão de festas quando estiver pronto.", se={"flag": "@baile"}, ao={"marcadores": [{"area": "salao_festas", "texto": "Baile da Fundação"}]}),
], destino_auto="hub_suite14",
   chegada={"ate": "06:30", "flags": {"pos_estado": "concluido", "caminho_fim": "B", "lugar": "suite14"},
            "relacoes": {"arthur": {"afeto": 10}}, "barras": {"sanidade": -5, "cansaco": -10}},
   dados={"raiz": True}, fundo="estoque")

# =====================================================================
# O BAILE — portão (conteúdo virá no próximo capítulo)
# =====================================================================
cena("baile_entrada", [
    "O salão de festas brilha. Lustres, fitas, uma orquestra sem músicos visíveis. O som de passos e de risos vai tomando todo o ar.",
    "Você respira fundo. Faz sentido que tudo comece e termine aqui.",
    sis("Fim da parte jogável desta versão. O <b>Baile da Fundação</b> será o próximo capítulo. Obrigado por testar! Seu progresso foi salvo."),
], destino_auto="hub_salao_festas", chegada={"flags": {"baile_inicio": True}, "tempo": 5}, dados={"raiz": True}, fundo="salao_festas")

_inserir_opcao("hub_salao_festas", op("baile_op", "Entrar no Baile da Fundação", "baile_entrada",
    se=[{"flag": "@baile"}, {"flag": "baile_inicio", "diferente": True}]))

# =====================================================================
# Pontos de partida (quando o pedido de desculpa termina)
# =====================================================================
for c in C:
    if c["id"] == "desculpas_fim":
        c["chegada"]["flags"]["pos_estado"] = "aberto"
        c["chegada"]["marcadores"] = [
            {"area": "bar", "texto": "Conversar com Jehan (à noite)"},
            {"area": "biblioteca", "texto": "Investigar a história de Elisabeta"},
            {"area": "biblioteca", "texto": "O Senhor Pálido"},
            {"area": "corredores", "texto": "Voltar à clínica (as dores)"}]
        c["narrativa"] = [x for x in c["narrativa"] if not (isinstance(x, dict) and "próximo capítulo" in x.get("texto", ""))]
        c["narrativa"].append(sis("Novas pistas surgiram: a <b>biblioteca</b>, o <b>bar</b> (à noite), a <b>clínica</b> e o <b>Senhor Pálido</b>."))
