// Hotel Los Segredos — janela do jogo + atualização automática dos arquivos do jogo pelo GitHub.
const { app, BrowserWindow, Menu } = require("electron");
const http = require("http"), fs = require("fs"), path = require("path"), https = require("https");

const REPO = "BrunoRamanery/hotel", RAMO = "main", PASTA_REMOTA = "game/";
const EMBUTIDO = path.join(__dirname, "game");              // cópia que vai dentro do programa
const ATUALIZADO = path.join(app.getPath("userData"), "game"); // cópia baixada do GitHub
const TIPOS = { ".html":"text/html; charset=utf-8", ".css":"text/css", ".js":"text/javascript", ".json":"application/json; charset=utf-8", ".png":"image/png", ".jpg":"image/jpeg", ".svg":"image/svg+xml", ".mp3":"audio/mpeg", ".ogg":"audio/ogg" };

function pegar(url, binario) {
  return new Promise((ok, falha) => {
    const req = https.get(url, { headers: { "User-Agent": "hotel-los-segredos" }, timeout: 5000 }, r => {
      if (r.statusCode !== 200) { r.resume(); return falha(new Error("HTTP " + r.statusCode)); }
      const partes = []; r.on("data", c => partes.push(c));
      r.on("end", () => { const b = Buffer.concat(partes); ok(binario ? b : b.toString("utf8")); });
    });
    req.on("timeout", () => req.destroy(new Error("tempo esgotado")));
    req.on("error", falha);
  });
}

// Compara a lista de arquivos do GitHub (pasta game/) com a cópia local e baixa só o que mudou.
async function atualizar() {
  try {
    const arvore = JSON.parse(await pegar(`https://api.github.com/repos/${REPO}/git/trees/${RAMO}?recursive=1`));
    const remotos = arvore.tree.filter(t => t.type === "blob" && t.path.startsWith(PASTA_REMOTA));
    if (!remotos.length) return;
    const arqShas = path.join(ATUALIZADO, ".shas.json");
    let locais = {}; try { locais = JSON.parse(fs.readFileSync(arqShas, "utf8")); } catch (e) {}
    const novos = {}; let mudou = false;
    for (const t of remotos) {
      const rel = t.path.slice(PASTA_REMOTA.length);
      novos[rel] = t.sha;
      const destino = path.join(ATUALIZADO, rel);
      if (locais[rel] === t.sha && fs.existsSync(destino)) continue;
      const dados = await pegar(`https://raw.githubusercontent.com/${REPO}/${RAMO}/${t.path}`, true);
      fs.mkdirSync(path.dirname(destino), { recursive: true });
      fs.writeFileSync(destino, dados); mudou = true;
    }
    for (const rel of Object.keys(locais)) if (!novos[rel]) { try { fs.unlinkSync(path.join(ATUALIZADO, rel)); mudou = true; } catch (e) {} }
    if (mudou || !fs.existsSync(arqShas)) { fs.mkdirSync(ATUALIZADO, { recursive: true }); fs.writeFileSync(arqShas, JSON.stringify(novos)); }
  } catch (e) { /* sem internet ou GitHub fora: usa o que já tem */ }
}

function pastaDoJogo() { return fs.existsSync(path.join(ATUALIZADO, "index.html")) ? ATUALIZADO : EMBUTIDO; }

function servidor(raiz) {
  return new Promise(ok => {
    const s = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split("?")[0]); if (p === "/") p = "/index.html";
      const f = path.join(raiz, path.normalize(p));
      if (!f.startsWith(raiz)) { res.writeHead(403); return res.end(); }
      fs.readFile(f, (e, d) => {
        if (e) { res.writeHead(404); return res.end(); }
        res.writeHead(200, { "Content-Type": TIPOS[path.extname(f)] || "application/octet-stream", "Cache-Control": "no-store" }); res.end(d);
      });
    }).listen(0, "127.0.0.1", () => ok(s.address().port));
  });
}

app.whenReady().then(async () => {
  Menu.setApplicationMenu(null);
  await Promise.race([atualizar(), new Promise(r => setTimeout(r, 8000))]);
  const porta = await servidor(pastaDoJogo());
  const w = new BrowserWindow({ width: 1000, height: 900, backgroundColor: "#0b0d12", title: "Hotel Los Segredos" });
  w.loadURL(`http://127.0.0.1:${porta}/index.html`);
});
app.on("window-all-closed", () => app.quit());
