# -*- coding: utf-8 -*-
"""
VIDA NO HOTEL — conversas livres com quem já foi conhecido + pequenas observações por lugar.
É executado (exec) por gerar_parte2.py, então usa os mesmos ajudantes (f, n, sis, op, cena...).

Regras:
- Cada pessoa pode ser procurada para conversar UMA vez por dia, só no lugar e no horário em que ela está.
- As conversas são em sequência (1ª, 2ª, 3ª...) e depois sorteadas. Cada conversa aumenta um pouquinho a relação.
- Quem sumiu do jogo (Gabriel, Louise, Eugénie, Morte) não aparece aqui.
- "Observar" é sempre possível: gasta alguns minutos e mostra a vida do hotel.
"""

def _inserir_opcao(cena_id, opcao):
    """Coloca a opção antes do botão do mapa, na cena indicada."""
    for c in C:
        if c["id"] == cena_id:
            ops = c.setdefault("opcoes", [])
            # o "mapa" é sempre o último
            pos = len(ops)
            for i, o in enumerate(ops):
                if o["id"] == "mapa":
                    pos = i
                    break
            ops.insert(pos, opcao)
            return
    raise SystemExit("cena não encontrada: " + cena_id)

def papos(chave, cena_hub, rotulo, fundo, volta, conversas, presenca):
    """Cria as conversas de `chave` e a opção no hub. `presenca` = condições do 'se'."""
    ids = []
    for i, linhas in enumerate(conversas, 1):
        cid = f"papo_{chave}_{i}"
        ids.append(cid)
        cena(cid, linhas, destino_auto=volta,
             chegada={"somar": {f"papo_{chave}_n": 1}, "flags": {f"papo_{chave}_dia": "@dia"},
                      "relacoes": {chave: {"afeto": 2}}, "barras": {"sanidade": 1}, "tempo": 8},
             dados={"raiz": True}, fundo=fundo)
    cena(f"papo_{chave}_vario", None, tipo="sorteio", dados={"raiz": True, "opcoes": ids})
    casos = {str(i): ids[i] for i in range(1, len(ids))}          # 1 -> segunda conversa, 2 -> terceira...
    for k in range(len(ids), 60):
        casos[str(k)] = f"papo_{chave}_vario"
    cena(f"papo_{chave}", None, tipo="condicional",
         dados={"flag": f"papo_{chave}_n", "casos": casos, "padrao": ids[0], "raiz": True})
    _inserir_opcao(cena_hub, op(f"papo_{chave}_op", rotulo, f"papo_{chave}",
                                se=list(presenca) + [{"flag": f"papo_{chave}_dia", "diferente": "@dia"}]))

DIA = lambda a, b: {"flag": "@hora", "min": a, "max": b}
NAO_ATAQUE = {"flag": "clinica_ataque", "diferente": True}

# ---------------------------------------------------------------- JONATHAN (refeitório, nas refeições)
papos("jonathan", "hub_refeitorio", "Conversar com Jonathan, que passa entre as mesas", "refeitorio", "hub_refeitorio", [
    [
        "Jonathan está encostado numa coluna, com uma bandeja vazia debaixo do braço, vendo o salão como quem conta cabeças.",
        f("jonathan", "Thiago! Sente aí um minuto. O pão hoje está bom, ninguém reclamou."),
        f("jonathan", "Está se acostumando? Os primeiros dias aqui são sempre os mais esquisitos. Depois a gente aprende o ritmo da casa."),
        f("thiago", "O ritmo da casa?"),
        f("jonathan", "Comer na hora certa, dormir na hora certa, não perguntar demais. Parece pouco. Quase ninguém consegue."),
        "Ele sorri, bate de leve no seu ombro e volta para as mesas.",
    ],
    [
        f("jonathan", "Você anda bastante pelo hotel, não é? Vejo você na biblioteca, nos corredores, no hall."),
        f("thiago", "É um lugar grande. Eu ainda me perco."),
        f("jonathan", "Que bom. Quem se perde, olha melhor. E me diga, o que mais chamou a sua atenção até agora?"),
        "A pergunta soa casual. Mas ele espera a resposta com uma atenção grande demais para uma conversa de refeitório.",
        f("thiago", "Os corredores. À noite, principalmente."),
        f("jonathan", "À noite os corredores são do hotel. De dia, deixam a gente passar."),
        pens("Ele disse isso rindo. Eu acho que riu."),
    ],
    [
        f("jonathan", "Sabe o que eu mais gosto neste trabalho? Ver os hóspedes chegarem assustados e irem embora... diferentes."),
        f("thiago", "Diferentes como?"),
        f("jonathan", "Mais atentos. Mais cuidadosos. Alguns, mais gratos."),
        "Ele arruma uma cadeira que já estava no lugar.",
        f("jonathan", "A Mavis cuida da casa com o coração. Eu cuido com a cabeça. Entre os dois, o hotel anda de pé."),
        "Há um peso curioso na frase, como uma conta feita em voz baixa.",
    ],
    [
        f("jonathan", "Hoje o salão está calmo. É nessas horas que dá para ouvir o hotel."),
        f("thiago", "Ouvir o quê?"),
        f("jonathan", "Tudo. As portas, os passos, o encanamento. Quem presta atenção descobre que esta casa conversa o tempo todo."),
        f("jonathan", "Tome o seu café, Thiago. E continue prestando atenção."),
    ],
], [{"flag": "@propostas"}, {"flag": "jon_estado", "diferente": "recusada"}, REFEICAO])

# ---------------------------------------------------------------- MAVIS (salão de festas, de dia)
papos("mavis", "hub_salao_festas", "Conversar com Mavis, que prende faixas no teto", "salao_festas", "hub_salao_festas", [
    [
        "Mavis está equilibrada na escada, com uma fita de cetim entre os dentes. Ao ver você, ela quase a engole.",
        f("mavis", "Thiago! Pode segurar a escada? Obrigada. Não, não, mais firme. Esse piso tem vontade própria."),
        f("thiago", "Falta muito para a festa?"),
        f("mavis", "Falta tempo para tudo. Eu faço uma lista, a lista cresce, e quando eu risco um item nascem três."),
        "Ela desce, bufa uma mecha de cabelo da testa e sorri, cansada e sincera.",
        f("mavis", "Mas está ficando bonito, não está? Diga que está ficando bonito."),
        f("thiago", "Está ficando bonito."),
    ],
    [
        f("mavis", "Você dorme bem? Aqui o pessoal reclama dos sons à noite. Canos, madeira velha, esse tipo de coisa."),
        f("thiago", "Eu escuto um piano, às vezes."),
        "Mavis para de mexer na faixa. Por um segundo, o rosto dela fica sem cor, depois se recompõe.",
        f("mavis", "Piano. É... eco. A sala de música fica longe, mas o som corre pelas paredes. Não ligue."),
        f("mavis", "Se algum dia o susto for demais, me procure. Eu sempre estou por aqui. Quer dizer, sempre atrasada, mas por aqui."),
    ],
    [
        f("mavis", "Posso te contar uma coisa boba? Eu adoro quando o salão está vazio assim. Dá para imaginar a música, as pessoas, os vestidos."),
        f("thiago", "Você já viu uma festa por aqui?"),
        f("mavis", "Muitas. Mas é sempre a primeira vez para alguém. Este ano, é a primeira vez para você."),
        "Ela olha o teto, onde um lustre coberto por pano balança de leve, sem vento.",
        f("mavis", "Eu quero que seja bonita. Para todo mundo. Até para quem não gosta de festas."),
    ],
    [
        f("mavis", "Eu tenho uma gata que vive sumindo. Se vir uma bolinha de pelo atravessando o corredor, não corre atrás. Ela odeia."),
        f("thiago", "Eu não sabia que você tinha uma gata."),
        f("mavis", "Todo mundo tem uma coisa que não conta de primeira. Aquela é a minha."),
        "Ela ri baixinho e volta para a escada.",
    ],
], [{"flag": "@propostas"}, {"flag": "mavis_estado", "diferente": "recusada"}, DIA(9, 18)])

# ---------------------------------------------------------------- MACHA (hall)
papos("macha", "hall_base", "Conversar com Macha, que encosta na moto perto do portão", "hall", "hall_base", [
    [
        "Macha está sentada de lado na moto preta, girando uma chave entre os dedos. Quando você se aproxima, ela nem finge que não viu.",
        f("macha", "Veio tentar a porta de novo ou só veio me fazer companhia?"),
        f("thiago", "Companhia. Hoje, só isso."),
        f("macha", "Boa resposta. Pode ficar."),
        f("macha", "Sabe o que é bom em moto? Ninguém conversa com você enquanto você anda. Aqui dentro todo mundo fala demais."),
    ],
    [
        f("macha", "Pergunta boba: você sabe o que é uma curva fechada?"),
        f("thiago", "Uma curva muito... fechada?"),
        f("macha", "Meu Deus. Vai precisar de aula de tudo."),
        "Ela ri com vontade, e por um instante o hall inteiro parece menos frio.",
        f("macha", "Meu pai trabalha com rotas. Eu cresci vendo mapas, estradas, atalhos. Quando eu falo que a porta fica fechada, é porque eu sei o que tem lá fora."),
        f("thiago", "E o que tem lá fora?"),
        f("macha", "Caminho. Muito caminho. Ninguém atravessa sem saber para onde vai."),
    ],
    [
        f("macha", "Você tem cara de quem nunca teve brinquedo novo."),
        f("thiago", "Eu tinha o que o orfanato dava."),
        "Macha fica quieta por um momento, e o sorriso de lado desaparece.",
        f("macha", "Desculpa. Falei sem pensar."),
        f("macha", "Olha, quando eu te ensinar a pilotar, a primeira moto vai ser pequena. Mas vai ser sua pelo tempo que você precisar dela."),
    ],
    [
        f("macha", "Sabia que a minha moto some quando alguém tenta tocar nela sem eu deixar?"),
        f("thiago", "Eu já vi sumir. Eu achei que era truque de luz."),
        f("macha", "Truque de luz. Gostei. Vou usar isso."),
    ],
], [{"flag": "macha_conhecida"}, {"flag": "@noite", "valor": False}, NAO_ATAQUE])

# ---------------------------------------------------------------- ENOLA (biblioteca)
papos("enola", "biblioteca_base", "Conversar com Enola, que arruma livros na mesa", "biblioteca", "biblioteca_base", [
    [
        "Enola mal ergue os olhos de um volume encadernado em couro. A coruja pequena no ombro dela acompanha você com um olhar redondo e atento.",
        f("enola", "Senhor Thiago. Os livros comuns estão à sua disposição, como eu disse. Mas a boa leitura começa por saber o que se procura."),
        f("thiago", "Eu ainda não sei o que procuro."),
        f("enola", "A maioria dos hóspedes também não. É por isso que ficam. Procurar dá trabalho, e o trabalho é a melhor forma de passar o tempo."),
    ],
    [
        f("thiago", "A senhora conhece todos os livros daqui?"),
        f("enola", "Conheço cada lombada. O conteúdo, nem sempre. Alguns volumes mudam de ideia."),
        f("thiago", "Mudam de ideia?"),
        f("enola", "Figura de linguagem, senhor Thiago. Tome nota: aqui, às vezes, as figuras de linguagem têm pés."),
        "A coruja pia, baixinho, como quem concorda.",
    ],
    [
        f("enola", "Posso lhe dar um conselho? Não leia depois da meia-noite. Os livros ficam mais honestos, e a honestidade cansa."),
        f("thiago", "Eu não circulo depois das dez, de qualquer jeito."),
        f("enola", "Ótimo. Já é um bom começo de leitor."),
        "Ela volta ao trabalho. Um livro desliza sozinho de uma estante alta para a mesa, e ela o recebe sem olhar.",
    ],
    [
        f("enola", "Há perguntas que a biblioteca responde e perguntas que ela guarda. Eu aprendi a diferença com os anos."),
        f("thiago", "E qual é a diferença?"),
        f("enola", "As primeiras têm resposta. As segundas têm dono."),
    ],
], [{"flag": "enola_conhecida"}, {"flag": "@noite", "valor": False}])

# ---------------------------------------------------------------- NOSFERATU (biblioteca)
papos("nosferatu", "biblioteca_base", "Conversar com o idoso pálido da mesa afastada", "biblioteca", "biblioteca_base", [
    [
        "O velho ergue o rosto devagar. A pele é de cera, os olhos cansados e atentos. Ele marca a página com um dedo longo antes de fechar o livro.",
        f("nosferatu", "O jovem do convite. Sente-se, se quiser. Eu falo pouco, mas escuto com paciência."),
        f("thiago", "Desculpe incomodar. Eu só queria agradecer pela atenção."),
        f("nosferatu", "Gratidão é raridade. Guarde-a para quem merece."),
        "Há uma delicadeza antiga na voz dele, como seda guardada demais.",
    ],
    [
        f("nosferatu", "Quantos anos o senhor tem, rapaz?"),
        f("thiago", "Dezenove."),
        f("nosferatu", "Dezenove. Uma idade em que tudo parece começar. E também a idade em que tantas coisas já terminaram."),
        f("nosferatu", "Não responda. Falei sozinho."),
        "Ele abre o livro de novo, mas não lê. Apenas observa você de canto de olho, como quem conta algo que não é número.",
    ],
    [
        f("nosferatu", "A biblioteca é boa companheira. Não pede nada, não julga, e esquece quando a gente quer ser esquecido."),
        f("thiago", "E se a gente não quiser ser esquecido?"),
        f("nosferatu", "Então escreva. A tinta dura mais que a memória."),
        "Ele sorri de leve, sem mostrar os dentes.",
    ],
], [{"flag": "conv_biblio"}, {"flag": "@noite", "valor": False}])

# ---------------------------------------------------------------- ARTHUR (biblioteca)
papos("arthur", "biblioteca_base", "Conversar com Arthur, que cruza anotações numa mesa", "biblioteca", "biblioteca_base", [
    [
        "Arthur tem a mesa tomada por cadernos, canetas e um bule de chá frio. Ele levanta a cabeça como quem acorda.",
        f("arthur", "Thiago! Chegou na hora certa. Eu preciso de alguém que discorde de mim."),
        f("thiago", "Sobre o quê?"),
        f("arthur", "Tudo. Hipóteses. Quanto mais eu escrevo, mais elas parecem sensatas, e isso é péssimo sinal."),
    ],
    [
        f("arthur", "Anotei os horários de cada coisa estranha. Portas, passos, objetos. Veja: nenhuma acontece na frente de mais de duas pessoas."),
        f("thiago", "Isso quer dizer o quê?"),
        f("arthur", "Quer dizer que quem faz isso sabe quando estamos olhando. Ou que é muito azarado."),
        "Ele ri sozinho, mas a caneta continua batucando na mesa.",
    ],
    [
        f("arthur", "Eu era do tipo que acreditava em tudo que fosse explicado em três parágrafos. Este hotel me deixou sem parágrafos."),
        f("thiago", "Isso é ruim?"),
        f("arthur", "É interessante. Perigoso, mas interessante. Tome cuidado, Thiago. E me avise se encontrar outro diário."),
    ],
], [{"flag": "arthur_estado", "valor": "concluido"}, DIA(9, 19)])

# ---------------------------------------------------------------- JEHAN (bar, à noite)
papos("jehan", "bar_base", "Pedir uma bebida e conversar com Jehan", "bar", "bar_base", [
    [
        "Jehan desliza um copo de suco gelado para você, sem perguntar o que você quer. Acerta mesmo assim.",
        f("jehan", "Dia comprido?"),
        f("thiago", "Todos são."),
        f("jehan", "É assim no começo. Depois você descobre que o dia é só o tempo entre uma noite e outra."),
        "Ele enxuga o balcão com um pano branco, devagar, como quem tem todo o tempo do mundo.",
    ],
    [
        f("jehan", "Quer um conselho gratuito? Coma sempre que puder, durma cedo e ande acompanhado depois das nove."),
        f("thiago", "Parece conselho de pai."),
        f("jehan", "Parece, é? Já tive filhos. Ou quase. Esquece. Bebe."),
        "Há um brilho de aliança na mão dele, e algo mais distante nos olhos.",
    ],
    [
        f("jehan", "Sabe o que eu mais gosto no bar? As pessoas falam aqui o que não falam em lugar nenhum."),
        f("thiago", "E o senhor guarda tudo?"),
        f("jehan", "Guardo o que merece ser guardado. O resto eu deixo no balcão. Se alguém quiser levar, que leve."),
    ],
], [{"flag": "jehan_estado", "valor": "concluido"}, DIA(19, 21)])

# ---------------------------------------------------------------- NIX (corredores, de dia)
papos("nix", "hub_corredores", "Conversar com Nix, que esfrega o rodapé do corredor", "corredor", "hub_corredores", [
    [
        "Nix está de joelhos, esfregando uma mancha do rodapé que parece não querer sair. Quando percebe você, ergue uma sobrancelha.",
        f("nix", "Se for pedir toalha, é no balcão. Se for pedir conversa, eu cobro por minuto."),
        f("thiago", "E se for só passar?"),
        f("nix", "Então passa. Pisa devagar que o chão está molhado."),
        "Mesmo assim, ela continua a falar, em voz baixa, sem olhar para você.",
        f("nix", "Esse hotel tem mais fofoca por metro quadrado do que quarto por andar. Mas dizem que você é o único hóspede que fala 'obrigado'."),
    ],
    [
        f("nix", "Sua suíte é a 14, né? Tem boa luz de manhã. Eu cuido do corredor, se precisar de alguma coisa."),
        f("thiago", "Você cuida de todos os quartos?"),
        f("nix", "De todos que importam."),
        "Ela abre um sorriso curto, treinado demais, e volta a esfregar.",
        pens("Ela perguntou do meu quarto como se já soubesse a resposta."),
    ],
    [
        f("nix", "O pessoal da copa deixa um bolinho para mim às vezes. Tomei um hoje. Quer metade?"),
        f("thiago", "Aceito."),
        "Ela parte o bolo ao meio, entrega a maior parte e finge que não percebeu.",
        f("nix", "Não conta para ninguém que eu sou boazinha. Estraga a reputação."),
    ],
], [{"flag": "nix_estado", "valor": "concluida"}, DIA(8, 18)])

# ---------------------------------------------------------------- VOVÓ (corredores, tarde)
papos("vovo", "hub_corredores", "Bater na porta da Vovó, que cuida de uma planta no corredor", "corredor", "hub_corredores", [
    [
        "A velha senhora rega uma samambaia ao lado da porta com um bule de chá. Os cabelos brancos estão presos num lenço, e o xale parece mais velho que o hotel.",
        f("vovo", "Ah, o rapazinho do convite. Pode chegar mais perto, mas no quarto eu não convido ninguém."),
        f("thiago", "A senhora cuida bem das plantas."),
        f("vovo", "Planta é como gente: cresce para o lado de quem fala com ela."),
        "Ela dá tapinhas na samambaia, que se inclina devagar na sua direção, e você prefere acreditar que foi o vento.",
    ],
    [
        f("vovo", "Tem comido direito? Magro desse jeito, vai o vento levar."),
        f("thiago", "Estou comendo nos horários."),
        f("vovo", "Os horários são bons. A comida é que às vezes engana."),
        f("thiago", "Como assim, engana?"),
        f("vovo", "Ah, meu bem. A gente só descobre o tempero depois de engolir."),
        "Ela ri baixinho, como uma chaleira esquecida no fogo.",
    ],
    [
        f("vovo", "Eu moro aqui há tanto tempo que as paredes me conhecem pelo nome."),
        f("thiago", "As paredes?"),
        f("vovo", "As paredes e o que mora em cima delas. Mas isso é conversa de velha."),
        "Lá no alto, na junção do forro com a parede, uma sombra se move, devagar, como se escutasse.",
    ],
], [{"flag": "conv_vovo"}, DIA(14, 20)])

# =====================================================================
# OBSERVAR — pequenas cenas da vida do hotel (sempre disponíveis)
# =====================================================================
def observar(area, cena_hub, fundo, volta, vinhetas):
    ids = []
    for i, linhas in enumerate(vinhetas, 1):
        cid = f"obs_{area}_{i}"
        ids.append(cid)
        cena(cid, linhas, destino_auto=volta, chegada={"tempo": 6},
             dados={"raiz": True}, fundo=fundo)
    cena(f"obs_{area}", None, tipo="sorteio", dados={"raiz": True, "opcoes": ids})
    _inserir_opcao(cena_hub, op(f"obs_{area}_op", "Ficar um pouco observando o movimento", f"obs_{area}",
                                se={"flag": "@noite", "valor": False}))

observar("hall", "hall_base", "hall", "hall_base", [
    ["Um casal de hóspedes de pele pálida atravessa o hall conversando em voz baixa. O homem tira o chapéu para a recepção. A recepção, sem ninguém atrás do balcão, tilinta o sino sozinha, como se agradecesse."],
    ["Um carregador empurra um carrinho de malas até o elevador. Há três malas, mas o carrinho range como se levasse dez. Ninguém comenta."],
    ["O relógio de pêndulo do hall bate a hora com um segundo de atraso em relação ao sino do hotel. Você fica atento, e ele de novo atrasa. Parece uma briga antiga entre dois relógios."],
])
observar("refeitorio", "hub_refeitorio", "refeitorio", "hub_refeitorio", [
    ["Uma atendente de olhos fundos dobra guardanapos em formato de cisnes. Ela faz isso sem olhar, e cada cisne fica perfeito. Quando percebe você, desfaz um, como se tivesse sido flagrada em algo íntimo."],
    ["Numa mesa ao fundo, uma família de hóspedes discute o cardápio com um respeito quase religioso. A criança, de rosto cinzento e olhos grandes, rouba um pão e esconde no bolso do casaquinho."],
    ["Do lado de dentro da cozinha, bem longe, vem o barulho cadenciado de uma faca na tábua. É lento, grave, e pontuado por uma risada rouca que não combina com o ritmo."],
])
observar("corredores", "hub_corredores", "corredor", "hub_corredores", [
    ["Uma porta entreaberta deixa escapar o cheiro doce de bolo no forno. Lá dentro, alguém cantarola uma música sem letra. Quando você passa de novo, a porta está fechada e o cheiro, apagado."],
    ["As armaduras estão alinhadas como sempre. Você conta: onze. Na volta, conta onze outra vez. Mas jura que uma está com a mão em posição diferente."],
    ["Dois funcionários cruzam o corredor carregando um espelho enorme coberto por um pano. Um deles dá um passo para o lado, como se abrisse espaço para alguém que não está lá."],
])
observar("biblioteca", "biblioteca_base", "biblioteca", "biblioteca_base", [
    ["Uma escada de madeira desliza sozinha por um trilho até o alto de uma estante. Enola, sem erguer os olhos do livro, diz: “Ainda não, querida.” A escada para, obediente."],
    ["A coruja pequena abre uma asa, depois a outra, e vira a cabeça num ângulo que um bicho normal não alcançaria. Ela encara um canto da sala por longos segundos, e então volta a dormir."],
    ["Um livro cai de uma prateleira baixa, aberto numa página em branco. Você o devolve ao lugar. Ao largar, a página escreve, sozinha, uma única palavra: “Obrigado.” Depois some."],
])
observar("salao", "hub_salao_festas", "salao_festas", "hub_salao_festas", [
    ["Os lustres cobertos por panos balançam um pouco, como cabeças de gigantes adormecidos. Em algum ponto do teto, um morcego grande de asas marrons ajeita os pendurados com o cuidado de quem enfeita bolo."],
    ["Uma pilha de cadeiras se desfaz e se refaz, em silêncio, cada uma encontrando seu lugar. Ninguém empurra nenhuma. Você prefere acreditar que são os trabalhadores de madrugada."],
    ["Você pisa no piso quadriculado e o reflexo parece sorrir meio segundo antes de você. Só então você nota que o reflexo usa um smoking. Você, não."],
])
observar("musica", "hub_sala_musica", "sala_musica", "hub_sala_musica", [
    ["A poeira sobre o piano desenha, ao luar, o contorno de duas mãos. As marcas estão frescas. Você olha as próprias mãos: limpas."],
    ["A tampa do piano estala, como se alguém acabasse de se sentar. O ar fica gelado por um instante. Depois, o silêncio volta, mais denso do que antes."],
])
observar("bar", "bar_base", "bar", "bar_base", [
    ["As garrafas atrás do balcão refletem a luz âmbar, e em cada uma delas há um rosto que não é o seu. Quando você pisca, os rostos desaparecem. As garrafas, não."],
    ["O relógio de parede marca uma hora, mas as sombras dizem outra. Você não sabe em qual acreditar, e decide que é melhor sentar e esperar a certa."],
])
