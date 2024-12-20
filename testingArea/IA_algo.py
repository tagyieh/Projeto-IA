import numpy as np

def printBoard(board):
    for i in board:
        for j in i:
            print(j, end="")
        print()
"""
def getLeft(pos, board):
    x = pos[0]
    y = pos[1]
    if x>=0:
        return board[y][x]

def getRight(pos, board):
    x = pos[0]
    y = pos[1]
    if x<10:
        return board[y][x]

def getCenter(pos, board):
    x = pos[0]
    y = pos[1]
    return board[y][x]

def getDecision(left, right, center, board):
    # Completely possible position for a boat.
    # Allowed to grow even more
    if (left == '~' or left == '.' or left == 'W') and \
        (right == '~' or right == '.' or right == 'W') and \
        center == '~':
           return 1 
    # Possible position for a boat. Ends
    if (left == '~' or left == '.' or left == 'W') and \
        (right == '~' or right == '.' or right == 'W') and \
        (center == 'W' or center == '.') :
           return 2 
    # Diagonal bottom piece. Ends 
    if (left == 'B' or left == 'b' or left=='R' or left == 'r' or left=='l' or left=='L') or \
        (right == 'B' or right == 'b' or right=='R' or right == 'r' or right =='l' or right=='L') or \
        (center == 'B' or center == 'b' or center =='R' or center== 'r' or center=='l' or center=='L'):
            return 3
    # Diagonal top piece. Ends
    if ((left == 'T' or left == 't') or \
        (right == 'T' or right == 't')) and \
        (center == '~'):
            return 4
    # Central top piece. Ends
    if center == 'T' or center == 't':
        return 5
    # Diagonal center piece. Ends
    if (left=='C' or left=='c') or \
            (right=='C' or right=='c'):
        return 6
    return 9 
    
def decision5(count):
    if count==0:
        return [0,1,0,0]
    if count==1:
        return [0,0,1,0]
    if count==2:
        return [1,0,0,1]
    if count==3:
        return [1,1,0,0]
    if count==4:
        return [1,1,1,0]

def up(x, y, board):
    left = getLeft((x-1,y), board)
    right = getRight((x+1,y), board)
    center = getCenter((x,y), board)

def decideBoat(x, y, board):
    for i in range(2):
        up(x,y-1-i,board)

def findUp(board, pos):
    x = pos[0]
    boatPossibilities = [0] * 4
    # Count 5 lines above
    for count in range(5):
        y = pos[1] - 1 - count
        if y>=0:
            # Gives the value in the position upper left, above and upper right
            # from the original position
            left = getLeft((x-1,y), board)
            right = getRight((x+1,y), board)
            center = getCenter((x,y), board)
            decision = getDecision(left, right, center, board)
            if decision==1 and count != 4:
                boatPossibilities[count] = 1
            elif decision==2 and count != 4:
                boatPossibilities[count] = 1 
                break
            elif decision==3 and count != 4:
                break
            elif decision==4:
                if count-1>=0:
                    boatPossibilities[count-1]=0
                break
            elif decision==5:
                boatPossibilities = decision5(count)
                break
            elif decision==6 and (left=='c' or left=='C'):
                direction = decideBoat(x-1,y, board)
        else:
            break
    print(boatPossibilities)
"""

def idkYet(board):
    for i in range(10):
        for  j in range(10):
            count = countNeighbours(i,j,board)
            print(count,end='')
        print()

def getPiece(x,y,board):
    return board[x][y].lower()

def vertical(x,y,board):
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

def horizontal(x,y,board):
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

def countNeighbours(x,y,board):
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

if __name__ == '__main__':
    board = []
    for i in range(10):
        line = []
        for j in range(10):
            line.append("~")
        board.append(line)
    board[0][1] = 't'
    board[1][1] = 'B'
    board[3][1] = 'r'
    board[3][2] = 'c'
    board[3][3] = 'l'
    #board[6][6] = 't'
    #board[7][6] = 'c'
    #board[8][6] = 'c'
    #board[9][6] = 'B'
    printBoard(board)    
    idkYet(board)
    
  


