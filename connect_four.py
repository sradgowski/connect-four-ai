from copy import deepcopy
import random
import time

random.seed(108)

def print_board(board):
    print()
    print(' ', end='')
    for x in range(1, len(board) + 1):
        print(' %s  ' % x, end='')
    print()

    print('+---+' + ('---+' * (len(board) - 1)))

    for y in range(len(board[0])):
        print('|   |' + ('   |' * (len(board) - 1)))
        print('|', end='')
        
        for x in range(len(board)):
            print(' %s |' % board[x][y], end='')
            
        print()
        print('|   |' + ('   |' * (len(board) - 1)))
        print('+---+' + ('---+' * (len(board) - 1)))

def select_space(board, column, player):
    if not move_is_valid(board, column):
        return False
    if player != "X" and player != "O":
        return False
    
    for y in range(len(board[0])-1, -1, -1):
        if board[column-1][y] == ' ':
            board[column-1][y] = player
            return True
        
    return False

def board_is_full(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == ' ':
                return False
    return True

def move_is_valid(board, move):
    if move < 1 or move > (len(board)):
        return False

    if board[move-1][0] != ' ':
        return False

    return True

def available_moves(board):
    moves = []
    for i in range(1, len(board) + 1):
        if move_is_valid(board, i):
            moves.append(i)
    return moves

def has_won(board, symbol):
    # Check horizontal spaces
    for y in range(len(board[0])):
        for x in range(len(board) - 3):
            if board[x][y] == symbol and board[x + 1][y] == symbol and board[x + 2][y] == symbol and board[x + 3][y] == symbol:
                return True

    # Check vertical spaces
    for x in range(len(board)):
        for y in range(len(board[0]) - 3):
            if board[x][y] == symbol and board[x][y + 1] == symbol and board[x][y + 2] == symbol and board[x][y + 3] == symbol:
                return True

    # Check / diagonal spaces
    for x in range(len(board) - 3):
        for y in range(3, len(board[0])):
            if board[x][y] == symbol and board[x + 1][y - 1] == symbol and board[x + 2][y - 2] == symbol and board[x + 3][y - 3] == symbol:
                return True

    # Check \ diagonal spaces
    for x in range(len(board) - 3):
        for y in range(len(board[0]) - 3):
            if board[x][y] == symbol and board[x + 1][y + 1] == symbol and board[x + 2][y + 2] == symbol and board[x + 3][y + 3] == symbol:
                return True

    return False


def game_is_over(board):
  return has_won(board, "X") or has_won(board, "O") or len(available_moves(board)) == 0

def evaluate_board(board):
    if has_won(board, "X"):
      return float("Inf")
    elif has_won(board, "O"):
      return -float("Inf")
    else:
      x_streaks = count_streaks(board, "X")
      o_streaks = count_streaks(board, "O")
      return x_streaks - o_streaks

def count_streaks(board, symbol):
    count = 0
    for col in range(len(board)):
        for row in range(len(board[0])):
            if board[col][row] != symbol:
                continue
                
            # Right
            if col < len(board) - 3:
                num_in_streak = 0
                for i in range(4):
                    if board[col + i][row] == symbol:
                        num_in_streak += 1
                    elif board[col + i][row] != " ":
                        num_in_streak = 0
                        break
                count += num_in_streak
                
            # Left
            if col > 2:
                num_in_streak = 0
                for i in range(4):
                    if board[col - i][row] == symbol:
                        num_in_streak += 1
                    elif board[col - i][row] != " ":
                        num_in_streak = 0
                        break
                count += num_in_streak
                
            # Up-right
            if col < len(board) - 3 and row > 2:
                num_in_streak = 0
                for i in range(4):
                    if board[col + i][row - i] == symbol:
                        num_in_streak += 1
                    elif board[col + i][row - i] != " ":
                        num_in_streak = 0
                        break
                count += num_in_streak
                
            # Down-right
            if col < len(board) - 3 and row < len(board[0]) - 3:
                num_in_streak = 0
                for i in range(4):
                    if board[col + i][row + i] == symbol:
                        num_in_streak += 1
                    elif board[col + i][row + i] != " ":
                        num_in_streak = 0
                        break
                count += num_in_streak
                
            # Down-left
            if col > 2 and row < len(board[0]) - 3:
                num_in_streak = 0
                for i in range(4):
                    if board[col - i][row + i] == symbol:
                        num_in_streak += 1
                    elif board[col - i][row + i] != " ":
                        num_in_streak = 0
                        break
                count += num_in_streak
                
            # Up-left
            if col > 2 and row > 2:
                num_in_streak = 0
                for i in range(4):
                    if board[col - i][row - i] == symbol:
                        num_in_streak += 1
                    elif board[col - i][row - i] != " ":
                        num_in_streak = 0
                        break
                count += num_in_streak
                
            # Down-left
            if col > 2 and row < len(board[0]) - 3:
                num_in_streak = 0
                for i in range(4):
                    if board[col - i][row + i] == symbol:
                        num_in_streak += 1
                    elif board[col - i][row + i] != " ":
                        num_in_streak = 0
                        break
                count += num_in_streak
                
            # Down
            num_in_streak = 0
            if row < len(board[0]) - 3:
                for i in range(4):
                    if row + i < len(board[0]):
                        if board[col][row + i] == symbol:
                            num_in_streak += 1
                        else:
                            break
            for i in range(4):
                if row - i > 0:
                    if board[col][row - i] == symbol:
                        num_in_streak += 1
                    elif board[col][row - i] == " ":
                        break
                    else:
                        num_in_streak == 0
            if row < 3:
                if num_in_streak + row < 4:
                    num_in_streak = 0
            count += num_in_streak
            
    return count

def minimax(input_board, is_maximizing, depth, alpha, beta, eval_function=evaluate_board):
  if game_is_over(input_board) or depth == 0:
        return [eval_function(input_board), ""]
    
  if is_maximizing:
    best_value = -float("Inf")
    moves = available_moves(input_board)
    random.shuffle(moves)
    best_move = moves[0]
    for move in moves:
      new_board = deepcopy(input_board)
      select_space(new_board, move, "X")
      hypothetical_value = minimax(new_board, False, depth - 1, alpha, beta, eval_function)[0]
      if hypothetical_value > best_value:
        best_value = hypothetical_value
        best_move = move
      alpha = max(alpha, best_value)
      if alpha >= beta:
        break
    return [best_value, best_move]

  else:
    best_value = float("Inf")
    moves = available_moves(input_board)
    random.shuffle(moves)
    best_move = moves[0]
    for move in moves:
      new_board = deepcopy(input_board)
      select_space(new_board, move, "O")
      hypothetical_value = minimax(new_board, True, depth - 1, alpha, beta, eval_function)[0]
      if hypothetical_value < best_value:
        best_value = hypothetical_value
        best_move = move
      beta = min(beta, best_value)
      if alpha >= beta:
        break
    return [best_value, best_move]

def make_board():
    new_game = None
    new_game = []
    for x in range(7):
        new_game.append([' '] * 6)
    return new_game

def play_game():
    answer = input("""Select your difficulty level:
    A. Beginner
    B. Regular
    C. Challenging
    D. Expert
    """)
    a_responses = ["a", "a.", "choice a", "beginner"]
    b_responses = ["b", "b.", "choice b", "regular"]
    c_responses = ["c", "c.", "choice c", "challenging"]
    d_responses = ["d", "d.", "choice d", "expert"]
    all_responses = a_responses + b_responses + c_responses + d_responses
    if answer.lower() in a_responses:
        ai = 1
    if answer.lower() in b_responses:
        ai = 2
    if answer.lower() in c_responses:
        ai = 3
    if answer.lower() in d_responses:
        ai = 4
    elif answer.lower() not in all_responses:
        print("Response not recognized. You will be punished with extra difficulty.")
        ai = 6
        
    board = make_board()
    while not game_is_over(board):
        print_board(board)
        moves = available_moves(board)
        print("Available moves: " , moves)
        
        choice = 100
        good_move = False
        while not good_move:
            choice = input("Select a move:\n")
            try:
                move = int(choice)
            except ValueError:
                continue
            if move in moves:
                good_move = True
                
        select_space(board, int(choice), "X")
        print_board(board)
        
        print("Computer thinking...")
        time.sleep(1.0) # Really just for the human player to process what's going on...
        
        if not game_is_over(board):
          result = minimax(board, False, ai, -float("Inf"), float("Inf"))
          print("Computer chose: ", result[1])
          select_space(board, result[1], "O")
        
    if has_won(board, "X"):
        print_board(board)
        print("You won!")
        
    elif has_won(board, "O"):
        print_board(board)
        print("The computer won!")
        
    else:
        print_board(board)
        print("It's a tie!")

def two_ai_game():
    answer = input("Do you want the bots to be equally smart?\n")
    if answer.lower() in ["yes", "y", "yup", "yep", "mhm", "duh"]:
        x_smart = 4
        o_smart = 4
        
    if answer.lower() in ["no", "n", "nope", "no thanks"]:
        answer2 = input("""How much smarter should bot number one be?
        A. A little smarter
        B. Noticeably smarter
        C. Dramatically smarter
        """)
        if answer2.lower() in ["a", "a.", "choice a"]:
            x_smart = 4
            o_smart = 3
        if answer2.lower() in ["b", "b.", "choice b"]:
            x_smart = 4
            o_smart = 2
        if answer2.lower() in ["c", "c.", "choice c"]:
            x_smart = 4
            o_smart = 1
            
    my_board = make_board()
    
    while not game_is_over(my_board):
      # The "X" player finds their best move.
      result = minimax(my_board, True, x_smart, -float("Inf"), float("Inf"), evaluate_board)
      print( "X Turn\nX selected ", result[1])
      print(result[1])
        
      select_space(my_board, result[1], "X")
      print_board(my_board)

      time.sleep(2.0)
    
      if not game_is_over(my_board):
        # The "O" player finds their best move
        result = minimax(my_board, False, o_smart, -float("Inf"), float("Inf"), evaluate_board)
        print( "O Turn\nO selected ", result[1])
        print(result[1])
        select_space(my_board, result[1], "O")
        print_board(my_board)

        time.sleep(2.0)

    if has_won(my_board, "X"):
        print("X won!")
        
    elif has_won(my_board, "O"):
        print("O won!")
        
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()
