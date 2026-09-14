def maxAreaOfIsland(grid) -> int:
    max_area = 0
    max_x = len(grid)
    max_y = len(grid[0])

    def dfs(x, y):
        if x < 0 or y < 0 or x >= max_x or y >= max_y:
            return 0

        if grid[x][y]:
            grid[x][y] = 0
            return 1 + dfs(x + 1, y) + dfs(x, y - 1) + dfs(x - 1, y) + dfs(x, y + 1)

        return 0

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if (cell):
                max_area = max(max_area, dfs(i, j))

    return max_area