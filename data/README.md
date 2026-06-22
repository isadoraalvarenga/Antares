# Dados

Esta pasta guarda arquivos de persistencia simples em texto.

## Arquivos

- `recorde.txt`: melhor pontuacao registrada.
- `README.txt`: arquivo legado; manter por compatibilidade se necessario.

## Sistema de pontuacao

O jogo possui um sistema de pontuacao simples, controlado em `src/jogo.py`:

- A pontuacao (`pontos`) comeca em `0` no inicio de cada partida.
- Cada nave inimiga destruida vale **+100** pontos (`calcular_pontos`).
- Cada asteroide que sai pela parte inferior da tela sem colidir vale **+1** ponto.

O recorde e persistido em `recorde.txt`:

- No inicio da partida o valor e lido por `carregar_recorde` (`src/dados.py`); se o
  arquivo nao existir ou estiver vazio, assume `0`.
- Sempre que a pontuacao atual supera o recorde, ele e atualizado e regravado por
  `salvar_recorde`.

