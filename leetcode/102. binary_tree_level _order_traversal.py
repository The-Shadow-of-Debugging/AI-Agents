from collections import deque

def levelOrder(root):
    if not root:
        return []

    queue = deque([root])
    result = []

    while queue:
        queue_size = len(queue)
        level_nodes = []

        for _ in range(queue_size):
            node = queue.popleft()
            level_nodes.append(node.val)

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        if level_nodes:
            result.append(level_nodes)

    return result