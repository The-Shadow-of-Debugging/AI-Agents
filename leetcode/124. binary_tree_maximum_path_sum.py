def maxPathSum(root) -> int:
    max_sum = -float('inf')

    def dfs(node):
        nonlocal max_sum

        if not node:
            return 0

        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))
        max_sum = max(max_sum, left + right + node.val)

        return node.val + max(left, right)

    dfs(root)

    return max_sum