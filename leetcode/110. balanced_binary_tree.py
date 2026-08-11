def isBalanced(root) -> bool:
    if not root:
        return True

    def calculate_height(root):
        if not root:
            return 0

        return max(calculate_height(root.left) + 1, calculate_height(root.right) + 1)

    leftSubtree = calculate_height(root.left)
    rightSubtree = calculate_height(root.right)

    if abs(leftSubtree - rightSubtree) > 1:
        return False

    return self.isBalanced(root.left) and self.isBalanced(root.right)