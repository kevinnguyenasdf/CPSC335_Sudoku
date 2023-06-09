"""
Group: Brogrammers
Team Members: 
Adam Harb: adamharb1999@csu.fullerton.edu
Julio Villegas: julio_villegas@hotmail.com
Antionio Gonzalez:
Kevin Nguyen: lnguyen37@csu.fullerton.edu

Program name: Sudoku
Purpose: Contains the main function which uses the Sudoku class from Sudoku.py. 
Allows user to play Sudoku via the terminal.
"""

from Sudoku import Sudoku
import random
import os
clear = lambda: os.system('clear')

if __name__ == "__main__":
    rnjesus= random.randint(1,5)
    board = Sudoku(1)
    board.generateBoard()
    
    board.getSolution()
    update = True
    win = False

    while True:
        if board.getMistakes() == 3:
            break
        if board.checkIfWin():
            win = True
            break
        if update == True:
            clear()
            board.updateBoard()
            update = False
        print("Valid rows: 0-8")
        print("Valid columns: 0-8")
        val = input("Please enter a number, Format is: rc:# (example: 01:3 will assign a value of 3 to row 0 column 1): ")
        if(not val[0].isdigit() or not val[1].isdigit() or not val[3].isdigit()):
            print("Invalid please enter numbers in the correct format!")
            continue
        if(len(val) < 4 or len(val) > 4):
            print("Invalid! Please enter the correct amount of characters.")
            continue
        row = int(val[0])
        if(row < 0 or row > 8):
            print("Invalid entry for row! Please choose between 0-8")
            continue
        column = int(val[1])
        if(column < 0 or column > 8):
            print("Invalid entry for column! Please choose between 0-8")
            continue
        value = int(val[3])
        if(value < 1 or value > 9):
            print("Invalid entry for value! Please choose between 1-9")
            continue
        
        if value != board.getCorrectValue(row,column):
            board.incrementMistake()
        
        if value == board.getCorrectValue(row,column):
            board.addValue(row,column,value)
        
        update = True

    board.displaySolution()
    if win == True:
        print("Congrats You Won!")
    board.displayScore()

