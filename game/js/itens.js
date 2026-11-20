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
  remedios:           { nome: "Remédios da clínica", peso: 1, usar: { barras: { vida: 15, sanidade: 3 }, texto: "Você toma os comprimidos. A dor afrouxa." } },
  livro_palido:       { nome: "Livro de magia (Senhor Pálido)", peso: 2 },
  livro_elisabeta:    { nome: "Livro cinza (história de Elisabeta)", peso: 2 },
  // comida e água: "usar" = botão no inventário (come/bebe e o item some)
  // a marmita NÃO se come: é para levar (ex.: Maya). Comer, só nos horários de refeição ou com a Cozinha Básica.
  marmita:         { nome: "Marmita do refeitório", peso: 2 },
  agua:            { nome: "Garrafa d'água",      peso: 1, usar: { barras: { fome: 3 },  texto: "Você bebe a água fria." } }
};

/** Habilidades que Thiago pode aprender (aparecem no Perfil). */
const HABILIDADES = {
  nocoes_magia: { nome: "Noções de Magia", dica: "Você aprendeu a reconhecer sinais de magia. Alguns diálogos mudam por causa disso." },
  cozinha_basica: { nome: "Cozinha Básica", dica: "Uma vez por dia, fora dos horários de refeição, prepara uma refeição simples com os ingredientes que carrega." }
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
// Em qual cena-base de cada lugar ficam as "presenças" (quem costuma estar ali).
const HUB_DA_AREA = {
  hall: "hall_base", refeitorio: "hub_refeitorio", corredores: "hub_corredores", biblioteca: "biblioteca_base",
  salao_festas: "hub_salao_festas", bar: "bar_base", sala_musica: "hub_sala_musica"
};

// O que aparece no Diário depois que uma missão termina: [flag, valor, título]
const DIARIO_MISSOES = [
  ["jon_estado", "concluida", "Os Três Convites"],
  ["jon_estado", "recusada", "Os Três Convites (recusada)"],
  ["mavis_estado", "concluida", "Não Era o que Eu Pedi"],
  ["mavis_estado", "recusada", "Não Era o que Eu Pedi (recusada)"],
  ["vestido_estado", "concluido", "O Vestido Roubado"],
  ["eug_estado", "concluida", "A Cozinha Básica"],
  ["nix_estado", "concluida", "Um Favor entre Funcionários"],
  ["arthur_estado", "concluido", "Os Dois Diários"],
  ["jehan_estado", "concluido", "Uma Conversa no Bar"],
  ["morte_estado", "concluida", "A Última Refeição"],
  ["lag_estado", "ignorou", "Os Barulhos (ignorados)"],
  ["lag_estado", "esqueceu", "O Homem Lagarto (deixado para lá)"],
  ["lag_estado", "venceu", "O Homem Lagarto (vencido)"],
  ["lag_estado", "resgatado", "O Homem Lagarto (resgatado)"],
  ["lag_biblio", "concluida", "O Que Era o Homem Lagarto"],
  ["pal_estado", "concluido", "O Livro do Senhor Pálido"],
  ["caminho_fim", "A", "Os Contos de Jehan (Caminho A)"],
  ["caminho_fim", "B", "A Sala de Música (Caminho B)"],
  ["inv2_estado", "concluida", "Um Passo Mais Perto do Homem Invisível"]
];

const TEMPO_POR_CENA = 2;   // minutos que cada cena de história/diálogo consome
const TEMPO_VIAGEM = { padrao: 5, estoque: 10, clinica: 8 };
