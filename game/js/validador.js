"use strict";

/* ============================================================
 * validador.js  —  A REDE DE SEGURANÇA
 * ------------------------------------------------------------
 * Roda UMA VEZ, quando o jogo abre, ANTES de começar a jogar.
 * Ele confere todas as cenas e avisa se há erro, por exemplo:
 *
 *   - uma escolha aponta para uma cena que não existe
 *   - uma cena ficou sem saída (e não é um final)
 *   - uma cena é impossível de alcançar
 *
 * Assim, se você escrever uma cena com erro, o jogo te avisa
 * na tela em vez de simplesmente quebrar sem explicação.
 *
 * Fica separado do motor de propósito: é fácil de achar e mexer.
 * ============================================================ */

/**
 * Confere o conjunto de cenas a partir da cena inicial.
 * Devolve uma lista de textos de problema (vazia = tudo certo).
 *
 * @param {Object} cenas  - dicionário { id: cena }
 * @param {string} inicio - id da cena inicial
 */
function validarCenas(cenas, inicio) {
  const problemas = [];
  const ids = new Set(Object.keys(cenas));

  // a cena inicial precisa existir
  if (!ids.has(inicio)) {
    problemas.push(`A cena inicial '${inicio}' não existe.`);
  }

  // lista todos os destinos para onde uma cena pode levar
  function destinosDe(cena) {
    const destinos = [];
    if (cena.destino_auto) destinos.push(cena.destino_auto);
    if (cena.tipo === "sorteio" && cena.dados && cena.dados.opcoes) {
      cena.dados.opcoes.forEach(op => {
        destinos.push(typeof op === "object" ? op.destino : op);
      });
    }
    if (cena.tipo === "condicional" && cena.dados) {
      Object.values(cena.dados.casos || {}).forEach(d => destinos.push(d));
      if (cena.dados.padrao) destinos.push(cena.dados.padrao);
    }
    (cena.opcoes || []).forEach(op => {
      [op.destino,
       op.sucesso && op.sucesso.destino,
       op.falha && op.falha.destino
      ].forEach(alvo => { if (alvo) destinos.push(alvo); });
    });
    return destinos;
  }

  // 1) destinos que apontam para cenas inexistentes + cenas sem saída
  Object.values(cenas).forEach(cena => {
    let temSaida = !!cena.destino_auto
      || (cena.tipo === "sorteio" && !!(cena.dados && cena.dados.opcoes && cena.dados.opcoes.length))
      || (cena.tipo === "condicional" && !!(cena.dados && cena.dados.casos));

    // conferir também se os destinos do sorteio existem de fato
    if (cena.tipo === "sorteio" && cena.dados && cena.dados.opcoes) {
      cena.dados.opcoes.forEach(op => {
        const alvo = typeof op === "object" ? op.destino : op;
        if (!ids.has(alvo)) problemas.push(`Cena '${cena.id}' (sorteio): o destino '${alvo}' não existe.`);
      });
    }
    // conferir os destinos do condicional
    if (cena.tipo === "condicional" && cena.dados) {
      Object.entries(cena.dados.casos || {}).forEach(([caso, alvo]) => {
        if (!ids.has(alvo)) problemas.push(`Cena '${cena.id}' (condicional, caso '${caso}'): o destino '${alvo}' não existe.`);
      });
      if (cena.dados.padrao && !ids.has(cena.dados.padrao)) {
        problemas.push(`Cena '${cena.id}' (condicional, padrão): o destino '${cena.dados.padrao}' não existe.`);
      }
    }

    (cena.opcoes || []).forEach(op => {
      const alvos = [op.destino,
                     op.sucesso && op.sucesso.destino,
                     op.falha && op.falha.destino];
      if (alvos.some(Boolean)) temSaida = true;

      alvos.forEach(alvo => {
        if (alvo && !ids.has(alvo)) {
          problemas.push(`Cena '${cena.id}', opção '${op.id}': o destino '${alvo}' não existe.`);
        }
      });
    });

    const ehFinal   = cena.dados && cena.dados.final;
    const ehEspecial = cena.tipo === "espelho" || cena.tipo === "pergunta_nome" || cena.tipo === "tracos";
    if (!temSaida && !(cena.opcoes || []).length && !ehFinal && !ehEspecial) {
      problemas.push(`Cena '${cena.id}' não tem saída e não é um final.`);
    }
  });

  // 2) cenas que ninguém consegue alcançar partindo do início
  if (ids.has(inicio)) {
    const vistos = new Set();
    const fila = [inicio];
    while (fila.length) {
      const atual = fila.pop();
      if (vistos.has(atual)) continue;
      vistos.add(atual);
      destinosDe(cenas[atual]).forEach(alvo => {
        if (ids.has(alvo) && !vistos.has(alvo)) fila.push(alvo);
      });
    }
    ids.forEach(id => {
      if (!vistos.has(id)) {
        problemas.push(`Cena '${id}' é inalcançável a partir de '${inicio}'.`);
      }
    });
  }

  return problemas;
}
