def canFinish(numCourses: int, prerequisitesr) -> bool:
    graph = [[] for _ in range(numCourses)]
    state = [0] * numCourses

    def dfs(c):
        if state[c] == 1:
            return False

        if state[c] == 2:
            return True

        state[c] = 1
        for neighbor in graph[c]:
            res = dfs(neighbor)

            if not res:
                return False

        state[c] = 2
        return True

    for i, [course, prereq] in enumerate(prerequisites):
        graph[prereq].append(course)

    canFinish = True
    for i, [course, prereq] in enumerate(prerequisites):
        canFinish &= dfs(course)

    return canFinish