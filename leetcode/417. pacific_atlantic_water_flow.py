from typing import List


def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    result = []
    n = len(heights)
    m = len(heights[0])

    pacific_visited = [[0 for _ in range(m)] for _ in range(n)]
    atlantic_visited = [[0 for _ in range(m)] for _ in range(n)]

    def dfs(x, y, visited):
        if x < 0 or y < 0 or x >= n or y >= m or visited[x][y]:
            return

        visited[x][y] = 1
        if y + 1 < m and heights[x][y] <= heights[x][y + 1]:
            dfs(x, y + 1, visited)

        if x + 1 < n and heights[x][y] <= heights[x + 1][y]:
            dfs(x + 1, y, visited)

        if y - 1 >= 0 and heights[x][y] <= heights[x][y - 1]:
            visited[x][y] = 1
            dfs(x, y - 1, visited)

        if x - 1 >= 0 and heights[x][y] <= heights[x - 1][y]:
            visited[x][y] = 1
            dfs(x - 1, y, visited)

    for i, row in enumerate(heights):
        for j, cell in enumerate(row):
            if i == 0 or j == 0:
                dfs(i, j, pacific_visited)

            if i == n - 1 or j == m - 1:
                dfs(i, j, atlantic_visited)

    for i, row in enumerate(heights):
        for j, cell in enumerate(row):
            if pacific_visited[i][j] == 1 and atlantic_visited[i][j] == 1:
                result.append([i, j])

    return result