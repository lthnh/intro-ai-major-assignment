from copy import deepcopy

n = int()
solutions = list()

def check_solution(board, row, column):
    for i in range(column):
        if row == board[i] or abs(row - board[i]) == column - i:
            return False
    return True

def expand_solution(board):
    next_column = len(board)
    generated_boards = list()
    for new_row in range(n):
        if check_solution(board, new_row, next_column):
            new_board = deepcopy(board)
            new_board.append(new_row)
            generated_boards.append(new_board)
    return generated_boards

def breath_first_search(n):
    solutions_count = 0
    for start_position in range(n):
        solutions.append([start_position])
    while len(solutions) != 0:
        board = solutions.pop(0)
        if len(board) >= n:
            solutions_count += 1
            print(board)
            continue
        generated_boards = expand_solution(board)
        if len(generated_boards) > 0:
            solutions.extend(expand_solution(board))
    return solutions_count


if __name__ == '__main__':
    n = int(input('N: '))
    solutions_count = breath_first_search(n)
    print(solutions_count)