"use strict";

/* ============================================================
 * titulo.js  —  A TELA DE ENTRADA
 * ------------------------------------------------------------
 * Nome do jogo, imagem de fundo, Jogar, Carregar save, Importar
 * arquivo e o botão Atualizar.
 *
 * O botão Atualizar só funciona dentro do aplicativo do Windows
 * (que oferece `window.hotelApp`). No navegador ele fica escondido.
 * ============================================================ */

let jogoEmAndamento = false;     // já começou uma partida nesta sessão?

function mostrarTitulo() {
  const t = document.getElementById("titulo");
  t.classList.remove("oculto");
  document.body.classList.add("no-titulo");
  atualizarMenuTitulo();
}

function esconderTitulo() {
  document.getElementById("titulo").classList.add("oculto");
  document.body.classList.remove("no-titulo");
  jogoEmAndamento = true;
}

function atualizarMenuTitulo() {
  const save = ultimoSave();
  const info = document.getElementById("t-carregar-info");
  info.textContent = descreverSave(save);
  document.getElementById("t-carregar").disabled = !save;
  document.getElementById("t-continuar").classList.toggle("oculto", !jogoEmAndamento);
  document.getElementById("t-jogar").querySelector("small").textContent =
    jogoEmAndamento ? "recomeçar do início" : "começar uma nova história";
}

/* ----- atualização (só no aplicativo) ----- */
let atuEstado = { fase: "parado" };

function pintarAtualizacao() {
  const btn = document.getElementById("btn-atualizar");
  const txt = document.getElementById("atu-texto");
  const f = atuEstado;
  btn.classList.remove("pronto");
  btn.disabled = false;
  if (f.fase === "verificando") { txt.textContent = "Procurando novidades…"; btn.disabled = true; btn.textContent = "Atualizar"; }
  else if (f.fase === "baixando") { txt.textContent = `Baixando ${f.feito} de ${f.total}…`; btn.disabled = true; btn.textContent = "Atualizando"; }
  else if (f.fase === "pronto") { txt.textContent = "Nova versão baixada!"; btn.textContent = "Aplicar agora"; btn.classList.add("pronto"); }
  else if (f.fase === "atualizado") { txt.textContent = "Você está na versão mais recente"; btn.textContent = "Atualizar"; }
  else if (f.fase === "erro") { txt.textContent = "Sem internet ou GitHub fora do ar"; btn.textContent = "Tentar de novo"; }
  else { txt.textContent = ""; btn.textContent = "Atualizar"; }
}

function ligarTitulo() {
  // versão do jogo
  fetch("versao.json").then(r => r.json()).then(v => {
    document.getElementById("t-versao").textContent = `${v.nome} · versão ${v.versao}`;
  }).catch(() => {});

  document.getElementById("t-jogar").onclick = () => reiniciar();
  document.getElementById("t-continuar").onclick = () => esconderTitulo();
  document.getElementById("t-carregar").onclick = () => continuar();
  document.getElementById("t-importar").onclick = () => importarSave();

  // aplicativo do Windows
  const app = window.hotelApp;
  if (!app) return;
  document.getElementById("btn-atualizar").classList.remove("oculto");
  if (app.sair) { const s = document.getElementById("t-sair"); s.classList.remove("oculto"); s.onclick = () => app.sair(); }
  app.aoProgresso(info => { atuEstado = info; pintarAtualizacao(); });
  app.estado().then(info => { atuEstado = info; pintarAtualizacao(); });
  document.getElementById("btn-atualizar").onclick = async () => {
    if (atuEstado.fase === "pronto") { if (jogoEmAndamento) autoSalvar(); app.recarregar(); return; }
    await app.atualizar();
  };
}
