#!/usr/bin/env python3
"""Jogo da Velha no Terminal ❌⭕

Modos: contra o computador (fácil ou impossível de vencer) ou dois jogadores.
Sem dependências externas: só precisa do Python 3.8+.
"""

import os
import random
import time

LINHAS_VENCEDORAS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontais
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # verticais
    (0, 4, 8), (2, 4, 6),             # diagonais
]

# Habilita cores ANSI no Windows 10+
if os.name == "nt":
    os.system("")


class Cor:
    AZUL = "\033[94m"
    VERMELHO = "\033[91m"
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    CIANO = "\033[96m"
    CINZA = "\033[90m"
    NEGRITO = "\033[1m"
    FIM = "\033[0m"


class SairDoJogo(Exception):
    """Lançada quando o jogador digita 'q' para sair."""


# ---------------------------------------------------------------- utilidades
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def ler_entrada(texto):
    """Lê uma entrada; 'q' encerra o jogo."""
    resposta = input(texto).strip()
    if resposta.lower() == "q":
        raise SairDoJogo
    return resposta


def outro(simbolo):
    return "O" if simbolo == "X" else "X"


# ---------------------------------------------------------------- regras
def vencedor(tab):
    """Devolve 'X', 'O' ou None. Também devolve a linha vencedora."""
    for a, b, c in LINHAS_VENCEDORAS:
        if tab[a] != " " and tab[a] == tab[b] == tab[c]:
            return tab[a], (a, b, c)
    return None, None


def jogadas_livres(tab):
    return [i for i, casa in enumerate(tab) if casa == " "]


# ---------------------------------------------------------------- IA
def minimax(tab, vez, ia, profundidade=0):
    """Pontua o tabuleiro do ponto de vista da IA (vitórias rápidas valem mais)."""
    ganhador, _ = vencedor(tab)
    if ganhador == ia:
        return 10 - profundidade
    if ganhador == outro(ia):
        return profundidade - 10
    livres = jogadas_livres(tab)
    if not livres:
        return 0

    pontuacoes = []
    for pos in livres:
        tab[pos] = vez
        pontuacoes.append(minimax(tab, outro(vez), ia, profundidade + 1))
        tab[pos] = " "
    return max(pontuacoes) if vez == ia else min(pontuacoes)


def jogada_ia(tab, simbolo, dificuldade):
    livres = jogadas_livres(tab)
    if dificuldade == "facil":
        return random.choice(livres)

    # Difícil: escolhe (aleatoriamente) entre as melhores jogadas do minimax
    melhor_nota = None
    melhores = []
    for pos in livres:
        tab[pos] = simbolo
        nota = minimax(tab, outro(simbolo), simbolo, 1)
        tab[pos] = " "
        if melhor_nota is None or nota > melhor_nota:
            melhor_nota, melhores = nota, [pos]
        elif nota == melhor_nota:
            melhores.append(pos)
    return random.choice(melhores)


# ---------------------------------------------------------------- telas
def desenhar_tabuleiro(tab, destaque=None):
    def celula(i):
        casa = tab[i]
        if casa == " ":
            return f"{Cor.CINZA}{i + 1}{Cor.FIM}"
        cor = Cor.AZUL if casa == "X" else Cor.VERMELHO
        if destaque and i in destaque:
            cor = Cor.VERDE
        return f"{cor}{Cor.NEGRITO}{casa}{Cor.FIM}"

    print()
    for linha in range(3):
        print("   " + " │ ".join(celula(linha * 3 + col) for col in range(3)))
        if linha < 2:
            print("  ───┼───┼───")
    print()


def mostrar_titulo():
    limpar_tela()
    print(f"{Cor.AMARELO}{Cor.NEGRITO}")
    print("╔══════════════════════════════════════╗")
    print("║           ❌  JOGO DA VELHA  ⭕       ║")
    print("╚══════════════════════════════════════╝")
    print(Cor.FIM)


def mostrar_placar(slots, placar):
    n1, n2 = slots[0]["nome"], slots[1]["nome"]
    print(
        f"{Cor.CIANO}Placar → {n1}: {placar[0]}  |  {n2}: {placar[1]}  |  "
        f"Empates: {placar[2]}{Cor.FIM}"
    )


def menu_modo():
    mostrar_titulo()
    print("  1) Jogar contra o computador (fácil)")
    print("  2) Jogar contra o computador (difícil — impossível de vencer)")
    print("  3) Dois jogadores")
    print("  4) Sair")
    print("\n(digite 'q' a qualquer momento para sair)")
    while True:
        escolha = ler_entrada("\nEscolha uma opção: ")
        if escolha in {"1", "2", "3", "4"}:
            if escolha == "4":
                raise SairDoJogo
            return escolha
        print(f"{Cor.VERMELHO}Opção inválida.{Cor.FIM}")


def ler_nome(padrao):
    nome = ler_entrada(f"Nome ({padrao}): ")[:15]
    return nome or padrao


def ler_jogada(tab, nome, simbolo):
    while True:
        escolha = ler_entrada(f"{nome} ({simbolo}), escolha uma casa (1-9): ")
        if not escolha.isdigit() or not 1 <= int(escolha) <= 9:
            print(f"{Cor.VERMELHO}Digite um número de 1 a 9.{Cor.FIM}")
            continue
        pos = int(escolha) - 1
        if tab[pos] != " ":
            print(f"{Cor.VERMELHO}Essa casa já está ocupada.{Cor.FIM}")
            continue
        return pos


# ---------------------------------------------------------------- partida
def jogar_rodada(jogadores, dificuldade, slots, placar):
    """Joga uma rodada. `jogadores` mapeia 'X'/'O' para o jogador da vez.
    Devolve 'X', 'O' ou None (empate)."""
    tab = [" "] * 9
    vez = "X"

    while True:
        mostrar_titulo()
        mostrar_placar(slots, placar)
        desenhar_tabuleiro(tab)
        jogador = jogadores[vez]

        if jogador["ia"]:
            print(f"{jogador['nome']} ({vez}) está pensando...")
            time.sleep(0.7)
            pos = jogada_ia(tab, vez, dificuldade)
        else:
            pos = ler_jogada(tab, jogador["nome"], vez)

        tab[pos] = vez
        ganhador, linha = vencedor(tab)
        if ganhador or not jogadas_livres(tab):
            mostrar_titulo()
            mostrar_placar(slots, placar)
            desenhar_tabuleiro(tab, destaque=linha)
            return ganhador
        vez = outro(vez)


def jogar_sessao(modo):
    if modo == "3":
        slots = [
            {"nome": ler_nome("Jogador 1"), "ia": False},
            {"nome": ler_nome("Jogador 2"), "ia": False},
        ]
        dificuldade = None
    else:
        slots = [
            {"nome": ler_nome("Você"), "ia": False},
            {"nome": "Computador", "ia": True},
        ]
        dificuldade = "facil" if modo == "1" else "dificil"

    placar = [0, 0, 0]  # vitórias do slot 0, vitórias do slot 1, empates
    rodada = 0

    while True:
        # Quem começa (X) alterna a cada rodada, para ser justo
        primeiro = rodada % 2
        jogadores = {"X": slots[primeiro], "O": slots[1 - primeiro]}
        resultado = jogar_rodada(jogadores, dificuldade, slots, placar)

        if resultado is None:
            placar[2] += 1
            print(f"{Cor.AMARELO}{Cor.NEGRITO}Deu velha! Empate 🤝{Cor.FIM}")
        else:
            indice = primeiro if resultado == "X" else 1 - primeiro
            placar[indice] += 1
            nome = slots[indice]["nome"]
            print(f"{Cor.VERDE}{Cor.NEGRITO}🏆 {nome} venceu a rodada!{Cor.FIM}")

        rodada += 1
        outra = input("\nJogar outra rodada? (ENTER = sim, n = voltar ao menu): ")
        if outra.strip().lower() in {"n", "nao", "não"}:
            return
        if outra.strip().lower() == "q":
            raise SairDoJogo


def main():
    try:
        while True:
            modo = menu_modo()
            jogar_sessao(modo)
    except (SairDoJogo, KeyboardInterrupt, EOFError):
        pass
    print("\nValeu por jogar! 👋")


if __name__ == "__main__":
    main()
