"use strict";

/* ============================================================
 * estado.js  —  O ESTADO DO JOGADOR (a "ficha viva" do Thiago)
 * ------------------------------------------------------------
 * Guarda TUDO que muda durante uma partida:
 *   - os 6 atributos (Força, Agilidade, Inteligência, Peso, Carisma, Sorte)
 *   - as 4 barras (Vida, Fome, Sanidade, Suspeita)
 *   - o relógio (UM contador único, em minutos)
 *   - as flags (marcações invisíveis, tipo "já tomou banho?")
 *   - inventário, personagens conhecidos, mapa
 *
 * Este arquivo NÃO desenha nada na tela e NÃO decide nada.
 * ============================================================ */

/* ----- O RELÓGIO -----
 * O tempo é UM número só: minutos desde a meia-noite do dia da chegada.
 * Dia, hora, mês e estação são calculados a partir dele. */
const MIN_POR_DIA = 24 * 60;
const HORA_INICIAL = 17 * 60 + 30;   // Thiago chega ao ponto de ônibus às 17:30

// Data da chegada. PROVISÓRIO (os documentos ainda não definem a época do ano):
// 15 de outubro. Para mudar, basta trocar estes dois números.
const MES_INICIAL = 10;
const DIA_INICIAL = 15;

const MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
               "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
const DIAS_DO_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

// Os 6 atributos do Thiago (ordem em que aparecem nas telas).
const ATRIBUTOS = ["forca", "agilidade", "inteligencia", "peso", "carisma", "sorte"];
const ATRIBUTO_ROTULO = {
  forca: "Força", agilidade: "Agilidade", inteligencia: "Inteligência",
  peso: "Peso", carisma: "Carisma", sorte: "Sorte"
};
const ATRIBUTO_DICA = {
  forca: "Combate, tarefas braçais, empurrar e quebrar.",
  agilidade: "Correr, fugir, desviar e agir rápido.",
  inteligencia: "Investigar, perceber detalhes, entender livros.",
  peso: "Quanto você consegue carregar no inventário.",
  carisma: "Conversar, convencer, mentir, negociar.",
  sorte: "O dado do jogo: acasos e oportunidades."
};

/** Ficha nova, do zero (usada ao começar ou recomeçar). */
function novoEstado() {
  return {
    // atributos: todos começam em 50 (o jogador distribui 30 pontos no espelho)
    forca: 50, agilidade: 50, inteligencia: 50, peso: 50, carisma: 50, sorte: 50,

    // barras (0 a 100) — a Fome pode passar de 100 depois (fomeMax)
    vida: 100,
    fome: 100, fomeMax: 100,   // quanto MAIOR, mais alimentado
    sanidade: 100,
    suspeita: 50,              // quanto MENOR, melhor. Todo humano chega "cheirando" a humano

    // relógio
    minutos: HORA_INICIAL,

    // o que a tela já mostra (a interface vai "acordando" aos poucos)
    hud: [],

    // memória do jogo
    flags: { nome: "Thiago", sobrenome: SOBRENOME_THIAGO },
    tracos: { virtudes: [], vicio: null },
    relacoes: {},
    conhecidos: [],     // ids de personagens que Thiago já conheceu (painel Social)
    inventario: [],     // ids de itens carregados (ver itens.js)
    mapa: [],           // ids de áreas liberadas no mapa
    marcadores: []      // missões liberadas: { area, texto }
  };
}

/** Mantém um número entre um mínimo e um máximo. */
function clamp(valor, minimo = 0, maximo = 100) {
  return Math.max(minimo, Math.min(maximo, Math.round(valor)));
}

/**
 * Faz o tempo passar: soma minutos ao relógio.
 * Depois do tutorial da Fome (flag "fome_ativa"), a Fome cai com o tempo.
 * `fator` < 1 = dormindo (gasta menos).
 */
const FOME_POR_MINUTO = 0.12;   // ~7 pontos por hora acordado
function avancarTempo(estado, minutos = 0, fator = 1) {
  const m = Math.max(0, minutos);
  estado.minutos += m;
  if (estado.flags.fome_ativa) {
    estado.fome = clamp(estado.fome - m * FOME_POR_MINUTO * fator, 0, estado.fomeMax);
  }
}

/**
 * Faz o tempo passar ATÉ a próxima vez que o relógio marcar "HH:MM".
 * Ex.: "03:00" às 21:00 -> pula para 03:00 do dia seguinte.
 */
function avancarTempoAte(estado, hhmm, fator = 1) {
  const [h, m] = hhmm.split(":").map(Number);
  const alvo = h * 60 + (m || 0);
  let falta = alvo - (estado.minutos % MIN_POR_DIA);
  if (falta <= 0) falta += MIN_POR_DIA;
  avancarTempo(estado, falta, fator);
}

/** Dia contado desde a chegada (1, 2, 3...). Vira à meia-noite. */
function diaAtual(estado) {
  return Math.floor(estado.minutos / MIN_POR_DIA) + 1;
}

/** "17:30" */
function horaTexto(estado) {
  const noDia = estado.minutos % MIN_POR_DIA;
  return String(Math.floor(noDia / 60)).padStart(2, "0") + ":" + String(noDia % 60).padStart(2, "0");
}

/** Data de hoje no jogo: { dia, mes (1-12) }, andando a partir da data inicial. */
function dataAtual(estado) {
  let dias = diaAtual(estado) - 1;
  let dia = DIA_INICIAL, mes = MES_INICIAL;
  while (dias > 0) {
    dia++; dias--;
    if (dia > DIAS_DO_MES[mes - 1]) { dia = 1; mes = mes % 12 + 1; }
  }
  return { dia, mes };
}

/** Estação do ano (hemisfério norte: a fortaleza fica na Europa). */
function estacaoDoAno(estado) {
  const { mes } = dataAtual(estado);
  if (mes === 12 || mes <= 2) return "inverno";
  if (mes <= 5) return "primavera";
  if (mes <= 8) return "verão";
  return "outono";
}

/** O período do dia: madrugada (0-6), manhã (6-12), tarde (12-18), noite (18-24). */
function periodoDoDia(estado) {
  const h = Math.floor((estado.minutos % MIN_POR_DIA) / 60);
  if (h < 6) return "madrugada";
  if (h < 12) return "manhã";
  if (h < 18) return "tarde";
  return "noite";
}

/** Dia (sol) ou noite (lua)? Serve para o ícone do relógio. */
function ehDeDia(estado) {
  const p = periodoDoDia(estado);
  return p === "manhã" || p === "tarde";
}

/** Resumo do tempo vivido no hotel, para a tela final. */
function resumoTempo(estado) {
  const total = Math.max(0, estado.minutos - HORA_INICIAL);
  const dias = Math.floor(total / MIN_POR_DIA);
  const horas = Math.floor((total % MIN_POR_DIA) / 60);
  const noites = Math.floor((estado.minutos - 6 * 60) / MIN_POR_DIA) - Math.floor((HORA_INICIAL - 6 * 60) / MIN_POR_DIA);
  return { dias, horas, noites: Math.max(0, noites) };
}

/** Saves de versões antigas do jogo não servem mais: recomeça limpo. */
function migrarEstado(e) {
  if (!e || typeof e.fome !== "number" || !Array.isArray(e.hud)) return novoEstado();
  return e;
}
