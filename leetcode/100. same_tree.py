def isSameTree(p, q) -> bool:
    def isSame(leftTree, rightTree):
        if not leftTree and not rightTree:
            return True

        if not leftTree or not rightTree:
            return False

        if leftTree.val != rightTree.val:
            return False

        return isSame(leftTree.left, rightTree.left) and isSame(leftTree.right, rightTree.right)

    return isSame(p, q)