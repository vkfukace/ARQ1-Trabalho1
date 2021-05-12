# Arquitetura e Organização de Computadores I
# Trabalho 1
# Implementação de simulador para uma arquitetura com pipeline simplificada
#
# Aluno: Vinícius Kenzo Fukace
# RA: 115672

from typing import List, TextIO, Union, Dict

# Definição de Dados


class Instrucao:
    def __init__(self, strInstrucao: str) -> None:
        strAux = strInstrucao.partition(' ')

        self.string: str = strInstrucao
        self.operandos: List[str] = []
        self.opcode: str = strAux[0]

        strAux = strAux[2].split(',')
        if self.opcode == 'lw' or self.opcode == 'sw':
            self.operandos.append(strAux[0].strip())
            strAux = strAux[1].strip(')').split('(')
            self.operandos.append(strAux[0].strip())
            self.operandos.append(strAux[1].strip())
        else:
            for operando in strAux:
                operando = operando.strip()
                self.operandos.append(operando)


class Pipeline:
    def __init__(self) -> None:
        # No primeiro estágio, será usada uma str, nos demais,
        # será usada uma Instrucao.
        # Caso um estágio estiver sem instruções, será usado None
        self.estagios: List[str] = []
        self.estagios.append('Busca')
        self.estagios.append('Decodificação')
        self.estagios.append('Execução')
        self.estagios.append('Acesso Memória')
        self.estagios.append('Escrita Resultado')

        self.instr: List[Union[Instrucao, str, None]]
        self.instr = [None] * len(self.estagios)

    # Exibe na tela quais instruções se encontram em cada estágio do pipeline.
    # Quando um estágio estiver sem instruções, a saída apresenta '-'
    def printEstado(self):
        print(f"\nPipeline =================================================")
        for i in range(len(self.estagios)):
            if type(self.instr[i]) is Instrucao:
                print(f"{self.estagios[i]:>20}: {self.instr[i].string}")
            elif type(self.instr[i]) is str:
                print(f"{self.estagios[i]:>20}: {self.instr[i]}")
            else:
                print(f"{self.estagios[i]:>20}: -")

    # Redefine as instruções de busca e decodificação na pipeline como None.
    # Usado somente em operações de desvio.
    def resetDesvio(self):
        self.instr[0] = None
        self.instr[1] = None


class Processador:
    def __init__(self) -> None:
        self.pipeline = Pipeline()

        # A arquitetura deve ter 32 registradores de uso geral;
        self.r: Dict[str, int] = {}
        for i in range(32):
            self.r["r" + str(i)] = 0

        # PC – Contador de programa;
        # SP – Ponteiro de pilha;
        # RA – Endereço de retorno;
        self.pc: int = 0
        self.sp: int = 0
        self.ra: int = 0

    # Exibe os valores armazenados em cada um dos registradores na tela.
    def printEstado(self):
        txt: str = f''
        print(f"\nRegistradores ============================================")
        for i in range(4):
            for j in range(8):
                chave: str = f'r{8*i+j}'
                temp: str = f'{chave:>3}: {self.r[chave]:4} | '
                txt = f'{txt}{temp}'
            print(txt)
            txt = f''
        print(f' pc: {self.pc:4} |  sp: {self.sp:4} |  ra: {self.ra:4}')


class Memoria:
    # Inicia a memória com todas as instruções em arq
    def __init__(self, arq: TextIO) -> None:
        self.tam: int = 256
        self.dados: List[int] = [0]*self.tam
        self.instrucoes: List[str] = []
        for linha in arq:
            self.instrucoes.append(linha.rstrip())

    def printEstado(self):
        txt: str = f''
        cont: int = 0
        i: int = 0
        print(f"\nMemoria ==================================================")
        while cont < self.tam:
            txt = f'{i*16:>3} - {i*16 + 15:>3}: '
            for j in range(16):
                temp: str = f'{self.dados[cont]:>3} | '
                txt = f'{txt}{temp}'
                cont += 1
            print(txt)
            i += 1
            txt = f''
        pass


class Simulador:
    # Inicia o simulador usando o arquivo que contém o conjunto de instruções
    def __init__(self, arq: TextIO) -> None:
        self.pro = Processador()
        self.mem = Memoria(arq)
        self.hazard: int = -1

        if self.mem.instrucoes:
            self.pro.pipeline.instr[0] = self.mem.instrucoes[0]
            self.pro.pc = 1

        self.opsAritmetica: List[str] = [
            'add', 'addi', 'sub', 'subi', 'mul', 'div']
        self.opsDesvio: List[str] = ['blt', 'bgt', 'beq', 'j', 'jr', 'jal']
        self.opsMemoria: List[str] = ['lw', 'sw']
        self.opsMovimentacao: List[str] = ['mov', 'movi']

    #####################
    # Operações

    # Aritméticas
    def add(self, i: Instrucao) -> None:
        self.pro.r[i.operandos[0]] = self.pro.r[i.operandos[1]] + \
            self.pro.r[i.operandos[2]]

    def addi(self, i: Instrucao) -> None:
        self.pro.r[i.operandos[0]] = self.pro.r[i.operandos[1]] + \
            int(i.operandos[2])

    def sub(self, i: Instrucao) -> None:
        self.pro.r[i.operandos[0]] = self.pro.r[i.operandos[1]] - \
            self.pro.r[i.operandos[2]]

    def subi(self, i: Instrucao) -> None:
        self.pro.r[i.operandos[0]] = self.pro.r[i.operandos[1]] - \
            int(i.operandos[2])

    def mul(self, i: Instrucao) -> None:
        self.pro.r[i.operandos[0]] = self.pro.r[i.operandos[1]] * \
            self.pro.r[i.operandos[2]]

    def div(self, i: Instrucao) -> None:
        if self.pro.r[i.operandos[2]] != 0:
            self.pro.r[i.operandos[0]] = self.pro.r[i.operandos[1]] / \
                self.pro.r[i.operandos[2]]
        else:
            self.pro.r[i.operandos[0]] = 0

    # Desvios

    def blt(self, i: Instrucao) -> None:
        if self.pro.r[i.operandos[0]] < self.pro.r[i.operandos[1]]:
            self.pro.pc = int(i.operandos[2])
            self.hazard = -1
            self.pro.pipeline.resetDesvio()

    def bgt(self, i: Instrucao) -> None:
        if self.pro.r[i.operandos[0]] > self.pro.r[i.operandos[1]]:
            self.pro.pc = int(i.operandos[2])
            self.hazard = -1
            self.pro.pipeline.resetDesvio()

    def beq(self, i: Instrucao) -> None:
        if self.pro.r[i.operandos[0]] == self.pro.r[i.operandos[1]]:
            self.pro.pc = int(i.operandos[2])
            self.hazard = -1
            self.pro.pipeline.resetDesvio()

    def j(self, i: Instrucao) -> None:
        self.pro.pc = int(i.operandos[0])
        self.hazard = -1
        self.pro.pipeline.resetDesvio()

    def jr(self, i: Instrucao) -> None:
        self.pro.pc = self.pro.r[i.operandos[0]]
        self.hazard = -1
        self.pro.pipeline.resetDesvio()

    def jal(self, i: Instrucao) -> None:
        self.pro.ra = self.pro.pc + 1
        self.pro.pc = int(i.operandos[0])
        self.hazard = -1
        self.pro.pipeline.resetDesvio()

    # Memória

    def lw(self, i: Instrucao) -> None:
        if int(i.operandos[1]) <= self.mem.tam:
            self.pro.r[i.operandos[0]] = self.mem.dados[int(i.operandos[1]) +
                                                        self.pro.r[i.operandos[2]]]

    def sw(self, i: Instrucao) -> None:
        if int(i.operandos[1]) <= self.mem.tam:
            self.mem.dados[int(i.operandos[1]) + self.pro.r[i.operandos[2]]] = \
                self.pro.r[i.operandos[0]]

    # Movimentação

    def mov(self, i: Instrucao) -> None:
        self.pro.r[i.operandos[0]] = self.pro.r[i.operandos[1]]

    def movi(self, i: Instrucao) -> None:
        self.pro.r[i.operandos[0]] = int(i.operandos[1])

    #####################
    # Estágios de pipeline

    # Faz a escrita do resultado nos registradores.
    def __escritaRes(self) -> None:
        if type(self.pro.pipeline.instr[4]) is Instrucao:
            if self.pro.pipeline.instr[4].opcode == 'add':
                self.add(self.pro.pipeline.instr[4])
            elif self.pro.pipeline.instr[4].opcode == 'addi':
                self.addi(self.pro.pipeline.instr[4])
            elif self.pro.pipeline.instr[4].opcode == 'sub':
                self.sub(self.pro.pipeline.instr[4])
            elif self.pro.pipeline.instr[4].opcode == 'subi':
                self.subi(self.pro.pipeline.instr[4])
            elif self.pro.pipeline.instr[4].opcode == 'mul':
                self.mul(self.pro.pipeline.instr[4])
            elif self.pro.pipeline.instr[4].opcode == 'div':
                self.div(self.pro.pipeline.instr[4])
            elif self.pro.pipeline.instr[4].opcode == 'lw':
                self.lw(self.pro.pipeline.instr[4])
            elif self.pro.pipeline.instr[4].opcode == 'mov':
                self.mov(self.pro.pipeline.instr[4])
            elif self.pro.pipeline.instr[4].opcode == 'movi':
                self.movi(self.pro.pipeline.instr[4])

            self.pro.pipeline.instr[4] = None

    # Faz o acesso a memória.
    def __acessoMem(self) -> None:
        if type(self.pro.pipeline.instr[3]) is Instrucao:
            if self.pro.pipeline.instr[3].opcode == 'sw':
                self.sw(self.pro.pipeline.instr[3])

            self.pro.pipeline.instr[4] = self.pro.pipeline.instr[3]
            self.pro.pipeline.instr[3] = None

    # Faz a execução da instrução.
    def __execucao(self) -> None:
        if type(self.pro.pipeline.instr[2]) is Instrucao:
            if self.pro.pipeline.instr[2].opcode == 'blt':
                self.blt(self.pro.pipeline.instr[2])
            elif self.pro.pipeline.instr[2].opcode == 'bgt':
                self.bgt(self.pro.pipeline.instr[2])
            elif self.pro.pipeline.instr[2].opcode == 'beq':
                self.beq(self.pro.pipeline.instr[2])
            elif self.pro.pipeline.instr[2].opcode == 'j':
                self.j(self.pro.pipeline.instr[2])
            elif self.pro.pipeline.instr[2].opcode == 'jr':
                self.jr(self.pro.pipeline.instr[2])
            elif self.pro.pipeline.instr[2].opcode == 'jal':
                self.jal(self.pro.pipeline.instr[2])

            self.pro.pipeline.instr[3] = self.pro.pipeline.instr[2]
            self.pro.pipeline.instr[2] = None

    # Faz a decodificação de instrução.
    # Se houver hazard, não é executado.
    def __decoInst(self) -> None:
        if self.hazard == -1:
            if type(self.pro.pipeline.instr[1]) is str:
                self.pro.pipeline.instr[2] = Instrucao(
                    self.pro.pipeline.instr[1])
                self.pro.pipeline.instr[1] = None

    # Faz a busca de instrução.
    # Se houver hazard, não é executado.
    def __buscaInst(self) -> None:
        if self.hazard == -1:
            self.pro.pipeline.instr[1] = self.pro.pipeline.instr[0]
            if self.pro.pc < len(self.mem.instrucoes):
                self.pro.pipeline.instr[0] = self.mem.instrucoes[self.pro.pc]
                self.pro.pc += 1
            else:
                self.pro.pipeline.instr[0] = None

    # Veirfica a existência de hazards de dados na pipeline.
    # Se houver hazard, guarda o índice do estágio em que se encontra o hazard
    # em self.hazard e retorna True.
    # Caso contrário, guarda -1 em self.hazard e retorna False.
    def __existeHazard(self) -> bool:
        # Verifica somente a instrução no estágio de decodificação, pois a
        # leitura de operandos é feita somente no estágio de execução
        if type(self.pro.pipeline.instr[1]) is str:
            inst: Instrucao = Instrucao(self.pro.pipeline.instr[1])

            # Para cada estágio após o de decodificação
            for i in range(2, len(self.pro.pipeline.estagios)):
                if type(self.pro.pipeline.instr[i]) is Instrucao:
                    # Se o primeiro operando da inst está nesse estágio (RAW, WAW)
                    if inst.operandos[0] in self.pro.pipeline.instr[i].operandos:
                        self.hazard = i
                        return True
                    # Se o primeiro operando desse estágio está em inst (WAR)
                    if self.pro.pipeline.instr[i].operandos[0] in inst.operandos:
                        self.hazard = i
                        return True
        self.hazard = -1
        return False

    # Avança o estado da execução.
    # Caso não haja hazard de dados, executa todas as instruções da pipeline.
    # Caso contrário, executa somente os 3 últimos estágios, e atualiza o status
    # do hazard.
    def avanca(self) -> None:
        # Se não existe hazard
        self.__escritaRes()
        self.__acessoMem()
        self.__execucao()
        self.__decoInst()
        self.__buscaInst()

        if self.hazard == -1:
            self.__existeHazard()
        else:
            if self.hazard == 4:
                self.hazard = -1
            else:
                self.hazard += 1

    # Mostra o estado da memória, registradores e pipeline
    def printEstado(self) -> None:
        self.mem.printEstado()
        self.pro.printEstado()
        self.pro.pipeline.printEstado()
        print(f'\nHazard: ', end='')
        if self.hazard == -1:
            print(f'-')
        else:
            print(
                f'{self.pro.pipeline.instr[1]}, {self.pro.pipeline.instr[self.hazard].string}')

    # Retorna True se existe instruções na pipeline, False caso contrário.
    def status(self) -> bool:
        for i in range(len(self.pro.pipeline.estagios)):
            if type(self.pro.pipeline.instr[i]) == str:
                return True
            if type(self.pro.pipeline.instr[i]) == Instrucao:
                return True
        return False

# Função Principal


def main():
    try:
        instrucoes = open("instrucoes.txt", mode='rt', encoding='utf-8')
        sim: Simulador = Simulador(instrucoes)
        print("Inicialização do Simulador Completa")

        sim.printEstado()

        opcao: str
        print(f'\nInsira \'x\' para sair, qualquer outra letra para avancar: ', end='')
        opcao = input()
        while opcao != 'x' and sim.status() == True:
            sim.avanca()
            sim.printEstado()
            print(
                f'\nInsira \'x\' para sair, qualquer outra letra para avancar: ', end='')
            opcao = input()

        print(f'Execucao Finalizada')

    finally:
        instrucoes.close()
    exit


# Teste
stringTeste = 'add rax, rbx, rcx'
instrucaoTeste = Instrucao(stringTeste)
print(instrucaoTeste.string)
instrucaoTeste = Instrucao('lw r13, 8(r2)')


if __name__ == '__main__':
    main()
