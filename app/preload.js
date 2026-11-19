// Ponte segura entre a janela do jogo e o programa (tela de entrada: botão Atualizar).
const { contextBridge, ipcRenderer } = require("electron");
contextBridge.exposeInMainWorld("hotelApp", {
  estado: () => ipcRenderer.invoke("app:estado"),            // { fase, feito, total }
  atualizar: () => ipcRenderer.invoke("app:atualizar"),      // procura e baixa novidades
  recarregar: () => ipcRenderer.send("app:recarregar"),      // aplica a nova versão
  sair: () => ipcRenderer.send("app:sair"),
  aoProgresso: cb => ipcRenderer.on("app:progresso", (_e, info) => cb(info))
});
