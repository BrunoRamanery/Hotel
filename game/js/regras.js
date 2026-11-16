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
function condicaoSe(estado, se) {
  if (!se) return true;
  const lista = Array.isArray(se) ? se : [se];
  return lista.every(c => {
    const atual = estado.flags[c.flag];
    if ("valor" in c) return atual === c.valor;
    if ("diferente" in c) return atual !== c.diferente;
    return !!atual;   // só "flag": basta estar ligada
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
    estado.flags[nome] = ef.flags[nome];
  }
  for (const quem in (ef.relacoes || {})) {
    estado.relacoes[quem] = estado.relacoes[quem] || {};
    for (const eixo in ef.relacoes[quem]) {
      const atual = estado.relacoes[quem][eixo] || 0;
      estado.relacoes[quem][eixo] = clamp(atual + ef.relacoes[quem][eixo], -100, 100);
    }
  }
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
