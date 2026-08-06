def invertTree(root):
    if not root:
        return root

    root.left, root.right = root.right, root.left

    self.invertTree(root.right)
    self.invertTree(root.left)

    return root
