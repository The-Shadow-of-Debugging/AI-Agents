def findOrder(self, numCourses: int, prerequisites):
    graph = [[] for _ in range(numCourses)]
    indegree = [0] * numCourses
    result = []
    queue = []

    for i, [course, prereq] in enumerate(prerequisites):
        graph[prereq].append(course)
        indegree[course] += 1

    for course, value in enumerate(indegree):
        if value == 0:
            queue.append(course)

    while queue:
        course = queue.pop()
        result.append(course)

        for i, value in enumerate(graph[course]):
            indegree[value] -= 1

            if indegree[value] == 0:
                queue.append(value)

    if len(result) == numCourses:
        return result

    return []
