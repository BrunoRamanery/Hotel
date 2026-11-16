@echo off
REM ============================================================
REM  abrir_jogo.bat  —  ABRE O JOGO COM DOIS CLIQUES
REM  Liga um servidor local (usando o Python) e abre o navegador.
REM  Feche esta janela preta quando terminar de jogar.
REM ============================================================
title Hotel RPG - servidor (nao feche enquanto joga)
echo Iniciando o Hotel RPG...
echo.
echo Abrindo no navegador: http://localhost:8000
echo (Deixe esta janela aberta enquanto joga. Feche-a ao terminar.)
echo.
start "" http://localhost:8000/index.html
python -m http.server 8000
