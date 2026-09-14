def numIslands(grid):
    if not grid or not grid[0]:
        return 0

    islands_count = 0
    max_x = len(grid)
    max_y = len(grid[0])

    def dfs(x, y):
        if x < 0 or y < 0 or x >= max_x or y >= max_y:
            return

        if grid[x][y] == "1":
            grid[x][y] = "0"
            dfs(x + 1, y)
            dfs(x - 1, y)
            dfs(x, y - 1)
            dfs(x, y + 1)

        return

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if grid[i][j] == "1":
                islands_count += 1
                dfs(i, j)

    return islands_count
