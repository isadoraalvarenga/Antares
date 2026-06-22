# Testes

Esta pasta contem testes automatizados do projeto.

## Arquivos

- `test_logica.py`: valida funcoes puras de logica em `src/funcoes.py`.
- `test_barra_vida`: testa se as reduções e alterações da barra de vida estão corretas em `src/jogo.py`.
- `test_death_star`: testa se as ações e o personagem da Estrela da Morte estão funcionais e de acordo com as condições/regras do jogo em `src/jogo.py`.
- `test_naves_inimigas`: testa se as naves inimigas causam e sofrem o dano estipulado pelo código, além de spawnarem e se movimentarem de forma correta em `src/jogo.py`.

## Como executar

```bash
python -m pytest
```
```bash
python tests/test_barra_vida.py
```

```bash
python tests/test_death_star.py
```

```bash
python tests/test_naves_inimigas.py
```
