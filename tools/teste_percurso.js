// Percorre TODOS os caminhos possíveis do Ato 1 usando o motor de verdade (com tela falsa)
// e confere: sem becos sem saída, tempo coerente, itens, barras.
const fs = require('fs'), path = require('path');
const raiz = path.resolve(__dirname, '../hotel_rpg');
function mk() { const t = { style: {}, classList: { toggle() {}, add() {}, remove() {} }, _h: '', textContent: '', dataset: {} };
  return new Proxy(t, { get(o, k) { if (k in o) return o[k]; if (k === 'innerHTML') return o._h; if (k === 'querySelectorAll') return () => []; return typeof k === 'string' ? (() => mk()) : undefined; },
    set(o, k, v) { o[k === 'innerHTML' ? '_h' : k] = v; return true; } }); }
const els = {};
global.document = { getElementById: id => els[id] || (els[id] = mk()), body: { classList: { toggle() {} }, appendChild() {} }, createElement() { return mk(); } };
global.window = { addEventListener() {}, scrollTo() {} }; global.localStorage = {};
const src = ['personagens', 'tracos', 'itens', 'estado', 'regras', 'validador', 'motor', 'main']
  .map(f => fs.readFileSync(path.join(raiz, 'js', f + '.js'), 'utf8').replace(/^"use strict";/, '')).join('\n');
const cenas = JSON.parse(fs.readFileSync(path.join(raiz, 'cenas/ato1.json'), 'utf8'));
const codigo = src + `
cenas.forEach(c => CENAS[c.id] = c);
const probs = validarCenas(CENAS, "c01_bilhete"); console.log("validador:", probs.length ? probs : "OK");
const clone = o => JSON.parse(JSON.stringify(o));
const visitadas = new Set(); const finais = []; const problemas = []; let caminhos = 0;

function entrar(id, st) {            // aplica o que o motor aplica ao entrar numa cena
  estado = st; const c = CENAS[id];
  if (c.chegada) aplicarEfeitos(estado, c.chegada);
  darItensDaCena(c);
  visitadas.add(id);
  // texto monta sem erro?
  if (c.narrativa) montarBlocosNarrativa(c.narrativa);
  return c;
}
function andar(id, st, trilha) {
  const c = entrar(id, st); const cur = st; trilha = trilha.concat(id);   // "cur" = estado desta ramificação (não o global)
  if (c.tipo === "sorteio") { c.dados.opcoes.forEach(o => { const s2 = clone(cur); if (o.efeitos) aplicarEfeitos(s2, o.efeitos); andar(o.destino, s2, trilha); }); return; }
  if (c.tipo === "condicional") { andar(c.dados.casos[cur.flags[c.dados.flag]] || c.dados.padrao, cur, trilha); return; }
  if (c.tipo === "espelho") { const s2 = clone(cur); s2.forca += 30; andar(c.destino_auto, s2, trilha); return; }
  if (c.tipo === "tracos") { const s2 = clone(cur); s2.tracos = { virtudes: ["leal", "curioso"], vicio: "impulsivo" }; andar(c.destino_auto, s2, trilha); return; }
  if (c.dados && c.dados.final) { caminhos++; finais.push({ trilha, estado: clone(cur) }); return; }
  estado = cur;
  const vis = (c.opcoes || []).filter(o => checarRequisitos(cur, o.requisitos) && condicaoSe(cur, o.se));
  if (!vis.length) {
    if (c.destino_auto) { andar(c.destino_auto, cur, trilha); return; }
    problemas.push("BECO SEM SAÍDA em " + id + " (flags: " + JSON.stringify(cur.flags) + ")"); return;
  }
  vis.forEach(o => { const s2 = clone(cur); aplicarEfeitos(s2, o.efeitos); andar(o.destino, s2, trilha); });
}
andar("c01_bilhete", novoEstado(), []);
console.log("caminhos completos:", caminhos);
console.log("problemas:", problemas.length ? problemas.slice(0, 5) : "nenhum");
const naoVisitadas = Object.keys(CENAS).filter(i => !visitadas.has(i)); console.log("cenas nunca visitadas:", naoVisitadas.length ? naoVisitadas : "nenhuma");
// resumo dos finais
const horas = new Set(finais.map(f => horaTexto(f.estado) + " dia " + diaAtual(f.estado)));
console.log("hora ao fim:", [...horas]);
const supra = finais.map(f => f.estado.suspeita); console.log("suspeita ao fim: min", Math.min(...supra), "max", Math.max(...supra));
const fo = finais.map(f => f.estado.fome); console.log("fome ao fim: min", Math.min(...fo), "max", Math.max(...fo));
const inv = new Set(finais.map(f => f.estado.inventario.join(","))); console.log("inventário:", [...inv]);
console.log("peso:", pesoCarregado(finais[0].estado) + "/" + finais[0].estado.peso);
// roteiro de horas num caminho
const ex = finais[0]; console.log("trilha exemplo:", ex.trilha.join(" > "));
// relógio por cena num caminho (Mavis + banho + piano)
estado = novoEstado();
for (const id of ex.trilha) { const c = CENAS[id]; if (c.chegada) aplicarEfeitos(estado, c.chegada); console.log(id.padEnd(22), horaTexto(estado), periodoDoDia(estado).padEnd(9), "dia", diaAtual(estado), "fome", estado.fome); }
console.log("data final:", JSON.stringify(dataAtual(estado)), estacaoDoAno(estado));
`;
new Function('cenas', codigo)(cenas);
