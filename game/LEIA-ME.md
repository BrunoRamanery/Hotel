# Hotel Los Segredos — Ato 1 (A Chegada e o Hóspede)

Jogo narrativo de texto. Roda no navegador (HTML, CSS e JavaScript).
Esta versão cobre o **Ato 1 completo**: do bilhete dourado ao pedido de desculpas da Elisabeta, com exploração livre pelo mapa, missões, fome, cansaço e horários.

## Como rodar (Windows, dois cliques)

Dê **dois cliques em `abrir_jogo.bat`**. Ele abre o jogo no navegador. Uma janela preta
fica aberta — é o servidor; **deixe-a aberta enquanto joga** e feche ao terminar.
(Precisa do Python instalado.)

> Por que não abrir o `index.html` direto? O jogo carrega as cenas de arquivos `.json`,
> e o navegador bloqueia isso em arquivos abertos "soltos".

## O que tem nesta versão

- Cenas 1 a 18 do roteiro oficial (`ROTEIRO_ATO_1_CENAS_01_A_06` e `07_A_18`).
- 6 atributos (Força, Agilidade, Inteligência, Peso, Carisma, Sorte): 50 + 30 pontos em blocos de 10, máximo 80.
- 4 barras: Vida, Fome, Sanidade, Suspeita. A tela "acorda" aos poucos, como no roteiro.
- Relógio com hora, período, data e estação.
- Painéis recolhíveis: Perfil, Social, Inventário (com peso) e Mapa.
- Recepção sorteada (Mavis ou Jonathan) com texto diferente para cada um.
- Primeira noite: piano ou telefone. Sonho com 2 virtudes e 1 vício.
- Sem botões de save (entram na segunda atualização — é só trocar `MOSTRAR_SAVE` em `js/main.js`).

## Pendências conhecidas (para o Bruno decidir)

- **Sobrenome do Thiago:** provisório ("Silva"). Troque em `js/personagens.js` (`SOBRENOME_THIAGO`).
- **Época do ano:** provisória (15 de outubro). Troque em `js/estado.js` (`MES_INICIAL`, `DIA_INICIAL`).
- **Falas rascunho:** onde o roteiro só resume a cena (cenas 7 a 10, 14 a 17), as falas foram escritas
  no mesmo tom e podem ser ajustadas.
- Os retratos aparecem como "?" com o nome embaixo, até a arte ficar pronta.

## O que é cada arquivo

    index.html            A estrutura da tela.
    css/estilo.css        Todo o visual.
    cenas/ato1.json       A HISTÓRIA (as cenas).
    js/
      personagens.js      Quem fala (nome e retrato) + sobrenome provisório.
      tracos.js           Virtudes e vícios.
      itens.js            Itens (com peso) e áreas do mapa.
      estado.js           A ficha do Thiago, o relógio, a data.
      regras.js           Efeitos, condições "se", testes de dado.
      validador.js        Rede de segurança: confere as cenas ao abrir.
      motor.js            Desenha as cenas, a barra de status e os painéis.
      main.js             Liga tudo e começa o jogo.

## Formato de uma cena

    {
      "id": "exemplo",
      "chegada": { "tempo": 20, "hud": ["suspeita"] },      // acontece ao ENTRAR na cena
      "narrativa": [
        "Texto narrado.",
        { "estilo": "pensamento", "texto": "O que Thiago pensa." },
        { "quem": "mavis", "texto": "Uma fala." },
        { "quem": "mavis", "texto": "Só se ela te recebeu.", "se": { "flag": "recepcionista", "valor": "mavis" } },
        { "item": "mapa_hotel" }                              // "Item recebido" + entra no inventário
      ],
      "opcoes": [
        { "id": "a", "texto": "Fazer isso.", "destino": "outra_cena",
          "efeitos": { "barras": { "suspeita": 5 }, "flags": { "fez_isso": true }, "tempo": 10 } }
      ]
    }

Efeitos aceitos: `barras`, `definir`, `flags`, `relacoes`, `tempo`, `ate` (+ `sono`), `itens`,
`conhece`, `hud`, `mapa`, `marcadores`. Condição `se`: `{flag, valor}` ou `{flag, diferente}`,
ou uma lista (todas valem). Cena com só `destino_auto` mostra um botão "continuar".

## Relógio

O tempo é UM contador em minutos (`js/estado.js`). O jogo começa às 17:30. A Fome só passa a cair
depois do tutorial da Fome (flag `fome_ativa`, ligada na cena 17).
