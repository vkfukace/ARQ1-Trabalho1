# Arquitetura e Organização de Computadores I
# Trabalho 1
# Implementação de simulador para uma arquitetura com pipeline simplificada
#
# Aluno: Vinícius Kenzo Fukace
# RA: 115672

from typing import List, TextIO, Union

# TODO: guardar todas as instruções na memória no começo da execução
# Ordem dos estagios está errada, o certo tá na avaliação no drive

# Definição de Dados


class Instrucao:
    def __init__(self, strInstrucao: str) -> None:
        strInstrucao = strInstrucao.partition(' ')
        self.opcode: str = strInstrucao[0]

        self.operandos: List[str] = []
        strInstrucao = strInstrucao[2].split(',')
        for operando in strInstrucao:
            self.operandos.append(operando.strip())
        self.valores: List[int] = [0] * len(self.operandos)

    def toString(self) -> str:
        return self.opcode + ' ' + ', '.join(self.operandos)


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
        print('\n\tPipeline ============================================')
        for i in range(len(self.estagios)):
            if type(self.instr[i]) is Instrucao:
                print(f"{self.estagios[i]:>20}: {self.instr[i].toString()}")
            elif type(self.instr[i]) is str:
                print(f"{self.estagios[i]:>20}: {self.instr[i]}")
            else:
                print(f"{self.estagios[i]:>20}: -")

    # Redefine as instruções de busca e decodificação na pipeline como None
    def resetJump(self):
        self.estagios[0] = None
        self.estagios[1] = None


class Processador:
    def __init__(self) -> None:
        self.pipeline = Pipeline()

        # A arquitetura deve ter 32 registradores de uso geral;
        self.r: List[int] = [0]*32

        # PC – Contador de programa;
        # SP – Ponteiro de pilha;
        self.pc: int = 0
        self.sp: int = 0


class Memoria:
    # TODO: Inicia a memória com todas as instruções em arq
    def __init__(self, arq: TextIO) -> None:
        self.dados: List[int] = [0]*2048
        self.instrucoes: List[str] = []
        for linha in arq:
            self.instrucoes.append(linha.rstrip())


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

    # Faz a busca de instrução.
    def __buscaInst(self) -> None:
        self.pro.pipeline.instr[1] = self.pro.pipeline.instr[0]
        if self.pro.pc < len(self.mem.instrucoes):
            self.pro.pipeline.instr[0] = self.mem.instrucoes[self.pro.pc]
            self.pro.pc += 1
        else:
            self.pro.pipeline.instr[0] = None

    # Faz a decodificação de instrução.
    def __decoInst(self) -> None:
        if self.pro.pipeline.instr[1] is None:
            self.pro.pipeline.instr[2] = None
        else:
            self.pro.pipeline.instr[2] = Instrucao(self.pro.pipeline.instr[1])

    # Faz a execução da instrução.
    def __execucao(self) -> None:
        if self.pro.pipeline.instr[2] is None:
            self.pro.pipeline.instr[3] = None
        else:
            # TODO: switch com tudo essas porra
            pass

    # Faz o acesso a memória.
    def __acessoMem(self) -> None:
        if self.pro.pipeline.instr[3] is None:
            self.pro.pipeline.instr[4] = None
        else:
            # TODO: selecionar os que escrevem coisas na memoria
            pass

    # Faz a escrita do resultado nos registradores.
    def __escritaRes(self) -> None:
        if self.pro.pipeline.instr[4] is Instrucao:
            # TODO: Selecionar os que escrevem coisas em registrador
            pass

    # Veirfica a existência de hazards de dados na pipeline.
    # Se houver hazard, guarda o índice do estágio em que se encontra o hazard
    # em self.hazard e retorna True.
    # Caso contrário, guarda -1 em self.hazard e retorna False.
    def __existeHazard(self) -> int:
        # Verifica somente a instrução no estágio de decodificação, pois a
        # leitura de operandos é feita somente no estágio de execução
        inst: Instrucao = Instrucao(self.pro.pipeline.instr[1])

        if inst.opcode != 'j' and inst.opcode != 'jal':
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
    # Caso não haja hazard de dados, insere uma nova instrução na pipeline
    # e retorna True.
    # Caso contrário, retorna False.
    def avanca(self) -> bool:
        # Se não existe hazard
        if self.hazard == -1:
            self.__escritaRes()
            self.__acessoMem()
            self.__execucao()
            self.__decoInst()
            self.__buscaInst()

            self.__existeHazard()
        else:
            self.__escritaRes()
            self.__acessoMem()
            self.__execucao()

            if self.hazard == 4:
                self.hazard = -1
            else:
                self.hazard += 1


# Função Principal
def main():
    try:
        instrucoes = open("instrucoes.txt", mode='rt', encoding='utf-8')
        sim: Simulador = Simulador(instrucoes)
    finally:
        instrucoes.close()

    exit


# Teste
stringTeste = 'add rax, rbx, rcx'
instrucaoTeste = Instrucao(stringTeste)
print(instrucaoTeste.toString())

if __name__ == '__main__':
    main()
