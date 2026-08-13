from collections import deque

def averageOfLevels(root):
    queue = deque([root])
    result = []

    while queue:
        level_size = len(queue)
        level_sum = 0

        for _ in range(level_size):
            node = queue.popleft()
            level_sum += node.val

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        average_sum = level_sum / level_size
        result.append(average_sum)

    return result