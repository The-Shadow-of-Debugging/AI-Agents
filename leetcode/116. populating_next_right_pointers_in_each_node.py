from collections import deque


def connect(root):
    if not root:
        return root

    queue = deque([root])

    while queue:
        level_size = len(queue)
        prev_node = None

        for i in range(level_size):
            current_node = queue.popleft()

            if prev_node:
                prev_node.next = current_node

            prev_node = current_node

            if (current_node.left):
                queue.append(current_node.left)

            if (current_node.right):
                queue.append(current_node.right)

        if prev_node:
            prev_node.next = None

    return root