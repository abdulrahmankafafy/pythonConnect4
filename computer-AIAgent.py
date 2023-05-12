import numpy as np
import random
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))
    print("*********************************************")

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or winning_move(board, 1) or winning_move(board, 2):
        if winning_move(board, 2):
            return (None, 100000000000000)
        elif winning_move(board, 1):
            return (None, -10000000000000)
        else:
            return (None, 0)

    if maximizing_player:
        value = -math.inf
        column = random.choice([c for c in range(COLUMN_COUNT) if is_valid_location(board, c)])
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                temp_board = board.copy()
                drop_piece(temp_board, row, col, 2)
                new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return column, value
    else:
        value = math.inf
        column = random.choice([c for c in range(COLUMN_COUNT) if is_valid_location(board, c)])
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                temp_board = board.copy()
                drop_piece(temp_board, row, col, 1)
                new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return column, value

def play_game():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    while not game_over:
        # Player 1's turn
        if turn == 0:
            col = random.choice([c for c in range(COLUMN_COUNT) if is_valid_location(board, c)])

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
                if winning_move(board, 1):
                    print_board(board)
                    print("Player 1 wins!")
                    game_over = True

        # AI agent's turn
        else:
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            if winning_move(board, 2):
                print_board(board)
                print("AI wins!")
                game_over = True

        print_board(board)
        turn += 1
        turn %= 2
play_game()