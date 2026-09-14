def solve(board) -> None:
    """
    Do not return anything, modify board in-place instead.
    """
    max_x = len(board)
    max_y = len(board[0])

    def dfs(x, y):
        if x < 0 or y < 0 or x >= max_x or y >= max_y:
            return

        if board[x][y] == 'O':
            board[x][y] = 'T'
            dfs(x + 1, y)
            dfs(x, y + 1)
            dfs(x - 1, y)
            dfs(x, y - 1)

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 'O' and (i == 0 or j == 0 or i == max_x - 1 or j == max_y - 1):
                dfs(i, j)

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 'O':
                board[i][j] = 'X'

            if cell == 'T':
                board[i][j] = 'O'