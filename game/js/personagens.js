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
  mulher_piano: { nome: "Mulher do Piano", retrato: "img/retratos/mulher_piano.jpg" },

  // ---- Personagens das missões da Parte 2 (retratos já prontos, ainda sem cenas) ----
  // Lily e Nix: os esboços estão em img/retratos/lily.jpg e nix.jpg, mas só entram no jogo
  // (retrato preenchido aqui em cima) quando elas puderem ser vistas.
  enola:    { nome: "Enola",    retrato: "img/retratos/enola.jpg" },
  nosferatu:{ nome: "Nosferatu",retrato: "img/retratos/nosferatu.jpg" },
  homem_invisivel: { nome: "Homem Invisível", retrato: "img/retratos/homem_invisivel.jpg" },
  vovo:     { nome: "Vovó",     retrato: "img/retratos/vovo.jpg" },
  jehan:    { nome: "Jehan",    retrato: "img/retratos/jehan.jpg" },
  viviane:  { nome: "Viviane",  retrato: "img/retratos/viviane.jpg" },
  macha:    { nome: "Macha",    retrato: "img/retratos/macha.jpg" },
  amanda:   { nome: "Amanda",   retrato: "img/retratos/amanda.jpg" },
  rafaela:  { nome: "Rafaela",  retrato: "img/retratos/rafaela.jpg" },
  maya:     { nome: "Maya",     retrato: "img/retratos/maya.jpg" },
  morte:    { nome: "A Criança", retrato: "img/retratos/morte.jpg" },
  aurora:   { nome: "Aurora",   retrato: "img/retratos/aurora.jpg" }
};

// Como cada personagem aparece no painel "Social" (estado da relação).
// Por enquanto todo mundo é "conhecendo"; depois os romances e rivalidades entram aqui.
const RELACAO_INICIAL = "conhecendo";
