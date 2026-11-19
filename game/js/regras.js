"use strict";

/* ============================================================
 * regras.js  —  AS REGRAS DO JOGO
 * ------------------------------------------------------------
 * Aqui ficam as três regras que fazem o jogo "funcionar":
 *
 *   1. checarRequisitos  -> uma escolha deve aparecer ou não?
 *   2. aplicarEfeitos    -> o que uma escolha faz com a ficha?
 *   3. rolarTeste        -> a jogada de dado (sucesso/falha)
 *
 * Este arquivo mexe na ficha (estado.js), mas NÃO desenha na tela.
 * ============================================================ */

/**
 * Decide se uma opção deve APARECER para o jogador.
 * Uma opção pode exigir um atributo mínimo, um valor de barra,
 * ou uma flag. Se não cumprir tudo, a opção fica escondida.
 *
 * Exemplo de requisito no JSON da cena:
 *   "requisitos": { "atributo": { "percepcao": 15 } }
 */
function checarRequisitos(estado, req) {
  if (!req) return true; // sem requisitos = sempre aparece

  // exige atributo mínimo, ex.: percepcao >= 15
  const atributos = req.atributo || {};
  for (const nome in atributos) {
    if ((estado[nome] || 0) < atributos[nome]) return false;
  }

  // exige barra em certo nível, ex.: { "suspeita_max": 40 }
  const barras = req.barra || {};
  for (const chave in barras) {
    if (chave.endsWith("_max")) {
      const nome = chave.slice(0, -4);
      if ((estado[nome] || 0) > barras[chave]) return false;
    } else if (chave.endsWith("_min")) {
      const nome = chave.slice(0, -4);
      if ((estado[nome] || 0) < barras[chave]) return false;
    }
  }

  // exige itens no inventário / exige NÃO ter certos itens
  for (const id of (req.itens || [])) if (!estado.inventario.includes(id)) return false;
  for (const id of (req.sem_itens || [])) if (estado.inventario.includes(id)) return false;

  // exige uma flag, ex.: { "tomou_banho": true }
  const flags = req.flags || {};
  for (const nome in flags) {
    if (estado.flags[nome] !== flags[nome]) return false;
  }

  return true;
}

/**
 * Decide se um trecho do texto (ou uma opção) vale para o estado atual.
 * É o campo "se" do JSON. Aceita UMA condição ou uma LISTA (todas precisam valer):
 *   "se": { "flag": "recepcionista", "valor": "mavis" }
 *   "se": { "flag": "tomou_banho", "valor": true }
 *   "se": { "flag": "lily_conhecida", "diferente": true }
 */
/**
 * Flags "virtuais": calculadas na hora, a partir do relógio. Começam com "@".
 *   @hora      hora cheia atual (0 a 23)
 *   @dia       número do dia desde a chegada
 *   @refeicao  true nos horários de comer (café 7-9, almoço 12-14, jantar 19-21)
 *   @noite     true na noite proibida (22h às 6h)
 */
/** Qual refeição do dia está servida agora: "3-cafe", "3-almoco", "3-jantar" (ou "" fora do horário). */
function turnoAtual(estado) {
  const h = Math.floor((estado.minutos % MIN_POR_DIA) / 60);
  const nome = (h >= 7 && h < 9) ? "cafe" : (h >= 12 && h < 14) ? "almoco" : (h >= 19 && h < 21) ? "jantar" : "";
  return nome ? diaAtual(estado) + "-" + nome : "";
}

function valorDeFlag(estado, nome) {
  if (nome[0] !== "@") return estado.flags[nome];
  // @pronto:X  -> o relógio já passou do horário guardado na flag X (em minutos)
  if (nome.startsWith("@pronto:")) {
    const alvo = estado.flags[nome.slice(8)];
    return alvo !== undefined && estado.minutos >= alvo;
  }
  // @arthur -> Vestido concluído + pelo menos 6 fragmentos (e Arthur ainda não visto)
  if (nome === "@arthur") {
    return estado.flags.vestido_estado === "concluido" && (estado.flags.fragmentos || 0) >= 6
        && estado.flags.arthur_estado === undefined;
  }
  // @jehan -> Vestido concluído e, se Arthur já está liberado, ele vem antes; Jehan ainda não visto
  if (nome === "@jehan") {
    return estado.flags.vestido_estado === "concluido" && estado.flags.jehan_estado === undefined
        && (estado.flags.arthur_estado === "concluido" || (estado.flags.fragmentos || 0) < 6);
  }
  // @dia_passou:X -> já virou o dia depois do dia guardado na flag X (precisa dormir/virar o dia)
  if (nome.startsWith("@dia_passou:")) {
    const d = estado.flags[nome.slice(12)];
    return d !== undefined && diaAtual(estado) > d;
  }
  // @propostas -> Jonathan e Mavis já tiveram resposta (aceita ou recusada)
  if (nome === "@propostas") {
    const j = estado.flags.jon_estado, m = estado.flags.mavis_estado;
    return j !== undefined && m !== undefined && m !== "derrubou";
  }
  const h = Math.floor((estado.minutos % MIN_POR_DIA) / 60);
  if (nome === "@hora") return h;
  if (nome === "@dia") return diaAtual(estado);
  if (nome === "@refeicao") return (h >= 7 && h < 9) || (h >= 12 && h < 14) || (h >= 19 && h < 21);
  if (nome === "@noite") return h >= 22 || h < 6;
  if (nome === "@turno") return turnoAtual(estado);
  return undefined;
}

/**
 * Uma condição "se" (uma ou várias, todas precisam ser verdadeiras):
 *   {flag:"x"}                  a flag está ligada
 *   {flag:"x", valor:V}         é igual a V        ("@dia" = o dia de hoje)
 *   {flag:"x", diferente:V}     é diferente de V
 *   {flag:"x", min:N, max:M}    número entre N e M
 */
function condicaoSe(estado, se) {
  if (!se) return true;
  const lista = Array.isArray(se) ? se : [se];
  const resolver = v => (v === "@dia" ? diaAtual(estado) : v === "@turno" ? turnoAtual(estado) : v);
  return lista.every(c => {
    const atual = valorDeFlag(estado, c.flag);
    let ok = true, temRegra = false;
    if ("valor" in c)     { temRegra = true; ok = ok && atual === resolver(c.valor); }
    if ("diferente" in c) { temRegra = true; ok = ok && atual !== resolver(c.diferente); }
    if ("min" in c)       { temRegra = true; ok = ok && (atual || 0) >= c.min; }
    if ("max" in c)       { temRegra = true; ok = ok && (atual || 0) <= c.max; }
    return temRegra ? ok : !!atual;   // sem regra: basta a flag estar ligada
  });
}

/**
 * Aplica os EFEITOS de uma escolha na ficha do jogador.
 *
 * Exemplo no JSON:
 *   "efeitos": {
 *     "barras": { "suspeita": 5 },          // soma/subtrai
 *     "definir": { "suspeita": 0 },         // fixa o valor
 *     "flags": { "tomou_banho": true },
 *     "relacoes": { "mavis": { "afeto": 5 } },
 *     "tempo": 25,                          // gasta 25 minutos
 *     "ate": "03:10", "sono": true,         // pula até a hora (dormindo)
 *     "somar": {"fragmentos": 1},           // soma 1 num contador (flag numérica)
 *     "ligacao": {"mavis":"romance"},      // mostra a 2ª barra (romance/rival/aliado/protegido); sobe com relacoes {x:{nivel:5}}
 *     "habilidades": ["cozinha_basica"],  // aparece no Perfil
 *     "itens": ["chave_quarto"],            // entra no inventário
 *     "conhece": ["mavis"],                 // aparece no painel Social
 *     "hud": ["suspeita"],                  // a tela "acorda" esse elemento
 *     "mapa": ["biblioteca"],               // libera área no mapa
 *     "marcadores": [{"area":"biblioteca","texto":"Missão de Mavis"}]
 *   }
 */
function aplicarEfeitos(estado, ef) {
  if (!ef) return;

  for (const nome in (ef.atributos || {})) {
    estado[nome] = clamp((estado[nome] || 0) + ef.atributos[nome]);
  }
  for (const nome in (ef.barras || {})) {
    const teto = nome === "fome" ? estado.fomeMax : 100;
    estado[nome] = clamp((estado[nome] || 0) + ef.barras[nome], 0, teto);
  }
  for (const nome in (ef.definir || {})) {
    estado[nome] = ef.definir[nome];
  }
  for (const nome in (ef.flags || {})) {
    const v = ef.flags[nome];
    if (v === "@dia") estado.flags[nome] = diaAtual(estado);
    else if (v === "@turno") estado.flags[nome] = turnoAtual(estado);
    else if (typeof v === "string" && v.startsWith("@+")) estado.flags[nome] = estado.minutos + parseInt(v.slice(2), 10); // daqui a N minutos
    else estado.flags[nome] = v;
  }
  for (const nome in (ef.somar || {})) {            // contadores: "somar": {"fragmentos": 1}
    estado.flags[nome] = (estado.flags[nome] || 0) + ef.somar[nome];
  }
  for (const quem in (ef.relacoes || {})) {
    estado.relacoes[quem] = estado.relacoes[quem] || {};
    for (const eixo in ef.relacoes[quem]) {
      const atual = estado.relacoes[quem][eixo] || 0;
      estado.relacoes[quem][eixo] = clamp(atual + ef.relacoes[quem][eixo], -100, 100);
    }
  }
  for (const quem in (ef.ligacao || {})) {          // "ligacao": {"mavis": "romance"} -> liga a 2ª barra
    estado.relacoes[quem] = estado.relacoes[quem] || {};
    estado.relacoes[quem].tipo = ef.ligacao[quem];
    if (estado.relacoes[quem].nivel === undefined) estado.relacoes[quem].nivel = 0;
  }
  (ef.habilidades || []).forEach(id => { estado.habilidades = estado.habilidades || []; if (!estado.habilidades.includes(id)) estado.habilidades.push(id); });
  (ef.itens || []).forEach(id => { if (!estado.inventario.includes(id)) estado.inventario.push(id); });
  (ef.tirar_itens || []).forEach(id => { estado.inventario = estado.inventario.filter(x => x !== id); });
  (ef.conhece || []).forEach(id => { if (!estado.conhecidos.includes(id)) estado.conhecidos.push(id); });
  (ef.hud || []).forEach(id => { if (!estado.hud.includes(id)) estado.hud.push(id); });
  (ef.mapa || []).forEach(id => { if (!estado.mapa.includes(id)) estado.mapa.push(id); });
  (ef.marcadores || []).forEach(m => {
    if (!estado.marcadores.some(x => x.area === m.area && x.texto === m.texto)) estado.marcadores.push(m);
  });
  (ef.tirar_marcadores || []).forEach(area => {
    estado.marcadores = estado.marcadores.filter(x => x.area !== area);
  });

  // tempo (por último, para a Fome já refletir as ações acima)
  const fator = ef.sono ? 0.5 : 1;
  if (ef.tempo) avancarTempo(estado, ef.tempo, fator);
  if (ef.ate) avancarTempoAte(estado, ef.ate, fator);
}

/**
 * Rola um "dado" de 1 a 100 e compara com o atributo do jogador.
 * A Sorte dá um empurrãozinho em todo teste (sorte / 5).
 *
 *   - tirar 1 a 5   -> CRÍTICO (passa sempre)
 *   - tirar 96 a 100 -> DESASTRE (falha sempre)
 *   - no meio -> compara atributo contra a dificuldade
 *
 * Devolve, por exemplo: { passou: true, categoria: "sucesso" }
 */
function rolarTeste(estado, teste) {
  const valor = (estado[teste.atributo] || 0) + Math.floor(estado.sorte / 5);
  const dificuldade = teste.dificuldade || 50;
  const dado = 1 + Math.floor(Math.random() * 100);

  if (dado <= 5)  return { passou: true,  categoria: "crítico" };
  if (dado >= 96) return { passou: false, categoria: "desastre" };

  const passou = (valor - dado) >= (dificuldade - 50);
  return { passou, categoria: passou ? "sucesso" : "falha" };
}


/**
 * Confere se o corpo do Thiago "pede" uma cena de emergência. Chamada depois
 * que o tempo passa (ao andar pelo mapa, dormir...). Devolve o id da cena
 * para onde desviar, ou null se está tudo bem.
 *   Fome 0            -> morte
 *   Fome <= 5         -> desmaio (acorda na clínica)
 *   Cansaço 0         -> desmaio
 *   Fome <= 10        -> alucinação (no máximo uma a cada 3 horas)
 */
function situacaoCritica(estado) {
  if (!estado.flags.fome_ativa) return null;
  if (estado.fome <= 0) return "morte_fome";
  if (estado.fome <= 5 || estado.cansaco <= 0) return "desmaio";
  if (estado.fome <= 10) {
    const bloco = Math.floor(estado.minutos / 180);
    if (estado.flags.alucinou_bloco !== bloco) return "alucinacao";
  }
  return null;
}


/** "O jantar é às 19h" / "A refeição está servida agora": ajuda o jogador a entender as regras. */
function textoProximaRefeicao(estado) {
  const h = Math.floor((estado.minutos % MIN_POR_DIA) / 60);
  if ((h >= 7 && h < 9) || (h >= 12 && h < 14) || (h >= 19 && h < 21)) return "A refeição está sendo servida agora no refeitório";
  if (h < 7) return "O café da manhã é às 7h";
  if (h < 12) return "O almoço é às 12h";
  if (h < 19) return "O jantar é às 19h";
  return "O café da manhã é às 7h";
}

/** Avisos curtos sob as barras (no máximo 2). */
function avisosDeStatus(estado) {
  if (!estado.flags.fome_ativa) return [];
  const h = Math.floor((estado.minutos % MIN_POR_DIA) / 60);
  const a = [];
  if (estado.fome <= 35) a.push(`Você está com fome. ${textoProximaRefeicao(estado)}; a água do refeitório está sempre disponível.`);
  if (estado.cansaco <= 30) a.push(`Você está exausto. Um cochilo ajuda, e à noite o certo é dormir na Suíte 14.`);
  if (h >= 21 && h < 22) a.push(`Falta pouco para as 22h: depois disso, os corredores são proibidos.`);
  else if (h >= 22 || h < 6) a.push(`Os corredores são proibidos a esta hora. Volte para a Suíte 14.`);
  return a.slice(0, 2);
}
