"use strict";

/* ============================================================
 * main.js  —  O INTERRUPTOR GERAL
 * ------------------------------------------------------------
 * É o arquivo que LIGA tudo, na ordem certa:
 *   1. carrega as cenas dos arquivos JSON
 *   2. roda o validador (a rede de segurança)
 *   3. liga os botões do rodapé
 *   4. mostra a primeira cena
 *
 * Se algo der errado (arquivo não carrega, cena com erro),
 * mostra um aviso claro na tela em vez de quebrar calado.
 * ============================================================ */

// Onde o jogo começa.
const INICIO = "c01_bilhete";

// Quais arquivos de cena carregar. Ao criar um ato novo,
// basta adicionar o arquivo aqui (ex.: "cenas/ato2.json").
const ARQUIVOS_DE_CENA = ["cenas/ato1.json", "cenas/ato1_parte2.json"];

/** Mostra uma caixa de erro grande e explicada no lugar do jogo. */
function mostrarErro(tituloHtml, corpoHtml) {
  document.getElementById("palco").innerHTML =
    `<div class="erro-carga"><b>${tituloHtml}</b><br><br>${corpoHtml}</div>`;
}

/** Sequência de partida. */
async function iniciar() {
  // 1) carregar as cenas
  try {
    for (const arquivo of ARQUIVOS_DE_CENA) {
      const resposta = await fetch(arquivo);
      const lista = await resposta.json();
      lista.forEach(cena => { CENAS[cena.id] = cena; });
    }
  } catch (e) {
    mostrarErro(
      "Não consegui carregar as cenas.",
      `Isto costuma acontecer quando o jogo é aberto com dois cliques direto no
       arquivo. Use o atalho <b>abrir_jogo.bat</b> (ou rode por um servidor
       local), que o problema some.`
    );
    return;
  }

  // 2) validar as cenas (a rede de segurança do validador.js)
  const problemas = validarCenas(CENAS, INICIO);
  if (problemas.length) {
    mostrarErro(
      "O validador encontrou problemas nas cenas:",
      `<ul>${problemas.map(p => `<li>${p}</li>`).join("")}</ul>
       Corrija os arquivos em <b>cenas/</b> e recarregue a página.`
    );
    return;
  }

  // 3) ligar os botões do rodapé
  // Interruptor dos botões de save. No Dia 1 (demo curta) ficam escondidos;
  // na atualização do save é só trocar para true.
  const MOSTRAR_SAVE = false;
  for (const id of ["btn-salvar", "btn-continuar", "btn-exportar", "btn-importar"]) {
    document.getElementById(id).hidden = !MOSTRAR_SAVE;
  }

  document.getElementById("btn-salvar").onclick = salvar;
  document.getElementById("btn-continuar").onclick = continuar;
  document.getElementById("btn-exportar").onclick = exportarSave;
  document.getElementById("btn-importar").onclick = importarSave;
  document.getElementById("btn-reiniciar").onclick = reiniciar;

  // botões da interface (painéis)
  document.getElementById("btn-perfil").onclick = () => alternarPainel("perfil");
  document.getElementById("btn-social").onclick = () => alternarPainel("social");
  document.getElementById("btn-inventario").onclick = () => alternarPainel("inventario");
  document.getElementById("btn-mapa").onclick = () => alternarPainel("mapa");

  // 4) começar!
  mostrarCena(INICIO);
}

// dispara quando a página termina de carregar
window.addEventListener("DOMContentLoaded", iniciar);
