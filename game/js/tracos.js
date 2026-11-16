"use strict";

/* ============================================================
 * tracos.js  —  O CATÁLOGO DE CARACTERÍSTICAS
 * ------------------------------------------------------------
 * Virtudes e vícios que o jogador escolhe no "sonho de voar"
 * (2 virtudes + 1 vício — a regra 2:1 do jogo). Diferente dos
 * 7 atributos (números), características são só "tem ou não
 * tem" — e influenciam personalidade, diálogos e reações dos
 * NPCs mais pra frente no jogo.
 *
 * Para adicionar um traço novo: acrescente uma linha aqui.
 * ============================================================ */

const VIRTUDES = [
  { id: "corajoso",    nome: "Corajoso",   descricao: "Enfrenta o medo em vez de fugir dele." },
  { id: "leal",        nome: "Leal",       descricao: "Não abandona quem confia em você." },
  { id: "curioso",     nome: "Curioso",    descricao: "Não resiste a um mistério." },
  { id: "empatico",    nome: "Empático",   descricao: "Sente o que os outros sentem, às vezes fundo demais." },
  { id: "perceptivo",  nome: "Perceptivo", descricao: "Nota o que os outros deixam passar." },
  { id: "prudente",    nome: "Prudente",   descricao: "Pensa duas vezes antes de agir." },
  { id: "determinado", nome: "Determinado",descricao: "Não desiste fácil." },
  { id: "honesto",     nome: "Honesto",    descricao: "Prefere a verdade, mesmo quando dói." }
];

const VICIOS = [
  { id: "covarde",      nome: "Covarde",      descricao: "Foge quando devia enfrentar." },
  { id: "impulsivo",    nome: "Impulsivo",    descricao: "Age antes de pensar." },
  { id: "desconfiado",  nome: "Desconfiado",  descricao: "Enxerga ameaça em toda mão estendida." },
  { id: "orgulhoso",    nome: "Orgulhoso",    descricao: "Não admite erro, nem pra si mesmo." },
  { id: "ganancioso",   nome: "Ganancioso",   descricao: "Sempre quer mais do que precisa." },
  { id: "mentiroso",    nome: "Mentiroso",    descricao: "A verdade é só mais uma ferramenta." }
];
