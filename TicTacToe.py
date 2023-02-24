"""
Student info: Sina Omidvar (992023003)
Course info: Artificial Intelligence at Kharazmi University
Instructor: M.M. Pedram
TA: Mahsa Arabi & Alireza Habibi
Title: Project 3
"""
# Tic_Tac_Toe game
# Using Minimax algorithm and alpha beta pruning
# Player vs AI and AI vs AI
# Heuristic function is implemented
# Two difficulties, beatable and unbeatable


from random import choice
from math import inf

# Global properties

board = [[0, 0, 0],

         [0, 0, 0],

         [0, 0, 0]]


moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],

         4: [1, 0], 5: [1, 1], 6: [1, 2],

         7: [2, 0], 8: [2, 1], 9: [2, 2]}

chars = {1: 'X', -1: 'O', 0: ' '}


def printBoard(board):

    for x in board:

        for y in x:

            ch = chars[y]

            print(f'| {ch} |', end='')

        print('\n' + '---------------')

    print('===============')


def winningPlayer(borad, player):

    conditions = [[board[0][0], board[0][1], board[0][2]],

                  [board[1][0], board[1][1], board[1][2]],

                  [board[2][0], board[2][1], board[2][2]],

                  [board[0][0], board[1][0], board[2][0]],

                  [board[0][1], board[1][1], board[2][1]],

                  [board[0][2], board[1][2], board[2][2]],

                  [board[0][0], board[1][1], board[2][2]],

                  [board[0][2], board[1][1], board[2][0]]]

    if [player, player, player] in conditions:

        return True

    return False


def gameWon(board):

    return winningPlayer(board, 1) or winningPlayer(board, -1)


def printResult(board):

    if winningPlayer(board, 1):

        print('X won! ' + '\n')

    elif winningPlayer(board, -1):

        print('O won! ' + '\n')

    else:

        print('Draw' + '\n')


def emptyBlocks(board):

    blank = []

    for x, row in enumerate(board):

        for y, col in enumerate(row):

            if board[x][y] == 0:

                blank.append([x, y])

    return blank


def boardFull(board):

    if len(emptyBlocks(board)) == 0:

        return True

    return False


def setMove(board, x, y, player):

    board[x][y] = player


# Player Turn

def playerMove(board):

    # User Prompt

    while True:
        try:

            move = int(input('Enter a number between 1-9: '))

            if move < 1 or move > 9:

                print('Invalid Move! Try again!')

            elif not (moves[move] in emptyBlocks(board)):

                print('Invalid Move! Try again!')
            else:

                setMove(board, moves[move][0], moves[move][1], 1)

                printBoard(board)

                break

        except (KeyError, ValueError):

            print('Enter a number!')

# Heuristic


def evaluate(board):

    conditions = [[board[0][0], board[0][1], board[0][2]],

                  [board[1][0], board[1][1], board[1][2]],

                  [board[2][0], board[2][1], board[2][2]],

                  [board[0][0], board[1][0], board[2][0]],

                  [board[0][1], board[1][1], board[2][1]],

                  [board[0][2], board[1][2], board[2][2]],

                  [board[0][0], board[1][1], board[2][2]],

                  [board[0][2], board[1][1], board[2][0]]]

    X = 0
    O = 0

    for con in conditions:

        for i in con:

            if not (i == 0 or i == 1):

                break

        else:

            X = X + 1

        for j in con:

            if not (j == 0 or j == -1):

                break

        else:

            O = O + 1

    return X - O

# Utility function


def getScore(board):

    if winningPlayer(board, 1):

        return 1

    elif winningPlayer(board, -1):

        return -1

    else:

        return 0

# Algorithm


def abminimax(board, depth, alpha, beta, player):

    # Returning values for best action

    row = -1

    col = -1

    # Base Case

    if gameWon(board):

        return [row, col, getScore(board)]

    elif depth == 0:

        return [row, col, evaluate(board)]

    # Child generation

    for cell in emptyBlocks(board):

        setMove(board, cell[0], cell[1], player)

        score = abminimax(board, depth - 1, alpha, beta, -player)

        if player == 1:

            # X is always the max player

            if score[2] > alpha:

                alpha = score[2]

                row = cell[0]
                col = cell[1]

        else:

            # O is always the min player

            if score[2] < beta:

                beta = score[2]

                row = cell[0]
                col = cell[1]

        # Backtracking

        setMove(board, cell[0], cell[1], 0)

        # Pruning if possible

        if alpha >= beta:
            break

    # Returning

    if player == 1:

        return [row, col, alpha]
    else:

        return [row, col, beta]

# Call algorithm


def play(board, player, z):

    result = abminimax(board, len(emptyBlocks(board)) - z, -inf, inf, player)

    setMove(board, result[0], result[1], player)

    printBoard(board)


def makeMove(board, player, mode, z):

    # Player vs AI
    if mode == 1:

        if player == 1:

            playerMove(board)
        else:

            play(board, -1, z)
    # AI vs AI
    else:

        if player == 1:

            play(board, 1, z)
        else:

            play(board, -1, z)


def menu(board):

    # User Prompt

    while True:
        try:

            command = int(input('AI vs AI or Player vs AI, [1/2]: '))

            if not (command == 1 or command == 2):

                print('Please pick 1 or 2')
            else:

                break

        except (KeyError, ValueError):

            print('Enter a number')

    # AI vs AI

    if command == 1:

        # Random Move

        x = choice([0, 1, 2])

        y = choice([0, 1, 2])

        setMove(board, x, y, -1)

        printBoard(board)

        # Play turn by turn

        currentPlayer = 1

        while not (boardFull(board) or gameWon(board)):

            makeMove(board, currentPlayer, 0, 0)

            currentPlayer *= -1

    # Player vs AI
    else:

        # User Prompt

        while True:
            try:

                order = int(input('Enter to play 1st or 2nd, [1/2]: '))

                if not (order == 1 or order == 2):

                    print('Please pick 1 or 2')
                else:

                    break
            except (KeyError, ValueError):

                print('Enter a number')

        while True:
            try:

                diff = int(
                    input('Difficulty: beatable or unbeatable ?, [1/2]: '))

                if not (diff == 1 or diff == 2):

                    print('Please pick 1 or 2')
                else:

                    break
            except (KeyError, ValueError):

                print('Enter a number')

        currentPlayer = 1
        z = 0

        # Second Order

        if order == 2:
            currentPlayer = -1

        # Beatable

        if diff == 1:
            z = 8

        # Play turn by turn

        while not (boardFull(board) or gameWon(board)):

            makeMove(board, currentPlayer, 1, z)

            currentPlayer *= -1

            # Reduce scope
            if z > 0:
                z = z - 1

    printResult(board)


print("========")

print("   XO   ")

print("========")

menu(board)
