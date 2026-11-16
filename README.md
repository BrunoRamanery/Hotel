# Hotel Los Segredos

Jogo narrativo de um hotel assombrado (HTML + CSS + JavaScript).

    game/    o jogo (cenas em game/cenas/*.json)
    app/     a janela do Windows (Electron) + atualização automática
    tools/   geradores e testes das cenas
    .github/ gera o executável sozinho

## Como a atualização funciona
Quem baixa o executável **uma vez** recebe toda mudança feita em `game/` automaticamente:
ao abrir, o programa compara com este repositório e baixa só o que mudou
(precisa de internet; sem internet, abre a última versão que tiver).
O executável só precisa ser gerado de novo se a pasta `app/` mudar.

## Gerar o executável
Aba **Actions** → "Gerar executável Windows" → **Run workflow** → baixar o zip em "Artifacts".
