# Arquitetura e Organização de Computadores I
# Trabalho 1
# Implementação de simulador para uma arquitetura com pipeline simplificada
#
# Aluno: Vinícius Kenzo Fukace
# RA: 115672

from typing import Deque, List
from collections import deque


# Definição de Dados

class Pipeline:
    def __init__(self) -> None:
        self.buscaInstrucao: str = '-'
        self.decoInstrucao: str = '-'
        self.execucao: str = '-'
        self.acessoMem: str = '-'
        self.escritaRes: str = '-'


class Processador:
    def __init__(self) -> None:
        self.pipeline = Pipeline()

        # A arquitetura deve ter 32 registradores de uso geral;
        self.r: List[int] = [0]*32

        # PC – Contador de programa;
        # SP – Ponteiro de pilha;
        # RA – Endereço de retorno;
        self.pc: int = None
        self.sp: int = None
        self.ra: int = None


class Memoria:
    def __init__(self) -> None:
        self.dados: List[int] = [0]*2048
        self.instrucoes: Deque[str] = deque([])


class Simulador:
    def __init__(self) -> None:
        self.processador = Processador()
        self.memoria = Memoria()


# Função Principal


def main():
    # try:
    #     instrucoes = open("instrucoes.txt", mode='rt', encoding='utf-8')
    #     for linha in instrucoes:
    #         print(linha)
    # finally:
    #     instrucoes.close()
    exit


if __name__ == '__main__':
    main()
