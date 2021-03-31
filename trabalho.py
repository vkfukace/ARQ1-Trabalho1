# Arquitetura e Organização de Computadores I
# Trabalho 1
# Implementação de simulador para uma arquitetura com pipeline simplificada
#
# Aluno: Vinícius Kenzo Fukace
# RA: 115672

from typing import Deque, List, Union
from collections import deque


# Definição de Dados

class Instrucao:
    def __init__(self, strInstrucao: str) -> None:
        strInstrucao = strInstrucao.split(' ')
        self.opcode: str = strInstrucao[0]

        self.operandos: List[str] = []
        for operando in strInstrucao[1:]:
            if operando.endswith(','):
                self.operandos.append(operando[:-1])
            else:
                self.operandos.append(operando)
        self.valores = [0] * len(self.operandos)

    def toString(self) -> str:
        return self.opcode + ' ' + ', '.join(self.operandos)


class Pipeline:
    def __init__(self) -> None:
        # No primeiro estágio, será usada uma str, nos demais,
        # será usada uma Instrucao.
        # Caso um estágio estiver sem instruções, será usado None
        self.estagios: List[str] = []
        self.estagios.append('Busca de Instrução')
        self.estagios.append('Decodificação de Instrução')
        self.estagios.append('Acesso a Memória')
        self.estagios.append('Execução')
        self.estagios.append('Escrita do Resultado')

        self.instr: List[Union[Instrucao, str, None]]
        self.instr = [None] * len(self.estagios)

    # Exibe na tela quais instruções se encontram em cada estágio do pipeline.
    # Quando um estágio estiver sem instruções, a saída apresenta '-'
    def printEstado(self):
        print('\n\tPipeline ============================================')
        for i in range(len(self.estagios)):
            if type(self.instr[i]) is Instrucao:
                print(self.estagios[i] + ': ' + self.instr[i].toString())
            elif type(self.instr[i]) is str:
                print(self.estagios[i] + ': ' + self.instr[i])
            else:
                print(self.estagios[i] + ': -')

    # Redefine todas as instruções na pipeline como None
    def reset(self):
        for estagio in self.estagios:
            estagio[1] = None


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
        self.pro = Processador()
        self.mem = Memoria()
        self.hazard: int = -1

        self.opsAritmetica: List[str] = [
            'add', 'addi', 'sub', 'subi', 'mul', 'div']
        self.opsDesvio: List[str] = ['blt', 'bgt', 'beq', 'j', 'jr', 'jal']
        self.opsMemoria: List[str] = ['lw', 'sw']
        self.opsMovimentacao: List[str] = ['mov', 'movi']

    # Faz a busca de instrução.
    def __buscaInst(self) -> bool:
        pass

    # Faz a decodificação de instrução.
    def __decoInst(self) -> bool:
        pass

    # Faz o acesso a memória.
    def __acessoMem(self) -> bool:
        pass

    # Faz a execução da instrução.
    def __execucao(self) -> bool:
        pass

    # Faz a escrita do resultado nos registradores.
    def __escritaRes(self) -> bool:
        pass

    # Veirfica a existência de hazards de dados na pipeline.
    # Se houver hazard, guarda o índice do estágio em que se encontra o hazard
    # em self.hazard e retorna True.
    # Caso contrário, guarda -1 em self.hazard e retorna False.
    def __existeHazard(self) -> int:
        # Verifica somente a instrução no estágio de decodificação, pois a
        # leitura de operandos é feita somente no estágio de acesso à memória
        inst: Instrucao = self.pro.pipeline.instr[1]
        if inst.opcode is 'blt' or inst.opcode is 'bgt' or inst.opcode is 'beq':
            pass  # TODO
        else:
            for i in range(2, len(self.pro.pipeline.estagios)):
                if type(self.pro.pipeline.instr[i]) is Instrucao:
                    if inst.operandos[0] == self.pro.pipeline.instr[i].operandos[0]:
                        self.hazard = i
                        return True
        self.hazard = -1
        return False

    # Avança o estado da execução, inserindo novaInstr na pipeline
    # Caso haja um hazard de dados, retorna False
    # Caso contrário, retorna True
    def avanca(self, novaInstr) -> bool:
        # Se não existe hazard
        if self.hazard == -1:
            # insere novaInstr
            # Executa coisas
            self.__existeHazard()
        else:
            if self.hazard <= 3:
                self.__escritaRes()
                self.hazard = -1

            if self.hazard <= 2:
                self.__execucao()
                self.hazard += 1


# Função Principal


def main():
    # try:
    #     instrucoes = open("instrucoes.txt", mode='rt', encoding='utf-8')
    #     for linha in instrucoes:
    #         print(linha)
    # finally:
    #     instrucoes.close()

    stringTeste = 'add rax, rbx, rcx'
    instrucaoTeste = Instrucao(stringTeste)
    print(instrucaoTeste.toString())
    exit


if __name__ == '__main__':
    main()
