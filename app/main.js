// Hotel Los Segredos — janela do jogo + atualização automática dos arquivos do jogo pelo GitHub.
const { app, BrowserWindow, Menu, ipcMain } = require("electron");
const http = require("http"), fs = require("fs"), path = require("path"), https = require("https");

const REPO = "BrunoRamanery/hotel", RAMO = "main", PASTA_REMOTA = "game/";
const PORTA = 47321;                                           // fixa: o navegador interno guarda os saves por endereço
const EMBUTIDO = path.join(__dirname, "game");                 // cópia que vai dentro do programa
const ATUALIZADO = path.join(app.getPath("userData"), "game"); // cópia baixada do GitHub
const TEMPORARIO = path.join(app.getPath("userData"), "game_novo"); // onde as novidades chegam antes de valer
const TIPOS = { ".html":"text/html; charset=utf-8", ".css":"text/css", ".js":"text/javascript", ".json":"application/json; charset=utf-8", ".png":"image/png", ".jpg":"image/jpeg", ".svg":"image/svg+xml", ".mp3":"audio/mpeg", ".ogg":"audio/ogg" };

let janela = null;
let situacao = { fase: "parado", feito: 0, total: 0 };   // parado | verificando | baixando | pronto | atualizado | erro
let rodando = null;

function emitir(info) {
  situacao = Object.assign({ feito: 0, total: 0 }, info);
  if (janela && !janela.isDestroyed()) janela.webContents.send("app:progresso", situacao);
}

function pegar(url, binario, tentativas = 3) {
  const uma = () => new Promise((ok, falha) => {
    const req = https.get(url, { headers: { "User-Agent": "hotel-los-segredos" }, timeout: 20000 }, r => {
      if (r.statusCode !== 200) { r.resume(); return falha(new Error("HTTP " + r.statusCode)); }
      const partes = []; r.on("data", c => partes.push(c));
      r.on("end", () => { const b = Buffer.concat(partes); ok(binario ? b : b.toString("utf8")); });
    });
    req.on("timeout", () => req.destroy(new Error("tempo esgotado")));
    req.on("error", falha);
  });
  return (async () => {
    let ultimo;
    for (let i = 0; i < tentativas; i++) { try { return await uma(); } catch (e) { ultimo = e; } }
    throw ultimo;
  })();
}

// Compara a lista de arquivos do GitHub (pasta game/) com a cópia local, baixa só o que mudou
// (vários ao mesmo tempo) numa pasta temporária e só então troca tudo de uma vez.
async function fazerAtualizacao() {
  emitir({ fase: "verificando" });
  try {
    const arvore = JSON.parse(await pegar(`https://api.github.com/repos/${REPO}/git/trees/${RAMO}?recursive=1`));
    const remotos = arvore.tree.filter(t => t.type === "blob" && t.path.startsWith(PASTA_REMOTA));
    if (!remotos.length) return emitir({ fase: "atualizado" });
    const arqShas = path.join(ATUALIZADO, ".shas.json");
    let locais = {}; try { locais = JSON.parse(fs.readFileSync(arqShas, "utf8")); } catch (e) {}
    const novos = {}, pendentes = [];
    for (const t of remotos) {
      const rel = t.path.slice(PASTA_REMOTA.length);
      novos[rel] = t.sha;
      if (!(locais[rel] === t.sha && fs.existsSync(path.join(ATUALIZADO, rel)))) pendentes.push({ rel, caminho: t.path });
    }
    const removidos = Object.keys(locais).filter(rel => !novos[rel]);
    if (!pendentes.length && !removidos.length) {
      if (!fs.existsSync(arqShas)) { fs.mkdirSync(ATUALIZADO, { recursive: true }); fs.writeFileSync(arqShas, JSON.stringify(novos)); }
      return emitir({ fase: "atualizado" });
    }
    fs.rmSync(TEMPORARIO, { recursive: true, force: true });
    let feito = 0; const total = pendentes.length;
    emitir({ fase: "baixando", feito, total });
    let i = 0;
    const trabalhador = async () => {
      while (i < pendentes.length) {
        const p = pendentes[i++];
        const dados = await pegar(`https://raw.githubusercontent.com/${REPO}/${RAMO}/${p.caminho}`, true);
        const destino = path.join(TEMPORARIO, p.rel);
        fs.mkdirSync(path.dirname(destino), { recursive: true });
        fs.writeFileSync(destino, dados);
        feito++; emitir({ fase: "baixando", feito, total });
      }
    };
    await Promise.all([trabalhador(), trabalhador(), trabalhador(), trabalhador()]);
    // tudo baixado: troca de uma vez
    for (const p of pendentes) {
      const destino = path.join(ATUALIZADO, p.rel);
      fs.mkdirSync(path.dirname(destino), { recursive: true });
      fs.copyFileSync(path.join(TEMPORARIO, p.rel), destino);
    }
    for (const rel of removidos) { try { fs.unlinkSync(path.join(ATUALIZADO, rel)); } catch (e) {} }
    fs.writeFileSync(arqShas, JSON.stringify(novos));
    fs.rmSync(TEMPORARIO, { recursive: true, force: true });
    emitir({ fase: "pronto", feito: total, total });
  } catch (e) {
    emitir({ fase: "erro", erro: String(e && e.message || e) });
  }
}

function atualizar() {
  if (!rodando) rodando = fazerAtualizacao().finally(() => { rodando = null; });
  return rodando;
}

function pastaDoJogo() { return fs.existsSync(path.join(ATUALIZADO, "index.html")) ? ATUALIZADO : EMBUTIDO; }

function servidor() {
  return new Promise(ok => {
    const s = http.createServer((req, res) => {
      const raiz = pastaDoJogo();                      // olha a cada pedido: depois de atualizar já vale a nova pasta
      let p = decodeURIComponent(req.url.split("?")[0]); if (p === "/") p = "/index.html";
      const f = path.join(raiz, path.normalize(p));
      if (!f.startsWith(raiz)) { res.writeHead(403); return res.end(); }
      fs.readFile(f, (e, d) => {
        if (e) { res.writeHead(404); return res.end(); }
        res.writeHead(200, { "Content-Type": TIPOS[path.extname(f)] || "application/octet-stream", "Cache-Control": "no-store" }); res.end(d);
      });
    });
    s.once("error", () => s.listen(0, "127.0.0.1", () => ok(s.address().port)));   // porta fixa ocupada: usa outra
    s.listen(PORTA, "127.0.0.1", () => ok(s.address().port));
  });
}

ipcMain.handle("app:estado", () => situacao);
ipcMain.handle("app:atualizar", () => atualizar());
ipcMain.on("app:recarregar", () => { if (janela) janela.webContents.reloadIgnoringCache(); });
ipcMain.on("app:sair", () => app.quit());

app.whenReady().then(async () => {
  Menu.setApplicationMenu(null);
  const porta = await servidor();
  janela = new BrowserWindow({
    width: 1280, height: 860, minWidth: 900, minHeight: 640, backgroundColor: "#07080c", title: "Hotel Los Segredos",
    webPreferences: { preload: path.join(__dirname, "preload.js"), contextIsolation: true }
  });
  janela.loadURL(`http://127.0.0.1:${porta}/index.html`);
  janela.webContents.once("did-finish-load", () => atualizar());   // procura novidades sozinho, sem travar a abertura
});
app.on("window-all-closed", () => app.quit());
