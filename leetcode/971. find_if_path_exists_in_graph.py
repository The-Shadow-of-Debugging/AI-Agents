def validPath(n: int, edges, source: int, destination: int) -> bool:
    graph = [[] for _ in range(n)]
    visited = [False for _ in range(n)]

    for u, v in edges:
        graph[v].append(u)
        graph[u].append(v)

    def dfs(v):
        if v == destination:
            return True

        visited[v] = True

        for u in graph[v]:
            if not visited[u]:
                res = dfs(u)

                if res:
                    return True

        return False

    return dfs(source)