# Manager DO-BR

Carreira de técnico com os clubes reais do Dugout Online (Brasil), no modelo do Boleiros Manager.
Irmão do Copa 7a0, do Fenômeno DO-BR e do Carreira DO-BR — usa o mesmo repo de escudos/uniformes/estádios.

## Rodar

    python -m http.server 8795

e abrir http://localhost:8795 (precisa de servidor por causa do `fetch("dados.json")`).

## Arquivos

- `index.html` — o jogo inteiro (client-side, save em `localStorage`, chave `manager_dobr_v1`).
- `dados.json` — 132 clubes e 1451 jogadores; gerado por `python gerar_dados.py` a partir de `../FenomenoDOBR`.

## O que tem

- 11 divisões de 12 clubes (Brasileirão, B1/B2, C1–C8), 22 rodadas, acesso/rebaixamento e playoff dos vices da B.
- Copa do Brasil com 128 clubes (7 fases, pênaltis).
- Partida ao vivo minuto a minuto: substituições (5), mentalidade, cartões, lesões, cansaço — ou "Simular".
- Tática (6 formações), mercado (compra com % de chance, venda por propostas), finanças, estádio e estrutura.
- Diretoria com objetivo e confiança: demissão, propostas de outros clubes, reputação e histórico do técnico.
- Evolução de jovens, envelhecimento, aposentadoria e garotos da base a cada virada de temporada.

## Calibração do motor

Constantes no topo do `index.html` (`BASE_GOLS`, `K_FORCA`, `CONV`). Medido em ~4300 jogos:
2,7 gols/jogo, 44% mandante, 22% empates, favorito com 4+ de força vence ~70%.
