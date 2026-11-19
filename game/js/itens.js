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
  mapa_hotel:      { nome: "Mapa do Hotel",       peso: 1 },
  convite_musica:     { nome: "Convite (sala de música)", peso: 0 },
  convite_biblioteca: { nome: "Convite (biblioteca)",    peso: 0 },
  convite_vovo:       { nome: "Convite (quarto da Vovó)", peso: 0 },
  cartao_bellacourt:  { nome: "Cartão dos Bellacourt", peso: 0 },
  ingredientes:       { nome: "Sacola de ingredientes", peso: 2 },
  bandeja_morte:      { nome: "Bandeja coberta", peso: 2 },
  chave_misteriosa:   { nome: "Chave misteriosa", peso: 1 },
  vassoura:           { nome: "Vassoura de palha", peso: 2 },
  // comida e água: "usar" = botão no inventário (come/bebe e o item some)
  marmita:         { nome: "Marmita do refeitório", peso: 2, usar: { barras: { fome: 35 }, texto: "Você come tudo, devagar. O estômago agradece." } },
  agua:            { nome: "Garrafa d'água",      peso: 1, usar: { barras: { fome: 3 },  texto: "Você bebe a água fria." } }
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
  sala_musica:  "Sala de música",
  bar:          "Bar",
  estoque:      "Estoque",
  clinica:      "Clínica",
  salao_festas: "Salão de festas"
};

// Quantos minutos leva ir de um lugar a outro (padrão 5; estoque fica mais longe).
const TEMPO_VIAGEM = { padrao: 5, estoque: 10, clinica: 8 };
