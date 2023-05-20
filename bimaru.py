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
    
    def __init__(self, rows, columns, values, boats, hints): 
        self.rows = rows
        self.columns = columns
        self.values = values
        self.boats = boats
        self.hints = hints

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.values[row, col]

    """
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        Devolve os valores imediatamente acima e abaixo,
        respectivamente.
        above = '~'
        below='~'
        if (row+1 < 10):
            below = self.values[row+1, col] 
        if (row-1 >= 0):
            above = self.values[row-1, col] 

        return (above, below)
        
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        Devolve os valores imediatamente à esquerda e à direita,
        respectivamente.
        left = '~'
        right='~'
        if (col+1 < 10):
            right = self.values[row, col+1] 
        if (col-1 >= 0):
            left = self.values[row, col-1] 

        return (left, right)
    """
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """

        """
        Cria o tabuleiro com os valores
        """
        values = []
        boats = [4,3,2,1]
        #hash_map = np.full(100, -1, dtype=int)

        for i in range(10):
            values_line = np.full(shape=10,fill_value="~")    #preenche o tabuleiro com vazios
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
        hintsVec = []
        for x in range(hints_n):
            line = input()
            line = line.split('\t')
            print(line)
            if (line[3]!='C' and line[3]!='W'):
                currentHint = np.array([int(line[1]), int(line[2]), line[3]])   #cria vetor de hint
                hintsVec.append(currentHint)                                    #adiciona vetor a lista de hints
            values[int(line[1]), int(line[2])] = line[3]                        #adiciona hint ao tabuleiro
        
        hintsVec = np.asarray(hintsVec)
        board = Board(string_row, string_column, values, boats, hintsVec)
        return board 

    def printBoard(self):
        print()
        for i in self.columns:
            print(" " + str(i),end="")                      #print dos valores de cada coluna
        print()
        for i in range(10):
            for j in range(10):
                print(" " + str(self.values[i][j]), end="")   #print de cada valor do tabuleiro
            print("  " + self.rows[i])                        #print dos valores de cada linha

    def getPiece(self,x,y,board):
        return board[x][y].lower()

    def vertical(self,x,y,board):
        print("entering vertical ---" + str(x) + str(y))
        bottomPiece = self.getPiece(x,y,board)
        topPiece = self.getPiece(x-1,y,board)
        if (bottomPiece=='m') and (topPiece=='m'):
            print("returning true --- 4")
            return True
        if (bottomPiece=='b') and (topPiece=='t'):
            print("returning true --- 3")
            return True
        if (bottomPiece=='b') and (topPiece=='m'):
            print("returning true --- 2")
            return True
        if (bottomPiece=='m') and (topPiece=='t'):
            print("returning true --- 1")
            return True
        print("returning false")
        return False

    def horizontal(self,x,y,board):
        leftPiece = self.getPiece(x,y,board)
        rightPiece = self.getPiece(x,y+1,board)
        if (leftPiece=='m') and (rightPiece=='m'):
            return True
        if (leftPiece=='r') and (rightPiece=='l'):
            return True
        if (leftPiece=='r') and (rightPiece=='m'):
            return True
        if (leftPiece=='m') and (rightPiece=='l'):
            return True
        return False

    def countNeighbours(self,x,y,board):
        count = 0
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
                condition = self.vertical(x,y,board)        #se o barco for o mesmo vertical(self, above)
            elif selfBoat and rightBoat:
                condition = self.horizontal(x,y,board)      #se o barco for o mesmo horizontal(self, right)
            elif rightBoat and diagonalBoat:
                condition = self.vertical(x,y+1,board)      #se o barco for o mesmo vertical(right, diagonal)
            elif aboveBoat and diagonalBoat:
                condition = self.horizontal(x-1,y,board)    #se o barco for o mesmo horizontal(above, diagonal)
        if condition:
            count-=1                                        #se for igual tirar um ao count P==1
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
        board = state.board
        actions = []
        # Vamos resolver primeiro as pistas
        if board.hints.size > 0:
            # Resolvemos uma pista e recebemos a lista de ações possíveis
            actions = self.solveHints()
            # MERO TESTE, NÃO SERÁ ASSIM
            i = 1
            for action in actions:
                d = self.result(state, action)
                print("Action #" + str(i))
                d.board.printBoard()
                print()
                i+=1


        return np.asarray(actions)

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        # TODO update pistas laterais
        board = np.copy(state.board.values)             #copia board
        rows = np.copy(state.board.rows)
        columns = np.copy(state.board.columns)
        boats = np.copy(state.board.boats)
        hints = np.copy(state.board.boats)
        direction = action[0]                           # H (horizontal), V (vertical)
        x = int(action[1])                              #action = (direction, x, y, size)
        y = int(action[2])
        size = int(action[3])

        if (direction=='V'):                            #se a direcao for vertical
            if (board[x, y]=='~'):                      #se a posicao for vazia
                rows[x] = int(rows[x]) - 1              #diminui o valor da row
                columns[y] = int(columns[y]) - 1        #diminui o valor da collumn
                board[x, y] = 't'                       #adiciona um top

            for i in range(1, size-1):
                if (board[x+i, y]=='~'):
                    rows[x+i] = int(rows[x+i]) - 1
                    columns[y] = int(columns[y]) - 1
                    board[x+i, y]='m'                   #adiciona um middle

            if (board[x+size-1, y]=='~'):
                rows[x+size-1] = int(rows[x+size-1]) - 1
                columns[y] = int(columns[y]) - 1
                board[x+size-1, y]='b'                  #adiciona um bottom

        boats[size-1] -= 1                              #retira o barco que foi metido
        hints = hints[1:]                               #atualiza o vetor das hints
        newBoard = Board(rows, columns, board, boats, hints)
        newState = BimaruState(newBoard)
        return newState

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

    def p(self):
        """
        Calcula a matriz P
        """
        for i in range(10):
            for  j in range(10):
                count = self.board.countNeighbours(i,j,self.board.values)
                if (count >= 2):
                    return False
        return True

    def boatFits(self, x, y, piece, size):
        condition = True
        oldPieces = np.full(shape=4,fill_value="~")
        # Verifica se o tabuleiro está apto para receber o navio
        if (piece == 'T' ) and (x+size<10) and (int(self.board.columns[y])-size>=0) and \
            (self.board.values[x+size-1][y] == '~' or self.board.values[x+size-1][y] == 'B'):
            # Inicializa as peças antigas com as peças nas posições atuais do tabuleiro
            oldPieces[0] = piece
            oldPieces[1] = self.board.values[x+1][y]
            oldPieces[2] = self.board.values[x+2][y]
            oldPieces[3] = self.board.values[x+3][y]

            # Verifica se as posiões que estão entre as pontas são vazias ou meios e se podemos por
            # a peça sem quebrar as pistas laterais
            for i in range(1,size-1):
                if self.board.values[x+i][y] != 'M' and self.board.values[x+i][y] != '~':
                    condition = False
                if int(self.board.rows[x+i])<1:
                    #Se a peça não poder ser posta por restrições laterais, então pomos uma água
                    #lá, para evitar procuras desnecessárias
                    condition = False
                    #TODO meter agua na row toda
                    oldPieces[i] = 'W'
                board.values[x+i][y] = 'm'

            self.board.values[x+size-1][y] = 'b'
            # Verificamos, ainda, se as pista lateral também permite por a peça terminal
            if int(self.board.rows[x+size-1]) < 1:
                #Novamente, pomos água se as restrições não permitem
                oldPieces[size-1] = 'W'
                condition = False

            # Se não der, temos que repor o tabuleiro e retornar Falso (o barco não cabe)
            if not condition:
                self.board.values[x+1][y] = oldPieces[1]
                self.board.values[x+2][y] = oldPieces[2]
                self.board.values[x+3][y] = oldPieces[3]
                #self.board.printBoard()
                return False

            # Só temos de verificar se a matriz P o permite
            result = self.p()

            # Antes de mais, temos que repor o tabuleiro, após testarmos a matriz P
            self.board.values[x+1][y] = oldPieces[1]
            self.board.values[x+2][y] = oldPieces[2]
            self.board.values[x+3][y] = oldPieces[3]

            #Então devolvemos se a matriz permite ou não
            return result  
        
        if (piece == 'B' ) and (x-size+1>=0) and (int(self.board.columns[y])-size>=0) and \
            (self.board.values[x-size+1][y] == '~' or self.board.values[x-size+1][y] == 'T'):
            # Inicializa as peças antigas com as peças nas posições atuais do tabuleiro
            oldPieces[0] = piece
            oldPieces[1] = self.board.values[x-1][y]
            oldPieces[2] = self.board.values[x-2][y]
            oldPieces[3] = self.board.values[x-3][y]

            # Verifica se as posiões que estão entre as pontas são vazias ou meios e se podemos por
            # a peça sem quebrar as pistas laterais
            for i in range(1,size-1):
                if self.board.values[x-i][y] != 'M' and self.board.values[x-i][y] != '~':
                    condition = False
                if int(self.board.rows[x-i])<1:
                    #Se a peça não poder ser posta por restrições laterais, então pomos uma água
                    #lá, para evitar procuras desnecessárias
                    condition = False
                    #TODO meter agua na row toda
                    oldPieces[i] = 'W'
                board.values[x-i][y] = 'm'

            self.board.values[x-size+1][y] = 't'
            # Verificamos, ainda, se as pista lateral também permite por a peça terminal
            if int(self.board.rows[x-size+1]) < 1:
                #Novamente, pomos água se as restrições não permitem
                oldPieces[size-1] = 'W'
                condition = False

            # Se não der, temos que repor o tabuleiro e retornar Falso (o barco não cabe)
            if not condition:
                self.board.values[x-1][y] = oldPieces[1]
                self.board.values[x-2][y] = oldPieces[2]
                self.board.values[x-3][y] = oldPieces[3]
                #self.board.printBoard()
                return False

            # Só temos de verificar se a matriz P o permite
            result = self.p()

            # Antes de mais, temos que repor o tabuleiro, após testarmos a matriz P
            self.board.values[x-1][y] = oldPieces[1]
            self.board.values[x-2][y] = oldPieces[2]
            self.board.values[x-3][y] = oldPieces[3]

            #Então devolvemos se a matriz permite ou não
            return result 

    def tryTop(self, hint):
        x = hint[0]
        y = hint[1]
        piece = hint[2]
        i = 4
        while (i>1):             #verifica o maior size de boat que podemos meter
            if (self.boatFits(int(x),int(y),piece,i)):
                break
            i -= 1
        print("here top  " + str(i))
        return i
    
    def tryBottom(self, hint):
        x = hint[0]
        y = hint[1]
        piece = hint[2]
        i = 4
        while (i>1):             #verifica o maior size de boat que podemos meter
            if (self.boatFits(int(x),int(y),piece,i)):
                break
            i -= 1
        print("here bottom  " + str(i))
        return i

    def solveHints(self):
        hint = self.board.hints[0]
        if hint[2]=='T':
            maxSize = self.tryTop(hint)
            possibilities = []
            for i in range(2, maxSize+1):
                possibility = np.full(shape=4,fill_value="~")
                possibility[0] = 'V'                        #vertical
                possibility[1] = hint[0]
                possibility[2] = hint[1]
                possibility[3] = i
                possibilities.append(possibility)
            possibilities = np.asarray(possibilities)
            return possibilities
                
        elif hint[2]=='B':            #termos que contar x-size para dar apenas o top
            maxSize = self.tryBottom(hint)
            possibilities = []
            for i in range(2, maxSize+1):
                possibility = np.full(shape=4,fill_value="~")
                possibility[0] = 'V'                        #vertical
                possibility[1] = int(hint[0]) - i +1 #pode ser -4+2=-3 ou seja no maximo vai ter 3 para cima
                possibility[2] = hint[1]
                possibility[3] = i
                possibilities.append(possibility)
            possibilities = np.asarray(possibilities)
            return possibilities
        elif hint[2]=='R':
            self.tryRight(hint)
        elif hint[2]=='L':            #termos que contar y+size para dar apenas o right
            self.tryLeft(hint)
        else:
            self.tryMiddle(hint)
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    board.values[2][0]='M'
    #board.printBoard()
    print()
    initialState = BimaruState(board)
    problem = Bimaru(board)
    problem.actions(initialState)
    pass
