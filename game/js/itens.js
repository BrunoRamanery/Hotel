"use strict";

/* ============================================================
 * itens.js  —  O CATÁLOGO DE ITENS
 * ------------------------------------------------------------
 * Cada item tem um nome e um PESO. A soma dos pesos do inventário
 * não pode passar do atributo Peso do Thiago (ex.: 18/50).
 * Para criar um item novo, acrescente uma linha aqui.
 * ============================================================ */

const ITENS = {
  bilhete_dourado: { nome: "Bilhete Dourado",     peso: 1 },
  cartao_cocheiro: { nome: "Cartão do Cocheiro",  peso: 1 },
  chave_quarto:    { nome: "Chave do Quarto (Suíte 14)", peso: 1 },
  mapa_hotel:      { nome: "Mapa do Hotel",       peso: 1 }
};

/** Peso total carregado agora. */
function pesoCarregado(estado) {
  return estado.inventario.reduce((soma, id) => soma + ((ITENS[id] && ITENS[id].peso) || 0), 0);
}

// Áreas do mapa (id -> nome). Só aparecem no mapa depois de liberadas.
const AREAS = {
  suite14:      "Suíte 14",
  corredores:   "Corredores públicos",
  hall:         "Hall de entrada",
  refeitorio:   "Refeitório",
  biblioteca:   "Biblioteca",
  sala_musica:  "Sala de música"
};
