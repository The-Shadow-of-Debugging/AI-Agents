def isBalanced(root) -> bool:
    if not root:
        return True

    def calculate_height(root):
        if not root:
            return 0

        leftHeight = calculate_height(root.left)
        if leftHeight == -1:
            return -1

        rightHeight = calculate_height(root.right)
        if rightHeight == -1:
            return -1

        if abs(leftHeight - rightHeight) > 1:
            return -1

        return max(leftHeight, rightHeight) + 1

    return calculate_height(root) != -1