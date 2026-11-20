# -*- coding: utf-8 -*-
"""
Gera cenas/ato1_parte2.json: a exploração livre do Ato 1 (Parte 2).
Fatia 1: sistema (noite proibida, fome, cansaço, dormir) + lugares do mapa + Maya + refeitório.
Texto marcado como RASCUNHO no README quando o canon só resume a cena.
"""
import json, sys

def f(q, t, se=None, ao=None):
    d = {"quem": q, "texto": t}
    if se: d["se"] = se
    if ao: d["ao_mostrar"] = ao
    return d
def n(t, se=None, ao=None):
    if se is None and ao is None: return t
    d = {"texto": t}
    if se: d["se"] = se
    if ao: d["ao_mostrar"] = ao
    return d
def pens(t, se=None):
    d = {"estilo": "pensamento", "texto": t}
    if se: d["se"] = se
    return d
def sis(t, se=None, ao=None):
    d = {"estilo": "sistema", "texto": t}
    if se: d["se"] = se
    if ao: d["ao_mostrar"] = ao
    return d
def item(i, se=None):
    d = {"item": i}
    if se: d["se"] = se
    return d
def op(id, texto, destino, efeitos=None, se=None, requisitos=None):
    d = {"id": id, "texto": texto, "destino": destino}
    if efeitos: d["efeitos"] = efeitos
    if se: d["se"] = se
    if requisitos: d["requisitos"] = requisitos
    return d

C = []
def cena(id, narrativa, opcoes=None, destino_auto=None, chegada=None, classe=None, tipo=None, dados=None, fundo=None):
    d = {"id": id}
    if tipo: d["tipo"] = tipo
    if classe: d["classe"] = classe
    if chegada: d["chegada"] = chegada
    if narrativa is not None: d["narrativa"] = narrativa
    if dados: d["dados"] = dados
    if opcoes: d["opcoes"] = opcoes
    if destino_auto: d["destino_auto"] = destino_auto
    if fundo is not None: d["fundo"] = fundo
    C.append(d)

MAPA = op("mapa", "Abrir o mapa", "@mapa")
HUB = {"hub": True}
NOITE = {"flag": "@noite"}
REFEICAO = {"flag": "@refeicao"}
FORA_REFEICAO = {"flag": "@refeicao", "valor": False}

# =====================================================================
# SISTEMA: regras do hotel, corpo (fome, cansaço), sono
# =====================================================================
cena("regra_noite", [
    "Você mal pisa no corredor quando uma figura gigantesca surge no fim dele, a cabeça quase tocando o teto. Um homem enorme, de rosto cheio de cicatrizes, com um terno impecável.",
    "“Hóspedes não circulam depois das dez da noite, senhor.” A voz dele é baixa, educadíssima, e por isso mesmo assusta.",
    "Ele acompanha você de volta até a porta da suíte, sem pressa e sem fazer uma única pergunta.",
    sis("Sua Suspeita aumentou. Respeite os horários do hotel: nada de circular entre 22h e 6h."),
], destino_auto="hub_suite14", chegada={"flags": {"lugar": "suite14"}}, dados={"raiz": True}, fundo="corredor")

cena("alucinacao", None, tipo="sorteio", dados={"raiz": True,
     "opcoes": ["alucinacao_1", "alucinacao_2", "alucinacao_3"]})
cena("alucinacao_1", [
    "O papel de parede se mexe, devagar, como se algo respirasse atrás dele. Você encara por um longo segundo.",
    "Pisca. Tudo volta ao normal.",
    sis("A fome está alta demais e você vê coisas que não existem. Sua Sanidade caiu. Coma algo logo."),
], destino_auto="@hub", chegada={"barras": {"sanidade": -5}}, dados={"raiz": True})
cena("alucinacao_2", [
    "Há um prato fumegante sobre o balcão. O cheiro de pão quente enche o ar, tão real que sua boca chega a salivar.",
    "Você estica a mão. O balcão está vazio.",
    sis("A fome está alta demais e você vê coisas que não existem. Sua Sanidade caiu. Coma algo logo."),
], destino_auto="@hub", chegada={"barras": {"sanidade": -5}}, dados={"raiz": True})
cena("alucinacao_3", [
    "Seus passos ecoam duas vezes. Uma terceira. Alguém caminha logo atrás de você, no mesmo ritmo.",
    "Você se vira de uma vez. Ninguém.",
    sis("A fome está alta demais e você ouve coisas que não existem. Sua Sanidade caiu. Coma algo logo."),
], destino_auto="@hub", chegada={"barras": {"sanidade": -5}}, dados={"raiz": True})

cena("desmaio", [
    "O chão se inclina. O corredor se alonga como um túnel e as bordas da visão escurecem, devagar, até restar nada.",
    "Quando você volta a si, está deitado numa maca, sob uma luz amarelada. Cheiro de álcool e de ervas.",
    "Alguém cuidou de você: há um copo d'água na mesinha e um pedaço de pão sobre um guardanapo. Quando você tenta se levantar, a cabeça gira. Você come e bebe tudo, lentamente.",
    "Ao anoitecer, uma funcionária acompanha você de volta à suíte, em silêncio.",
    sis("Você desmaiou de fome ou de cansaço e foi levado à clínica. Cuide do corpo: coma nos horários e durma."),
], destino_auto="hub_suite14", fundo="clinica",
   chegada={"tempo": 180, "definir": {"fome": 45, "cansaco": 55}, "barras": {"sanidade": -5},
            "flags": {"lugar": "suite14"}}, dados={"raiz": True})

cena("morte_fome", [
    "Você não sente mais o estômago. Nem as mãos. O corredor fica longe, como se você olhasse por um vidro sujo.",
    "Os joelhos cedem. O tapete vem ao seu encontro com uma suavidade que você não esperava.",
    "Ninguém aparece a tempo.",
    "Sua história termina aqui. Lembre-se sempre de comer.",
], dados={"final": True, "raiz": True}, fundo=None)

cena("dormiu", [
    "Você afunda no colchão. O hotel range, respira e ao longe, quase imperceptível, uma música de piano atravessa as paredes.",
    "Quando acorda, a luz da manhã empurra as cortinas. Seu corpo pesa menos.",
    sis("Você dormiu. Cansaço e Sanidade recuperados. A Fome, porém, também cobrou o seu preço durante a noite."),
], destino_auto="hub_suite14", chegada={"ate": "07:00", "sono": True,
   "barras": {"cansaco": 100, "sanidade": 30, "vida": 10}, "flags": {"lugar": "suite14"}},
   dados={"raiz": True}, fundo="suite14")

cena("cochilo", [
    "Você se deita só por um momento e cai num sono leve, sem sonhos.",
    "Quando abre os olhos, algumas horas se foram. Você se sente um pouco melhor.",
], destino_auto="hub_suite14", chegada={"tempo": 180, "sono": True, "barras": {"cansaco": 25, "sanidade": 5}},
   dados={"raiz": True}, fundo="suite14")

# =====================================================================
# LUGARES DO MAPA (cada um é um "hub": o mapa só deixa andar a partir deles)
# =====================================================================
cena("suite_base", [
    "Sua suíte. A cama está arrumada, a janela fechada, e o abajur desenha sombras compridas nas paredes.",
    n("O quarto está em silêncio, mas você tem a sensação de que o hotel inteiro respira do outro lado da porta.", se=NOITE),
    sis("Nova barra: <b>Cansaço</b>. Ela cai com o tempo acordado. Quando chega a zero você desmaia, e dormir é o que a recupera. Dormir também restaura a Sanidade.",
        se={"flag": "tut_cansaco", "valor": True, "diferente": True} if False else {"flag": "tut_cansaco", "diferente": True},
        ao={"flags": {"tut_cansaco": True}, "hud": ["cansaco"]}),
], opcoes=[
    op("pegar_sacola", "Pegar a sacola deixada junto à porta", "ingredientes_recebidos",
       se=[{"flag": "eug_estado", "valor": "ingredientes"}, {"flag": "@dia_passou:ing_dia"}]),
    op("dormir_noite", "Dormir até de manhã", "dormir_gate", se={"flag": "@hora", "min": 19}),
    op("dormir_madrugada", "Dormir até de manhã", "dormir_gate", se={"flag": "@hora", "max": 5}),
    op("cochilar", "Tirar um cochilo (3 horas)", "cochilo", se=[{"flag": "@hora", "min": 6, "max": 18}]),
    MAPA,
], dados=HUB, fundo="suite14")

cena("hub_corredores", [
    "Os corredores dos quartos: tapete vermelho, armaduras vazias alinhadas como sentinelas e portas fechadas, cada uma com um número de bronze.",
    n("A luz é fraca e o silêncio, pesado.", se=NOITE),
    n("Desde ontem, o hotel parece outro: guirlandas escuras, fitas douradas e cartazes do aniversário se espalham por todo canto.", se={"flag": "clinica_ataque"}),
], opcoes=[
    op("morte_levar", "Levar a bandeja ao quarto no fim do corredor", "morte_quarto_cond",
       se={"flag": "morte_estado", "valor": "aceita"}, requisitos={"itens": ["bandeja_morte"]}),
    op("vestido_ir", "Seguir a voz de Gabriel, que acaba de sair do quarto", "vestido_inicio",
       se={"flag": "vestido_estado", "valor": "aberto"}),
    op("mavis_ajudar", "Ajudar a moça que derrubou os papéis", "mavis_oferta",
       se={"flag": "mavis_estado", "valor": "derrubou"}),
    op("nix_falar", "Falar com a camareira que varre o corredor", "nix_oferta",
       se=[{"flag": "lily_conhecida", "valor": True}, {"flag": "nix_estado", "diferente": "pedido"}, {"flag": "nix_estado", "diferente": "concluida"}]),
    op("nix_entregar", "Entregar a vassoura à camareira", "nix_entrega",
       se={"flag": "nix_estado", "valor": "pedido"}, requisitos={"itens": ["vassoura"]}),
    op("vovo_entrar", "Alcançar a senhora que entra no quarto", "vovo_convite",
       se=[{"flag": "jon_estado", "valor": "aceita"}, {"flag": "conv_vovo", "diferente": True}],
       requisitos={"itens": ["convite_vovo"]}),
    MAPA], dados=HUB, fundo="corredor")

cena("biblioteca_base", [
    "A biblioteca. Estantes altas até o teto, escadas de madeira e o cheiro doce de papel antigo. Uma bibliotecária de cabelos brancos arruma livros numa mesa, com uma coruja pequena empoleirada ao lado.",
], opcoes=[
    op("nosf_falar", "Aproximar-se do idoso que lê na mesa afastada", "nosferatu_convite",
       se=[{"flag": "jon_estado", "valor": "aceita"}, {"flag": "conv_biblio", "diferente": True}],
       requisitos={"itens": ["convite_biblioteca"]}),
    op("arthur_falar", "Aproximar-se do rapaz que lê dois diários, sozinho", "arthur_intro",
       se={"flag": "@arthur"}),
    op("enola_salao", "Contar a Enola que as peças estão prontas", "enola_salao",
       se=[{"flag": "mavis_estado", "valor": "entregar"}, {"flag": "salao_liberado", "diferente": True}]),
    MAPA], dados=HUB, fundo="biblioteca")

cena("hub_sala_musica", [
    "A sala de música. O piano de cauda repousa no centro, coberto por uma poeira fina que brilha ao luar. Tudo parece esperar alguém.",
], opcoes=[
    op("invis_convite", "Entrar na sala de onde vem a música", "invisivel_convite",
       se=[{"flag": "jon_estado", "valor": "aceita"}, {"flag": "conv_musica", "diferente": True}],
       requisitos={"itens": ["convite_musica"]}),
    MAPA], dados=HUB, fundo="sala_musica")

# --- hall: Maya e (futuramente) Macha ---
cena("hub_hall", None, tipo="condicional",
     dados={"flag": "maya_vista", "casos": {"true": "hall_base"}, "padrao": "maya_encontro", "raiz": True})

cena("maya_encontro", [
    "Algo roça seu tornozelo, frio como orvalho. Você olha para baixo.",
    "Uma cachorrinha de pelo caramelo, com uma listra branca descendo da testa até o focinho, o peito claro e as patas da frente brancas, salpicadas de pintinhas marrons. As orelhas caem, mansas. Os olhos escuros fitam você com uma ternura que parte o coração.",
    "Mas o pelo dela é translúcido. Através do corpo, você enxerga o desenho do mármore no chão.",
    "Ninguém mais no hall parece vê-la.",
    "Ela encosta o focinho na sua mão. Depois olha para a porta do refeitório, e de novo para você. As costelas aparecem sob o pelo claro.",
    pens("Ela está com fome. E com sede."),
    sis("Dica: no refeitório você pode pegar <b>comida</b> e <b>água</b> para levar. Uma vez por dia você pode dar <b>água</b> a ela, e uma vez por dia, <b>comida</b>. Cada gesto aproxima vocês.",
        ao={"flags": {"maya_vista": True}, "conhece": ["maya"], "hud": ["social"],
            "marcadores": [{"area": "hall", "texto": "Maya está com fome"}]}),
], destino_auto="hall_base", dados={"raiz": True}, fundo="hall")

cena("hall_base", [
    "O hall de entrada. O balcão da recepção, o elevador de grades douradas e, ao fundo, as portas pesadas que dão para o portão. Estão fechadas.",
    n("Desde ontem, o hotel parece outro: guirlandas escuras, fitas douradas e cartazes do aniversário se espalham por todo canto.", se={"flag": "clinica_ataque"}),
    n("Maya cochila aos seus pés, quase invisível à luz do lustre, de barriga cheia e satisfeita.", se=[{"flag": "maya_vista"}, {"flag": "maya_agua_dia", "valor": "@dia"}, {"flag": "maya_comida_dia", "valor": "@dia"}]),
    n("Maya olha para você, esperançosa. Ela já bebeu, mas ainda parece com fome.", se=[{"flag": "maya_vista"}, {"flag": "maya_agua_dia", "valor": "@dia"}, {"flag": "maya_comida_dia", "diferente": "@dia"}]),
    n("Maya olha para você, esperançosa. Ela já comeu, mas ainda parece com sede.", se=[{"flag": "maya_vista"}, {"flag": "maya_comida_dia", "valor": "@dia"}, {"flag": "maya_agua_dia", "diferente": "@dia"}]),
    n("Maya olha para você, esperançosa. Você não tem o que oferecer a ela.", se=[{"flag": "maya_vista"}, {"flag": "maya_agua_dia", "diferente": "@dia"}, {"flag": "maya_comida_dia", "diferente": "@dia"}]),
], opcoes=[
    op("maya_dar_agua", "Dar água à Maya", "maya_bebe",
       se=[{"flag": "maya_vista"}, {"flag": "maya_agua_dia", "diferente": "@dia"}],
       requisitos={"itens": ["agua"]}),
    op("maya_dar_comida", "Dar comida à Maya", "maya_come",
       se=[{"flag": "maya_vista"}, {"flag": "maya_comida_dia", "diferente": "@dia"}],
       requisitos={"itens": ["marmita"]}),
    op("macha_sair", "Tentar sair pelo portão", "macha_porta"),
    MAPA,
], dados=HUB, fundo="hall")

cena("maya_bebe", [
    "Você se agacha e derrama um pouco de água na tampa da garrafa, bem perto do focinho dela.",
    "Maya bebe com pressa, depois devagar, e levanta os olhos escuros para você. Parece dizer obrigada do único jeito que sabe.",
    sis("Sua relação com <b>Maya</b> aumentou. Uma vez por dia você pode dar água a ela, e uma vez por dia, comida."),
], destino_auto="hall_base",
   chegada={"tirar_itens": ["agua"], "flags": {"maya_agua_dia": "@dia"},
            "relacoes": {"maya": {"afeto": 5}}, "tempo": 5, "barras": {"sanidade": 1},
            "tirar_marcadores": ["hall"]}, dados={"raiz": True}, fundo="hall")

cena("maya_come", [
    "Você se agacha e abre a marmita no chão, perto do focinho dela.",
    "Maya cheira, hesita, e então come com cuidado, como quem não quer incomodar. Depois lambe a sua mão, e a sensação é de uma brisa fria e boa.",
    "Quando ela se deita ao seu lado, de barriga cheia, o hall parece menos frio.",
    sis("Sua relação com <b>Maya</b> aumentou."),
], destino_auto="hall_base",
   chegada={"tirar_itens": ["marmita"], "flags": {"maya_comida_dia": "@dia"},
            "relacoes": {"maya": {"afeto": 8}}, "tempo": 8, "barras": {"sanidade": 2},
            "tirar_marcadores": ["hall"]}, dados={"raiz": True}, fundo="hall")

# --- refeitório ---
cena("hub_refeitorio", [
    n("O refeitório recende a pão quente e café. Mesas compridas, toalhas brancas, vapor subindo das travessas.", se=REFEICAO),
    n("O refeitório está quase vazio. As mesas foram postas, mas a comida do próximo horário ainda não chegou. A água do bebedouro, essa sim, está sempre ali.", se=FORA_REFEICAO),
    n("Você já comeu neste horário. Os pratos vão sendo recolhidos.", se=[REFEICAO, {"flag": "comeu_turno", "valor": "@turno"}]),
    n("Desde ontem, o hotel parece outro: guirlandas escuras, fitas douradas e cartazes do aniversário se espalham por todo canto.", se={"flag": "clinica_ataque"}),
], opcoes=[
    op("comer", "Fazer uma refeição", "refeicao", se=[REFEICAO, {"flag": "comeu_turno", "diferente": "@turno"}]),
    op("jon_falar", "Falar com Jonathan, que corre entre as mesas", "jonathan_oferta",
       se={"flag": "jon_estado", "diferente": "aceita"} if False else [{"flag": "jon_estado", "diferente": "aceita"}, {"flag": "jon_estado", "diferente": "recusada"}, {"flag": "jon_estado", "diferente": "concluida"}]),
    op("jon_voltar", "Procurar Jonathan para contar sobre os convites", "jonathan_conclusao",
       se=[{"flag": "jon_estado", "valor": "aceita"}, {"flag": "convites", "valor": 3}]),
    op("eug_falar", "Falar com a senhora de avental, sentada a uma mesa", "eugenie_primeira",
       se=[{"flag": "@propostas"}, {"flag": "eug_estado", "diferente": "ingredientes"}, {"flag": "eug_estado", "diferente": "levar"}, {"flag": "eug_estado", "diferente": "concluida"}]),
    op("morte_falar", "Falar com a moça de preto, de cabelos longos, que não come nada", "morte_pedido",
       se=[{"flag": "@propostas"}, {"flag": "morte_estado", "diferente": "aceita"}, {"flag": "morte_estado", "diferente": "concluida"}]),
    op("eug_voltar", "Entregar os ingredientes a Eugénie", "eugenie_aula",
       se={"flag": "eug_estado", "valor": "levar"}, requisitos={"itens": ["ingredientes"]}),
    op("cozinhar", "Preparar uma refeição simples (Cozinha Básica)", "cozinhou",
       se=[{"flag": "cozinha_basica"}, {"flag": "@refeicao", "valor": False}, {"flag": "cozinhou_dia", "diferente": "@dia"}],
       requisitos={"itens": ["ingredientes"]}),
    op("levar_comida", "Pegar uma marmita para levar", "pegou_marmita", se=[REFEICAO, {"flag": "marmita_turno", "diferente": "@turno"}], requisitos={"sem_itens": ["marmita"]}),
    op("levar_agua", "Pegar uma garrafa d'água", "pegou_agua", requisitos={"sem_itens": ["agua"]}),
    MAPA,
], dados=HUB, fundo="refeitorio")

cena("refeicao", [
    "Você se serve de pão, ovos, uma sopa grossa e uma xícara de algo quente. Come sem pressa, ouvindo os murmúrios das outras mesas.",
], destino_auto="@hub", chegada={"tempo": 35, "barras": {"fome": 55, "sanidade": 2}, "flags": {"comeu_turno": "@turno"}}, dados={"raiz": True}, fundo="refeitorio")
cena("pegou_marmita", [
    "Uma atendente de olhos fundos embrulha pão, queijo e um pedaço de torta numa marmita de papel encerado. Ela não diz nada, apenas empurra o embrulho na sua direção.",
    item("marmita"),
], destino_auto="@hub", chegada={"tempo": 3, "flags": {"marmita_turno": "@turno"}}, dados={"raiz": True}, fundo="refeitorio")
cena("pegou_agua", [
    "Você enche uma garrafa de vidro no bebedouro de bronze. A água é gelada e tem um leve gosto de pedra.",
    item("agua"),
], destino_auto="@hub", chegada={"tempo": 2}, dados={"raiz": True}, fundo="refeitorio")


# =====================================================================
# MACHA — "Onde Você Pensa Que Vai"  (bloqueio permanente do portão)
# =====================================================================
cena("macha_porta", None, tipo="condicional",
     dados={"flag": "macha_conhecida", "casos": {"true": "macha_de_novo"}, "padrao": "macha_primeira", "raiz": True})

cena("macha_primeira", [
    "Você empurra uma das portas pesadas. Ela cede um palmo, e o ar frio da noite entra pela fresta.",
    "Um rugido de motor rasga o hall. Uma moto preta, que você jurava não estar ali, derrapa até parar entre você e a porta.",
    "Quem desce dela é uma garota de jaqueta de couro, capacete debaixo do braço, cabelos negros e longos e olhos de um castanho quase vermelho. Ela sorri com dentes perfeitos, e o sorriso não é exatamente amistoso.",
    f("macha", "Onde você pensa que vai?"),
    f("thiago", "Eu só queria procurar o Cocheiro. Ele me trouxe até aqui, e eu..."),
    f("macha", "O Cocheiro? Ele é amigo do meu pai. E o meu pai trabalha aqui, então eu cresci neste hotel. Ninguém sai por essa porta sem eu saber."),
    f("macha", "Aliás, você nem sabe dirigir, sabe? Dá para ver na sua cara."),
    f("thiago", "Eu... não. Nunca tive ninguém para me ensinar."),
    f("macha", "Hum. Órfão, então."),
    "Ela gira o capacete nas mãos e olha para você de cima a baixo, avaliando.",
    f("macha", "Quando a garagem e o resto do hotel estiverem abertos, eu posso te ensinar. Mas até lá, a porta fica fechada. Combinado?"),
], opcoes=[
    op("macha_aceita", "“Combinado. Eu adoraria aprender.”", "macha_aceitou",
       efeitos={"flags": {"macha_conhecida": True, "macha_missao": "aceita"}, "relacoes": {"macha": {"afeto": 8}},
                "conhece": ["macha"], "tempo": 5}),
    op("macha_agora_nao", "“Por enquanto, só queria passar.”", "macha_negou",
       efeitos={"flags": {"macha_conhecida": True}, "conhece": ["macha"], "tempo": 5}),
], dados={"raiz": True}, fundo="hall")

cena("macha_aceitou", [
    f("macha", "Boa. Todo mundo devia saber pilotar alguma coisa."),
    "Ela sobe na moto e acelera uma vez, só de exibição, e a máquina desaparece no escuro do corredor lateral como se nunca tivesse existido.",
    sis("Missão secundária registrada: <b>Onde Você Pensa Que Vai</b>. Macha vai ensinar você a dirigir quando o hotel e a garagem estiverem abertos. Enquanto isso, ela vigia o portão."),
], destino_auto="hub_hall", dados={"raiz": True}, fundo="hall")

cena("macha_negou", [
    f("macha", "Pode ser. Mas a porta continua fechada, e eu continuo aqui."),
    "Ela dá um sorriso de lado, monta na moto e desaparece pelo corredor lateral num ronco abafado.",
    sis("Macha vigia o portão. Se você mudar de ideia, fale com ela de novo."),
], destino_auto="hub_hall", dados={"raiz": True}, fundo="hall")

cena("macha_de_novo", [
    "Você mal encosta na porta e o ronco da moto vem do nada. Macha aparece ao seu lado, com o capacete na mão.",
    f("macha", "Onde você pensa que vai?", ),
    f("macha", "Já falei: a porta continua fechada. Mas eu ainda estou esperando você dizer que quer aprender a dirigir.", se={"flag": "macha_missao", "diferente": "aceita"}),
    f("macha", "Fique tranquilo. Quando a garagem abrir, eu te chamo.", se={"flag": "macha_missao", "valor": "aceita"}),
], opcoes=[
    op("macha_agora_sim", "“Quero aprender, sim.”", "macha_aceitou", se={"flag": "macha_missao", "diferente": "aceita"},
       efeitos={"flags": {"macha_missao": "aceita"}, "relacoes": {"macha": {"afeto": 3}}}),
    op("macha_ok", "Voltar para o hall", "hub_hall", efeitos={"tempo": 2}),
], chegada={"relacoes": {"macha": {"afeto": -3}}}, dados={"raiz": True}, fundo="hall")

# =====================================================================
# JONATHAN — os três convites da festa
# =====================================================================
cena("jonathan_oferta", [
    "Jonathan atravessa o refeitório quase correndo, uma prancheta numa mão e uma pilha de papéis na outra. Quando vê você, ele estanca.",
    f("jonathan", "Thiago! Que sorte a minha. Você tem um minuto? Bem, tem que ter."),
    f("jonathan", "O hotel vai fazer uma festa de aniversário em breve. Uma data muito importante para o fundador, e eu... esqueci de entregar três convites especiais. Três! Se eu for atrás de cada um, perco o dia."),
    f("jonathan", "Você poderia levar? Um para a sala de música, um para a biblioteca e um para uma senhora num dos quartos do corredor. É só entregar. Eu te agradeceria muito."),
], opcoes=[
    op("jon_aceita", "“Claro, eu levo.”", "jonathan_aceitou",
       efeitos={"flags": {"jon_estado": "aceita", "convites": 0}, "relacoes": {"jonathan": {"afeto": 8}},
                "itens": ["convite_musica", "convite_biblioteca", "convite_vovo"],
                "mapa": ["sala_musica"],
                "marcadores": [{"area": "sala_musica", "texto": "Convite"},
                               {"area": "biblioteca", "texto": "Convite"},
                               {"area": "corredores", "texto": "Convite"}],
                "conhece": ["jonathan"], "tirar_marcadores": ["refeitorio"], "tempo": 5}),
    op("jon_recusa", "“Desculpe, não posso agora.”", "jonathan_recusou",
       efeitos={"flags": {"jon_estado": "recusada"}, "relacoes": {"jonathan": {"afeto": -8}},
                "tirar_marcadores": ["refeitorio"], "tempo": 3}),
], dados={"raiz": True}, fundo="refeitorio")

cena("jonathan_aceitou", [
    "Jonathan solta o ar como quem tirou um piano das costas.",
    f("jonathan", "Obrigado, de verdade. Os convites são estes."),
    item("convite_musica"), item("convite_biblioteca"), item("convite_vovo"),
    f("jonathan", "Na sala de música, ao Homem das Faixas. Na biblioteca, a um senhor que tem o hábito de se esconder na sombra das estantes. E a Vovó... qualquer porta de quarto no corredor onde a lareira fica acesa."),
    sis("Missão: <b>Os Três Convites</b>. Pontos de exclamação apareceram no mapa."),
], destino_auto="@hub", dados={"raiz": True}, fundo="refeitorio")

cena("jonathan_recusou", [
    f("jonathan", "Ah... entendo. Cada um tem o seu dia, imagino."),
    "Ele força um sorriso, ajeita a pilha de papéis e se afasta, apressado. Não olha para trás.",
    sis("Você recusou a missão de Jonathan. Ela se perdeu para sempre e a relação com ele diminuiu."),
], destino_auto="@hub", dados={"raiz": True}, fundo="refeitorio")

cena("jonathan_conclusao", [
    "Jonathan está de pé numa cadeira, pendurando uma guirlanda de papel. Ao ver você, quase cai.",
    f("jonathan", "Os três? Você entregou os três? Thiago, eu poderia te abraçar. Não vou, porque tenho vergonha."),
    f("jonathan", "Fique com isto. É pouco, mas a festa vai ser inesquecível, e você vai estar nela."),
    sis("Missão <b>Os Três Convites</b> concluída. Sua relação com Jonathan aumentou."),
], destino_auto="@hub",
   chegada={"flags": {"jon_estado": "concluida"}, "relacoes": {"jonathan": {"afeto": 10}},
            "barras": {"sanidade": 5}, "tirar_marcadores": ["refeitorio"], "tempo": 5},
   dados={"raiz": True}, fundo="refeitorio")

# --- convite 1: sala de música (Homem Invisível) ---
cena("invisivel_convite", [
    "Há música no ar: um disco antigo gira num toca-discos apoiado no piano, e uma poltrona de couro está virada para a janela. Dela se ergue uma mão enluvada, marcando o compasso.",
    "Quando a poltrona gira, você vê o dono da mão: um homem inteiro enrolado em faixas, de óculos escuros, sobretudo comprido e chapéu de aba larga. Nem um centímetro de pele aparece.",
    f("homem_invisivel", "Um hóspede! Que honra. Faz tempo que ninguém me interrompe com tanta educação."),
    f("thiago", "Desculpe incomodar. Tenho um convite do Jonathan, para a festa de aniversário."),
    f("homem_invisivel", "Festa. Que ideia sedutora. Música, gente, copos, tudo aquilo que não combina com bandagens."),
    "Ele pega o envelope com dois dedos, examina-o com a atenção de quem enxerga muito bem através das lentes escuras e o guarda no bolso do sobretudo.",
    f("thiago", "O senhor... se machucou?"),
    f("homem_invisivel", "Ah, as faixas. Um acidente, claro. Eu escorreguei numa banheira. Ou foi uma explosão no laboratório? Não, espere, foi um duelo. Sim, um duelo. Perdi."),
    f("homem_invisivel", "Ou talvez tenha sido uma queda de cavalo. Escolha a versão de que mais gostar, meu jovem. Todas têm a mesma quantidade de verdade."),
    f("thiago", "Isso... não faz sentido."),
    f("homem_invisivel", "Exatamente! Agora vá, vá. O disco está chegando na parte boa."),
    "Você se vira para sair. Na porta, ouve a voz dele de novo, mas agora ela parece vir da direita, perto da janela, quando a poltrona está à sua esquerda.",
    f("homem_invisivel", "Passe bem, Thiago. E cuidado com os corredores."),
    pens("Eco da sala. Só pode ser a acústica. Salas de música têm esse efeito."),
], destino_auto="hub_sala_musica",
   chegada={"flags": {"conv_musica": True}, "somar": {"convites": 1, "fragmentos": 1},
            "tirar_itens": ["convite_musica"], "relacoes": {"homem_invisivel": {"afeto": 3}},
            "conhece": ["homem_invisivel"], "tirar_marcadores": ["sala_musica"], "barras": {"sanidade": -2}, "tempo": 10},
   dados={"raiz": True}, fundo="sala_musica")

# --- convite 2: biblioteca (Nosferatu) ---
cena("nosferatu_convite", [
    "Numa mesa de leitura afastada, sob uma lâmpada de abajur verde, um homem muito idoso lê, com um livro tão grande que quase cobre o rosto. A pele dele é de uma palidez de cera, o crânio é liso, e as mãos têm dedos finos demais para a idade que aparenta.",
    "Quando você se aproxima, ele fecha o livro com um estalo seco, antes que você possa ver uma única palavra da capa.",
    f("nosferatu", "Pois não, jovem. Você é o hóspede novo."),
    f("thiago", "Sou. Meu nome é Thiago. Tenho um convite do Jonathan para o aniversário do hotel."),
    "Ele toma o envelope com as pontas dos dedos e o examina com um interesse calmo, quase afável.",
    f("nosferatu", "O aniversário do fundador. Faz muito tempo que não vou a uma festa dessas. Talvez eu apareça. Talvez."),
    f("nosferatu", "Diga-me, o que um rapaz tão jovem veio fazer num hotel como este?"),
    f("thiago", "Trabalhar e... descobrir, acho."),
    f("nosferatu", "Descobrir. Que palavra otimista. Aqui todos me chamam de Senhor Pálido, e eu nunca discuti. Pode me encontrar por aqui, na maioria das tardes."),
    "A conversa acabou. Ele abre o livro, de novo, e você nem percebe quando foi dispensado.",
], destino_auto="hub_biblioteca",
   chegada={"flags": {"conv_biblio": True}, "somar": {"convites": 1}, "tirar_itens": ["convite_biblioteca"],
            "relacoes": {"nosferatu": {"afeto": 4}}, "conhece": ["nosferatu"],
            "tirar_marcadores": ["biblioteca"], "tempo": 10},
   dados={"raiz": True}, fundo="biblioteca")

# --- convite 3: Vovó ---
cena("vovo_convite", [
    "Mais adiante no corredor, uma porta se abre sozinha e uma senhora minúscula, de xale cinza e cabelos de algodão, entra devagar num dos quartos, apoiada numa bengala.",
    f("thiago", "Com licença! A senhora tem um minuto?"),
    "Ela se volta com uma lentidão paciente e sorri. Os olhos são pequenos e muito vivos.",
    f("vovo", "Ora, um rapaz novo. Eu sou a Vovó. Assim todo mundo me chama, e já não me lembro se tive outro nome."),
    f("thiago", "Tenho um convite do Jonathan, para a festa de aniversário do hotel."),
    f("vovo", "Que gentileza. Dê aqui, querido."),
    "Ela lê o envelope sem pressa, movendo os lábios, e o guarda no bolso do xale.",
    f("vovo", "Eu moro aqui há muito tempo. Conheço quase todo mundo, e todo mundo me conhece. Vou, sim, com muito prazer. Obrigada por se lembrar de uma velha."),
    f("vovo", "Agora entre aí na sua vida e coma alguma coisa. Está magrinho."),
    "Ela entra no quarto e fecha a porta com um clique delicado.",
], destino_auto="hub_corredores",
   chegada={"flags": {"conv_vovo": True}, "somar": {"convites": 1}, "tirar_itens": ["convite_vovo"],
            "relacoes": {"vovo": {"afeto": 5}}, "conhece": ["vovo"],
            "tirar_marcadores": ["corredores"], "tempo": 8},
   dados={"raiz": True}, fundo="corredor")

# =====================================================================
# HOMEM INVISÍVEL — travessuras aleatórias ao andar pelo hotel
# (cada uma soma 1 fragmento; o Thiago não sabe quem faz)
# =====================================================================
def evento(id, areas, texto, fundo_, extra=None):
    ef = {"somar": {"fragmentos": 1}, "barras": {"sanidade": -2}, "tempo": 3}
    cena(id, texto, destino_auto="@hub", chegada=ef,
         dados={"evento_invisivel": {"areas": areas}, "raiz": True}, fundo=fundo_)

evento("ev_porta", ["corredores", "hall", "biblioteca"], [
    "Uma porta bate atrás de você, forte o bastante para fazer o chão vibrar. Você se vira.",
    "Ninguém. A maçaneta ainda balança de leve, como se tivesse acabado de ser solta.",
    pens("Corrente de ar. Só pode ser."),
    "Mas todas as janelas do corredor estão fechadas.",
], "corredor")
evento("ev_risada", ["corredores", "refeitorio", "sala_musica"], [
    "Uma risada baixa, quase um suspiro, passa rente à sua nuca. Seus pelos se eriçam.",
    "Você gira o corpo. Só o tapete, as armaduras e o silêncio de sempre.",
    pens("Alguém riu de mim. Alguém estava aqui."),
], "corredor")
evento("ev_objeto", ["refeitorio", "biblioteca", "hall"], [
    "Sobre a mesa mais próxima, uma colher flutua uns dois palmos no ar. Gira devagar, quase preguiçosa.",
    "Quando você pisca, ela cai com um tilintar. Um rapaz de olhos fundos numa mesa vizinha olha para você e dá de ombros, como quem diz que aqui isso é normal.",
    pens("Aqui, aparentemente, objetos fazem o que querem."),
], "refeitorio")
evento("ev_sussurro", ["biblioteca", "sala_musica", "corredores"], [
    "“Você não pertence a este lugar.”",
    "A frase é dita tão perto que você sente o ar morno de uma respiração. Você congela. Ninguém ao redor tem lábios que se movam.",
    pens("Eu ouvi isso. Eu ouvi isso, não ouvi?"),
], "biblioteca")

# =====================================================================
# MAVIS — "Não Era o que Eu Pedi"  +  ESTOQUE  +  SALÃO DE FESTAS
# =====================================================================
cena("hub_biblioteca", None, tipo="condicional",
     dados={"flag": "enola_conhecida", "casos": {"true": "biblioteca_base"}, "padrao": "biblioteca_primeira", "raiz": True})

cena("biblioteca_primeira", [
    "A porta da biblioteca se abre antes de você tocá-la. Uma moça de cabelos escuros e olhos claros sai atropelando o ar, os braços carregados de livros, cartas e envelopes que ameaçam escorregar a cada passo.",
    f("mavis", "Desculpa, desculpa, desculpa! Estou atrasadíssima!"),
    "Ela quase tromba em você, equilibra a pilha com o queixo e aponta com a cabeça para dentro da sala.",
    f("mavis", "Você deve ser o Thiago. Eu sou a Mavis. Aquela é a Enola, a bibliotecária-chefe. Ela te mostra tudo. Preciso correr!"),
    "E corre mesmo. O som dos passos some pelo corredor, junto com uma bronca em voz baixa contra o relógio.",
    "Dentro, uma névoa branca paira entre as estantes mais altas. Aos poucos ela se condensa em uma bibliotecária de cabelos prateados, com uma coruja pequena no ombro.",
    f("enola", "Seja bem-vindo à biblioteca, senhor Thiago. Os livros comuns estão à sua disposição. Os outros, por ora, preferem ficar quietos."),
    f("enola", "A senhorita Mavis anda sobrecarregada. Se encontrá-la no corredor, talvez valha a pena oferecer ajuda."),
], destino_auto="biblioteca_base",
   chegada={"flags": {"enola_conhecida": True, "mavis_estado": "derrubou"},
            "conhece": ["mavis", "enola"], "tirar_marcadores": ["biblioteca"],
            "marcadores": [{"area": "corredores", "texto": "Mavis precisa de ajuda"}], "tempo": 6},
   dados={"raiz": True}, fundo="biblioteca")

cena("mavis_oferta", [
    "No fim do corredor, a pilha que Mavis levava terminou de desabar. Papéis, cartas e dois livros grossos formam um tapete de caos diante das armaduras.",
    f("mavis", "Não acredito. Eu tinha tudo organizado. Tinha!"),
    "Você se agacha e começa a juntar as folhas. Ela suspira de alívio.",
    f("mavis", "Obrigada. Você é o hóspede novo, né? Olha, vou ser sincera: preciso de ajuda de verdade."),
    f("mavis", "O hotel vai fazer o Baile da Fundação, e a decoração é comigo. Preciso de seis peças guardadas no estoque. Eu mesma iria, mas tenho mil coisas a resolver. Você poderia buscar?"),
    f("mavis", "Eu não sei explicar direito quais são. Você vai ver e escolhe o que achar que combina. Confio no seu bom gosto."),
], opcoes=[
    op("mavis_aceita", "“Pode deixar, eu busco.”", "mavis_aceitou",
       efeitos={"flags": {"mavis_estado": "estoque"}, "relacoes": {"mavis": {"afeto": 8}},
                "mapa": ["estoque"], "tirar_marcadores": ["corredores"],
                "marcadores": [{"area": "estoque", "texto": "Decoração da Mavis"}], "tempo": 5}),
    op("mavis_recusa", "“Desculpe, hoje não consigo.”", "mavis_recusou",
       efeitos={"flags": {"mavis_estado": "recusada"}, "relacoes": {"mavis": {"afeto": -8}},
                "tirar_marcadores": ["corredores"], "tempo": 3}),
], dados={"raiz": True}, fundo="corredor")

cena("mavis_aceitou", [
    f("mavis", "Você é um anjo. Ou algo parecido. O estoque fica na ala dos fundos, pelo mapa. Eu aviso o responsável que você vai."),
    sis("Missão: <b>Não Era o que Eu Pedi</b>. O <b>estoque</b> foi liberado no mapa. Escolha seis peças de decoração."),
], destino_auto="hub_corredores", dados={"raiz": True}, fundo="corredor")

cena("mavis_recusou", [
    f("mavis", "Tudo bem. Eu me viro. Sempre me viro."),
    "Ela recolhe o resto dos papéis em silêncio e sai, mais devagar do que veio.",
    sis("Você recusou a missão de Mavis. Ela se perdeu para sempre e a relação com ela diminuiu."),
], destino_auto="hub_corredores", dados={"raiz": True}, fundo="corredor")

# --- estoque ---
cena("hub_estoque", [
    "O estoque ocupa um galpão enorme nos fundos, com prateleiras de ferro até o teto e um cheiro de poeira, cera e naftalina. Caixas etiquetadas à mão se empilham em corredores estreitos.",
    n("Dos fundos ecoa um barulho de caixas, como se algo mudasse de lugar sozinho.", se={"flag": "invisivel_ativo"}),
], opcoes=[
    op("estoque_decoracao", "Procurar peças de decoração para Mavis", "estoque_escolha",
       se={"flag": "mavis_estado", "valor": "estoque"}),
    op("estoque_vassoura", "Procurar uma vassoura para a camareira", "estoque_vassoura",
       se={"flag": "nix_estado", "valor": "pedido"}, requisitos={"sem_itens": ["vassoura"]}),
    MAPA,
], dados=HUB, fundo="estoque")

CATALOGO = [
 ("baloes","Balões pretos, vermelhos, dourados e brancos","alegre"),
 ("fitas","Rolos de fitas de cetim","elegante"),
 ("cartolinas","Cartolinas e papéis para placas","alegre"),
 ("globo","Globo musical luminoso","estranho"),
 ("vassoura_dec","Vassoura de palha","estranho"),
 ("purpurina","Potes de purpurina","alegre"),
 ("recortes","Recortes de morcegos, luas, torres e castelos","gotico"),
 ("velas","Caixa de velas ornamentais","gotico"),
 ("candelabros","Candelabros antigos","historico"),
 ("flores","Flores artificiais vermelhas, brancas e negras","gotico"),
 ("luzes","Cordões de luzes","alegre"),
 ("mascaras","Máscaras de baile","elegante"),
 ("toalhas","Toalhas de mesa bordadas","elegante"),
 ("veludo","Cortinas e tecidos de veludo","elegante"),
 ("bandeirolas","Bandeirolas antigas","historico"),
 ("confetes","Caixa de confetes","alegre"),
 ("sinos","Pequenos sinos decorativos","estranho"),
 ("miniaturas","Miniaturas das cinco torres, muralhas e portão","historico"),
 ("livro_msgs","Livro de mensagens da festa","historico"),
 ("tacas","Taças ornamentais","elegante"),
 ("lanternas","Lanternas de papel","alegre"),
 ("retratos","Retratos antigos","historico"),
 ("penas","Caixa de penas coloridas","estranho"),
 ("faixas","Faixas com o nome Hotel Los Segredos","historico"),
 ("fumaca","Máquina de fumaça","gotico"),
]

cena("estoque_escolha", [
    "Um bilhete preso à porta, com a letra apressada de Mavis, diz apenas: “6 peças. Você vai saber.”",
    "Entre as prateleiras, algumas caixas parecem se destacar das outras, como se esperassem ser escolhidas.",
    pens("Seis peças. Não sei o que ela quer. Vou ter que confiar no meu gosto."),
], tipo="selecao", dados={
    "catalogo": [{"id": i, "nome": nm, "estilo": est} for i, nm, est in CATALOGO],
    "sortear": 10, "sortear_extra": {"flag": "nix_estado", "valor": "concluida", "mais": 4},
    "escolher": 6, "flag_sorteio": "estoque_sorteio", "prefixo": "dec_", "flag_estilo": "decoracao_estilo",
    "efeitos": {"flags": {"mavis_estado": "entregar"}, "tempo": 20,
                "tirar_marcadores": ["estoque"], "marcadores": [{"area": "biblioteca", "texto": "Voltar a Enola"}]},
    "destino": "estoque_levou", "raiz": True}, fundo="estoque")

cena("estoque_levou", [
    "Você fecha a caixa e a ergue nos braços. É mais pesada do que parece.",
    n("Um dos retratos antigos dentro da caixa parece acompanhar você com os olhos. Você prefere não olhar de novo.", se={"flag": "dec_retratos"}),
    n("Um dos sininhos tilinta sozinho, sem vento, e para.", se={"flag": "dec_sinos"}),
    n("O globo musical acende por um segundo e solta duas notas de uma melodia que você não reconhece.", se={"flag": "dec_globo"}),
    n("A vassoura de palha parece ter mudado de lugar dentro da caixa. Você tem quase certeza de que ela estava do outro lado.", se={"flag": "dec_vassoura_dec"}),
    sis("As peças são encantadas: o que acontece com elas não vem do Homem das Faixas.", se={"flag": "dec_retratos"}),
], destino_auto="hub_estoque", chegada={"barras": {"sanidade": -2}, "mapa": [], "tempo": 3},
   dados={"raiz": True}, fundo="estoque")

cena("enola_salao", [
    f("enola", "O senhor voltou do estoque? E está carregando uma caixa. Que pontualidade."),
    f("thiago", "Estou procurando a Mavis para entregar isto."),
    f("enola", "A senhorita Mavis foi ao salão de festas. É lá que o baile será montado."),
    n("Você franze a testa e pensa na sala do piano, no escuro, ao luar.", se={"flag": "conheceu_elisabeta", "valor": True}),
    f("thiago", "A sala de música?", se={"flag": "conheceu_elisabeta", "valor": True}),
    f("enola", "Não, senhor Thiago. O salão de festas. São lugares bem diferentes.", se={"flag": "conheceu_elisabeta", "valor": True}),
    sis("O <b>salão de festas</b> foi liberado no mapa."),
], destino_auto="biblioteca_base",
   chegada={"flags": {"salao_liberado": True}, "mapa": ["salao_festas"],
            "tirar_marcadores": ["biblioteca"], "marcadores": [{"area": "salao_festas", "texto": "Entregar a decoração"}], "tempo": 4},
   dados={"raiz": True}, fundo="biblioteca")

cena("hub_salao_festas", [
    "O salão de festas é um espaço imenso, de teto alto e piso quadriculado, com lustres cobertos por panos. Cadeiras se empilham contra as paredes e uma escada de armar espera no centro.",
], opcoes=[
    op("mavis_entregar", "Entregar a caixa a Mavis", "mavis_entrega",
       se={"flag": "mavis_estado", "valor": "entregar"}),
    MAPA,
], dados=HUB, fundo="salao_festas")

cena("mavis_entrega", [
    "Mavis está de pé numa escada, tentando prender uma faixa no alto. Quando vê você, quase a derruba.",
    f("mavis", "Você voltou! Deixa eu ver, deixa eu ver..."),
    "Ela abre a caixa, tira uma peça, outra, e vai franzindo a testa.",
    f("mavis", "Hum. Interessante. Não era exatamente o que eu pedi. Mas..."),
    "Um sino bate no alto do hotel, longo e grave. Mavis olha para o relógio e engole em seco.",
    f("mavis", "Acabou o prazo. Tudo bem, a gente improvisa. Eu gostei, na verdade. De um jeito estranho."),
    n("Ela passa a mão por um tecido de veludo e sorri. Tem algo elegante no jeito como as peças se completam.", se={"flag": "decoracao_estilo", "valor": "elegante"}),
    n("Ela ri alto, sacode um punhado de confete e o salão inteiro parece mais leve. A festa vai ser alegre.", se={"flag": "decoracao_estilo", "valor": "alegre"}),
    n("Ela ergue um candelabro contra a luz. Sombras compridas dançam pela parede. O baile será gótico, sem dúvida.", se={"flag": "decoracao_estilo", "valor": "gotico"}),
    n("Ela examina as peças antigas com um carinho quase respeitoso. O baile terá cara de tradição.", se={"flag": "decoracao_estilo", "valor": "historico"}),
    n("Ela olha para a caixa e para você, desconfiada, enquanto um sininho tilinta sozinho. O baile será... esquisito.", se={"flag": "decoracao_estilo", "valor": "estranho"}),
    n("Ela espalha as peças pelo chão, sem predominância de nada, e dá de ombros. O salão ficará deliciosamente improvisado.", se={"flag": "decoracao_estilo", "valor": "improvisado"}),
    sis("Missão <b>Não Era o que Eu Pedi</b> concluída. Sua relação com Mavis aumentou. A decoração escolhida vai aparecer no baile do próximo ato."),
], destino_auto="hub_salao_festas",
   chegada={"flags": {"mavis_estado": "concluida"}, "relacoes": {"mavis": {"afeto": 10}},
            "tirar_marcadores": ["salao_festas"], "barras": {"sanidade": 4}, "tempo": 10},
   dados={"raiz": True}, fundo="salao_festas")

# =====================================================================
# NIX — "Um Favor entre Funcionários"  (só se atendeu o telefone)
# =====================================================================
cena("nix_oferta", [
    "Uma camareira varre o tapete do corredor com uma pressa quase furiosa. Mal ergue os olhos, mas ao notar você, a vassoura trava no meio de um movimento.",
    f("thiago", "Oi. Você é a Nix? A Lily comentou de você."),
    f("nix", "A Lily fala demais. Mas é, sou eu."),
    f("nix", "Olha, desculpa a grosseria, mas estou atrasada em tudo. Tem quarto por limpar, bandeja por levar, e a minha vassoura quebrou no meio do serviço."),
    f("thiago", "Posso ajudar em alguma coisa?"),
    "Ela hesita. Dá uma olhada rápida para o corredor vazio e abaixa a voz.",
    f("nix", "Pode. No estoque tem uma vassoura de palha, nova. Se você buscar, eu adianto o resto. E, olha, isso fica entre nós. Os supervisores não gostam que a gente peça favor a hóspede."),
], destino_auto="hub_corredores",
   chegada={"flags": {"nix_estado": "pedido"}, "conhece": ["nix"], "mapa": ["estoque"],
            "marcadores": [{"area": "estoque", "texto": "Vassoura para a Nix"}], "tempo": 6},
   dados={"raiz": True}, fundo="corredor")

cena("estoque_vassoura", [
    "Entre os cabos de pá e rolos de arame, uma vassoura de palha nova repousa num canto, amarrada com barbante.",
    item("vassoura"),
    "Você ouve, lá longe, o leve rangido de uma porta. Parece que alguém limpa um quarto e abre gavetas bem rápido, mas você não dá importância.",
], destino_auto="hub_estoque", chegada={"tempo": 12}, dados={"raiz": True}, fundo="estoque")

cena("nix_entrega", [
    "Nix aparece sem ruído atrás de uma porta, com um pano no ombro. O corredor inteiro cheira a sabão.",
    f("nix", "Você trouxe! Eu te devo uma."),
    f("nix", "Olha, aprecio mesmo. Aqui quase ninguém ajuda ninguém. Se precisar de alguma coisa no hotel, pode me procurar."),
    "Ela pega a vassoura e sai varrendo, mais leve, como se o corredor tivesse ficado menor.",
    sis("Missão <b>Um Favor entre Funcionários</b> concluída. Sua relação com Nix aumentou. O <b>estoque</b> ficou liberado de vez e oferece mais peças."),
], destino_auto="hub_corredores",
   chegada={"flags": {"nix_estado": "concluida"}, "relacoes": {"nix": {"afeto": 6}},
            "tirar_itens": ["vassoura"], "tirar_marcadores": ["estoque"], "barras": {"sanidade": 2}, "tempo": 5},
   dados={"raiz": True}, fundo="corredor")

# =====================================================================
# BELLACOURT — "O Vestido Roubado"  (obrigatória)
# =====================================================================
cena("hub_suite14", None, tipo="condicional",
     dados={"flag": "nix_gatilho", "casos": {"true": "nix_quarto"}, "padrao": "suite_base", "raiz": True})

cena("hub_bar", None, tipo="condicional",
     dados={"flag": "bellacourt_vistos", "casos": {"true": "bar_base"}, "padrao": "bar_bellacourt", "raiz": True})

cena("bar_base", [
    "O bar é uma sala de madeira escura, de balcão longo e banquetas altas. As garrafas formam um altar de vidro atrás do balcão, iluminadas por uma luz âmbar.",
    n("Ainda é cedo: ninguém atende. Apenas o tique-taque de um relógio de parede.", se=[{"flag": "@hora", "max": 18}]),
], opcoes=[
    op("jehan_falar", "Sentar no balcão e conversar com o barman", "jehan_conversa",
       se=[{"flag": "@jehan"}, {"flag": "@hora", "min": 19, "max": 21}]),
    MAPA], dados=HUB, fundo="bar")

cena("bar_bellacourt", [
    "Você empurra a porta do bar e quase tropeça numa discussão. Ao fundo, junto à lareira, um casal elegante parece ter parado de se falar no meio de uma frase.",
    "Ele é alto, de ombros largos e cabelo curto cuidadosamente bagunçado. Ela é esguia, de cabelos escuros presos num coque impecável, e um olhar capaz de cortar vidro.",
    f("louise", "Você sabe muito bem o que estou dizendo, Gabriel. Ontem estava no armário e hoje sumiu."),
    f("gabriel", "Eu não toquei no seu vestido, Louise. Pare com isso."),
    "Os dois percebem você ao mesmo tempo. A expressão dela muda de repente, como se alguém acendesse uma luz.",
    f("louise", "Meu Deus. Olha esse rosto! Gabriel, olha."),
    f("gabriel", "Estou olhando."),
    f("louise", "Pele limpa, mandíbula marcada, olhos expressivos... Jovem, você já pensou em ser modelo?"),
    f("thiago", "Eu? Modelo? Eu só vim tomar um ar."),
    f("louise", "Ninguém vem a este hotel sem querer ser descoberto. Aqui está meu cartão. Pense nisso."),
    item("cartao_bellacourt"),
    f("gabriel", "Desculpe pela cena. A gente se vê."),
    "Eles saem do bar em direção ao elevador, retomando a discussão em voz mais baixa antes mesmo de a porta fechar.",
    sis("Surgiu uma nova pista nos <b>corredores</b>: o casal Bellacourt voltou ao quarto discutindo."),
], destino_auto="bar_base",
   chegada={"flags": {"bellacourt_vistos": True, "vestido_estado": "aberto"}, "conhece": ["gabriel", "louise"],
            "relacoes": {"gabriel": {"afeto": 4}, "louise": {"afeto": 6}},
            "tirar_marcadores": ["bar"], "marcadores": [{"area": "corredores", "texto": "Discussão dos Bellacourt"}], "tempo": 12},
   dados={"raiz": True}, fundo="bar")

# a pista nos corredores

cena("vestido_inicio", [
    "Uma porta bate com força no fim do corredor. Gabriel surge em mangas de camisa, fecha-a atrás de si e leva as mãos à cabeça.",
    f("louise", "...e não volte sem o vestido, ouviu bem?"),
    "A voz de Louise abafa-se atrás da madeira. Gabriel respira fundo e só então vê você.",
    f("gabriel", "Thiago, não é? Desculpe a cena do bar. E a daqui."),
    f("gabriel", "A Louise tem um vestido que usaria na festa do hotel. Ele sumiu do quarto e ela jura que fui eu, por ciúme. Eu juro que não fui."),
    f("gabriel", "Você poderia me ajudar a procurar? Quatro olhos acham mais que dois."),
], opcoes=[
    op("vest_aceita", "“Claro, vamos procurar.”", "vestido_busca", efeitos={"flags": {"vestido_estado": "busca"}, "relacoes": {"gabriel": {"afeto": 4}}, "tempo": 3}),
    op("vest_depois", "“Agora não posso. Mais tarde.”", "hub_corredores", efeitos={"tempo": 1}),
], dados={"raiz": True}, fundo="corredor")

cena("vestido_busca", [
    "Gabriel olha ao redor, impaciente. Corredores longos, vasos, armaduras vazias alinhadas, cortinas pesadas.",
    f("gabriel", "Onde esconderiam um vestido de seda numa casa deste tamanho?"),
    n("Gabriel baixa a voz, quase para si mesmo: “Às vezes eu juro que as armaduras estão ouvindo a gente.”", se={"flag": "vest_dica"}),
], opcoes=[
    op("vest_cortina", "Olhar atrás das cortinas pesadas", "vestido_cortina"),
    op("vest_carrinho", "Revirar o carrinho de limpeza abandonado", "vestido_carrinho"),
    op("vest_armadura", "Examinar as armaduras vazias", "vestido_armadura"),
], dados={"raiz": True}, fundo="corredor")

cena("vestido_cortina", [
    "Você afasta uma cortina de veludo. Poeira, uma janela fechada e uma aranha enorme, que parece ofendida com a visita.",
    f("gabriel", "Nada. Vamos tentar outro lugar."),
], destino_auto="vestido_busca", chegada={"tempo": 8, "flags": {"vest_dica": True}}, dados={"raiz": True}, fundo="corredor")

cena("vestido_carrinho", [
    "Lençóis dobrados, um pano de chão, um balde e sabonetes. Nada de seda vermelha.",
    f("gabriel", "Se não está aqui, deve estar escondido de um jeito mais criativo."),
], destino_auto="vestido_busca", chegada={"tempo": 8, "flags": {"vest_dica": True}}, dados={"raiz": True}, fundo="corredor")

cena("vestido_armadura", [
    "Você vai de armadura em armadura, batendo de leve nas placas de metal. Todas soam ocas, mas uma delas, perto do quarto do casal, tem o elmo ligeiramente torto.",
    "Você levanta a viseira. Lá dentro, comprimido como um pergaminho, há um tecido de seda cor de vinho.",
    f("gabriel", "O vestido! Dentro da armadura? Quem faria uma coisa dessas?"),
    "A armadura permanece imóvel. Mas, enquanto você puxa o tecido, tem a nítida sensação de que alguém, bem perto, prende uma risadinha.",
    f("thiago", "Alguém queria que você o encontrasse. Ou queria ver você procurando."),
    f("gabriel", "Ninguém além de nós passou por este corredor. Eu juro."),
    pens("Ninguém passou por aqui. E ainda assim, o vestido estava aqui."),
    "Gabriel segura o vestido com cuidado, como quem carrega um bebê, e bate na porta do quarto.",
    f("louise", "Se for você, Gabriel..."),
    f("gabriel", "Louise. Achamos. Estava dentro de uma armadura. Eu nem sei como."),
    "A porta se abre devagar. Louise olha o vestido, depois o marido, depois você. Cruza os braços, mas o canto da boca se curva.",
    f("louise", "Dentro de uma armadura. Meu Deus. Desculpe, Gabriel. Eu estava errada."),
    f("louise", "E obrigada, jovem. Cartão no bolso, não esqueça."),
    sis("Missão <b>O Vestido Roubado</b> concluída. Você ganhou <b>3 Fragmentos do Homem das Faixas</b> permanentes."),
], destino_auto="hub_corredores",
   chegada={"flags": {"vestido_estado": "concluido"}, "somar": {"fragmentos": 3},
            "relacoes": {"gabriel": {"afeto": 8}, "louise": {"afeto": 8}},
            "tirar_marcadores": ["corredores"], "barras": {"sanidade": -3}, "tempo": 15, "hud": ["social"]},
   dados={"raiz": True}, fundo="corredor")

# =====================================================================
# EUGÉNIE — ingredientes, Nix no quarto, Cozinha Básica
# =====================================================================
cena("eugenie_primeira", [
    "Numa mesa de canto do refeitório, uma senhora de cabelos brancos presos num coque e avental de linho observa os pratos das outras mesas com o cenho franzido, como quem avalia a nota de um aluno.",
    f("eugenie", "Está pálido, rapaz. E olha que aqui a comida não é ruim. Pelo menos é mais honesta que a média."),
    f("thiago", "Eu... estou me virando como dá. Não sei cozinhar."),
    f("eugenie", "Nada? Nem um ovo?"),
    f("thiago", "Eu queimaria a água."),
    "Ela solta uma risada curta e rouca.",
    f("eugenie", "Eu sou Eugénie. Cozinhei para metade da Europa antes de me aposentar. Se você me trouxer ingredientes simples, eu te ensino o básico. Sem fogo, sem panela, sem cozinha."),
    f("thiago", "A cozinha é proibida, não é?"),
    f("eugenie", "Muito. Então consiga os ingredientes por fora. Pão, ovos, algum tempero, frutas. Algo que se coma sem desculpas."),
    pens("Onde eu arranjo isso? Talvez alguém do hotel possa me ajudar."),
], destino_auto="hub_refeitorio",
   chegada={"flags": {"eug_estado": "ingredientes", "nix_gatilho": True},
            "conhece": ["eugenie"], "tirar_marcadores": ["refeitorio"],
            "relacoes": {"eugenie": {"afeto": 3}}, "tempo": 12},
   dados={"raiz": True}, fundo="refeitorio")

# o encontro com a Nix no quarto (3 variações), disparado na próxima visita à suíte
cena("nix_quarto", None, tipo="condicional",
     dados={"flag": "nix_estado", "casos": {"concluida": "nix_q3"}, "padrao": "nix_q_tel", "raiz": True})
cena("nix_q_tel", None, tipo="condicional",
     dados={"flag": "lily_conhecida", "casos": {"true": "nix_q2"}, "padrao": "nix_q1", "raiz": True})

FIM_NIX = {"flags": {"nix_gatilho": False, "ing_dia": "@dia"}, "tempo": 8}

cena("nix_q1", [
    "Ao girar a chave, você nota que a porta já estava destrancada. Dentro da suíte, uma camareira de uniforme cinza fecha uma gaveta com um estalo e dá um pulo ao vê-lo.",
    f("nix", "Ah. Desculpe! Eu estava só conferindo o quarto. Rotina. Você é o hóspede da catorze?"),
    f("thiago", "Sou. E você?"),
    f("nix", "Nix, da governança. Me avisaram que a suíte tinha recebido visita estranha. Eu confiro."),
    f("thiago", "Visita estranha?"),
    f("nix", "Coisa de hotel. Esquece. Quem é você, afinal? Chegou há pouco, né?"),
    "Vocês conversam um pouco. Ela pergunta do convite, de quem o enviou, e você conta sobre uma amiga que patrocina o evento.",
    f("thiago", "A propósito, eu estou tentando aprender a cozinhar. Falta de ingredientes, falta de tudo."),
    f("nix", "Ingredientes simples? Isso eu consigo. Deixa comigo. Amanhã cedo eu deixo na sua porta."),
    "Ela sai com o pano no ombro, rápida como veio. Você olha para a gaveta que ela fechou e não consegue lembrar se estava aberta antes.",
], destino_auto="suite_base", chegada=FIM_NIX, dados={"raiz": True}, fundo="suite14")

cena("nix_q2", [
    "Ao girar a chave, você nota que a porta já estava destrancada. Uma camareira de uniforme cinza vira-se com um pano na mão. Ela o reconhece no mesmo instante.",
    f("nix", "Ah, então é você. O hóspede da catorze. A Lily comentou que ligou para o quarto à noite."),
    f("thiago", "Ela ligou. Você é a Nix da Lily, então."),
    f("nix", "Se é pra ser conhecida pelo nome dela, sim. Sou a Nix. Estava só olhando o quarto."),
    f("thiago", "Eu queria perguntar uma coisa: preciso de ingredientes simples para aprender a cozinhar."),
    f("nix", "Cozinhar? Hmm. Eu estou ocupada, mas dou um jeito. Amanhã cedo eu deixo na sua porta."),
    "Ela sai e deixa no ar um cheiro de sabão e de pressa. Você tem a impressão de que alguma coisa nesta suíte mudou de lugar.",
], destino_auto="suite_base", chegada=FIM_NIX, dados={"raiz": True}, fundo="suite14")

cena("nix_q3", [
    "Ao girar a chave, você encontra a porta aberta. A camareira de uniforme cinza endireita a cabeça ao vê-lo, com um sorriso torto.",
    f("nix", "Novamente você aqui."),
    f("thiago", "A suíte é minha, tecnicamente."),
    f("nix", "É. Eu só estava olhando o quarto. Rotina. Como você me ajudou com a vassoura, eu vou te ajudar também."),
    f("thiago", "Estou procurando ingredientes simples para aprender a cozinhar."),
    f("nix", "Fácil. Amanhã cedo eu deixo na sua porta."),
    "Ela some pela porta antes mesmo de você piscar.",
], destino_auto="suite_base", chegada=FIM_NIX, dados={"raiz": True}, fundo="suite14")

cena("ingredientes_recebidos", [
    "Junto à porta, uma sacola de papel pardo, dobrada no topo. Dentro: pão, ovos cozidos, queijo, duas maçãs e um pote de sal grosso.",
    item("ingredientes"),
    pens("A Nix cumpriu. Agora é hora de levar isto à Eugénie."),
], destino_auto="suite_base", chegada={"flags": {"eug_estado": "levar"}, "tempo": 2}, dados={"raiz": True}, fundo="suite14")

cena("eugenie_aula", [
    "Eugénie examina a sacola como quem confere um diploma, e aprova com um aceno.",
    f("eugenie", "Pão, queijo, ovos já cozidos, fruta. Perfeito. Sente aqui, rapaz."),
    f("eugenie", "Primeiro: cozinhar não é fogo, é ordem. Segundo: comida simples não é comida fraca."),
    "Ela mostra como cortar o pão em fatias iguais, como esmagar o ovo com um garfo e o sal para misturar com queijo, como equilibrar doce e salgado com meia maçã.",
    f("eugenie", "Pronto. Você acabou de fazer o seu primeiro prato, sem uma única chama."),
    "Você prova. Está ótimo, de um jeito simples que parece abraço.",
    f("eugenie", "Estou impressionada com a comida deste hotel. Alguém aqui cozinha muito bem, e eu preciso elogiar essa pessoa."),
    "Ela se levanta, ajeita o avental e caminha até a porta fechada no fundo do refeitório, aquela que ninguém ousa tocar.",
    f("thiago", "Eugénie, a cozinha é proibida!"),
    f("eugenie", "Para você, querido. Para mim, é a minha casa."),
    "Ela empurra a porta, entra, e a porta se fecha atrás dela sem fazer o menor ruído. Você espera. Nenhum som volta.",
    sis("Habilidade aprendida: <b>Cozinha Básica</b>. Os ingredientes continuam com você: uma vez por dia, fora dos horários de refeição, você pode preparar uma refeição simples no refeitório."),
], destino_auto="hub_refeitorio",
   chegada={"habilidades": ["cozinha_basica"], "flags": {"eug_estado": "concluida", "cozinha_basica": True}, "barras": {"fome": 25},
            "relacoes": {"eugenie": {"afeto": 8}}, "tempo": 40},
   dados={"raiz": True}, fundo="refeitorio")

cena("cozinhou", [
    "Você junta o que sobrou do pão, uns pedaços de queijo e uma maçã. Cortar, esmagar, misturar, tudo na ordem certa, como Eugénie ensinou.",
    "O resultado não é bonito, mas é seu. Você come sem pressa, com um orgulho estranho.",
], destino_auto="@hub", chegada={"tempo": 40, "flags": {"cozinhou_dia": "@dia"}, "barras": {"fome": 30, "sanidade": 2}}, dados={"raiz": True}, fundo="refeitorio")

# =====================================================================
# ARTHUR — "Dois Diários"   (só com Vestido + 6 fragmentos)
# =====================================================================
cena("arthur_intro", [
    "Numa mesa baixa da biblioteca, um rapaz de óculos redondos e blusa de lã amarrotada folheia dois livros de capa mole, anotando algo num caderno. Ao ver você, ele se endireita como quem foi pego no meio de um segredo.",
    f("arthur", "Ah! Você é o Thiago, não é? Eu sou o Arthur. Estou aqui há algumas semanas. Já ouvi falar de você. Comentam que anda... vivendo experiências curiosas."),
    f("thiago", "Curiosas é uma palavra educada."),
    f("arthur", "Eu também sinto coisas estranhas neste hotel. Vozes, objetos que mudam de lugar. Achei que era só comigo."),
    f("arthur", "Então encontrei isto. Dois diários de hóspedes antigos, esquecidos num canto da biblioteca. Quer ver comigo?"),
    "Ele empurra os dois cadernos na sua direção. O primeiro tem capa verde-musgo e a assinatura “L. Brandão”. O segundo é de capa vinho, com um nome feminino quase apagado: “Cecília”.",
], destino_auto="arthur_leitura", dados={"raiz": True}, fundo="biblioteca")

cena("arthur_leitura", [
    "Você lê as páginas junto com Arthur, na luz fraca do abajur.",
    "No diário de L. Brandão: “Terceira noite que uma voz me chama do corredor. Abro a porta, não há ninguém. Quarta noite: a mesma voz, rindo.” Mais adiante: “Meus óculos sumiram. Achei dentro do sapato. Eu não os pus lá.”",
    "No diário de Cecília: “Hoje a xícara voou da mesa até a janela. Eu vi. Mas quando contei na recepção, riram de mim. Preciso dormir mais.” As últimas páginas têm letra tremida: “Quem está aí? Quem está aí?”",
    f("arthur", "Os dois foram embora de uma hora para outra. Os quartos foram limpos, os pertences recolhidos. Ninguém soube explicar."),
    n("Você percebe que várias das situações descritas parecem com as suas. Voz sem dono. Objetos fora do lugar. Uma risada curta.", se={"flag": "fragmentos", "min": 6}),
    n("As datas das anotações coincidem com semanas em que o hotel organizou algum evento. Em festas, o hotel fica mais agitado, e as brincadeiras também.", se={"flag": "fragmentos", "min": 10}),
    n("Você nota que as ocorrências sempre acontecem em horários em que os corredores estão vazios, e quase sempre perto de quartos específicos.", se={"flag": "fragmentos", "min": 13}),
    f("arthur", "E agora você? O que você vê, Thiago? O que acha que está acontecendo?"),
], destino_auto="arthur_hipoteses", dados={"raiz": True}, fundo="biblioteca",
   chegada={"flags": {"hip_n": 0}, "tirar_marcadores": ["biblioteca"], "tempo": 10})

cena("arthur_hipoteses", [
    "Arthur apoia o queixo na mão, esperando. Você precisa escolher o que considera mais provável.",
], opcoes=[
    op("hip1", "“Talvez seja coincidência, cansaço, imaginação.”", "hip1",
       se={"flag": "hip1", "diferente": True}),
    op("hip2", "“Acho que alguém está pregando peças nos hóspedes.”", "hip2",
       se=[{"flag": "hip2", "diferente": True}, {"flag": "fragmentos", "min": 7}]),
    op("hip3", "“Isso parece planejado. Talvez pelo mesmo responsável.”", "hip3",
       se=[{"flag": "hip3", "diferente": True}, {"flag": "fragmentos", "min": 10}]),
    op("hip4", "“Quem faz isso conhece os quartos, os horários, o hotel por dentro.”", "hip4",
       se=[{"flag": "hip4", "diferente": True}, {"flag": "fragmentos", "min": 13}]),
    op("hip5", "“E se... não for uma pessoa?”", "hip5",
       se=[{"flag": "hip5", "diferente": True}, {"flag": "fragmentos", "min": 16}]),
    op("hip_fim", "“Já falamos o bastante por hoje.”", "arthur_fim", se={"flag": "hip_n", "min": 1}),
], dados={"raiz": True}, fundo="biblioteca")

def hip(id, fala_thiago, resp):
    cena(id, [f("thiago", fala_thiago)] + resp, destino_auto="arthur_hipoteses",
         chegada={"flags": {id: True}, "somar": {"hip_n": 1}, "tempo": 4}, dados={"raiz": True}, fundo="biblioteca")

hip("hip1", "Talvez seja só cansaço. Estresse. A gente chega num lugar estranho e imagina coisas.", [
    f("arthur", "Eu pensei nisso. Pensei muito. Mas Brandão e Cecília nem se conheciam e descrevem situações parecidas. Cansaço não combina detalhes."),
    f("arthur", "Mesmo assim, é bom manter a hipótese viva. Se a gente descartar tudo cedo demais, vai ver o que quiser ver."),
])
hip("hip2", "Alguém pode estar pregando peças nos hóspedes. Uma brincadeira de mau gosto.", [
    f("arthur", "É a explicação mais simples. Alguém com acesso aos quartos, que gosta de rir do susto dos outros."),
    f("arthur", "Mas por que mirar em hóspedes humanos específicos? Isso me incomoda."),
])
hip("hip3", "As ocorrências parecem planejadas. Não é aleatório. Talvez seja uma pessoa só.", [
    f("arthur", "Planejadas... Então há intenção, e intenção exige motivo. Qual motivo faria alguém atormentar hóspedes por anos?"),
    "Ele anota algo, sublinha duas vezes e olha para a página como se esperasse uma resposta.",
])
hip("hip4", "Quem faz isso conhece os quartos, os horários, os corredores. Conhece o hotel por dentro.", [
    f("arthur", "Um funcionário, então? Ou alguém que mora aqui há muito tempo. Mas funcionários não somem do nada e não flutuam xícaras."),
    f("arthur", "Isso eu não sei explicar."),
])
hip("hip5", "E se... não for uma pessoa, Arthur?", [
    "O silêncio que segue é longo. Arthur tira os óculos, limpa-os na blusa e os recoloca devagar.",
    f("arthur", "Sobrenatural. Eu... considero essa possibilidade quase absurda. Mas não consigo descartá-la."),
    f("arthur", "Vamos tratar isso como uma hipótese de último recurso. Nada além disso. Por enquanto."),
])

cena("arthur_fim", [
    "Vocês fecham os diários. Nenhum dos dois chegou a uma conclusão, e ambos sabem disso.",
    f("arthur", "Vou continuar investigando. Se acontecer alguma coisa nova, me procure. Combinamos de nos encontrar no bar à noite, quando a biblioteca fechar. Lá a gente conversa melhor."),
    f("thiago", "Combinado."),
    "Ele guarda os dois diários debaixo do braço e segue para o corredor, ainda murmurando consigo mesmo.",
    sis("Missão <b>Dois Diários</b> concluída. Um marcador deve surgir no <b>bar</b> à noite."),
], destino_auto="biblioteca_base",
   chegada={"flags": {"arthur_estado": "concluido"}, "relacoes": {"arthur": {"afeto": 10}},
            "conhece": ["arthur"], "barras": {"sanidade": 2}, "tempo": 15},
   dados={"raiz": True}, fundo="biblioteca")

# =====================================================================
# JEHAN — o barman (só à noite, 19h–22h)
# =====================================================================
cena("jehan_conversa", [
    "À noite, o bar muda de rosto. As luzes ficam mais baixas, a lareira estala e o balcão ganha um brilho âmbar. Atrás dele, um homem de camisa branca arregaçada e colete preto seca um copo com a calma de quem tem todo o tempo do mundo.",
    f("jehan", "Boa noite. Você deve ser o Thiago. Eu sou o Jehan. O que vai ser?"),
    n("Arthur já está num banquinho, com o caderno aberto, e acena para você.", se={"flag": "arthur_estado", "valor": "concluido"}),
    f("thiago", "Alguma coisa que não me faça dormir. Ou que faça."),
    f("jehan", "Tenho uma bebida para cada tipo de noite. Esta serve para as duas."),
    "Ele desliza um copo na sua direção. Tem gosto de especiaria e de mel.",
    f("jehan", "Então. A noite começa e eu escuto muita coisa neste balcão. Dizem que o hotel anda agitado."),
    f("arthur", "Tem objetos mudando de lugar e vozes sem dono. A gente vem tentando entender.", se={"flag": "arthur_estado", "valor": "concluido"}),
    f("thiago", "Vozes sem dono, objetos que somem. Um vestido dentro de uma armadura."),
    f("jehan", "Ah, a armadura. Uma boa."),
    "Ele sorri de lado, sem dizer mais nada por um momento.",
    f("jehan", "Eu já vi esse tipo de brincadeira. É sempre alguém que gosta de ver humano fazendo papel de bobo. Não vou dizer quem, porque eu não tenho prova. Mas conheço o estilo."),
    f("thiago", "O senhor sabe quem faz isso?"),
    f("jehan", "Sei como funciona. Esse tipo de coisa começa de dia, com objetos, e termina à noite, com vozes. Pode ser engraçado. Mas só até alguém seguir a voz errada."),
    f("jehan", "Então um conselho de barman, que vale mais que bebida: quando os corredores esvaziarem, depois da hora, e você ouvir alguém chamando, não siga. Nem que seja uma voz conhecida."),
    f("jehan", "Principalmente se for uma voz conhecida."),
    pens("Por que ele fala com tanta certeza?"),
    f("jehan", "Agora beba. Amanhã é um dia comprido."),
], destino_auto="bar_base",
   chegada={"flags": {"jehan_estado": "concluido", "ataque_pendente": True}, "conhece": ["jehan"], "relacoes": {"jehan": {"afeto": 8}},
            "barras": {"sanidade": 3, "fome": 4}, "tirar_marcadores": ["bar"], "tempo": 40},
   dados={"raiz": True}, fundo="bar")

# =====================================================================
# O ATAQUE DA ELISABETA, A CLÍNICA E AS DESCULPAS  (encerramento)
# =====================================================================
cena("dormir_gate", None, tipo="condicional",
     dados={"flag": "ataque_pendente", "casos": {"true": "ataque_acorda"}, "padrao": "dormir_gate2", "raiz": True})
cena("dormir_gate2", None, tipo="condicional",
     dados={"flag": "desculpas_pendente", "casos": {"true": "porta_batem"}, "padrao": "dormiu", "raiz": True})

cena("ataque_acorda", [
    "Algo desperta você no meio da noite. O quarto está escuro, o relógio marca pouco depois das três.",
    "Então você ouve de novo: uma voz de mulher, vinda do corredor, abafada e desesperada.",
    f("voz", "Socorro... por favor... alguém me ajude..."),
    "É uma voz que você acha que conhece. Não consegue dizer de quem.",
    pens("Depois que os corredores esvaziarem... não siga a voz, mesmo que seja conhecida."),
    pens("Mas e se alguém realmente precisar de ajuda?"),
], opcoes=[
    op("seguir_voz", "Levantar e ir atrás da voz", "ataque_cond",
       efeitos={"barras": {"suspeita": 15}, "somar": {"fragmentos": 1}, "flags": {"lugar": "corredores"}, "tempo": 5}),
    op("ignorar_voz", "Ficar na cama e ignorar", "ataque_ignorou"),
], chegada={"ate": "03:10", "sono": True, "barras": {"cansaco": 70, "sanidade": 10}},
   dados={"raiz": True}, fundo="suite14")

cena("ataque_ignorou", [
    "Você aperta o cobertor contra o peito, fecha os olhos e conta até cem. A voz repete, mais fraca, até silenciar.",
    "Você dorme de novo, mal. Pela manhã, o corredor está vazio.",
    sis("Você seguiu o conselho de Jehan. A voz pode voltar na próxima noite."),
], destino_auto="hub_suite14",
   chegada={"ate": "07:00", "sono": True, "barras": {"cansaco": 100, "sanidade": 15, "vida": 5}, "flags": {"lugar": "suite14"}},
   dados={"raiz": True}, fundo="suite14")

cena("ataque_cond", None, tipo="condicional",
     dados={"flag": "conheceu_elisabeta", "casos": {"true": "ataque_corredor_a"}, "padrao": "ataque_corredor_b", "raiz": True})

cena("ataque_corredor_a", [
    "Você veste o casaco por cima do pijama e abre a porta. O corredor está iluminado só pelas lâmpadas de emergência, vermelhas e tremidas.",
    "A voz vem de longe, e você já sabe para onde ela leva. Pelas escadas, pelo corredor lateral, até a porta entreaberta da sala de música.",
    pens("Ela. A mulher do piano. Se ela estiver em perigo..."),
    "Você corre. O som das suas passadas desaparece no tapete.",
], destino_auto="ataque_sala_a", dados={"raiz": True}, fundo="corredor")

cena("ataque_corredor_b", [
    "Você abre a porta com cuidado. O corredor está iluminado só pelas lâmpadas de emergência, vermelhas e tremidas.",
    "A voz muda de direção a cada passo: agora parece vir de trás, depois da esquerda. Você segue, lentamente, com a mão na parede.",
    "Nenhuma porta está aberta. Mas, pouco a pouco, outro som se mistura: notas de piano, lentas e tristes.",
    "O piano te guia até uma porta entreaberta no fim da ala.",
], destino_auto="ataque_sala_b", dados={"raiz": True}, fundo="corredor")

cena("ataque_sala_b", [
    "A sala de música está iluminada só pela lua. No piano, sentada de costas, uma mulher de vestido antigo toca devagar.",
    "Você não sabe quem ela é. Mas a voz de socorro some quando você entra. Só resta o piano.",
    "Você se aproxima. Quando está a um passo, estende a mão e toca o ombro dela.",
    "Ela para de tocar. Vira o rosto devagar. O rosto é desfigurado: a pele cinzenta se repuxa, os olhos são dois buracos escuros e a boca se abre mais do que devia.",
    "Você cai para trás, apoiando as mãos no chão, e se arrasta para longe.",
    f("thiago", "Está... tudo bem? Eu ouvi alguém gritando. Uma mulher pedindo socorro."),
    f("mulher_piano_medo", "Eu só estou tocando a minha música."),
], opcoes=[
    op("b_elogia", "“É uma música bonita...”", "ataque_sala_b2", efeitos={"relacoes": {"mulher_piano": {"afeto": 2}}}),
    op("b_calado", "Ficar em silêncio, sem tirar os olhos dela", "ataque_sala_b2"),
], dados={"raiz": True}, fundo="sala_musica")

cena("ataque_sala_b2", [
    f("thiago", "Eu ouvi uma mulher gritando agora há pouco. Você não ouviu?"),
    f("mulher_piano_medo", "Não ouvi."),
    "Do corredor, a voz de socorro grita de novo, nítida, bem atrás de você.",
    f("thiago", "Você não ouviu? Agora?"),
    "Ela se levanta. O vestido arrasta no chão, e as teclas do piano soam sozinhas, uma nota grave e feia.",
    f("mulher_piano_medo", "NÃO OUVI."),
], destino_auto="ataque_golpe", dados={"raiz": True}, fundo="sala_musica")

cena("ataque_sala_a", [
    "A sala de música está iluminada só pela lua. No piano, sentada de costas, a mulher toca. Ela ergue os olhos quando você entra, e o olhar dela é mais assustado do que da primeira vez.",
    f("thiago", "Ouvi uma mulher gritando. Achei que fosse você. Está bem?"),
    f("mulher_piano", "Não estou bem. Nunca estou."),
    "Você se senta ao lado dela no banco do piano. Ela não para de tocar.",
    f("thiago", "Quer conversar? Posso ficar aqui."),
    "Ela continua tocando, os olhos fixos nas teclas. Você, sem pensar, pousa a mão sobre a dela.",
    "O piano se cala de uma vez. Ela vira a cabeça devagar, e o rosto está diferente: distorcido, cinzento, os olhos negros.",
    f("mulher_piano_medo", "Você não quer que eu toque? Você não quer que eu toque a minha música? Você disse que gostava dela."),
], destino_auto="ataque_golpe", dados={"raiz": True}, fundo="sala_musica")

cena("ataque_golpe", [
    "Ela avança. A mão dela, que era fria, é de repente uma garra. Você sente algo rasgar o seu ombro, depois o peito.",
    "A dor é branca. O som do piano se transforma num grito só, e você não sabe se é dela ou seu.",
    "Você tropeça, cai, levanta. Corre. Pelas escadas, pelo corredor, sem olhar para trás.",
    "Atrás de você, uma risada longa e satisfeita. Você não sabe quem ri, e não tem tempo de perguntar.",
    "Quando alcança a porta da suíte 14, suas mãos tremem tanto que quase não conseguem girar a chave.",
    "Você tranca a porta, escorrega até o chão e só então vê o sangue.",
], destino_auto="manha_ferido",
   chegada={"barras": {"vida": -35, "sanidade": -30}, "flags": {"lugar": "suite14", "ataque_feito": True, "ataque_pendente": False},
            "somar": {"fragmentos": 1}, "tempo": 20},
   dados={"raiz": True}, fundo="suite14")

cena("manha_ferido", [
    "Você desmaia em algum momento. Quando acorda, a luz da manhã empurra as cortinas.",
    "O ombro e o peito estão grudados na camisa, em sangue seco. Você sente tontura. Quando tenta pensar na noite passada, só vêm pedaços: um rosto, um piano, uma risada.",
    sis("Você está ferido e abalado. Sua Vida e sua Sanidade estão muito baixas. Procure ajuda."),
    "Você veste um casaco por cima e desce para o café, se escorando na parede.",
], destino_auto="jehan_cafe",
   chegada={"ate": "07:30", "sono": True, "flags": {"lugar": "refeitorio"}}, dados={"raiz": True}, fundo="suite14")

cena("jehan_cafe", [
    "O refeitório está cheio de cheiro de pão e café. Numa mesa de canto, Jehan toma o dele, lendo um jornal. Quando você passa, ele ergue os olhos e a xícara pára no meio do caminho.",
    f("jehan", "Thiago. Sente-se. Agora."),
    "Ele levanta o seu casaco com dois dedos e olha o ombro. A expressão dele muda: já não é o barman bem-humorado.",
    f("jehan", "Você não está bem. Isso aí não é de queda, nem de caco de vidro. Vou te levar à clínica."),
    f("thiago", "Eu... saí do quarto à noite. Ouvi uma voz..."),
    f("jehan", "Depois a gente conversa sobre isso. Levante-se. Devagar."),
    "Ele passa o seu braço por cima dos ombros dele e leva você para fora do refeitório, discretamente, como quem acompanha um velho amigo bêbado.",
], destino_auto="clinica_sorteio", chegada={"tempo": 15, "relacoes": {"jehan": {"afeto": 5}}},
   dados={"raiz": True}, fundo="refeitorio")

cena("clinica_sorteio", None, tipo="sorteio", dados={"raiz": True, "opcoes": [
    {"destino": "clinica_amanda", "efeitos": {"flags": {"medica": "amanda"}}},
    {"destino": "clinica_rafaela", "efeitos": {"flags": {"medica": "rafaela"}}}]})

cena("clinica_amanda", [
    "A clínica cheira a ervas e álcool. Sobre uma maca, sob uma luz amarelada, uma jovem médica de olhos gentis lava as mãos numa pia de porcelana.",
    f("amanda", "Jehan! O que aconteceu? Deite ele aqui."),
    "Ela faz você tirar o casaco e fica um bom tempo em silêncio, analisando as marcas.",
    f("amanda", "Sou a Amanda. Isso não foi acidente. Quem fez isso?"),
    f("thiago", "Uma mulher. Tocando piano na sala de música. Ela parecia... parecia o retrato da esposa do fundador, aquele no hall."),
    "Jehan e Amanda trocam um olhar que você não consegue ler.",
    f("amanda", "Não faz sentido nenhum. Mas é assim que o hotel funciona às vezes, e eu prefiro cuidar primeiro, perguntar depois."),
    f("amanda", "Vou limpar e fechar. Fique tranquilo: não vou contar a ninguém. Humanos me fascinam, sabe? Você me parece um menino com muito azar."),
], destino_auto="clinica_fim", chegada={"conhece": ["amanda"], "relacoes": {"amanda": {"afeto": 6}}},
   dados={"raiz": True}, fundo="clinica")

cena("clinica_rafaela", [
    "A clínica cheira a ervas e álcool. Uma jovem médica de olhar afiado vira-se bruscamente quando a porta se abre, com um prontuário nas mãos.",
    f("rafaela", "Jehan. Está de novo trazendo criatura estranha para a minha clínica?"),
    f("jehan", "É o Thiago. Está bem machucado, Rafaela."),
    "Ela olha o ferimento por um tempo mais longo do que o necessário e anota alguma coisa no prontuário.",
    f("rafaela", "Sou a Rafaela. Conte rápido: quem fez isso?"),
    f("thiago", "Uma mulher tocando piano na sala de música. Ela parecia o retrato da esposa do fundador, lá do hall."),
    "Rafaela e Jehan trocam um olhar rápido.",
    f("rafaela", "Isso não é normal. Nem para este lugar. Vou tratar do ferimento. E não conte isso a ninguém, entendeu? A ninguém. Eu mesma vou investigar."),
    f("rafaela", "Depois volte aqui. Quero ver como cicatriza. E quero saber de qualquer detalhe novo."),
], destino_auto="clinica_fim", chegada={"conhece": ["rafaela"], "relacoes": {"rafaela": {"afeto": 6}}},
   dados={"raiz": True}, fundo="clinica")

cena("clinica_fim", [
    "O curativo é apertado, mas a dor diminui. Quando você se levanta, o mundo já não gira.",
    f("jehan", "Fique longe da sala de música. E, da próxima vez, escute o conselho do barman."),
    f("thiago", "Eu escutei. Não adiantou."),
    f("jehan", "Então a gente conversa mais tarde, com uma bebida na mão."),
    "A médica não entregou ninguém. Nem Jehan. Esse silêncio, de um jeito estranho, é um alívio.",
    "No caminho de volta, você percebe que o hotel está diferente: há guirlandas, fitas e cartazes por toda parte, como se o aniversário estivesse mais perto do que você imaginava.",
    sis("Você pode <b>dormir</b> para recuperar a Sanidade, ou continuar explorando. Mas cuidado com a noite."),
], destino_auto="hub_corredores",
   chegada={"barras": {"vida": 25, "sanidade": 5}, "flags": {"clinica_ataque": True, "desculpas_pendente": True, "lugar": "corredores"},
            "tempo": 35},
   dados={"raiz": True}, fundo="clinica")

cena("alto_falante", [
    "Um estalo metálico atravessa o corredor, seguido de um chiado. A voz do alto-falante do hotel é calma e educada, e a mesma de sempre:",
    "“Atenção, prezados hóspedes. Por motivos de segurança, solicitamos que nenhum hóspede permaneça fora de seus aposentos depois do horário de recolhimento. Agradecemos a compreensão.”",
    "A mensagem se repete duas vezes. Depois, só o chiado. Ninguém parece surpreso.",
    pens("Eles sabem. De alguma forma, sabem."),
], destino_auto="@hub", dados={"raiz": True}, fundo="corredor")

cena("porta_batem", [
    "Algo desperta você no meio da noite. O quarto está frio, e o relógio mostra pouco depois das duas.",
    "Batem na porta. Três pancadas leves, educadas. Depois, silêncio.",
    pens("Quem bate à essa hora? As regras do hotel..."),
], opcoes=[
    op("porta_abrir", "Levantar e abrir a porta", "porta_abre"),
    op("porta_nao", "Ficar na cama, sem se mexer", "porta_nao_abre"),
], chegada={"ate": "02:10", "sono": True, "barras": {"cansaco": 60, "sanidade": 5}}, dados={"raiz": True}, fundo="suite14")

FALA_ELI = [
    f("elisabeta", "Perdão. Eu sei que é tarde. Não vim fazer nada de mau."),
    f("elisabeta", "Meu nome é Elisabeta. Eu... acho que ainda é meu nome."),
    f("elisabeta", "Eu não queria machucar você. Quando disseram que a música não era real, algo dentro de mim se perdeu."),
]
cena("porta_abre", [
    "Você hesita, o coração martelando, mas se levanta. Quando abre a porta, não está lá a mulher desfigurada da sala de música. Está uma mulher de vestido branco antigo, pálida, de olhos baixos, com os cabelos soltos e frios.",
] + FALA_ELI, opcoes=[
    op("eli1", "“Você está morta?”", "porta_resp", efeitos={"flags": {"eli_morta": True}}),
    op("eli2", "“O que você é?”", "porta_resp"),
    op("eli3", "“Quero que você vá embora.”", "porta_resp"),
], dados={"raiz": True}, fundo="suite14")

cena("porta_resp", [
    f("elisabeta", "Aqui as coisas são muito confusas. Às vezes eu não sei onde termina a música e começo eu."),
    f("elisabeta", "Eu não vou mais atormentar você. Prometo."),
    "Ela leva a mão ao pescoço, como se procurasse algo que não está lá. Depois só o frio e três notas de piano ao longe.",
    "Quando você pisca, o corredor está vazio.",
], destino_auto="desculpas_fim", dados={"raiz": True}, fundo="suite14")

cena("porta_nao_abre", [
    "Você aperta o lençol e não se mexe. As batidas param. A porta range, mas ninguém entra.",
    "Você vira para o outro lado. O colchão está frio. Ela está deitada ao seu lado, os olhos abertos, fixos no teto.",
    f("elisabeta", "Perdão."),
    "Você pula da cama, com o coração na garganta.",
    f("elisabeta", "Não grite. Por favor. Só queria dizer que não vou mais atormentar você."),
    f("elisabeta", "Meu nome é Elisabeta. Eu não queria machucar você. Quando disseram que a música não era real, algo dentro de mim se perdeu."),
], opcoes=[
    op("eli_b1", "“Você está morta?”", "cama_resp"),
    op("eli_b2", "Ficar calado, encostado na parede", "cama_resp2"),
], chegada={"barras": {"sanidade": -10}}, dados={"raiz": True}, fundo="suite14")

cena("cama_resp", [
    f("elisabeta", "Aqui as coisas são muito confusas."),
    "Ela leva a mão ao pescoço, procurando algo que não está lá. Quando você pisca, ela não está mais. Só o lençol amassado e o frio.",
], destino_auto="desculpas_fim", dados={"raiz": True}, fundo="suite14")
cena("cama_resp2", [
    "Ela leva a mão ao pescoço, procurando algo que não está lá. Quando você pisca, ela não está mais. Só o lençol amassado e o frio.",
], destino_auto="desculpas_fim", dados={"raiz": True}, fundo="suite14")

cena("desculpas_fim", [
    "Você passa o resto da noite sentado na cama, com a luz acesa, sem coragem de fechar os olhos.",
    "Pela manhã, o corpo pesa, mas a cabeça está mais clara. Você sente que algo se resolveu, ainda que não entenda o quê.",
    "Aquelas semanas foram diferentes de tudo que eu já havia vivido. Os corredores começaram a parecer familiares, mas os sons durante a noite nunca deixaram de me assustar. Quanto mais eu conhecia aquele lugar, menos conseguia acreditar nas explicações que inventava para mim mesmo.",
    sis("Uma nova pista foi liberada na <b>biblioteca</b>: a vida de Elisabeta. (Conteúdo previsto para o próximo capítulo.)"),
], destino_auto="hub_suite14",
   chegada={"ate": "07:00", "sono": True, "flags": {"desculpas_pendente": False, "elisabeta_desculpou": True, "biblioteca_elisabeta": True, "lugar": "suite14"},
            "barras": {"cansaco": 90, "sanidade": 10, "vida": 5}},
   dados={"raiz": True}, fundo="suite14")

# =====================================================================
# A MORTE — "A Última Refeição"
# =====================================================================
cena("morte_pedido", [
    "Numa mesa isolada do refeitório, uma moça de vestido preto e simples, de cabelos castanhos longos e olhos azul-claros, observa a sala sem tocar na comida que tem diante de si. A pele é clara, sem ser pálida. Parece uma menina do sul, saída de uma festa de interior.",
    "Quando você passa, ela ergue os olhos, e você tem a impressão de que ela esperava exatamente por você.",
    f("morte_jovem", "Você tem as mãos livres. Isso é raro neste hotel."),
    f("thiago", "Perdão?"),
    f("morte_jovem", "Alguém precisa muito comer. Não consegue mais levantar da cama e ninguém está olhando por ele. Eu não posso ir até lá."),
    f("thiago", "Por que não pode?"),
    "Ela sorri, e o sorriso é doce e cansado.",
    f("morte_jovem", "Porque eu assustaria quem eu quero ajudar. Leve esta bandeja por mim. Quarto no fim do corredor, perto da escada. Nada de pressa, mas também nada de demora."),
], opcoes=[
    op("morte_aceita", "“Pode deixar, eu levo.”", "morte_aceitou",
       efeitos={"flags": {"morte_estado": "aceita"}, "itens": ["bandeja_morte"], "conhece": ["morte_jovem"],
                "tirar_marcadores": ["refeitorio"], "marcadores": [{"area": "corredores", "texto": "Bandeja para o quarto do fim do corredor"}], "tempo": 5}),
    op("morte_recusa", "“Desculpe, não estou em condições.”", "morte_recusou", efeitos={"tempo": 2}),
], dados={"raiz": True}, fundo="refeitorio")

cena("morte_aceitou", [
    f("morte_jovem", "Obrigada. De verdade."),
    "Ela se levanta com uma leveza estranha, empurra uma bandeja coberta com um pano branco na sua direção e some atrás de uma coluna. Quando você olha, não há mais ninguém.",
    item("bandeja_morte"),
    sis("Missão: <b>A Última Refeição</b>. Leve a bandeja ao quarto no fim do corredor."),
], destino_auto="hub_refeitorio", dados={"raiz": True}, fundo="refeitorio")

cena("morte_recusou", [
    f("morte_jovem", "Entendo. Se mudar de ideia, estarei por aqui."),
    "Ela volta a observar a sala, como se tivesse todo o tempo do mundo. E, no fundo, talvez tenha.",
], destino_auto="hub_refeitorio", dados={"raiz": True}, fundo="refeitorio")

cena("morte_quarto_cond", None, tipo="condicional",
     dados={"flag": "medica", "casos": {"amanda": "morte_quarto", "rafaela": "morte_quarto"}, "padrao": "morte_medica", "raiz": True})
cena("morte_medica", None, tipo="sorteio", dados={"raiz": True, "opcoes": [
    {"destino": "morte_quarto", "efeitos": {"flags": {"medica": "amanda"}}},
    {"destino": "morte_quarto", "efeitos": {"flags": {"medica": "rafaela"}}}]})

cena("morte_quarto", [
    "No fim do corredor, perto da escada de serviço, uma porta de madeira escura tem a tinta descascada. Você ouve alguém lá dentro, tossindo baixo.",
    "A porta se abre antes de você bater. Uma médica de jaleco sai, com uma maleta, passa por você sem olhar, como se você fosse parte da parede.",
    n("É a Amanda. Os olhos dela estão fundos, e ela segue pelo corredor sem uma palavra.", se={"flag": "medica", "valor": "amanda"}),
    n("É a Rafaela. A boca está apertada numa linha dura, e ela segue pelo corredor sem uma palavra.", se={"flag": "medica", "valor": "rafaela"}),
    "O quarto é pequeno e cheira a remédio e a cera de vela. Numa cama de ferro, sob cobertores gastos, um homem muito magro e muito idoso respira com dificuldade.",
    "Quando você coloca a bandeja na mesinha de cabeceira, ele abre os olhos, de um azul esmaecido, e sorri.",
    f("paciente", "Você é um dos hóspedes novos. Não me lembro da sua cara. Mas a bandeja... ah, a bandeja eu reconheço."),
    sis("Você pode deixar a bandeja e partir, ou ficar e ajudá-lo a comer."),
], opcoes=[
    op("morte_deixar", "Deixar a bandeja e ir embora", "morte_deixou"),
    op("morte_ficar", "Sentar ao lado dele e ajudá-lo a comer", "morte_alimentou"),
], chegada={"definir": {"fomeMax": 150}, "tempo": 10}, dados={"raiz": True}, fundo="quarto_doente")

cena("morte_deixou", [
    f("thiago", "Coma devagar. Eu volto mais tarde."),
    f("paciente", "Obrigado, rapaz. Boa noite, ou boa tarde. Já não sei."),
    "Você sai e fecha a porta devagar. Ouve, lá dentro, o tilintar da colher na louça.",
], destino_auto="morte_agradece", dados={"raiz": True}, fundo="quarto_doente")

cena("morte_alimentou", [
    "Você puxa uma cadeira e senta ao lado da cama. Com cuidado, ergue a colher, e ele aceita cada porção com a lentidão de quem saboreia.",
    f("paciente", "Faz tanto tempo que ninguém fica. Nem minha mãe teve tanta paciência."),
    "Vocês conversam pouco. Ele fala de uma casa ao lado de um rio, de um cachorro de nome Barão, de uma mulher chamada Lena. Nada que lhe diga quem ele é. Nada que importe agora.",
    "Quando o prato está limpo, ele pega algo debaixo do travesseiro: uma chave pequena, de ferro escuro, amarrada a um barbante.",
    f("paciente", "Eu não tenho herdeiro. Isso abre um baú, em algum lugar deste hotel. Guarde. Alguém tem que ficar com o que sobra."),
    item("chave_misteriosa"),
    "Ele sorri, fecha os olhos e respira mais devagar. Você espera um tempo. Quando percebe, a respiração parou. O rosto dele está em paz.",
    "Você puxa o cobertor até o peito dele, fica um instante em silêncio e sai.",
], destino_auto="morte_agradece",
   chegada={"flags": {"morte_chave": True, "bau_sem_herdeiros": True}, "barras": {"sanidade": -5}, "tempo": 30},
   dados={"raiz": True}, fundo="quarto_doente")

cena("morte_agradece", [
    "Você volta pelo refeitório. Na mesa isolada, onde a moça de preto estava, agora só há um prato intocado e um guardanapo dobrado.",
    "Ao se aproximar, você lê, em letra miúda e elegante: “Obrigada.” O papel se desfaz em cinza fina entre os seus dedos, sem nenhum cheiro.",
    "A cadeira está fria. Ninguém, em volta, parece ter visto a moça.",
    sis("Missão <b>A Última Refeição</b> concluída. Sua barra de <b>Fome</b> agora vai até <b>150</b>, e você se sente mais cheio e mais forte."),
    sis("Você recebeu uma <b>chave misteriosa</b>. Ela abrirá algo no futuro.", se={"flag": "morte_chave"}),
], destino_auto="hub_refeitorio",
   chegada={"flags": {"morte_estado": "concluida", "lugar": "refeitorio"}, "tirar_itens": ["bandeja_morte"],
            "barras": {"fome": 50, "sanidade": 3}, "tempo": 5},
   dados={"raiz": True}, fundo="refeitorio")

exec(open(__file__.rsplit("/",1)[0] + "/vida_hotel.py", encoding="utf-8").read())
exec(open(__file__.rsplit("/",1)[0] + "/arvore_v3.py", encoding="utf-8").read())

json.dump(C, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(C), "cenas geradas (parte 2)")
