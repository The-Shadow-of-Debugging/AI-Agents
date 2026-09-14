def cloneGraph(node):
    if not node:
        return node

    visited = {}

    def dfs(v):
        if v in visited:
            return visited[v]
        else:
            new_node = Node(v.val)
            visited[v] = new_node

            for neighbor in v.neighbors:
                new_node.neighbors.append(dfs(neighbor))

            return new_node

    return dfs(node)
