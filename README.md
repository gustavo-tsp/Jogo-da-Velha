# ❌⭕ Jogo da Velha no Terminal

Jogo da velha feito em Python para rodar direto no terminal. Sem dependências externas.

## Funcionalidades

- **Contra o computador (fácil):** jogadas aleatórias
- **Contra o computador (difícil):** usa o algoritmo *minimax*, então nunca perde (o melhor que você consegue é empatar)
- **Dois jogadores** no mesmo teclado
- Placar com vitórias e empates entre várias rodadas
- Quem começa alterna a cada rodada, para ser justo
- Tabuleiro colorido, com a linha vencedora destacada

## Como rodar

Requisito: Python 3.8 ou superior.

```bash
git clone https://github.com/SEU-USUARIO/jogo-da-velha.git
cd jogo-da-velha
python jogo_da_velha.py
```

No Linux/macOS, se `python` não funcionar, use `python3 jogo_da_velha.py`.

Durante o jogo, digite `q` a qualquer momento para sair.

## Como jogar

As casas do tabuleiro são numeradas de 1 a 9:

```
   1 │ 2 │ 3
  ───┼───┼───
   4 │ 5 │ 6
  ───┼───┼───
   7 │ 8 │ 9
```

Digite o número da casa onde quer jogar. Vence quem completar uma linha, coluna ou diagonal.

## Como a IA difícil funciona

O computador simula todas as jogadas possíveis até o fim da partida (algoritmo **minimax**),
assumindo que o adversário também joga da melhor forma. Vitórias mais rápidas e derrotas mais
tardias recebem notas melhores. Quando há mais de uma jogada igualmente boa, ele escolhe uma
delas ao acaso, para o jogo não ficar sempre igual.

## Ideias para evoluir

- Dificuldade média (bloqueia e ganha quando pode, mas sem olhar adiante)
- Escolher entre X e O
- Tabuleiros maiores (4x4, 5x5)
- Salvar o placar em arquivo
