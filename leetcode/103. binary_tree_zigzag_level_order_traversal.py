from collections import deque


def zigzagLevelOrder(root):
    if not root:
        return []

    queue = deque([root])
    result = []
    isReverse = False

    while queue:
        level_size = len(queue)
        level_values = deque([])

        for _ in range(level_size):
            node = queue.popleft()

            if isReverse:
                level_values.appendleft(node.val)
            else:
                level_values.append(node.val)

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        result.append(list(level_values))
        isReverse = not isReverse

    return result