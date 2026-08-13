from collections import deque


def rightSideView(root):
    if not root:
        return []

    queue = deque([root])
    result = []

    while queue:
        level_size = len(queue)

        for i in range(level_size):
            node = queue.popleft()

            if i == 0:
                result.append(node.val)

            if node.right:
                queue.append(node.right)

            if node.left:
                queue.append(node.left)

    return result