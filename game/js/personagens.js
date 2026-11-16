"use strict";

/* ============================================================
 * personagens.js  —  QUEM É QUEM NO JOGO
 * ------------------------------------------------------------
 * Cada personagem que fala (ou que aparece no painel Social)
 * ganha uma linha aqui. Enquanto não temos os retratos, o
 * quadradinho mostra "?" e o nome do personagem embaixo.
 * Quando tivermos a arte, basta preencher "retrato" com o
 * caminho da imagem — o resto do jogo não muda.
 * ============================================================ */

// SOBRENOME DO THIAGO — PROVISÓRIO (ainda não foi definido).
// Aparece no bilhete dourado. Troque aqui e muda no jogo inteiro.
const SOBRENOME_THIAGO = "Silva";

const PERSONAGENS = {
  thiago:   { nome: "Thiago",   retrato: null },
  mavis:    { nome: "Mavis",    retrato: null },
  jonathan: { nome: "Jonathan", retrato: null },
  lily:     { nome: "Lily",     retrato: null },
  nix:      { nome: "Nix",      retrato: null },
  louise:   { nome: "Louise",   retrato: null },
  gabriel:  { nome: "Gabriel",  retrato: null },
  eugenie:  { nome: "Eugénie",  retrato: null },
  arthur:   { nome: "Arthur",   retrato: null },
  cocheiro: { nome: "Cocheiro", retrato: null },
  porteiro: { nome: "Porteiro", retrato: null },
  desconhecida: { nome: "Desconhecida", retrato: null },
  // A mulher do piano é a Elisabeta, mas o jogo ainda não pode dizer isso.
  mulher_piano: { nome: "Mulher do Piano", retrato: null }
};

// Como cada personagem aparece no painel "Social" (estado da relação).
// Por enquanto todo mundo é "conhecendo"; depois os romances e rivalidades entram aqui.
const RELACAO_INICIAL = "conhecendo";
