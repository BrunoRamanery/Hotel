"use strict";

/* ============================================================
 * motor.js  —  O CORAÇÃO DO JOGO
 * ------------------------------------------------------------
 * Este é o "diretor da peça": ele pega uma cena e a coloca na
 * tela — desenha o texto, os botões das escolhas, a barra de
 * status e os painéis — e escuta os cliques do jogador.
 *
 * Ele USA os outros arquivos:
 *   - estado.js  (a ficha do jogador e o relógio)
 *   - regras.js  (efeitos, condições "se", testes)
 *   - itens.js   (itens e áreas do mapa)
 *
 * Quem começa o jogo é o main.js. Este arquivo só sabe DESENHAR.
 * ============================================================ */

// O "cofre" de todas as cenas do jogo. O main.js enche isto.
const CENAS = {};

// A ficha viva do jogador e a cena em que ele está agora.
let estado = novoEstado();
let cenaAtual = null;

/* ----- mostrar / esconder um elemento da tela ----- */
function mostrarElemento(id, ligado) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle("oculto", !ligado);
}

/* ----- desenhar a barra de status (topo) -----
 * A interface "acorda" aos poucos: cada peça só aparece depois que o
 * jogo a apresenta (efeito "hud" nas cenas). */
function pintarStatus() {
  const hud = estado.hud;

  mostrarElemento("status", hud.length > 0);
  mostrarElemento("bloco-tempo", hud.includes("tempo"));
  mostrarElemento("btn-perfil", hud.includes("perfil"));
  mostrarElemento("btn-social", hud.includes("social"));
  mostrarElemento("btn-inventario", hud.includes("inventario"));
  mostrarElemento("btn-mapa", hud.includes("mapa"));

  // nome completo + relógio (hora, período, data, estação)
  document.getElementById("nome-jogador").textContent =
    `${estado.flags.nome} ${estado.flags.sobrenome || ""}`.trim();
  const icone = ehDeDia(estado) ? "☀" : "☾";
  const { dia, mes } = dataAtual(estado);
  document.getElementById("tempo").innerHTML =
    `<span class="rel-icone">${icone}</span> ${horaTexto(estado)}` +
    `<span class="rel-periodo">${periodoDoDia(estado)}</span>` +
    `<span class="rel-data">${dia} de ${MESES[mes - 1]} · ${estacaoDoAno(estado)}</span>`;
  document.body.classList.toggle("noite-fora", !ehDeDia(estado));

  // as 4 barras
  for (const barra of ["vida", "fome", "sanidade", "suspeita"]) {
    mostrarElemento("b-" + barra, hud.includes(barra));
    const max = barra === "fome" ? estado.fomeMax : 100;
    document.getElementById("p-" + barra).style.width = (estado[barra] / max * 100) + "%";
    document.getElementById("v-" + barra).textContent = estado[barra];
  }

  // quando a suspeita passa de 50, a tela "esquenta" de perigo
  document.body.classList.toggle("perigo", hud.includes("suspeita") && estado.suspeita >= 50);

  // se um painel está aberto, mantém ele atualizado
  if (painelAberto) desenharPainel(painelAberto);
}

/* ----- PAINÉIS (Perfil, Social, Inventário, Mapa) -----
 * Ficam fechados. Abrir um fecha o outro, para a tela não ficar poluída. */
let painelAberto = null;

function alternarPainel(qual) {
  painelAberto = (painelAberto === qual) ? null : qual;
  if (painelAberto) desenharPainel(painelAberto);
  else document.getElementById("painel").classList.add("oculto");
}
function fecharPainel() {
  painelAberto = null;
  document.getElementById("painel").classList.add("oculto");
}

function desenharPainel(qual) {
  const el = document.getElementById("painel");
  let titulo = "", corpo = "";

  if (qual === "perfil") {
    titulo = `${estado.flags.nome} ${estado.flags.sobrenome || ""}`.trim();
    corpo = `<h4>Atributos</h4><ul class="lista-attr">` +
      ATRIBUTOS.map(a => `<li title="${ATRIBUTO_DICA[a]}"><span>${ATRIBUTO_ROTULO[a]}</span><b>${estado[a]}</b></li>`).join("") +
      `</ul><h4>Características</h4>`;
    const v = estado.tracos.virtudes.map(id => (VIRTUDES.find(x => x.id === id) || {}).nome).filter(Boolean);
    const vicio = (VICIOS.find(x => x.id === estado.tracos.vicio) || {}).nome;
    corpo += (v.length || vicio)
      ? `<p>${v.map(n => `<span class="tag tag-virtude">${n}</span>`).join("")}${vicio ? `<span class="tag tag-vicio">${vicio}</span>` : ""}</p>`
      : `<p class="vazio">Ainda por descobrir.</p>`;
    corpo += `<h4>Habilidades</h4><p class="vazio">Nenhuma aprendida ainda.</p>`;
  }
  if (qual === "social") {
    titulo = "Social";
    corpo = estado.conhecidos.length
      ? `<ul class="lista-social">` + estado.conhecidos.map(id => {
          const p = PERSONAGENS[id];
          return `<li><span>${p ? p.nome : id}</span><i>${RELACAO_INICIAL}</i></li>`;
        }).join("") + `</ul>`
      : `<p class="vazio">Você ainda não conhece ninguém.</p>`;
  }
  if (qual === "inventario") {
    titulo = "Inventário";
    corpo = `<p class="peso-total">Capacidade de peso: <b>${pesoCarregado(estado)}/${estado.peso}</b></p>` +
      (estado.inventario.length
        ? `<ul class="lista-itens">` + estado.inventario.map(id => {
            const it = ITENS[id] || { nome: id, peso: 0 };
            return `<li><span>${it.nome}</span><i>peso ${it.peso}</i></li>`;
          }).join("") + `</ul>`
        : `<p class="vazio">Você não está carregando nada.</p>`) +
      `<p class="dica">O que não está aqui fica guardado no armário da Suíte 14.</p>`;
  }
  if (qual === "mapa") {
    titulo = "Mapa do Hotel";
    corpo = estado.mapa.length
      ? `<ul class="lista-mapa">` + estado.mapa.map(id => {
          const marcas = estado.marcadores.filter(m => m.area === id);
          return `<li><span>${AREAS[id] || id}</span>` +
            marcas.map(m => `<i class="marcador">? ${m.texto}</i>`).join("") + `</li>`;
        }).join("") + `</ul>`
      : `<p class="vazio">Você ainda não tem um mapa.</p>`;
  }

  el.innerHTML = `<div class="painel-topo"><h3>${titulo}</h3>
    <button class="painel-fechar" onclick="fecharPainel()">fechar ✕</button></div>${corpo}`;
  el.classList.remove("oculto");
}

/* ----- transformar a narrativa em BLOCOS (narração + falas) -----
 * Cada item de "narrativa" pode ser:
 *   - uma string                     -> texto narrado
 *   - ""                             -> quebra de parágrafo
 *   - {quem, texto}                  -> fala de um personagem (com quadradinho)
 *   - {texto}                        -> narração (útil junto com "se")
 *   - {estilo, texto}                -> bilhete | pensamento | sistema
 *   - {item: "id"}                   -> "Item recebido: ..." (e entra no inventário)
 * Qualquer item de objeto aceita  "se": {...}  -> só aparece se a condição valer.
 * {nome} e {sobrenome} são trocados pelo nome do jogador.
 *
 * Devolve um ARRAY de blocos de HTML — um por parágrafo/fala — para
 * revelar um de cada vez (estilo "caixa de diálogo" de RPG).
 */
function montarBlocosNarrativa(linhas) {
  const blocos = [];
  const acoes = [];          // acoes[i] = efeitos que acontecem quando o bloco i APARECE
  let acaoPend = [];         // efeitos das linhas do bloco que ainda está sendo montado
  let paragrafoAtual = [];   // narração acumulada
  let falaAtual = null;      // { quem, paragrafos: [] }

  function empurrar(html) {
    blocos.push(html);
    acoes[blocos.length - 1] = acaoPend;
    acaoPend = [];
  }
  function fecharParagrafo() {
    if (paragrafoAtual.length) {
      const texto = paragrafoAtual.join(" ");
      // letra grande (capitular) só em parágrafos longos
      empurrar(`<p class="${texto.length > 140 ? "longo" : "curto"}">${texto}</p>`);
      paragrafoAtual = [];
    }
  }
  function fecharFala() {
    if (falaAtual) {
      empurrar(montarBlocoDeFala(falaAtual.quem, falaAtual.paragrafos));
      falaAtual = null;
    }
  }
  // quem fala passa a ser "conhecido" (painel Social) no momento em que aparece
  const NAO_CONHECIVEIS = ["thiago", "desconhecida"];

  // só o que vale para o estado atual (campo "se")
  linhas.filter(l => typeof l === "string" || condicaoSe(estado, l.se)).forEach(linha => {
    if (typeof linha === "object" && linha !== null) {
      if (linha.quem) {
        // fala: se for a MESMA pessoa de antes, empilha no mesmo quadradinho
        fecharParagrafo();
        if (falaAtual && falaAtual.quem === linha.quem) {
          falaAtual.paragrafos.push(substituirNome(linha.texto));
        } else {
          fecharFala();
          falaAtual = { quem: linha.quem, paragrafos: [substituirNome(linha.texto)] };
        }
        if (!NAO_CONHECIVEIS.includes(linha.quem)) {
          acaoPend.push({ conhece: [linha.quem], hud: ["social"] });
        }
        if (linha.ao_mostrar) acaoPend.push(linha.ao_mostrar);
      } else if (linha.item) {
        fecharParagrafo(); fecharFala();
        const it = ITENS[linha.item] || { nome: linha.item };
        acaoPend.push({ itens: [linha.item], hud: ["inventario"] });
        if (linha.ao_mostrar) acaoPend.push(linha.ao_mostrar);
        empurrar(`<p class="estilo-item">Item recebido: <b>${it.nome}</b></p>`);
      } else if (linha.estilo) {
        fecharParagrafo(); fecharFala();
        const t = substituirNome(linha.texto);
        if (linha.ao_mostrar) acaoPend.push(linha.ao_mostrar);
        empurrar(linha.estilo === "sistema"
          ? `<div class="estilo-sistema"><p>${t}</p></div>`
          : `<p class="estilo-${linha.estilo}">${t}</p>`);
      } else {
        fecharFala();
        paragrafoAtual.push(substituirNome(linha.texto));
        if (linha.ao_mostrar) acaoPend.push(linha.ao_mostrar);
      }
    } else if (linha === "") {
      fecharParagrafo();
      fecharFala();
    } else {
      fecharFala();
      paragrafoAtual.push(substituirNome(linha));
    }
  });
  fecharParagrafo();
  fecharFala();
  blocos.acoes = acoes;
  return blocos;
}

/** Versão "tudo de uma vez" (usada pelo espelho: cena curta com interação própria). */
function montarNarrativa(linhas) {
  return montarBlocosNarrativa(linhas).join("");
}

/** Monta o quadradinho + um ou mais parágrafos de fala do mesmo personagem. */
function montarBlocoDeFala(quemId, paragrafos) {
  const p = PERSONAGENS[quemId];
  const nome = p ? p.nome : quemId;
  const retratoHtml = (p && p.retrato)
    ? `<img src="${p.retrato}" alt="${nome}">`
    : `<span class="interrogacao">?</span>`;
  const textoHtml = paragrafos.map(t => `<p class="fala-texto">${t}</p>`).join("");

  return `<div class="fala">
    <div class="avatar" title="${nome}">
      ${retratoHtml}
      <span class="avatar-nome">${nome}</span>
    </div>
    <div class="fala-textos">${textoHtml}</div>
  </div>`;
}

/** Troca {nome} e {sobrenome} pelos do jogador. */
function substituirNome(texto) {
  return texto
    .replace(/\{nome\}/g, estado.flags.nome || "Thiago")
    .replace(/\{sobrenome\}/g, estado.flags.sobrenome || "");
}

/* ----- mostrar uma cena na tela ----- */
function mostrarCena(id, restaurando = false) {
  cenaAtual = id;
  const cena = CENAS[id];
  const palco = document.getElementById("palco");

  // O que acontece ao CHEGAR nesta cena (campo "chegada" no JSON): tempo que
  // passa, flags, hud... Tudo o que o "efeitos" de uma opção aceita.
  // Se a cena só está sendo recarregada de um save, não aplica de novo.
  if (cena && !restaurando) {
    if (cena.chegada) aplicarEfeitos(estado, cena.chegada);
  }
  pintarStatus();
  window.scrollTo && window.scrollTo(0, 0);

  if (!cena) {
    palco.innerHTML = `<div class="cena"><p>[erro] cena '${id}' não encontrada.</p></div>`;
    return;
  }

  // cenas especiais
  if (cena.tipo === "espelho") return mostrarEspelho(cena);
  if (cena.tipo === "tracos") return mostrarTracos(cena);

  // sorteio: escolhe um destino ao acaso (opção = id simples ou {destino, efeitos})
  if (cena.tipo === "sorteio") {
    const opcoes = cena.dados.opcoes;
    const sorteado = opcoes[Math.floor(Math.random() * opcoes.length)];
    if (typeof sorteado === "object") {
      aplicarEfeitos(estado, sorteado.efeitos);
      mostrarCena(sorteado.destino);
    } else {
      mostrarCena(sorteado);
    }
    return;
  }
  // condicional: decide o destino sozinha olhando uma flag
  if (cena.tipo === "condicional") {
    const valor = estado.flags[cena.dados.flag];
    mostrarCena(cena.dados.casos[valor] || cena.dados.padrao);
    return;
  }

  // cena normal: narrativa em blocos + escolhas
  const ehFinal = cena.dados && cena.dados.final;
  const blocos = montarBlocosNarrativa(cena.narrativa);
  avancarLeitura(cena, blocos, 0, ehFinal);
}

/* ----- leitura em blocos (estilo "caixa de diálogo" de RPG clássico) -----
 * Mostra UM bloco por vez. Ao clicar em "continuar", o atual some e o
 * próximo aparece. No último bloco aparecem as escolhas (ou o botão de
 * seguir, se a cena tem só "destino_auto"; ou o recomeçar, se for final). */
function avancarLeitura(cena, blocos, indice, ehFinal) {
  const palco = document.getElementById("palco");
  // itens, pessoas conhecidas etc. só valem a partir do momento em que o bloco aparece
  const acaoDoBloco = blocos.acoes && blocos.acoes[indice];
  if (acaoDoBloco && acaoDoBloco.length) {
    acaoDoBloco.forEach(ef => aplicarEfeitos(estado, ef));
    pintarStatus();
  }
  const textoAtual = blocos[indice] || "";
  const ehUltimoBloco = indice >= blocos.length - 1;
  const classe = `cena ${cena.classe || ""} ${ehFinal ? "final" : ""}`;

  let html = `<div class="${classe}">
                <div class="narrativa">${textoAtual}</div>`;

  if (!ehUltimoBloco) {
    html += `<div class="avancar">
               <button class="btn-avancar" id="btn-avancar">continuar ▼</button>
             </div></div>`;
    palco.innerHTML = html;
    document.getElementById("btn-avancar").onclick =
      () => avancarLeitura(cena, blocos, indice + 1, ehFinal);
    return;
  }

  // último bloco
  if (ehFinal) {
    let extra = "";
    if (cena.dados.mostrar_tempo) {
      const t = resumoTempo(estado);
      const partes = [];
      if (t.dias) partes.push(`${t.dias} dia${t.dias > 1 ? "s" : ""}`);
      if (t.horas || !t.dias) partes.push(`${t.horas} hora${t.horas === 1 ? "" : "s"}`);
      extra = `<p class="tempo-final">Tempo no hotel: ${partes.join(" e ")} — ${t.noites} noite${t.noites === 1 ? "" : "s"} vivida${t.noites === 1 ? "" : "s"}.</p>`;
    }
    html += `${extra}<div class="escolhas">
               <button class="escolha" onclick="reiniciar()">— recomeçar —</button>
             </div></div>`;
    palco.innerHTML = html;
    return;
  }

  const visiveis = (cena.opcoes || []).filter(op =>
    checarRequisitos(estado, op.requisitos) && condicaoSe(estado, op.se));

  if (!visiveis.length && cena.destino_auto) {
    html += `<div class="avancar">
               <button class="btn-avancar" id="btn-seguir">continuar ▼</button>
             </div></div>`;
    palco.innerHTML = html;
    document.getElementById("btn-seguir").onclick = () => {
      if (cena.efeitos_saida) aplicarEfeitos(estado, cena.efeitos_saida);
      mostrarCena(cena.destino_auto);
    };
    return;
  }

  html += `<div class="escolhas">`;
  visiveis.forEach((op, i) => {
    const risco = op.teste ? `<span class="risco">⚄ risco</span>` : "";
    html += `<button class="escolha" data-i="${i}">${substituirNome(op.texto)}${risco}</button>`;
  });
  html += `</div></div>`;
  palco.innerHTML = html;

  palco.querySelectorAll(".escolha").forEach(botao => {
    botao.addEventListener("click", () => escolher(visiveis[+botao.dataset.i]));
  });
}

/* ----- o que acontece quando o jogador clica numa escolha ----- */
function escolher(op) {
  // escolha com teste de atributo (pode dar certo ou errado)
  if (op.teste) {
    const resultado = rolarTeste(estado, op.teste);
    const ramo = resultado.passou ? op.sucesso : op.falha;
    aplicarEfeitos(estado, ramo.efeitos);
    pintarStatus();
    const palco = document.getElementById("palco");
    palco.insertAdjacentHTML("afterbegin",
      `<div class="cena" style="animation:none">
         <p class="aviso-teste">Teste de ${op.teste.atributo}: ${resultado.categoria}</p>
       </div>`);
    setTimeout(() => mostrarCena(ramo.destino), 900);
    return;
  }
  // escolha simples
  aplicarEfeitos(estado, op.efeitos);
  mostrarCena(op.destino);
}

/* ----- cena especial: o espelho (distribuir os atributos) -----
 * Regras (em "dados" da cena, com estes padrões):
 *   base 50 · pontos 30 · passo 10 (blocos) · máximo 80 na criação.
 * O jogador pode ir e voltar, mas só confirma quando gastar tudo. */
function mostrarEspelho(cena) {
  const palco = document.getElementById("palco");
  const d = cena.dados || {};
  const TOTAL = d.pontos ?? 30;
  const PASSO = d.passo ?? 10;
  const MAXIMO = d.max ?? 80;
  let pontos = TOTAL;

  // valor de entrada = "piso": os pontos do espelho nunca descem abaixo dele
  const piso = {};
  ATRIBUTOS.forEach(attr => { piso[attr] = estado[attr]; });

  function desenhar() {
    let html = `<div class="cena">
      <div class="narrativa">${montarNarrativa(cena.narrativa)}</div>
      <div class="espelho">
        <h3>Quem é você</h3>
        <p class="restam">pontos a distribuir: <b>${pontos}</b> <span class="dica-inline">(de ${PASSO} em ${PASSO}, máximo ${MAXIMO})</span></p>`;

    ATRIBUTOS.forEach(attr => {
      const noMinimo = estado[attr] <= piso[attr];
      const semPontos = pontos < PASSO || estado[attr] + PASSO > MAXIMO;
      html += `<div class="attr" title="${ATRIBUTO_DICA[attr]}">
        <span class="nome">${ATRIBUTO_ROTULO[attr]}<small>${ATRIBUTO_DICA[attr]}</small></span>
        <button class="pill" data-menos="${attr}" ${noMinimo ? "disabled" : ""}>−</button>
        <span class="n">${estado[attr]}</span>
        <button class="pill" data-mais="${attr}" ${semPontos ? "disabled" : ""}>+</button>
      </div>`;
    });

    html += `<button class="confirmar" ${pontos !== 0 ? "disabled" : ""}>Confirmar</button>
      </div></div>`;
    palco.innerHTML = html;

    palco.querySelectorAll("[data-mais]").forEach(b => b.onclick = () => {
      const attr = b.dataset.mais;
      if (pontos >= PASSO && estado[attr] + PASSO <= MAXIMO) {
        estado[attr] += PASSO; pontos -= PASSO; desenhar();
      }
    });
    palco.querySelectorAll("[data-menos]").forEach(b => b.onclick = () => {
      const attr = b.dataset.menos;
      if (estado[attr] > piso[attr]) { estado[attr] -= PASSO; pontos += PASSO; desenhar(); }
    });
    palco.querySelector(".confirmar").onclick = () => {
      if (pontos === 0) mostrarCena(cena.destino_auto);
    };
  }

  desenhar();
}

/* ----- cena especial: o sonho de voar (2 virtudes + 1 vício) -----
 * Três sub-passos, na mesma cena:
 *   1) escolhe 2 VIRTUDES (de VIRTUDES em tracos.js)
 *   2) uma frase de transição ("perfeito demais...")
 *   3) escolhe 1 VÍCIO (de VICIOS em tracos.js)
 * Ao terminar, guarda tudo em estado.tracos e segue para destino_auto.
 */
function mostrarTracos(cena) {
  const palco = document.getElementById("palco");
  const QTD_VIRTUDES = (cena.dados && cena.dados.virtudes) || 2;
  const QTD_VICIOS = (cena.dados && cena.dados.vicios) || 1;
  const virtudesEscolhidas = [];
  let vicioEscolhido = null;

  function desenharVirtudes() {
    let html = `<div class="cena">
      <div class="narrativa">${montarNarrativa(cena.narrativa)}</div>
      <div class="tracos">
        <h3>Escolha ${QTD_VIRTUDES} virtudes</h3>
        <div class="traco-lista">`;
    VIRTUDES.forEach(v => {
      const marcado = virtudesEscolhidas.includes(v.id);
      const travado = !marcado && virtudesEscolhidas.length >= QTD_VIRTUDES;
      html += `<button class="traco-opcao ${marcado ? "selecionado" : ""}"
                 data-id="${v.id}" ${travado ? "disabled" : ""}>
                 <span class="traco-nome">${v.nome}</span>
                 <span class="traco-desc">${v.descricao}</span>
               </button>`;
    });
    html += `</div>
        <button class="confirmar" ${virtudesEscolhidas.length !== QTD_VIRTUDES ? "disabled" : ""}>Confirmar</button>
      </div></div>`;
    palco.innerHTML = html;

    palco.querySelectorAll("[data-id]").forEach(b => b.onclick = () => {
      const id = b.dataset.id;
      const i = virtudesEscolhidas.indexOf(id);
      if (i >= 0) {
        virtudesEscolhidas.splice(i, 1);
      } else if (virtudesEscolhidas.length < QTD_VIRTUDES) {
        virtudesEscolhidas.push(id);
      }
      desenharVirtudes();
    });
    palco.querySelector(".confirmar").onclick = () => {
      if (virtudesEscolhidas.length === QTD_VIRTUDES) desenharTransicao();
    };
  }

  function desenharTransicao() {
    const html = `<div class="cena">
      <div class="narrativa"><p>Perfeito. Perfeito demais. Nenhum humano é perfeito.</p></div>
      <div class="avancar">
        <button class="btn-avancar" id="btn-avancar-tracos">continuar ▼</button>
      </div></div>`;
    palco.innerHTML = html;
    document.getElementById("btn-avancar-tracos").onclick = desenharVicios;
  }

  function desenharVicios() {
    let html = `<div class="cena">
      <div class="tracos">
        <h3>Escolha ${QTD_VICIOS} vício</h3>
        <div class="traco-lista">`;
    VICIOS.forEach(v => {
      const marcado = vicioEscolhido === v.id;
      html += `<button class="traco-opcao ${marcado ? "selecionado" : ""}" data-id="${v.id}">
                 <span class="traco-nome">${v.nome}</span>
                 <span class="traco-desc">${v.descricao}</span>
               </button>`;
    });
    html += `</div>
        <button class="confirmar" ${!vicioEscolhido ? "disabled" : ""}>Confirmar</button>
      </div></div>`;
    palco.innerHTML = html;

    palco.querySelectorAll("[data-id]").forEach(b => b.onclick = () => {
      vicioEscolhido = b.dataset.id;
      desenharVicios();
    });
    palco.querySelector(".confirmar").onclick = () => {
      if (vicioEscolhido) {
        estado.tracos = { virtudes: virtudesEscolhidas.slice(), vicio: vicioEscolhido };
        mostrarCena(cena.destino_auto);
      }
    };
  }

  desenharVirtudes();
}

/* ----- salvar / continuar / recomeçar (gaveta do navegador — rápido) ----- */
function salvar() {
  try {
    localStorage.setItem("hotel_save", JSON.stringify({ estado, cenaAtual }));
    aviso("jogo salvo (neste navegador)");
  } catch (e) { aviso("não foi possível salvar aqui"); }
}
function continuar() {
  try {
    const dados = JSON.parse(localStorage.getItem("hotel_save"));
    if (!dados) { aviso("nenhum jogo salvo"); return; }
    estado = migrarEstado(dados.estado);
    mostrarCena(dados.cenaAtual, true);
  } catch (e) { aviso("nenhum jogo salvo"); }
}
function reiniciar() {
  estado = novoEstado();
  fecharPainel();
  mostrarCena(INICIO);
}

/* ----- exportar / importar save como ARQUIVO de verdade ----- */
// Gera um arquivo .json de verdade e manda o navegador baixá-lo.
// Esse arquivo é independente do navegador: pode ser copiado, enviado,
// guardado em outro lugar, e usado para continuar em qualquer computador.
function exportarSave() {
  const nome = (estado.flags && estado.flags.nome) ? estado.flags.nome : "jogo";
  const dados = JSON.stringify({ estado, cenaAtual }, null, 2);
  const blob = new Blob([dados], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const dataHoje = new Date().toISOString().slice(0, 10);
  const link = document.createElement("a");
  link.href = url;
  link.download = `hotel_save_${nome}_${dataHoje}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);

  aviso("arquivo de save baixado");
}

// Abre o seletor de arquivos do sistema e carrega um save de volta.
function importarSave() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "application/json";
  input.onchange = () => {
    const arquivo = input.files[0];
    if (!arquivo) return;
    const leitor = new FileReader();
    leitor.onload = () => {
      try {
        const dados = JSON.parse(leitor.result);
        if (!dados.estado || !dados.cenaAtual) throw new Error("arquivo inválido");
        estado = migrarEstado(dados.estado);
        mostrarCena(dados.cenaAtual, true);
        aviso("save carregado");
      } catch (e) {
        aviso("este arquivo não é um save válido");
      }
    };
    leitor.readAsText(arquivo);
  };
  input.click();
}

/* ----- avisinho flutuante no rodapé ----- */
function aviso(texto) {
  const el = document.createElement("div");
  el.className = "toast";
  el.textContent = texto;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1600);
}
