import os
import numpy as np
from collections import defaultdict, deque

clear = lambda: os.system('clear')

class Sudoku:
    def __init__(self, randomNumber):
        self.boardVersion = randomNumber
        self.board = [[0 for j in range(9)] for i in range(9)]
        self.cleanBoard = []
        self.mistakes = 0
        self.correct = 0
        self.score = 0
        self.missing = 81
        self.streak = 0

    def generateBoard(self):
        open("boards.txt", "r")
        copying = False
        r = 0
        c = 0

        with open("boards.txt") as file:
            for line in file:
                if copying == True:
                    for number in line:
                        if number.isdigit():
                            self.board[r][c] = int(number)
                            if int(number) > 0:
                                self.missing -= 1
                            c+= 1
                elif "Grid" in line and int(line[-2]) == self.boardVersion:
                    copying = True
                    #Offset r += 1 or else the copying won't work correctly.
                    r-=1
                if copying == True:
                    r += 1
                if r == 9:
                    break
                c = 0
        
        self.cleanBoard = np.copy(self.board)
        

    #This solution I came up with myself.
    def checkValid(self):
        #check each row to see if it repeats
        #check each column as well
        for row in self.board:
            print(row)
        repeat = 0
        repeatColumn = 0
        for i in range(9):
            for j in range(9):
                checkingRow = self.board[i][j]
                checkingColumn = self.board[j][i]
                for k in range(9):
                    if checkingRow == self.board[i][k] and checkingRow != 0:
                        repeat += 1
                        if repeat > 1:
                            return False
                    if checkingColumn == self.board[k][i] and checkingColumn != 0:
                        repeatColumn += 1
                        if repeatColumn > 1:
                            return False
                repeat = 0
                repeatColumn = 0
        #now check each matrix and see if there are any repeats
        #create 9 matrixes so we need 9 iteration
        jumpR = 0
        jumpC = 0
        for column in range(3):#handles matrix in the column
            jumpC = column*3
            for row in range(3):#handles matrix in the row
                jumpR = row*3
                matrix = []*9
                tempMap = {}
                for i in range(0+jumpR,3+jumpR): #handles the item in the row
                    for j in range(0+jumpC,3+jumpC): #handles the item in the column
                        matrix.append(self.board[i][j])
                for n in matrix:
                    if n not in tempMap:
                        tempMap[n] = 1
                    else:
                        if n != 0:
                            return False
        return True
    
    def getMistakes(self):
        return self.mistakes
    
    def updateBoard(self):
        count = 1
        print("******************* Mistakes: %d *********************" % self.getMistakes())
        print("_____________________________________________________")
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                if count == 9:
                    if self.board[row][column] == 0:
                        print(" ", " "," ")
                    else:
                        print(" ", self.board[row][column]," ")
                    print("_____________________________________________________")
                    count = 1
                else:
                    if self.board[row][column] == 0:
                        print(" ", " "," ", end = '')
                    else:
                        print(" ",self.board[row][column], " ", end = '')
                    print("|", end = '')
                    count += 1
        print()

    def displaySolution(self):
        clear()
        count = 1
        print("******************* Mistakes: %d *********************" % self.getMistakes())
        print("_____________________________________________________")
        for row in range(len(self.cleanBoard)):
            for column in range(len(self.cleanBoard[0])):
                if count == 9:
                    if self.cleanBoard[row][column] == 0:
                        print(" ", " "," ")
                    else:
                        print(" ", self.cleanBoard[row][column]," ")
                    print("_____________________________________________________")
                    count = 1
                else:
                    if self.cleanBoard[row][column] == 0:
                        print(" ", " "," ", end = '')
                    else:
                        print(" ",self.cleanBoard[row][column], " ", end = '')
                    print("|", end = '')
                    count += 1
        print()



    #This solution was taken from https://leetcode.com/problems/sudoku-solver/solutions/1417073/97-faster-clean-concise-well-explained/
    def getSolution(self):
        rows,cols,block,seen = defaultdict(set),defaultdict(set),defaultdict(set),deque([])
        for i in range(9):
            for j in range(9):
                if self.cleanBoard[i][j]!=0:
                    rows[i].add(self.cleanBoard[i][j])
                    cols[j].add(self.cleanBoard[i][j])
                    block[(i//3,j//3)].add(self.cleanBoard[i][j])
                else:
                    seen.append((i,j))
        
        def dfs():
            if not seen:
                return True
            
            r,c = seen[0]
            t = (r//3,c//3)
            for n in {1,2,3,4,5,6,7,8,9}:
                if n not in rows[r] and n not in cols[c] and n not in block[t]:
                    self.cleanBoard[r][c]=n
                    rows[r].add(n)
                    cols[c].add(n)
                    block[t].add(n)
                    seen.popleft()
                    if dfs():
                        return True
                    else:
                        self.cleanBoard[r][c]= 0
                        rows[r].discard(n)
                        cols[c].discard(n)
                        block[t].discard(n)
                        seen.appendleft((r,c))
            return False
        
        dfs()

    def getCorrectValue(self,row,column):
        return self.cleanBoard[row][column]
    
    def incrementMistake(self):
        self.mistakes += 1
        self.streak = 0

    def addValue(self,row,column,value):
        if self.board[row][column] == value:
            return
        self.board[row][column] = value
        self.correct += 1
        self.streak += 1
        
        if self.correct == 0:
            self.score = 100
        elif self.correct > 0:
            if self.correct < 2:
                self.score += 50*self.streak
            else:
                self.score *= 2
    
    def checkIfWin(self):
        if self.missing == 0:
            return True
        return False
    
    def getMissing(self):
        print(self.missing)

    def displayScore(self):
        print("You got %d correct" % self.correct)
        print("Score: %d" % self.score)



