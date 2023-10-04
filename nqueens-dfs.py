from collections import deque
# from copy import deepcopy

my_deque = deque()
n = int()
board = list()

def is_safe(row, column):
    for i in range(column):
        if row == board[i] or abs(row - board[i]) == column - i:
            return False
    return True

def depth_first_search(n):
    # solutions = list()
    solutions_count = 0
    for i in range(n):
        my_deque.append((i, 0))
    while len(my_deque) != 0:
        # print(my_deque)
        # print(board)
        (row, column) = my_deque.pop()
        board[column] = row
        next_column = column + 1
        if next_column > n-1:
            # solutions.append(deepcopy(board))
            solutions_count += 1
            for column, row in enumerate(board):
                print(row, column)
            print()
            continue
        for i in range(n):
            if is_safe(i, next_column):
                my_deque.append((i, next_column))
    # return solutions
    return solutions_count

if __name__ == '__main__':
    n = int(input('N: '))
    board = [-1] * n
    solutions_count = depth_first_search(n)
    print(solutions_count)
    # solutions = depth_first_search(n)
    # print(solutions)
