# Hotel Los Segredos

Jogo narrativo de um hotel assombrado (HTML + CSS + JavaScript).

    game/    o jogo (cenas em game/cenas/*.json)
    app/     a janela do Windows (Electron) + atualização automática
    tools/   geradores e testes das cenas
    .github/ gera o executável sozinho

## Como a atualização funciona
Quem baixa o executável **uma vez** recebe toda mudança feita em `game/` automaticamente:
ao abrir, o programa procura novidades em segundo plano e baixa só o que mudou
(vários arquivos ao mesmo tempo, numa pasta temporária, trocando tudo de uma vez no fim).
Na tela de entrada, o botão **Atualizar** mostra o progresso e, quando há versão nova,
vira **Aplicar agora**. Sem internet, abre a última versão que tiver.
O executável só precisa ser gerado de novo se a pasta `app/` mudar (v1.1.0 trouxe a tela de entrada).

## Gerar o executável
Aba **Actions** → "Gerar executável Windows" → **Run workflow** → baixar o zip em "Artifacts".
Ou criar uma tag `vX.Y.Z`: o zip aparece na aba **Releases**.
