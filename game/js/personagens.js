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

// Nomes que o JOGADOR vê: os verdadeiros (Homem Invisível, Nosferatu) são mistério até Thiago descobrir o que são.
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
  mulher_piano_medo: { nome: "Mulher do Piano", retrato: "img/retratos/mulher_piano_medo.jpg" },
  elisabeta: { nome: "Elisabeta", retrato: "img/retratos/mulher_piano.jpg" },
  paciente: { nome: "Paciente", retrato: null },
  voz:      { nome: "Voz",      retrato: null },
  mulher_piano: { nome: "Mulher do Piano", retrato: "img/retratos/mulher_piano.jpg" },

  // ---- Personagens das missões da Parte 2 (retratos já prontos, ainda sem cenas) ----
  // Lily e Nix: os esboços estão em img/retratos/lily.jpg e nix.jpg, mas só entram no jogo
  // (retrato preenchido aqui em cima) quando elas puderem ser vistas.
  enola:    { nome: "Enola",    retrato: "img/retratos/enola.jpg" },
  nosferatu:{ nome: "Senhor Pálido",retrato: "img/retratos/nosferatu.jpg" },
  homem_invisivel: { nome: "Homem das Faixas", retrato: "img/retratos/homem_invisivel.jpg" },
  vovo:     { nome: "Vovó",     retrato: "img/retratos/vovo.jpg" },
  jehan:    { nome: "Jehan",    retrato: "img/retratos/jehan.jpg" },
  viviane:  { nome: "Viviane",  retrato: "img/retratos/viviane.jpg" },
  macha:    { nome: "Macha",    retrato: "img/retratos/macha.jpg" },
  amanda:   { nome: "Amanda",   retrato: "img/retratos/amanda.jpg" },
  rafaela:  { nome: "Rafaela",  retrato: "img/retratos/rafaela.jpg" },
  maya:     { nome: "Maya",     retrato: "img/retratos/maya.jpg" },
  morte:    { nome: "A Criança", retrato: "img/retratos/morte.jpg" },
  // A Morte muda de forma: aqui aparece como jovem adulta (nome provisório, o jogador não sabe quem é).
  morte_jovem: { nome: "A Moça", retrato: "img/retratos/morte_jovem.jpg" },
  aurora:   { nome: "Aurora",   retrato: "img/retratos/aurora.jpg" }
};

// Como cada personagem aparece no painel "Social" (estado da relação).
// Por enquanto todo mundo é "conhecendo"; depois os romances e rivalidades entram aqui.
const RELACAO_INICIAL = "conhecendo";

/* Etiqueta da relação a partir do afeto (-100 a +100). Sem números na tela: só a barra e a palavra. */
const FAIXAS_AFETO = [
  [-100, "Inimigo"], [-59, "Hostil"], [-19, "Conhecendo"], [10, "Simpático"], [40, "Amigo"], [70, "Confidente"]
];
function etiquetaAfeto(afeto) {
  let nome = FAIXAS_AFETO[0][1];
  for (const [min, n] of FAIXAS_AFETO) if (afeto >= min) nome = n;
  return nome;
}
/* Segunda barra: só aparece quando a história deixa a ligação clara (efeito "ligacao"). */
const TIPOS_LIGACAO = {
  romance: { nome: "Romance",     faixas: [[0, "Interesse"], [30, "Namoro"], [70, "Amor"]] },
  rival:   { nome: "Rivalidade",  faixas: [[0, "Provocação"], [30, "Rival"], [70, "Rival declarado"]] },
  aliado:  { nome: "Aliança",     faixas: [[0, "Cooperação"], [30, "Aliado"], [70, "Aliado fiel"]] },
  protegido: { nome: "Proteção",  faixas: [[0, "Cuidado"], [30, "Protegido"], [70, "Laço forte"]] }
};
function etiquetaLigacao(tipo, nivel) {
  const t = TIPOS_LIGACAO[tipo]; if (!t) return "";
  let n = t.faixas[0][1];
  for (const [min, nome] of t.faixas) if (nivel >= min) n = nome;
  return n;
}
