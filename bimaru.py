# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 40:
# 102823 Beatriz Paulo
# 103726 Tomás Fonseca

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, rows, columns, values): 
        self.rows = rows
        self.columns = columns
        self.values = values

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO
        pass

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        # TODO
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        pass

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """

        """
        Cria o tabuleiro com os valores
        """
        values = []
        for i in range(10):
            values_line = np.full(shape=10,fill_value="~")
            values.append(values_line)
        values = np.asarray(values)
        """
        Le e cria a lista com os valores de cada linha
        """
        string_row = input()
        string_row = string_row.split('\t')
        string_row.remove("ROW")
        string_row = np.asarray(string_row)
        """
        Le e cria a lista com os valores de cada coluna 
        """
        string_column = input()
        string_column = string_column.split('\t')
        string_column.remove("COLUMN")
        string_column = np.asarray(string_column)

        """
        Le as hints e comeca a preencher o tabuleiro
        """ 
        hints_n = input()
        hints_n = int(hints_n)

        for x in range(hints_n):
            line = input()
            line = line.split('\t')
            values[int(line[1]), int(line[2])] = line[3]
        
        board = Board(string_row, string_column, values)
        return board 

    def printBoard(self):
        for i in range(10):
            for j in range(10):
                print(self.values[i][j], end="")
            print()

    def getPiece(self,x,y,board):
        return board[x][y].lower()

    def vertical(self,x,y,board):
        bottomPiece = getPiece(x,y,board)
        topPiece = getPiece(x-1,y,board)
        if (bottomPiece=='c') and (topPiece=='c'):
            return True
        if (bottomPiece=='b') and (topPiece=='t'):
            return True
        if (bottomPiece=='b') and (topPiece=='c'):
            return True
        if (bottomPiece=='c') and (topPiece=='t'):
            return True
        return False

    def horizontal(self,x,y,board):
        leftPiece = getPiece(x,y,board)
        rightPiece = getPiece(x,y+1,board)
        if (leftPiece=='c') and (rightPiece=='c'):
            return True
        if (leftPiece=='r') and (rightPiece=='l'):
            return True
        if (leftPiece=='r') and (rightPiece=='c'):
            return True
        if (leftPiece=='c') and (rightPiece=='l'):
            return True
        return False

    def countNeighbours(self,x,y,board):
        count = 0
        boats = 0
        selfBoat = False
        aboveBoat = False
        rightBoat = False
        diagonalBoat = False
        if (board[x][y] != 'W' and board[x][y] != '.' and board[x][y] != '~'):                      #self
            count += 1
            selfBoat = True

        if (x-1>=0) and (board[x-1][y] != 'W' and board[x-1][y] != '.' and board[x-1][y] != '~'):   #acima
            count += 1
            aboveBoat = True

        if (y+1<10) and (board[x][y+1] != 'W' and board[x][y+1] != '.' and board[x][y+1] != '~'):   #frente
            count+=1
            rightBoat=True

        if (x-1>=0 and y+1<10) and (board[x-1][y+1] != 'W' and board[x-1][y+1] != '.' and board[x-1][y+1] != '~'):    #diagonal
            count += 1
            diagonalBoat=True
        
        condition = False
        if (count==2):
            if selfBoat and aboveBoat:
                condition = vertical(x,y,board)
            elif selfBoat and rightBoat:
                condition = horizontal(x,y,board)
            elif rightBoat and diagonalBoat:
                condition = vertical(x,y+1,board)
            elif aboveBoat and diagonalBoat:
                condition = horizontal(x-1,y,board)
        if condition:
            count-=1
        return count
    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        for i in range(10):
            for  j in range(10):
                count = state.board.countNeighbours(i,j,state.board.values)
                print(count,end='')
            print()

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    board.printBoard()
    print()
    initialState = BimaruState(board)
    problem = Bimaru(board)
    problem.actions(initialState)
    pass
