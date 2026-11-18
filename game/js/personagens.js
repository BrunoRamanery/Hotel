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
  thiago:   { nome: "Thiago",   retrato: "img/retratos/thiago.jpg" },
  mavis:    { nome: "Mavis",    retrato: "img/retratos/mavis.jpg" },
  jonathan: { nome: "Jonathan", retrato: "img/retratos/jonathan.jpg" },
  lily:     { nome: "Lily",     retrato: null },
  nix:      { nome: "Nix",      retrato: null },
  louise:   { nome: "Louise",   retrato: "img/retratos/louise.jpg" },
  gabriel:  { nome: "Gabriel",  retrato: "img/retratos/gabriel.jpg" },
  eugenie:  { nome: "Eugénie",  retrato: "img/retratos/eugenie.jpg" },
  arthur:   { nome: "Arthur",   retrato: "img/retratos/arthur.jpg" },
  cocheiro: { nome: "Cocheiro", retrato: "img/retratos/cocheiro.jpg" },
  porteiro: { nome: "Porteiro", retrato: "img/retratos/porteiro.jpg" },
  desconhecida: { nome: "Desconhecida", retrato: null },
  // A mulher do piano é a Elisabeta, mas o jogo ainda não pode dizer isso.
  mulher_piano: { nome: "Mulher do Piano", retrato: "img/retratos/mulher_piano.jpg" }
};

// Como cada personagem aparece no painel "Social" (estado da relação).
// Por enquanto todo mundo é "conhecendo"; depois os romances e rivalidades entram aqui.
const RELACAO_INICIAL = "conhecendo";
