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
    
    def __init__(self, rows, columns, values, boats, hints, free, ofree): 
        self.rows = rows
        self.columns = columns
        self.values = values
        self.boats = boats
        self.hints = hints
        self.free = free
        self.ofree = ofree

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.values[row, col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        above = '~'
        below='~'
        if (row+1 < 10):
            below = self.values[row+1, col] 
        if (row-1 >= 0):
            above = self.values[row-1, col] 

        return (above, below)
        
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        left = '~'
        right='~'
        if (col+1 < 10):
            right = self.values[row, col+1] 
        if (col-1 >= 0):
            left = self.values[row, col-1] 

        return (left, right)
     
    def adjacent_diagonal_values(self,x,y):
        topRight = '~'
        topLeft = '~'
        bottomRight = '~'
        bottomLeft = '~'
        if (x-1>=0):
            if (y-1>=0):
                topLeft = self.values[x-1][y-1]
            if (y+1<10):
                topRight = self.values[x-1][y+1]
        if (x+1<10):
            if (y-1>=0):
                bottomLeft = self.values[x+1][y-1]
            if (y+1<10):
                bottomRight = self.values[x+1][y+1]
        return (topRight, topLeft, bottomRight, bottomLeft)

    def isPlaceable(self,piece):
        return piece=='W' or piece=='~' or piece=='.'

    def validPos(self,x,y):
        diagonals = self.adjacent_diagonal_values(x,y)
        if \
        not self.isPlaceable(diagonals[0]) or not self.isPlaceable(diagonals[1]) or \
        not self.isPlaceable(diagonals[2]) or not self.isPlaceable(diagonals[3]):
            return False
        sides = self.adjacent_vertical_values(x,y)
        if board.values[x][y] != '~' or \
        not self.isPlaceable(sides[0]) or not self.isPlaceable(sides[1]):
            return False
        topAndBottom = self.adjacent_horizontal_values(x,y)    
        if \
        not self.isPlaceable(topAndBottom[0]) or not self.isPlaceable(topAndBottom[1]):
            return False
        return True

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
        for i in range(10):
            string_row[i] = string_row[i].rstrip('\r')
        """
        Le e cria a lista com os valores de cada coluna 
        """
        string_column = input()
        string_column = string_column.split('\t')
        string_column.remove("COLUMN")
        string_column = np.asarray(string_column)
        for i in range(10):
            string_column[i] = string_column[i].rstrip('\r')
        """
        Le as hints e comeca a preencher o tabuleiro
        """ 
        hints_n = input()
        hints_n = int(hints_n)
        hintsVec = []
        for x in range(hints_n):
            line = input()
            line = line.split('\t')
            #print(line)
            if line[3]=='C':
                boats[0] -= 1
            if line[3]!='W':
                string_row[int(line[1])] = int(string_row[int(line[1])]) -1
                string_column[int(line[2])] = int(string_column[int(line[2])]) -1
            if (line[3]!='C' and line[3]!='W'):
                currentHint = np.array([int(line[1]), int(line[2]), line[3]])   #cria vetor de hint
                hintsVec.append(currentHint)                                    #adiciona vetor a lista de hints
            values[int(line[1]), int(line[2])] = line[3]                        #adiciona hint ao tabuleiro
        
        hintsVec = np.asarray(hintsVec)
        key = [*range(11,19)] + [*range(21,29)] + [*range(31,39)] + [*range(41,49)] + [*range(51,59)] + [*range(61,69)] + [*range(71,79)] +[*range(81,89)]
        valuesD = range(64)
        free = dict(zip(key,valuesD))
        okey = [*range(0,10)] + [10,19,20,29,30,39,40,49,50,59,60,69,70,79,80,89] + [*range(90,100)]
        valuesD1 = range(36)
        ofree = dict(zip(okey,valuesD1))
        board = Board(string_row, string_column, values, np.asarray(boats), hintsVec, free, ofree)
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
        bottomPiece = self.getPiece(x,y,board)
        topPiece = self.getPiece(x-1,y,board)
        if (bottomPiece=='m') and (topPiece=='m'):
            return True
        if (bottomPiece=='b') and (topPiece=='t'):
            return True
        if (bottomPiece=='b') and (topPiece=='m'):
            return True
        if (bottomPiece=='m') and (topPiece=='t'):
            return True
        return False

    def horizontal(self,x,y,board):
        leftPiece = self.getPiece(x,y,board)
        rightPiece = self.getPiece(x,y+1,board)
        if (leftPiece=='m') and (rightPiece=='m'):
            return True
        if (leftPiece=='l') and (rightPiece=='r'):
            return True
        if (leftPiece=='l') and (rightPiece=='m'):
            return True
        if (leftPiece=='m') and (rightPiece=='r'):
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
    
    def replaceTilde(self):
        for i in range(10):
            for j in range(10):
                if self.values[i,j]=='~':
                    print(".", end="")
                else:
                    print(str(self.values[i][j]), end="")   #print de cada valor do tabuleiro
            print()                     #print dos valores de cada linha
    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        actions = [ ]
        # Vamos resolver primeiro as pistas
        if board.hints.size > 0:
            # Resolvemos uma pista e recebemos a lista de ações possíveis
            actions = self.solveHints(state)
        else: 
            size = self.maxSize(board)
            if size == 0:
                return []
            
            if size==1:
                toDelete = []
                for coord in board.free:
                        y = coord%10
                        x = coord//10
                        if board.values[x][y] != '~':
                            toDelete.append(x*10+y)
                            continue
                        elif int(board.columns[y])==0 or int(board.rows[x])==0:
                            board.values[x,y]='.'
                            toDelete.append(x*10+y)
                            continue
                        elif board.validPos(x,y):
                            actions.append(['C',x,y,size])
                        else:
                            toDelete.append(x*10+y)
                board.free = {key: value for key, value in board.free.items() if key not in toDelete}

                toDelete = []
                for coord in board.ofree:
                    x = coord//10
                    y = coord%10
                    if x==0:
                        if board.values[0][y] != '~':
                            toDelete.append(coord)
                        elif int(board.columns[y])==0 or int(board.rows[0])==0:
                            toDelete.append(coord)
                        elif board.validPos(0,y):
                            action = ['C',0,y,size]
                            actions.append(action)
                        else:
                            toDelete.append(coord)
                    elif x==9:
                        if board.values[9][y] != '~':
                            toDelete.append(coord)
                        elif int(board.columns[y])==0 or int(board.rows[9])==0:
                            toDelete.append(coord)
                            board.values[9,y]='.'
                        elif board.validPos(9,y):
                            action = ['C',9,y,size]
                            actions.append(action)
                        else:
                            toDelete.append(coord)
                    if y==0:
                        if board.values[x][0] != '~':
                            toDelete.append(coord)
                            pass
                        elif int(board.columns[0])==0 or int(board.rows[x])==0:
                            toDelete.append(coord)
                            board.values[x,0] = '.'
                        elif board.validPos(x,0):
                            action = ['C',x,0,size]
                            actions.append(action)
                        else:
                            toDelete.append(coord)
                    elif y==9:
                        if board.values[x][9] != '~':
                                toDelete.append(coord)
                                pass
                        elif int(board.columns[9])==0 or int(board.rows[x])==0:
                            toDelete.append(coord)
                            board.values[x,9] = '.'
                        elif board.validPos(x,9):
                            action = ['C',x,9,size]
                            actions.append(action)
                        else:
                            toDelete.append(coord)
                board.ofree = {key: value for key, value in board.ofree.items() if key not in toDelete}
            else:
                toDelete = []
                for coord in board.free:
                    x = coord//10
                    y = coord%10
                    if (x + size - 1) < 10 and int(board.columns[y]) - size >= 0 and self.tryVertical(x, y, size, board, toDelete):
                        actions.append(['V', x, y, size])
                    if (y + size - 1) < 10 and int(board.rows[x]) - size >= 0 and self.tryHorizontal(x, y, size, board, toDelete):
                        actions.append(['H', x, y, size])
                board.free = {key: value for key, value in board.free.items() if key not in toDelete}

                toDelete = []
                order = sorted(board.ofree.keys(), key=lambda x: 90-(x%10*100))
                
                for coord in order:
                    x = coord//10
                    y = coord%10
                    if y==9:
                        if board.values[x][9] != '~':
                            toDelete.append(coord)
                        else:
                            if (x+size-1)<10 and int(board.columns[9]) - size >= 0 and self.tryVertical(x,9,size,board, toDelete):
                                action = ['V',x,9,size]
                                actions.append(action)
                                
                            if (9+size-1)<10 and int(board.rows[x]) - size >= 0 and self.tryHorizontal(x,9,size,board, toDelete):
                                action = ['H',x,9,size]
                                actions.append(action)
                            
                    elif y==0:
                        if board.values[x][0] != '~':
                            toDelete.append(coord)
                        else:
                            if (x+size-1)<10 and int(board.columns[0]) - size >= 0 and self.tryVertical(x,0,size,board, toDelete):
                                action = ['V',x,0,size]
                                actions.append(action)
                            
                            if (0+size-1)<10 and int(board.rows[x]) - size >= 0 and self.tryHorizontal(x,0,size,board, toDelete):
                                action = ['H',x,0,size]
                                actions.append(action)
                    if x==9:
                        if board.values[9][y] != '~':
                            toDelete.append(coord)
                        else:
                            if (9+size-1)<10 and int(board.columns[y]) - size >= 0 and self.tryVertical(9,y,size,board, toDelete):
                                action = ['V',9,y,size]
                                actions.append(action)
                            if (y+size-1)<10 and int(board.rows[9]) - size >= 0 and self.tryHorizontal(9,y,size,board, toDelete):
                                action = ['H',9,y,size]
                                actions.append(action)

                    elif x==0:
                        if board.values[0][y] != '~':
                            toDelete.append(coord)
                        else:
                            if (0+size-1)<10 and int(board.columns[y]) - size >= 0 and self.tryVertical(0,y,size,board, toDelete):
                                action = ['V',0,y,size]
                                actions.append(action)
                            if (y+size-1)<10 and int(board.rows[0]) - size >= 0 and self.tryHorizontal(0,y,size,board, toDelete):
                                action = ['H',0,y,size]
                                actions.append(action)
                    
                board.ofree = {key: value for key, value in board.ofree.items() if key not in toDelete}
        return reversed(actions)

    def sorter(self, action):
        return abs(50 - int(action[1])*10 - int(action[2]))
    
    def isPlaceable(self,piece):
        return piece=='W' or piece=='~' or piece=='.'

    def tryVertical(self,x,y,size,board,toDelete):
        for i in range(size):
            if int(board.rows[x+i]) == 0:
                toDelete.append((x+i)*10+y)
                return False
            if not board.validPos(x+i,y):
                toDelete.append((x+i)*10+y)
                return False
        
        return True
    
    def tryHorizontal(self,x,y,size,board,toDelete):
        for i in range(size):
            if int(board.columns[y+i]) == 0:
                toDelete.append(x*10+y+i)
                return False
            if not board.validPos(x,y+i):
                toDelete.append(x*10+y+i)
                return False
        return True
    
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
        free = dict(state.board.free)
        #hints = np.copy(state.board.hints)
        ofree = dict(state.board.ofree)
        direction = action[0]                           # H (horizontal), V (vertical)
        x = int(action[1])                              #action = (direction, x, y, size)
        y = int(action[2])
        size = int(action[3])

        if (direction=='V'):                            #se a direcao for vertical
            pieces = 0
            if (board[x, y]=='~'):                      #se a posicao for vazia
                rows[x] = int(rows[x]) - 1              #diminui o valor da row
                pieces+= 1        #diminui o valor da collumn
                board[x, y] = 't'                       #adiciona um top

            for i in range(1, size-1):
                if (board[x+i, y]=='~'):
                    rows[x+i] = int(rows[x+i]) - 1
                    pieces+=1
                    board[x+i, y]='m'                   #adiciona um middle

            if (board[x+size-1, y]=='~'):
                rows[x+size-1] = int(rows[x+size-1]) - 1
                pieces+=1
                board[x+size-1, y]='b'                  #adiciona um bottom
            columns[y] = int(columns[y]) - pieces
        elif (direction=='H'):                            #se a direcao for vertical
            pieces=0
            if (board[x, y]=='~'):                      #se a posicao for vazia
                pieces+=1             #diminui o valor da row
                columns[y] = int(columns[y]) - 1        #diminui o valor da collumn
                board[x, y] = 'l'                       #adiciona um top

            for i in range(1, size-1):
                if (board[x, y+i]=='~'):
                    pieces+=1
                    columns[y+i] = int(columns[y+i]) - 1
                    board[x, y+i]='m'                   #adiciona um middle

            if (board[x, y+size-1]=='~'):
                pieces+=1 
                columns[y+size-1] = int(columns[y+size-1]) - 1
                board[x, y+size-1]='r'                  #adiciona um bottom
            rows[x] = int(rows[x]) - pieces

        elif (direction=='C'):
            board[x,y] = 'c'
            rows[x] = int(rows[x]) - 1
            columns[y] = int(columns[y]) - 1
            if x*10 + y in free:
                del free[x*10+y]
            elif x*10+y in ofree:
                del ofree[x*10+y]
        boats[size-1] -= 1                              #retira o barco que foi metido

        hints = []
        if not (state.board.hints.size==0):                          #atualiza o vetor das hints
            for hint in state.board.hints:
                condition = False
                for i in range(size):
                    if direction=='V' and hint[0] == str(x+i) and hint[1] == str(y): 
                        condition = True
                    if direction=='H' and hint[0] == str(x) and hint[1] == str(y+i): 
                        condition = True
                if not condition:
                    hints.append(hint)
        newBoard = Board(rows, columns, board, boats, np.asarray(hints), free, ofree)
        newState = BimaruState(newBoard)
        return newState

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        return np.all(state.board.columns == '0') and np.all(state.board.rows == '0') and np.all(state.board.boats == 0)

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return 1
        pass

    def p(self, board):
        """
        Calcula a matriz P
        """
        for i in range(10):
            for  j in range(10):
                count = board.countNeighbours(i,j,board.values)
                if (count >= 2):
                    return False
        return True

    def boatFits(self, x, y, piece, size, board):
        condition = True
        oldPieces = np.full(shape=4,fill_value="~")
        # Verifica se o tabuleiro esta apto para receber o navio
        if (piece == 'T' ) and (x+size-1<10) and \
            (board.values[x+size-1][y] == 'B' or (board.values[x+size-1][y] == '~' and \
                                                  int(board.rows[x+size-1]) > 0)):
            # Inicializa as pecas antigas com as pecas nas posicoes atuais do tabuleiro
            oldPieces[0] = piece
            oldPieces[1] = board.values[x+1,y]
            oldPieces[2] = '~'
            oldPieces[3] = '~'

            # Se o tabuleiro permitir, adicionamos a peca duas rows abaixo
            if (x+2<10):
                oldPieces[2] = board.values[x+2,y]
            # A mesma coisa para tres rows abaixo
            if (x+3<10):
                oldPieces[3] = board.values[x+3,y]
            
            # Vamos ver quantas pecas temos que por
            pieces = size-1

            # Se ja estiver la uma peca, nao a adicionamos
            if (board.values[x+size-1][y] == 'B'):
                pieces-=1

            # Verifica se as posicoes que estao entre as pontas sao vazias ou meios e se podemos por
            # a peca sem quebrar as pistas laterais
            for i in range(1,size-1):
                # Caso ja la esteja uma peca, nao contamos como peca adicional
                if board.values[x+i][y] == 'M':
                    pieces-=1
                # Se a posicao nao for vazia, nao podemos por la uma peca
                elif board.values[x+i][y] != '~':
                    condition = False
                elif int(board.rows[x+i])<1:
                    # A posicao esta vazia mas nao cabe la uma peca
                    condition = False
                    #TODO meter agua na row toda
                    oldPieces[i] = '.'
                # No tabuleiro fica um middle
                board.values[x+i][y] = 'm'

            board.values[x+size-1][y] = 'b'

            # Vamos ver se ainda podemos por as peças necessárias
            if (int(board.columns[y])-pieces<0):
                condition = False

            # Se não der, temos que repor o tabuleiro e retornar Falso (o barco não cabe)
            if not condition:
                board.values[x+1][y] = oldPieces[1]
                if (x+2<10):
                    board.values[x+2][y] = oldPieces[2]
                if (x+3<10):
                    board.values[x+3][y] = oldPieces[3]
                return False

            # Só temos de verificar se a matriz P o permite
            result = self.p(board)

            # Antes de mais, temos que repor o tabuleiro, após testarmos a matriz P
            board.values[x+1][y] = oldPieces[1]
            if (x+2<10):
                board.values[x+2][y] = oldPieces[2]
            if (x+3<10):
                board.values[x+3][y] = oldPieces[3]

            #Então devolvemos se a matriz permite ou não
            return result  
        
        if (piece == 'B' ) and (x-size+1>=0) and \
            (board.values[x-size+1][y] == 'T' or (board.values[x-size+1][y] == '~'  and \
                                                  int(board.rows[x-size+1]) > 0)):
            # Inicializa as peças antigas com as peças nas posições atuais do tabuleiro
            oldPieces[0] = piece
            oldPieces[1] = board.values[x-1][y]
            oldPieces[2] = '~'
            oldPieces[3] = '~'
            if (x-2>=0):
                oldPieces[2] = board.values[x-2][y]
            if (x-3>=0):
                oldPieces[3] = board.values[x-3][y]

            pieces = size - 1
            if (board.values[x-size+1][y] == 'T'):
                pieces-=1
            
            # Verifica se as posiões que estão entre as pontas são vazias ou meios e se podemos por
            # a peça sem quebrar as pistas laterais
            for i in range(1,size-1):
                if board.values[x-i][y] == 'M':
                    pieces-=1
                elif board.values[x-i][y] != '~':
                    condition = False
                elif int(board.rows[x-i])<1:
                    #Se a peça não poder ser posta por restrições laterais, então pomos uma água
                    #lá, para evitar procuras desnecessárias
                    condition = False
                    #TODO meter agua na row toda
                    oldPieces[i] = '.'
                board.values[x-i][y] = 'm'

            board.values[x-size+1][y] = 't'
            
            # Vamos ver se ainda podemos por as peças necessárias
            if (int(board.columns[y])-pieces<0):
                condition = False

            # Se não der, temos que repor o tabuleiro e retornar Falso (o barco não cabe)
            if not condition:
                if (x-2>=0):
                    board.values[x-2][y] = oldPieces[2]
                if (x-3>=0):
                    board.values[x-3][y] = oldPieces[3]

                board.values[x-1][y] = oldPieces[1]
                
                #board.printBoard()
                return False

            # Só temos de verificar se a matriz P o permite
            result = self.p(board)

            # Antes de mais, temos que repor o tabuleiro, após testarmos a matriz P
            if (x-2>=0):
                    board.values[x-2][y] = oldPieces[2]
            if (x-3>=0):
                board.values[x-3][y] = oldPieces[3]

            board.values[x-1][y] = oldPieces[1]

            #Então devolvemos se a matriz permite ou não
            return result 

        if (piece == 'L' ) and (y+size-1<10) and \
            (board.values[x][y+size-1] == 'R' or (board.values[x][y+size-1] == '~'  and \
                                                  int(board.columns[y+size-1]) > 0)):
            # Inicializa as peças antigas com as peças nas posições atuais do tabuleiro
            oldPieces[0] = piece
            oldPieces[1] = board.values[x][y+1]
            oldPieces[2] = '~'
            oldPieces[3] = '~'

            if (y+2<10):
                oldPieces[2] = board.values[x][y+2]
            if (y+3<10):
                oldPieces[3] = board.values[x][y+3]

            pieces = size - 1
            if (board.values[x][y+size-1] == 'R'):
                pieces-=1

            # Verifica se as posiões que estão entre as pontas são vazias ou meios e se podemos por
            # a peça sem quebrar as pistas laterais
            for i in range(1,size-1):
                if board.values[x][y+i] == 'M':
                    pieces -= 1
                elif board.values[x][y+i] != '~':
                    condition = False
                elif int(board.columns[y+i])<1:
                    #Se a peça não poder ser posta por restrições laterais, então pomos uma água
                    #lá, para evitar procuras desnecessárias
                    condition = False
                    oldPieces[i] = '.'
                board.values[x][y+i] = 'm'

            board.values[x][y+size-1] = 'r'

            if (int(board.rows[x])-pieces<0):
                condition = False

            # Se não der, temos que repor o tabuleiro e retornar Falso (o barco não cabe)
            if not condition:
                if (y+2<10):
                    board.values[x][y+2] = oldPieces[2]
                if (y+3<10):
                    board.values[x][y+3] = oldPieces[3]

                board.values[x][y+1] = oldPieces[1]
                #board.printBoard()
                return False

            # Só temos de verificar se a matriz P o permite
            result = self.p(board)

            # Antes de mais, temos que repor o tabuleiro, após testarmos a matriz P
            if (y+2<10):
                board.values[x][y+2] = oldPieces[2]
            if (y+3<10):
                board.values[x][y+3] = oldPieces[3]

            board.values[x][y+1] = oldPieces[1]

            #Então devolvemos se a matriz permite ou não
            return result  
        
        if (piece == 'R' ) and (y-size+1>=0) and \
            (board.values[x][y-size+1] == 'L' or (board.values[x][y-size+1] == '~' and \
                                                  int(board.columns[y-size+1]) > 0)):
            # Inicializa as peças antigas com as peças nas posições atuais do tabuleiro
            oldPieces[0] = piece
            oldPieces[1] = board.values[x][y-1]
            oldPieces[2] = '~'
            oldPieces[3] = '~'

            if (y-2>=0):
                oldPieces[2] = board.values[x][y-2]
            if (y-3>=0):
                oldPieces[3] = board.values[x][y-3]

            pieces = size - 1

            if board.values[x][y-size+1] == 'L':
                pieces -= 1
            # Verifica se as posiões que estão entre as pontas são vazias ou meios e se podemos por
            # a peça sem quebrar as pistas laterais
            for i in range(1,size-1):
                if board.values[x][y-i] == 'M':
                    pieces -= 1
                elif board.values[x][y-i] != '~':
                    condition = False
                elif int(board.columns[y-i])<1:
                    #Se a peça não poder ser posta por restrições laterais, então pomos uma água
                    #lá, para evitar procuras desnecessárias
                    condition = False
                    #TODO meter agua na row toda
                    oldPieces[i] = '.'
                board.values[x][y-i] = 'm'

            board.values[x][y-size+1] = 'l'

            if ((int(board.rows[x])-pieces<0) ):
                condition = False
            # Se não der, temos que repor o tabuleiro e retornar Falso (o barco não cabe)
            if not condition:
                board.values[x][y-1] = oldPieces[1]
                if (y-2>=0):
                    board.values[x][y-2] = oldPieces[2]
                if (y-3>=0):
                    board.values[x][y-3] = oldPieces[3]
                
                #board.printBoard()
                return False

            # Só temos de verificar se a matriz P o permite
            result = self.p(board)

            # Antes de mais, temos que repor o tabuleiro, após testarmos a matriz P
            board.values[x][y-1] = oldPieces[1]
            if (y-2>=0):
                board.values[x][y-2] = oldPieces[2]
            if (y-3>=0):
                board.values[x][y-3] = oldPieces[3]

            #Então devolvemos se a matriz permite ou não
            return result 

    def tryTop(self, hint, board):
        x = hint[0]
        y = hint[1]
        piece = hint[2].rstrip("\r")
        possibilities = []
        for i in range(2,5):             #verifica o maior size de boat que podemos meter
            if (board.boats[i-1] > 0 and self.boatFits(int(x),int(y),piece,i,board) ):
                possibility = np.full(shape=4,fill_value="~")
                possibility[0] = 'V'                        #vertical
                possibility[1] = hint[0]
                possibility[2] = hint[1]
                possibility[3] = i
                possibilities.append(possibility)
        return np.asarray(possibilities)
    
    def tryBottom(self, hint, board):
        x = hint[0]
        y = hint[1]
        piece = hint[2].rstrip("\r")
        possibilities = []
        for i in range(1,5):             #verifica o maior size de boat que podemos meter
            if (board.boats[i-1] > 0 and self.boatFits(int(x),int(y),piece,i,board)):
                possibility = np.full(shape=4,fill_value="~")
                possibility[0] = 'V'                        #vertical
                possibility[1] = int(hint[0]) - i +1 #pode ser -4+2=-3 ou seja no maximo vai ter 3 para cima
                possibility[2] = hint[1]
                possibility[3] = i
                possibilities.append(possibility)
        return np.asarray(possibilities)

    def tryLeft(self, hint, board):
        x = hint[0]
        y = hint[1]
        piece = hint[2].rstrip("\r")
        possibilities = []
        for i in range(1,5):             #verifica o maior size de boat que podemos meter
            if (board.boats[i-1] > 0 and self.boatFits(int(x),int(y),piece,i, board)):
                possibility = np.full(shape=4,fill_value="~")
                possibility[0] = 'H'                        #horizontal
                possibility[1] = hint[0]
                possibility[2] = hint[1]
                possibility[3] = i
                possibilities.append(possibility)
        return np.asarray(possibilities)
    
    def tryRight(self, hint, board):
        x = hint[0]
        y = hint[1]
        piece = hint[2].rstrip("\r")
        possibilities = []
        for i in range(1,5):             #verifica o maior size de boat que podemos meter
            if (board.boats[i-1] > 0 and self.boatFits(int(x),int(y),piece,i,board)):
                possibility = np.full(shape=4,fill_value="~")
                possibility[0] = 'H'                        #vertical
                possibility[1] = hint[0]
                possibility[2] = int(hint[1]) - i +1 #pode ser -4+2=-3 ou seja no maximo vai ter 3 para a esquerda
                possibility[3] = i
                possibilities.append(possibility)
        return np.asarray(possibilities)

    def tryMiddle(self, hint, board):
        x = int(hint[0])
        y = int(hint[1])
        actions = []
        # Vamos começar por testar na horizontal esta forma: lMmr
        if (y-1>=0) and (y+2<10) and board.boats[3] > 0:
            pieces = 3
            condition = True

            # Vemos se as peças ao lado estao bem postas
            if (board.values[x][y-1]=='L'):
                pieces -= 1
            elif board.values[x][y-1]!='~':
                condition = False
            elif int(board.columns[y-1])==0:
                condition = False

            if (board.values[x][y+1]=='M'):
                pieces -= 1
            elif board.values[x][y+1]!='~':
                condition = False
            elif int(board.columns[y+1])==0:
                condition = False

            if (board.values[x][y+2]=='R'):
                pieces -= 1
            elif board.values[x][y+2]!='~':
                condition = False
            elif int(board.columns[y+2])==0:
                condition = False
            
            # Se estiver tudo bem, entao podemos começar
            if (int(board.rows[x])-pieces>=0) and condition:
                oldPieces = []
                oldPieces.append(board.values[x][y-1])
                oldPieces.append(board.values[x][y])
                oldPieces.append(board.values[x][y+1])
                oldPieces.append(board.values[x][y+2])
                board.values[x][y-1] = 'l'
                board.values[x][y+1] = 'm'
                board.values[x][y+2] = 'r'
                if self.p(board):
                    action = ['H', x, y-1, 4]
                    actions.append(action)
                # Repor  o tabuleiro  
                board.values[x][y-1] = oldPieces[0]
                board.values[x][y+1] = oldPieces[2]
                board.values[x][y+2] = oldPieces[3]

        #lmMr
        if (y-2>=0) and (y+1<10) and board.boats[3] > 0:
            pieces = 3
            condition = True

            # Vemos se as peças ao lado estao bem postas
            if (board.values[x][y-2]=='L'):
                pieces -= 1
            elif board.values[x][y-2]!='~':
                condition = False
            elif int(board.columns[y-2])==0:
                condition = False

            if (board.values[x][y-1]=='M'):
                pieces -= 1
            elif board.values[x][y-1]!='~':
                condition = False
            elif int(board.columns[y-1])==0:
                condition = False

            if (board.values[x][y+1]=='R'):
                pieces -= 1
            elif board.values[x][y+1]!='~':
                condition = False
            elif int(board.columns[y+1])==0:
                condition = False
            
            # Se estiver tudo bem, entao podemos começar
            if (int(board.rows[x])-pieces>=0) and condition:
                oldPieces = []
                oldPieces.append(board.values[x][y-2])
                oldPieces.append(board.values[x][y-1])
                oldPieces.append(board.values[x][y])
                oldPieces.append(board.values[x][y+1])
                board.values[x][y-2] = 'l'
                board.values[x][y-1] = 'm'
                board.values[x][y+1] = 'r'
                if self.p(board):
                    action = ['H', x, y-2, 4]
                    actions.append(action)
                # Repor  o tabuleiro  
                board.values[x][y-2] = oldPieces[0]
                board.values[x][y-1] = oldPieces[1]
                board.values[x][y+1] = oldPieces[3]
        
        # Testar agora lMr
        if (y-1>=0) and (y+1<10) and board.boats[2] > 0:
            pieces = 2
            condition = True

            # Vemos se as peças ao lado estao bem postas
            if (board.values[x][y-1]=='L'):
                pieces -= 1
            elif board.values[x][y-1]!='~':
                condition = False
            elif int(board.columns[y-1])==0:
                condition = False

            if (board.values[x][y+1]=='R'):
                pieces -= 1
            elif board.values[x][y+1]!='~':
                condition = False
            elif int(board.columns[y+1])==0:
                condition = False
            
            # Se estiver tudo bem, entao podemos começar
            if (int(board.rows[x])-pieces>=0) and condition:
                oldPieces = []
                oldPieces.append(board.values[x][y-1])
                oldPieces.append(board.values[x][y])
                oldPieces.append(board.values[x][y+1])
                board.values[x][y-1] = 'l'
                board.values[x][y+1] = 'r'
                if self.p(board):
                    action = ['H', x, y-1, 3]
                    actions.append(action)
                # Repor  o tabuleiro  
                board.values[x][y-1] = oldPieces[0]
                board.values[x][y+1] = oldPieces[2]

        #VERTICAL WISE
        # Vamos começar por testar na vertical esta forma: tMmb
        if (x-1>=0) and (x+2<10) and board.boats[3] > 0:
            pieces = 3
            condition = True

            # Vemos se as peças ao lado estao bem postas
            if (board.values[x-1][y]=='T'):
                pieces -= 1
            elif board.values[x-1][y]!='~':
                condition = False
            elif int(board.rows[x-1])==0:
                condition = False

            if (board.values[x+1][y]=='M'):
                pieces -= 1
            elif board.values[x+1][y]!='~':
                condition = False
            elif int(board.rows[x+1])==0:
                condition = False

            if (board.values[x+2][y]=='B'):
                pieces -= 1
            elif board.values[x+2][y]!='~':
                condition = False
            elif int(board.rows[x+2])==0:
                condition = False
            
            # Se estiver tudo bem, entao podemos começar
            if (int(board.columns[y])-pieces>=0) and condition:
                oldPieces = []
                oldPieces.append(board.values[x-1][y])
                oldPieces.append(board.values[x][y])
                oldPieces.append(board.values[x+1][y])
                oldPieces.append(board.values[x+2][y])
                board.values[x-1][y] = 't'
                board.values[x+1][y] = 'm'
                board.values[x+2][y] = 'b'
                if self.p(board):
                    action = ['V', x-1, y, 4]
                    actions.append(action)
                # Repor  o tabuleiro  
                board.values[x-1][y] = oldPieces[0]
                board.values[x+1][y] = oldPieces[2]
                board.values[x+2][y] = oldPieces[3]

        #tmMb
        if (x-2>=0) and (x+1<10) and board.boats[3] > 0:
            pieces = 3
            condition = True

            # Vemos se as peças ao lado estao bem postas
            if (board.values[x-2][y]=='T'):
                pieces -= 1
            elif board.values[x-2][y]!='~':
                condition = False
            elif int(board.rows[x-2])==0:
                condition = False

            if (board.values[x-1][y]=='M'):
                pieces -= 1
            elif board.values[x-1][y]!='~':
                condition = False
            elif int(board.rows[x-1])==0:
                condition = False

            if (board.values[x+1][y]=='B'):
                pieces -= 1
            elif board.values[x+1][y]!='~':
                condition = False
            elif int(board.rows[x+1])==0:
                condition = False
            
            # Se estiver tudo bem, entao podemos começar
            if (int(board.columns[y])-pieces>=0) and condition:
                oldPieces = []
                oldPieces.append(board.values[x-2][y])
                oldPieces.append(board.values[x-1][y])
                oldPieces.append(board.values[x][y])
                oldPieces.append(board.values[x+1][y])
                board.values[x-2][y] = 't'
                board.values[x-1][y] = 'm'
                board.values[x+1][y] = 'b'
                if self.p(board):
                    action = ['V', x-2, y, 4]
                    actions.append(action)
                # Repor  o tabuleiro  
                board.values[x-2][y] = oldPieces[0]
                board.values[x-1][y] = oldPieces[1]
                board.values[x+1][y] = oldPieces[3]
        
        # Testar agora tMb
        if (x-1>=0) and (x+1<10) and board.boats[2] > 0:
            pieces = 2
            condition = True

            # Vemos se as peças ao lado estao bem postas
            if (board.values[x-1][y]=='T'):
                pieces -= 1
            elif board.values[x-1][y]!='~':
                condition = False
            elif int(board.rows[x-1])==0:
                condition = False

            if (board.values[x+1][y]=='B'):
                pieces -= 1
            elif board.values[x+1][y]!='~':
                condition = False
            elif int(board.rows[x+1])==0:
                condition = False
            
            # Se estiver tudo bem, entao podemos começar
            if (int(board.columns[y])-pieces>=0) and condition:
                oldPieces = []
                oldPieces.append(board.values[x-1][y])
                oldPieces.append(board.values[x][y])
                oldPieces.append(board.values[x+1][y])
                board.values[x-1][y] = 't'
                board.values[x+1][y] = 'b'
                if self.p(board):
                    action = ['V', x-1, y, 3]
                    actions.append(action)
                # Repor  o tabuleiro  
                board.values[x-1][y] = oldPieces[0]
                board.values[x+1][y] = oldPieces[2]

        return np.asarray(actions)
        
    def solveHints(self, state):
        hint = state.board.hints[0]
        if hint[2].rstrip("\r")=='T':
            return self.tryTop(hint, state.board)
                
        elif hint[2].rstrip("\r")=='B':            #termos que contar x-size para dar apenas o top
            return self.tryBottom(hint, state.board)
        
        elif hint[2].rstrip("\r")=='R':
            return self.tryRight(hint, state.board)
        
        elif hint[2].rstrip("\r")=='L':            #termos que contar y+size para dar apenas o right
            return self.tryLeft(hint, state.board)

        elif hint[2].rstrip("\r")=='M':
            return self.tryMiddle(hint, state.board)
        
    def maxSize(self,board):
        i = 3
        while i>=0:
            if board.boats[i]>0:
                return i+1
            i-=1
        return i
    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    problem = Bimaru(board)
    result = depth_first_tree_search(problem)
    result.state.board.replaceTilde()
    pass