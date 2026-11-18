# -*- coding: utf-8 -*-
"""
Gera cenas/ato1.json a partir do roteiro oficial (cenas 1 a 18).
Fonte: ROTEIRO_ATO_1_CENAS_01_A_06.md e ROTEIRO_ATO_1_CENAS_07_A_18.md
Onde o roteiro só resume a cena, o texto aqui é rascunho no mesmo tom (marcado no README).
"""
import json, sys

MAVIS = {"flag": "recepcionista", "valor": "mavis"}
JON   = {"flag": "recepcionista", "valor": "jonathan"}
BANHO = {"flag": "tomou_banho", "valor": True}
SEM_BANHO = {"flag": "tomou_banho", "valor": False}
VIU_ELI = {"flag": "conheceu_elisabeta", "valor": True}
NAO_VIU_ELI = {"flag": "conheceu_elisabeta", "valor": False}
ATENDEU = {"flag": "lily_conhecida", "valor": True}

def f(q, t, se=None, ao=None):
    d = {"quem": q, "texto": t}
    if se: d["se"] = se
    if ao: d["ao_mostrar"] = ao
    return d
def com(t, ao):
    return {"texto": t, "ao_mostrar": ao}
def n(t, se=None):
    return t if se is None else {"texto": t, "se": se}
def pens(t, se=None):
    d = {"estilo": "pensamento", "texto": t}
    if se: d["se"] = se
    return d
def sis(t, se=None):
    d = {"estilo": "sistema", "texto": t}
    if se: d["se"] = se
    return d
def bil(t):
    return {"estilo": "bilhete", "texto": t}
def item(i, se=None):
    d = {"item": i}
    if se: d["se"] = se
    return d
def op(id, texto, destino, efeitos=None, se=None):
    d = {"id": id, "texto": texto, "destino": destino}
    if efeitos: d["efeitos"] = efeitos
    if se: d["se"] = se
    return d

C = []   # lista de cenas
def cena(id, narrativa, opcoes=None, destino_auto=None, chegada=None, classe=None, tipo=None, dados=None):
    d = {"id": id}
    if tipo: d["tipo"] = tipo
    if classe: d["classe"] = classe
    if chegada: d["chegada"] = chegada
    if narrativa is not None: d["narrativa"] = narrativa
    if dados: d["dados"] = dados
    if opcoes: d["opcoes"] = opcoes
    if destino_auto: d["destino_auto"] = destino_auto
    C.append(d)

# =====================================================================
# CENA 1 — O BILHETE DOURADO
# =====================================================================
cena("c01_bilhete", [
    bil("Parabéns!"),
    bil("Você ganhou um ano inteiro de hospedagem, com tudo pago!"),
    bil("Deixe-me conferir os seus dados..."),
    bil("Seu nome é Thiago {sobrenome}.<br>Você tem 19 anos. Certo?"),
    bil("Aqui também diz que você é órfão."),
    bil("Nunca conheceu sua família...<br>E nunca foi adotado."),
    bil("Que triste..."),
    bil("Mas não precisa continuar assim."),
    bil("Esta pode ser a oportunidade que você esperou durante toda a sua vida."),
    bil("Um ano inteiro longe do orfanato."),
    bil("Hospedagem, alimentação e transporte completamente pagos."),
    bil("Nenhuma conta.<br>Nenhuma preocupação.<br>Nenhum motivo para voltar."),
    bil("Então... vamos lá?"),
    bil("O grandioso <b>Hotel Los Segredos</b> está esperando por você."),
    "O bilhete desaparece. Ainda no escuro, começa o som do motor de um ônibus.",
], destino_auto="c02_viagem", classe="bilhete",
   chegada={"flags": {"conheceu_elisabeta": False, "lily_conhecida": False}})

# =====================================================================
# CENA 2 — A VIAGEM
# =====================================================================
cena("c02_viagem", [
    "O motor do ônibus continua sobre a escuridão. A imagem abre e fecha, como um piscar de olhos: você acorda, encostado na janela.",
    "A estrada é ruim. O ônibus balança, e você segura sua única mochila entre as pernas.",
    pens("Um ano inteiro num hotel... com tudo pago."),
    pens("Como será que vou viver aqui?"),
    pens("Eu só trouxe algumas roupas e meus objetos pessoais. É tudo o que tenho."),
    pens("Ainda parece estranho... Como um simples brasileiro conseguiu uma passagem para o outro lado do mundo?"),
    "Você olha de novo o bilhete dourado.",
    pens("Mas não importa. Esta é a minha oportunidade. Uma chance de começar algo novo."),
    "O ônibus passa por um desnível e a imagem treme. A voz do motorista anuncia a chegada ao ponto.",
], destino_auto="c03_ponto")

# =====================================================================
# CENA 3 — O PONTO DE ÔNIBUS
# =====================================================================
cena("c03_ponto", [
    "O ônibus para num local isolado. Você desce meio torto, quase tropeça no último degrau e segura a mochila contra o corpo.",
    "Também descem quatro outros passageiros: um casal elegante, uma senhora de postura firme e um homem de olhar atento, com um caderno no bolso do casaco.",
    "No ponto, duas pessoas de pele acinzentada esperam em silêncio. Observam o grupo sem demonstrar reação alguma.",
    com("O ônibus parte. Os cinco ficam sozinhos, cada um segurando um bilhete dourado.", {"itens": ["bilhete_dourado"]}),
    "",
    f("louise", "Parece que todos estamos esperando o mesmo transporte."),
    "Ela mostra o próprio bilhete.",
    f("louise", "Eu sou Louise de Bellacourt. Este é Gabriel, meu marido.", ao={"conhece": ["gabriel"], "hud": ["social"]}),
    f("louise", "Nós nos casamos recentemente. Ganhamos dois bilhetes para passar um ano aqui. Consideramos uma espécie de lua de mel prolongada."),
    "Gabriel apenas cumprimenta o grupo com a cabeça.",
    "",
    f("eugenie", "Meu nome é Eugénie Bresson."),
    f("eugenie", "Trabalhei a vida inteira. Agora estou aposentada e quero aproveitar um ano de paz. Boa comida e nenhum restaurante para administrar."),
    "",
    f("arthur", "Arthur Doyle. Também ganhei o sorteio, como vocês."),
    f("arthur", "Para ser sincero, achei a premiação estranha. Um ano de hospedagem, alimentação e transporte gratuitos não é exatamente um prêmio comum."),
    f("arthur", "Sou jornalista. Trabalho a distância, faço pesquisas e escrevo pequenas reportagens. Por isso, consigo continuar trabalhando durante a viagem."),
    "Arthur olha de relance para as duas pessoas acinzentadas.",
    f("arthur", "Pelo menos, acho que consigo."),
    "",
    "Você não diz nada. Segura o bilhete e observa o grupo.",
    "Ao longe, o som de cascos se aproxima. As duas pessoas acinzentadas viram a cabeça, ao mesmo tempo, para a estrada.",
], destino_auto="c04_carruagem",
   chegada={"hud": ["tempo"]})

# =====================================================================
# CENA 4 — A CARRUAGEM
# =====================================================================
cena("c04_carruagem", [
    "Uma carruagem antiga surge pela estrada, puxada por dois cavalos completamente brancos.",
    "Um homem de trajes vitorianos desce do assento do condutor, passa a mão sobre um dos cavalos e abre a porta.",
    f("cocheiro", "Por favor, entrem. Posso ajudá-los com as bagagens?"),
    f("louise", "Sim, por favor."),
    "O Cocheiro recolhe as malas. A cada uma que ele guarda, um turista entra. Você é o último.",
    f("cocheiro", "Sua bagagem, por favor."),
    "Você entrega a única mochila. Todos os lugares internos já estão ocupados.",
    f("cocheiro", "Parece que não há mais espaço. Você terá que viajar comigo."),
    "Ele fecha a porta, sobe no assento e estende a mão. Você aceita a ajuda e senta ao lado dele.",
    "",
    f("thiago", "Então... qual é o seu nome?"),
    f("cocheiro", "Todos me chamam de Cocheiro. E você?"),
    f("thiago", "Meu nome é Thiago."),
    f("thiago", "Como é trabalhar naquele hotel?"),
    f("cocheiro", "Diferente. Aquele lugar é diferente de qualquer outro que você já conheceu."),
    f("cocheiro", "Pelo que entendi, todos vocês ganharam um ano de hospedagem."),
    f("thiago", "Sim. Isso é normal?"),
    "O Cocheiro esboça um sorriso frio.",
    f("cocheiro", "Mais do que você imagina. Mas fale um pouco sobre você."),
], opcoes=[
    op("reservado", "“Não existe muito o que contar. Sou apenas um órfão.”", "c04b_chegada",
       {"flags": {"cocheiro_impressao": "reservado"}}),
    op("otimista", "“Sou um cara de muita sorte. Um órfão que ganhou um ano inteiro num hotel, com tudo pago.”", "c04b_chegada",
       {"flags": {"cocheiro_impressao": "otimista"}}),
], chegada={"tempo": 10})

# =====================================================================
# CENA 4 (cont.) — A CHEGADA E O CARTÃO
# =====================================================================
cena("c04b_chegada", [
    n("O Cocheiro olha para você por um instante. Parece enxergar, por trás da frase, a solidão de quem não tem para onde voltar.",
      {"flag": "cocheiro_impressao", "valor": "reservado"}),
    n("O Cocheiro olha para você por um instante. Parece ter percebido que você acredita, de verdade, no sorteio.",
      {"flag": "cocheiro_impressao", "valor": "otimista"}),
    "Ele apenas acena com a cabeça.",
    "",
    "Os portões se abrem antes de a carruagem parar. O Cocheiro descarrega as malas e conduz Gabriel, Louise, Eugénie e Arthur até a entrada.",
    "Você tenta ver quem recolhe as bagagens, mas, quando acompanha o movimento, os turistas já desapareceram no interior.",
    "O Cocheiro volta, ajuda você a descer e entrega um cartão.",
    f("cocheiro", "Pelo que me contou, talvez você precise de um emprego quando sua hospedagem terminar."),
    f("cocheiro", "Você não tem uma família nem outro lugar esperando por você. Correto?"),
    f("thiago", "Sim."),
    f("cocheiro", "Então guarde isto. Se precisar de alguma coisa, procure por mim."),
    item("cartao_cocheiro"),
    "Você caminha até a entrada. Ao olhar para trás, a carruagem, os cavalos e o Cocheiro desapareceram.",
    "O portão começa a se fechar.",
], opcoes=[
    op("correr", "Correr até o portão.", "c05_porteiro"),
], chegada={"tempo": 30})

# =====================================================================
# CENA 5 — O PORTEIRO
# =====================================================================
cena("c05_porteiro", [
    "Você atravessa o portão no último instante.",
    "Do lado de dentro, vê uma menina vestida de preto brincando sozinha com uma bola. Ela a joga contra a muralha e espera que volte. Não olha para você, nem fala.",
    "Antes que você consiga observá-la melhor, uma voz chama sua atenção.",
    f("porteiro", "Você está atrasado."),
    f("thiago", "Atrasado? E os outros hóspedes?"),
    f("porteiro", "Todos estão atrasados. Nenhum de vocês deveria estar aqui a esta hora."),
    f("thiago", "Mas eu ganhei um sorteio. Posso entrar?"),
    f("porteiro", "Mostre-me o seu bilhete."),
    "Você entrega o bilhete dourado. O Porteiro examina a escrita, o selo e o próprio hóspede.",
    f("porteiro", "O bilhete parece verdadeiro. Mas preciso fazer uma última pergunta."),
    f("porteiro", "Você realmente deseja estar aqui?"),
], opcoes=[
    op("sim", "“Sim.”", "c05b_porteiro_fim"),
], chegada={"tempo": 5})

cena("c05b_porteiro_fim", [
    f("thiago", "Eu sou órfão. Não tenho outro lugar para onde ir."),
    "O Porteiro avalia você em silêncio e devolve o bilhete.",
    f("porteiro", "Entendo. Siga-me, por favor."),
    "Ele conduz você até o hall. A porta se fecha atrás de vocês e, quando você se vira, o Porteiro já desapareceu.",
    "Ao longe, você vê Arthur, o último dos turistas, entrando no elevador. Depois, caminha até a recepção.",
], destino_auto="c06_sorteio")

# =====================================================================
# CENA 6 — BEM-VINDO AO HOTEL LOS SEGREDOS
# =====================================================================
cena("c06_sorteio", None, tipo="sorteio", dados={"opcoes": [
    {"destino": "c06_recepcao", "efeitos": {"flags": {"recepcionista": "mavis"}}},
    {"destino": "c06_recepcao", "efeitos": {"flags": {"recepcionista": "jonathan"}}},
]})

cena("c06_recepcao", [
    n("Uma jovem de cabelos pretos e curtos organiza as chaves atrás do balcão.", MAVIS),
    f("mavis", "Você deve ser o último hóspede.", MAVIS),
    f("thiago", "Acho que sim. Meu nome é Thiago.", MAVIS),
    f("mavis", "Prazer, Thiago. Eu sou Mavis. Bem-vindo ao Hotel Los Segredos.", MAVIS),
    n("Ela encontra o nome dele no registro.", MAVIS),
    f("mavis", "Dezenove anos... hospedagem por um ano inteiro... Está tudo certo.", MAVIS),
    n("Mavis observa sua única mochila.", MAVIS),
    f("mavis", "Essa é toda a sua bagagem?", MAVIS),

    n("Um homem de terno impecável organiza documentos e chaves atrás do balcão.", JON),
    f("jonathan", "Thiago. Dezenove anos. Brasil.", JON),
    f("thiago", "Como você sabe?", JON),
    n("Jonathan vira o livro de hóspedes na sua direção.", JON),
    f("jonathan", "Eu estava esperando por você. Meu nome é Jonathan. Bem-vindo ao Hotel Los Segredos.", JON),
    n("Ele observa a mochila.", JON),
    f("jonathan", "Você trouxe pouca bagagem para alguém que ficará hospedado durante um ano.", JON),
], opcoes=[
    op("m1", "“É tudo o que tenho.”", "c06_regras",
       {"flags": {"impressao_recepcao": "sinceridade"}, "relacoes": {"mavis": {"afeto": 3}}}, MAVIS),
    op("m2", "“Prefiro viajar com pouca coisa.”", "c06_regras",
       {"flags": {"impressao_recepcao": "bom_humor"}, "relacoes": {"mavis": {"afeto": 2}}}, MAVIS),
    op("m3", "“Podemos falar sobre o meu quarto?”", "c06_regras",
       {"flags": {"impressao_recepcao": "reservado"}}, MAVIS),
    op("j1", "“É tudo o que tenho.”", "c06_regras",
       {"flags": {"impressao_recepcao": "vulneravel"}, "relacoes": {"jonathan": {"confianca": 2}}}, JON),
    op("j2", "“Se eu precisar de alguma coisa, o hotel paga. Certo?”", "c06_regras",
       {"flags": {"impressao_recepcao": "confiante"}}, JON),
    op("j3", "“Isso é algum problema?”", "c06_regras",
       {"flags": {"impressao_recepcao": "desconfiado"}, "relacoes": {"jonathan": {"confianca": -2}}}, JON),
], chegada={"tempo": 5})

cena("c06_regras", [
    n("Mavis sorri, um pouco apressada, e abre o registro numa página com três linhas.", MAVIS),
    n("Jonathan fecha o livro de hóspedes e apoia as mãos no balcão.", JON),
    f("mavis", "São só três regras. Prometo que são fáceis.", MAVIS),
    f("jonathan", "Existem três regras. Espero que você as memorize.", JON),
    "",
    sis("<b>REGRA 1</b><br>RESPEITE OS HORÁRIOS DAS REFEIÇÕES"),
    f("mavis", "O restaurante tem horários certinhos. Por favor, não perca nenhuma refeição, tá? Depois fica difícil arranjar comida.", MAVIS),
    f("jonathan", "O restaurante não permanecerá aberto por causa de atrasos individuais.", JON),
    "",
    sis("<b>REGRA 2</b><br>NÃO CIRCULE DURANTE A NOITE"),
    f("mavis", "O hotel é muito antigo, e os corredores podem ser perigosos quando estão vazios. É mais seguro ficar no quarto.", MAVIS),
    f("jonathan", "Depois que os corredores fecharem, você permanece no seu quarto. Sem exceções.", JON),
    "",
    sis("<b>REGRA 3</b><br>NÃO ENTRE EM ÁREAS PROIBIDAS"),
    f("mavis", "Se uma porta estiver trancada, por favor, não tente abri-la. Existem bons motivos para certas áreas ficarem fechadas.", MAVIS),
    f("jonathan", "Portas trancadas e avisos não devem ser ignorados.", JON),
    "",
    "Você recebe uma chave pesada, de metal escuro.",
    item("chave_quarto"),
    f("mavis", "Não precisa ficar assustado. Se respeitar as regras, tenho certeza de que vai adorar este lugar.", MAVIS),
    f("mavis", "Venha. Vou mostrar o seu quarto.", MAVIS),
    f("jonathan", "Siga as regras e sua permanência será tranquila.", JON),
    f("thiago", "E se eu quebrar alguma delas?", JON),
    f("jonathan", "Então sua permanência poderá terminar antes do previsto.", JON),
    f("jonathan", "Venha. Vou levá-lo ao seu quarto.", JON),
], destino_auto="c07_elevador", chegada={"tempo": 5})

# =====================================================================
# CENA 7 — O SÉTIMO ANDAR
# =====================================================================
cena("c07_elevador", [
    "Você olha a chave: <b>Suíte 14</b>. O botão do sétimo andar se acende.",
    f("thiago", "Este hotel parece muito maior por dentro.", MAVIS),
    f("mavis", "E você ainda não viu quase nada.", MAVIS),
    f("thiago", "Este hotel é muito grande.", JON),
    f("jonathan", "Maior do que você imagina.", JON),
    "",
    "Depois do elevador, vocês atravessam um corredor ladeado por armaduras.",
    f("thiago", "Que armaduras estranhas."),
    f("mavis", "Eu gosto delas. Mas tome cuidado com o que fala perto delas. As paredes têm ouvidos. Quer dizer... as armaduras.", MAVIS),
    f("jonathan", "Estão aqui há séculos. Velhas e bastante empoeiradas. Tenha cuidado com o que fala perto delas. Dizem as lendas que elas têm ouvidos.", JON),
], destino_auto="c08_suite", chegada={"tempo": 10})

# =====================================================================
# CENA 8 — A SUÍTE 14
# =====================================================================
cena("c08_suite", [
    "A porta se abre para um quarto amplo: cama de casal, janela fechada, um guarda-roupa grande, mesa, criado-mudo, uma penteadeira com espelho e a porta do banheiro.",
    f("thiago", "Isso tudo é meu?"),
    f("mavis", "Durante um ano, sim. Espero que você se sinta em casa.", MAVIS),
    f("mavis", "O banheiro é ali, caso queira. Vou buscar seu jantar, já que você chegou atrasado.", MAVIS),
    f("jonathan", "Durante o período indicado no seu bilhete.", JON),
    f("jonathan", "O banheiro é ali. Daqui a pouco voltarei com seu jantar, já que você chegou atrasado.", JON),
    "A porta se fecha e você fica sozinho. Coloca a mochila sobre a cama.",
], opcoes=[
    op("banho", "Tomar um banho.", "c08b_suspeita",
       {"flags": {"tomou_banho": True}, "definir": {"suspeita": 0}, "tempo": 25}),
    op("descansar", "Deitar e descansar.", "c08b_suspeita",
       {"flags": {"tomou_banho": False}, "tempo": 15}),
], chegada={"tempo": 5, "mapa": ["suite14"]})

cena("c08b_suspeita", [
    n("A água quente leva embora o cansaço e o cheiro da viagem. Você se sente, de algum jeito, mais leve e menos visível.", BANHO),
    n("Você se joga na cama, sem tirar os sapatos. O cheiro da viagem ainda está em você, e o cansaço pesa nas pálpebras.", SEM_BANHO),
    "",
    sis("<b>SUSPEITA</b><br>Esta barra mostra o quanto os moradores desconfiam de você. Quanto maior o valor, mais eles suspeitam; quanto mais perto de zero, menos você chama atenção.<br>Banho, roupas limpas e comportamento convincente ajudam a baixar. Ela sobe quando você faz algo que não devia."),
    n("Como você tomou banho, sua Suspeita caiu para <b>0</b>.", BANHO),
    n("Como você não tomou banho, sua Suspeita continua em <b>50</b>.", SEM_BANHO),
], destino_auto="c09_jantar", chegada={"hud": ["suspeita"]})

# =====================================================================
# CENA 9 — ENTREGA DO JANTAR
# =====================================================================
cena("c09_jantar", [
    "Uma batida leve na porta. O cheiro de comida quente chega antes de qualquer coisa.",
    n("Você abre a porta usando apenas uma toalha. Mavis fica vermelha, entrega a bandeja rapidamente e olha para qualquer lugar menos para você.", [BANHO, MAVIS]),
    f("mavis", "Ah... você resolveu tomar banho. Aqui está seu jantar. Espero que goste. Não vou incomodar mais.", [BANHO, MAVIS]),
    f("jonathan", "Pelo visto, resolveu tomar banho. Aqui está seu jantar. Não vou atrapalhá-lo mais.", [BANHO, JON]),
    n("As batidas na porta acordam você. Mavis está do outro lado, segurando uma bandeja grande demais para os braços dela.", [SEM_BANHO, MAVIS]),
    f("mavis", "Desculpe acordar você! Aqui está o jantar. Boa noite, Thiago.", [SEM_BANHO, MAVIS]),
    n("As batidas na porta acordam você. Jonathan está do outro lado, com a bandeja equilibrada numa mão só.", [SEM_BANHO, JON]),
    f("jonathan", "Seu jantar. Boa noite.", [SEM_BANHO, JON]),
    "Quem trouxe a comida se retira, fechando a porta com cuidado.",
], opcoes=[
    op("comer", "Comer o jantar.", "c10_fome"),
], chegada={"tempo": 30})

# =====================================================================
# CENA 10 — FOME E ATRIBUTOS
# =====================================================================
cena("c10_fome", [
    "É estranho. Você não consegue identificar bem o que é, mas o cheiro é inegavelmente convidativo. Come tudo. Uma refeição normal e segura, pelo menos aparentemente.",
    "",
    sis("<b>FOME</b><br>Esta barra mostra o quanto você está alimentado: <b>100/100</b>.<br>Quanto maior, menos fome você sente; quanto mais perto de zero, mais faminto. Refeições restauram a barra."),
    "",
    "Você se levanta, ainda mastigando o último pedaço, e para diante do espelho da penteadeira.",
], destino_auto="c10_espelho", chegada={"hud": ["fome"], "tempo": 20})

cena("c10_espelho", [
    "O espelho é antigo, de moldura escura. O rosto que o encara é o seu: moreno, cabelos negros, olhos castanhos claros, um corpo forte de quem sempre precisou se virar sozinho.",
    pens("Um ano inteiro neste lugar..."),
    pens("Quem eu vou ser durante esse tempo?"),
], tipo="espelho", dados={"pontos": 30, "passo": 10, "max": 80, "base": 50},
   destino_auto="c11_musica", chegada={"tempo": 10})

# =====================================================================
# CENA 11 — A MÚSICA
# =====================================================================
cena("c11_musica", [
    "Depois da confirmação, você deita e adormece quase de imediato.",
    "",
    "Algum tempo depois, você acorda com um som distante: um piano.",
    f("thiago", "Música a uma hora dessas? Isso deve estar acordando os outros hóspedes."),
], opcoes=[
    op("seguir", "Levantar e seguir a música.", "c11a_piano"),
    op("ignorar", "Ignorar e tentar dormir.", "c11b_telefone"),
], chegada={"ate": "03:10", "sono": True})

# 11A — A MULHER DO PIANO
cena("c11a_piano", [
    "Você abre a porta e atravessa o corredor escuro. A música vem de uma sala no fim do andar. Lá dentro, na penumbra, uma mulher de vestido branco e cabelos longos toca ao piano.",
    f("mulher_piano", "Não consegue dormir?"),
    f("thiago", "Eu ouvi a música."),
    f("mulher_piano", "Desculpe. Às vezes esqueço que algumas pessoas ainda precisam dormir."),
    f("thiago", "É uma música muito bonita."),
    f("mulher_piano", "Fui eu quem compôs. E então? O que achou do hotel?"),
    f("thiago", "Antigo. Muito grande... e bastante velho."),
    "A mulher ri, sem desviar os olhos das teclas.",
    f("mulher_piano", "Diga-me uma coisa, Thiago. Você acredita em fantasmas?"),
], opcoes=[
    op("sim", "“Acredito, sim.”", "c11a_pos", {"flags": {"resposta_fantasmas": "sim"}}),
    op("nao", "“Não. Fantasmas não existem.”", "c11a_pos", {"flags": {"resposta_fantasmas": "nao"}}),
], chegada={"tempo": 15, "flags": {"conheceu_elisabeta": True},
            "mapa": ["sala_musica"]})

cena("c11a_pos", [
    n("Ela inclina a cabeça, com um brilho de curiosidade nos olhos.", {"flag": "resposta_fantasmas", "valor": "sim"}),
    f("mulher_piano", "Interessante. Poucos têm essa coragem.", {"flag": "resposta_fantasmas", "valor": "sim"}),
    n("Ela sorri, e há algo de triste nesse sorriso.", {"flag": "resposta_fantasmas", "valor": "nao"}),
    f("mulher_piano", "Que pena. Seria bom se fosse verdade.", {"flag": "resposta_fantasmas", "valor": "nao"}),
    "",
    "Ela se levanta e se aproxima. Antes que você possa recuar, ela sopra um pó branco no seu rosto.",
    "As pernas cedem. Você cai para trás, e a última coisa que vê é o vestido branco se afastando na penumbra.",
], destino_auto="c11a_acorda", chegada={"tempo": 10})

cena("c11a_acorda", [
    "Você acorda num sobressalto, deitado na cama, ainda vestido. O quarto está escuro e em silêncio. O piano parou.",
    pens("Eu voltei para a cama sozinho? Eu não lembro de ter voltado."),
    pens("Deve ter sido um sonho. A mulher, a música, aquele pó... Só pode ter sido um sonho."),
    "Você puxa o cobertor até o queixo e, depois de muito tempo olhando para o teto, volta a dormir.",
], destino_auto="c12_sonho", chegada={"tempo": 5})

# 11B — O TELEFONEMA
cena("c11b_telefone", [
    "Você puxa o cobertor sobre a cabeça. A música continua, distante. De repente, outro som: o telefone do quarto começa a tocar.",
], opcoes=[
    op("atender", "Atender o telefone.", "c11b_lily"),
    op("ignorar", "Ignorar e voltar a dormir.", "c12_sonho",
       {"flags": {"lily_conhecida": False}}),
], chegada={"tempo": 5})

cena("c11b_lily", [
    f("desconhecida", "Thiago? Espero não ter acordado você."),
    f("thiago", "Quem está falando?"),
    f("lily", "Meu nome é Lily. Sou responsável pelo sorteio que você ganhou."),
    f("lily", "Chegou bem? Está tudo tranquilo? Notou alguma coisa diferente?"),
], opcoes=[
    op("tranquilo", "“Está tudo tranquilo.”", "c11b_lily_fim", {"flags": {"resposta_lily": "tranquilo"}}),
    op("estranho", "“O hotel é velho e estranho.”", "c11b_lily_fim", {"flags": {"resposta_lily": "estranho"}}),
], chegada={"tempo": 10, "flags": {"lily_conhecida": True}})

cena("c11b_lily_fim", [
    n("Há uma pausa curta do outro lado da linha.", {"flag": "resposta_lily", "valor": "estranho"}),
    f("lily", "Entendo. É assim mesmo no começo.", {"flag": "resposta_lily", "valor": "estranho"}),
    f("lily", "Que bom que está tudo bem.", {"flag": "resposta_lily", "valor": "tranquilo"}),
    f("lily", "Tenho uma amiga que trabalha aí. O nome dela é Nix.", ao={"conhece": ["nix"]}),
    f("lily", "Se precisar de ajuda, pode procurá-la."),
    f("lily", "Aproveite sua estadia, Thiago. Voltaremos a conversar."),
    "A linha fica muda. Você deixa o fone no gancho e volta a se deitar, sem conseguir tirar a voz da cabeça.",
], destino_auto="c12_sonho", chegada={"tempo": 5})

# =====================================================================
# CENA 12 — O SONHO
# =====================================================================
cena("c12_sonho", [
    "Você sonha que está voando. Voando no escuro, sem chão, sem teto, sem medo.",
    n("Uma voz sem dono ecoa:"),
    pens("Bem... quem é você?"),
], tipo="tracos", dados={"virtudes": 2, "vicios": 1}, destino_auto="c13_despertar")

# =====================================================================
# CENA 13 — O DESPERTAR
# =====================================================================
cena("c13_despertar", [
    "Você deixa de voar. Começa a cair. O escuro acelera, o vento rasga, e o chão vem ao seu encontro até o impacto apagar tudo.",
    "",
    "Você acorda assustado, caído ao lado da cama, enrolado no cobertor. Ainda sente o estômago preso na queda.",
    "A luz da manhã passa pelas frestas da janela.",
    "",
    sis("<b>SEU PERFIL</b><br>Agora você pode consultar seus atributos, suas características (duas virtudes e um vício) e suas habilidades no botão <b>Perfil</b>, no topo da tela. As barras de <b>Vida</b> e <b>Sanidade</b> também aparecem ali."),
], destino_auto="c14_retrato",
   chegada={"ate": "07:00", "sono": True, "hud": ["perfil", "vida", "sanidade"]})

# =====================================================================
# CENA 14 — O OUTRO RECEPCIONISTA E O RETRATO
# =====================================================================
OUTRO_MAVIS = JON      # se Jonathan recebeu, quem aparece é Mavis
OUTRO_JON = MAVIS
cena("c14_retrato", [
    n("Alguém bate à porta. É Mavis, de braços cruzados e com um sorriso cansado de quem já acordou há horas.", OUTRO_MAVIS),
    n("Alguém bate à porta. É Jonathan, impecável como na véspera, com o relógio de bolso na mão.", OUTRO_JON),
    f("mavis", "Bom dia! Vim buscar você para o café. Está na hora.", OUTRO_MAVIS),
    f("jonathan", "O café da manhã tem horário. Vamos.", OUTRO_JON),
    "Vocês descem pelo corredor das armaduras. No caminho, você para diante de um grande retrato a óleo: uma mulher de vestido branco e cabelos longos.",
    "",
    # --- viu a Mulher do Piano ---
    f("thiago", "Esta mulher... eu a vi ontem à noite. Ela estava tocando piano.", VIU_ELI),
    f("mavis", "Impossível. Aquela é minha mãe. Elisabeta morreu há muito tempo.", [VIU_ELI, OUTRO_MAVIS]),
    n("Mavis desvia o rosto, magoada, e fica em silêncio.", [VIU_ELI, OUTRO_MAVIS]),
    f("jonathan", "Você sonhou. A esposa do fundador morreu há séculos.", [VIU_ELI, OUTRO_JON]),
    pens("Morta há séculos... Mas eu a vi. Eu falei com ela.", VIU_ELI),
    # --- não viu ---
    f("thiago", "Quem é ela?", NAO_VIU_ELI),
    f("mavis", "Elisabeta. Minha mãe. Ela morreu há muito tempo.", [NAO_VIU_ELI, OUTRO_MAVIS]),
    f("jonathan", "Elisabeta, a esposa do fundador. Mãe de Mavis. Já falecida.", [NAO_VIU_ELI, OUTRO_JON]),
    # --- atendeu a Lily ---
    "",
    f("thiago", "Falando em pessoas... uma mulher chamada Lily ligou para o meu quarto. Disse ser responsável pelo sorteio. Mencionou uma amiga, a Nix.", ATENDEU),
    f("mavis", "Nix? Ela é nova aqui. Por favor, não atrapalhe o trabalho dela, tá?", [ATENDEU, OUTRO_MAVIS]),
    f("jonathan", "Lily? Estranho. Recomendo que você não interfira nos funcionários.", [ATENDEU, OUTRO_JON]),
], destino_auto="c15_refeitorio",
   chegada={"tempo": 15})

# =====================================================================
# CENA 15 — APRESENTAÇÃO NO REFEITÓRIO
# =====================================================================
cena("c15_refeitorio", [
    "O refeitório é um salão comprido, de mesas pesadas e janelas altas. No cheiro do café, há algo que você não consegue nomear.",
    "Mavis e Jonathan ficam lado a lado, junto da entrada.",
    f("jonathan", "Esta é Mavis. Minha noiva.", JON),
    n("Mavis sorri para você, mas há um segundo de hesitação antes do sorriso.", JON),
    f("mavis", "Então você conheceu o Jonathan. Ele é o meu noivo.", MAVIS),
    f("jonathan", "Nós dois administramos a parte hoteleira, com a ajuda de outros funcionários. Qualquer dúvida, procure um de nós.", MAVIS),
    f("jonathan", "Nós dois administramos a parte hoteleira, com a ajuda de outros funcionários. Qualquer dúvida, procure um de nós.", JON),
    "",
    "Você pega sua refeição e olha ao redor, procurando um lugar. Só dá para sentar com um grupo.",
], opcoes=[
    op("arthur", "Sentar com Arthur.", "c16_arthur", {"flags": {"mesa": "arthur"}}),
    op("casal", "Sentar com Gabriel e Louise.", "c16_casal", {"flags": {"mesa": "casal"}}),
    op("eugenie", "Sentar com Eugénie.", "c16_eugenie", {"flags": {"mesa": "eugenie"}}),
], chegada={"tempo": 15})

# =====================================================================
# CENA 16 — CONVERSA ESCOLHIDA
# =====================================================================
cena("c16_arthur", [
    f("arthur", "Dormiu bem?"),
    # viu a Mulher do Piano
    f("thiago", "Na verdade, tive um sonho estranho. Uma mulher de branco, tocando piano.", VIU_ELI),
    n("Arthur larga o garfo. O olhar de repórter se acende.", VIU_ELI),
    f("arthur", "Branco, cabelos longos... e um pó que ela soprava no rosto? Eu sonhei com a mesma mulher.", VIU_ELI),
    f("thiago", "Isso é... uma coincidência enorme.", VIU_ELI),
    f("arthur", "Coincidência. Deve ser coincidência. A gente jantou a mesma comida pesada, dormiu no mesmo hotel antigo... é natural.", VIU_ELI),
    # atendeu a Lily
    f("thiago", "Alguém ligou para o meu quarto, no meio da noite.", [ATENDEU, NAO_VIU_ELI]),
    f("arthur", "Uma tal de Lily? Ela ligou para mim também. Disse que era responsável pelo sorteio.", ATENDEU),
    f("arthur", "Eu não dei muita atenção. Acho que ela liga para todos os hóspedes.", ATENDEU),
    # nenhum
    f("thiago", "Tranquila. Dormi como uma pedra.", [NAO_VIU_ELI, {"flag": "lily_conhecida", "valor": False}]),
    f("arthur", "Eu também. Uma noite normal, o que já é um alívio nesse lugar.", [NAO_VIU_ELI, {"flag": "lily_conhecida", "valor": False}]),
    "Arthur racionaliza tudo com um sorriso torto, anotando alguma coisa no caderno. Mas, por um momento, você nota que ele não tira os olhos da porta da cozinha.",
], destino_auto="c17_tutorial", chegada={"tempo": 25})

cena("c16_casal", [
    f("louise", "Dormiu bem, querido? Esses colchões são divinos."),
    f("thiago", "Foi uma noite tranquila."),
    f("louise", "Que bom! Nós também. Gabriel e eu já começamos a lua de mel... se é que me entende."),
    n("Gabriel limpa a garganta e finge examinar o próprio prato.", None),
    f("gabriel", "Louise."),
    f("louise", "O que foi? Ele é jovem, não é bobo."),
    "Os dois riem. É uma risada sem maldade, de gente que sempre teve tudo. Você sente que vai gostar deles, mesmo que eles sejam um pouco insuportáveis.",
], destino_auto="c17_tutorial", chegada={"tempo": 25})

cena("c16_eugenie", [
    f("eugenie", "E então, rapaz? O que achou da comida?"),
    f("thiago", "Ótima. Não sei bem o que é, mas é ótima."),
    "Eugénie levanta uma sobrancelha, satisfeita.",
    f("eugenie", "Fui chef a vida inteira. Tive restaurantes famosos. Eu sei reconhecer mão de mestre quando provo."),
    f("eugenie", "Quem quer que cozinhe aqui... é muito bom. Preciso conhecê-lo pessoalmente."),
    "Ela diz isso com um brilho de admiração profissional, sem notar o olhar de Mavis, do outro lado do salão, que se vira bruscamente em sua direção.",
], destino_auto="c17_tutorial", chegada={"tempo": 25})

# =====================================================================
# CENA 17 — TUTORIAIS DE FOME E VIDA
# =====================================================================
cena("c17_tutorial", [
    "Enquanto você come, o salão fica levemente fora de foco, como se o hotel quisesse lhe dizer uma coisa em voz baixa.",
    "",
    sis("<b>FOME</b><br>Lembre-se sempre de comer para não morrer de fome.<br>Se sua fome baixar para <b>10</b>, você pode ter alucinações. Isso afeta sua sanidade.<br>Se baixar para <b>5</b>, você pode desmaiar e acordar na clínica.<br>Se sua fome zerar, bem... você morre."),
    sis("<b>VIDA</b><br>Valor inicial: <b>100/100</b>.<br>Ataques, ferimentos e fome extrema reduzem esta barra. Se chegar a zero, você pode morrer."),
    "",
    "Quando o salão volta ao foco, você termina o café e anuncia que vai voltar ao quarto.",
], destino_auto="c17_sorteio", classe="desfoque",
   chegada={"definir": {"fome": 100}, "tempo": 20})

cena("c17_sorteio", None, tipo="sorteio", dados={"opcoes": [
    {"destino": "c17_despedida", "efeitos": {"flags": {"despedida": "mavis"}}},
    {"destino": "c17_despedida", "efeitos": {"flags": {"despedida": "jonathan"}}},
]})

cena("c17_despedida", [
    f("mavis", "Qualquer coisa, é só chamar. Bom primeiro dia, Thiago!", {"flag": "despedida", "valor": "mavis"}),
    f("jonathan", "Respeite os horários. Até logo.", {"flag": "despedida", "valor": "jonathan"}),
], destino_auto="c18_corredor", chegada={"flags": {"fome_ativa": True}, "tempo": 5})

# =====================================================================
# CENA 18 — O MAPA
# =====================================================================
cena("c18_corredor", [
    "No corredor, você para novamente diante do retrato da mulher de branco.",
    pens("Será que foi tudo um sonho?", VIU_ELI),
    pens("Como é que nós dois sonhamos com a mesma pessoa?", [VIU_ELI, {"flag": "mesa", "valor": "arthur"}]),
    pens("Uma mulher muito bonita...", NAO_VIU_ELI),
    "",
    "Você entra na Suíte 14. A bandeja suja da noite passada desapareceu, e ninguém bateu na porta.",
], destino_auto="c18_cond", chegada={"tempo": 5})

# quem atendeu o telefone à noite vai direto ao mapa; quem não atendeu recebe a ligação da manhã
cena("c18_cond", None, tipo="condicional", dados={"flag": "lily_conhecida",
    "casos": {"true": "c18_mapa"}, "padrao": "c18_ligacao"})

cena("c18_ligacao", [
    "O telefone do quarto começa a tocar. Desta vez, você atende.",
    f("desconhecida", "Thiago? Espero não estar incomodando."),
    f("thiago", "Quem está falando?"),
    f("lily", "Meu nome é Lily. Sou responsável pelo sorteio que você ganhou."),
    f("lily", "Chegou bem? Está tudo tranquilo? Notou alguma coisa diferente?"),
], opcoes=[
    op("tranquilo", "“Está tudo tranquilo.”", "c18_ligacao_fim", {"flags": {"resposta_lily": "tranquilo"}}),
    op("estranho", "“O hotel é velho e estranho.”", "c18_ligacao_fim", {"flags": {"resposta_lily": "estranho"}}),
], chegada={"tempo": 5})

cena("c18_ligacao_fim", [
    n("Há uma pausa curta do outro lado da linha.", {"flag": "resposta_lily", "valor": "estranho"}),
    f("lily", "Entendo. É assim mesmo no começo.", {"flag": "resposta_lily", "valor": "estranho"}),
    f("lily", "Que bom que está tudo bem.", {"flag": "resposta_lily", "valor": "tranquilo"}),
    f("lily", "Aproveite sua estadia, Thiago. Voltaremos a conversar."),
    "A linha fica muda. Você deixa o fone no gancho.",
], destino_auto="c18_mapa", chegada={"tempo": 5, "flags": {"lily_ligou_manha": True}})

cena("c18_mapa", [
    "No lugar da bandeja, sobre a cama, há um mapa dobrado.",
    item("mapa_hotel"),
    sis("<b>MAPA DO HOTEL</b><br>O botão <b>Mapa</b>, no canto inferior direito, mostra as áreas que você já conhece e as missões liberadas. Áreas sempre liberadas: Suíte 14, corredores públicos, hall de entrada, refeitório e biblioteca."),
    n("A <b>sala de música</b> também aparece no mapa.", VIU_ELI),
    "Dois pontos de interrogação já aparecem: um no refeitório e outro na biblioteca.",
], destino_auto="c18_janela",
   chegada={"tempo": 5, "hud": ["mapa"],
            "mapa": ["suite14", "corredores", "hall", "refeitorio", "biblioteca"],
            "marcadores": [{"area": "refeitorio", "texto": "Missão de Jonathan"},
                           {"area": "biblioteca", "texto": "Missão de Mavis"}]})

cena("c18_janela", [
    "Você desdobra o mapa sobre a cama. Uma sombra clara cruza a janela.",
    "Você levanta os olhos. No parapeito, do lado de fora, uma gata branca de olhos azuis observa você através do vidro.",
    "Ela fica imóvel por um instante. Então salta para o vazio.",
    pens("Este quarto fica no sétimo andar."),
], destino_auto="c19_fim", chegada={"tempo": 2})

cena("c19_fim", [
    "Capítulo 1 — A Chegada.",
    "",
    "Você tem um mapa, uma chave, um bilhete dourado e a vaga sensação de que o hotel sabe mais sobre você do que você sobre ele.",
    "A partir daqui, o hotel se abre. As missões, as pessoas e os segredos esperam por você. Algumas desaparecem se você demorar demais.",
    "",
    "Obrigado por jogar esta primeira parte. Se algo parecer estranho, anote a cena e a hora que aparece no relógio e me conte.",
], dados={"final": True, "mostrar_tempo": True})

json.dump(C, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(C), "cenas geradas")
