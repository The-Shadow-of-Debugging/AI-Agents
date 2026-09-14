def isValidBST(root) -> bool:
    def is_valid_tree(node, min_value, max_value):
        if not node:
            return True

        if node.val >= max_value or node.val <= min_value:
            return False

        return is_valid_tree(node.left, min_value, node.val) and is_valid_tree(node.right, node.val, max_value)

    return is_valid_tree(root, float("-inf"), float("inf"))