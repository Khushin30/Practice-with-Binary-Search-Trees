import random


class BSTree:
    class Node:
        def __init__(self, key, val, left=None, right=None):
            self.key = key
            self.val = val
            self.left = left
            self.right = right

    def __init__(self):
        self.size = 0
        self.root = None

    def __getitem__(self, key):
        assert (key in self)

        def getitemRec(node):
            if node.key > key:
                return getitemRec(node.left)
            elif node.key < key:
                return getitemRec(node.right)
            else:
                return node.val

        return getitemRec(self.root)

    def __setitem__(self, key, val):
        if key in self:
            def setKey(node):
                if key > node.key:
                    setKey(node.right)
                elif key < node.key:
                    setKey(node.left)
                else:
                    node.val = val

            setKey(self.root)
        else:
            if self.root is None:
                self.root = BSTree.Node(key, val)
            else:
                def addKey(node):
                    if key > node.key:
                        if node.right is None:
                            node.right = BSTree.Node(key, val)
                        else:
                            addKey(node.right)
                    elif key < node.key:
                        if node.left is None:
                            node.left = BSTree.Node(key, val)
                        else:
                            addKey(node.left)

                addKey(self.root)
            self.size += 1

    def __delitem__(self, key):
        assert (key in self)

        def delNode(node):
            if key > node.key:
                node.right = delNode(node.right)
                return node
            elif key < node.key:
                node.left = delNode(node.left)
                return node
            else:
                if not node.right and not node.left:
                    return None
                elif not node.right and node.left:
                    return node.left
                elif node.right and not node.left:
                    return node.right
                else:
                    n = node.left
                    if n.right:
                        parent = node
                        while n.right:
                            parent = n
                            n = n.right
                        node.val = n.val
                        node.key = n.key
                        parent.right = None
                        return node
                    else:
                        node.val = n.val
                        node.key = n.key
                        node.left = node.left.left
                        return node
        delNode(self.root)

    def __contains__(self, key):
        def containsRec(node):
            if node is None:
                return False
            if node.key > key:
                return containsRec(node.left)
            elif node.key < key:
                return containsRec(node.right)
            else:
                return True

        return containsRec(self.root)

    def __len__(self):
        return self.size

    def __iter__(self):
        def iterRec(node):
            if node is not None:
                yield from iterRec(node.left)
                yield node.key
                yield from iterRec(node.right)
        return iterRec(self.root)

    def keys(self):
        return iter(self)

    def values(self):
        def iterRec(node):
            if node is not None:
                yield from iterRec(node.left)
                yield node.val
                yield from iterRec(node.right)
        return iterRec(self.root)

    def items(self):
        for x,y in self.keys(),self.values():
            yield x,y

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n, level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height - 1:
                    nodes.extend([(None, level + 1), (None, level + 1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width // 2 ** level)
            elif n:
                if n.left or level < height - 1:
                    nodes.append((n.left, level + 1))
                if n.right or level < height - 1:
                    nodes.append((n.right, level + 1))
                repr_str += '{val:^{width}}'.format(val=n.key, width=width // 2 ** level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""

        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1 + height_rec(t.left), 1 + height_rec(t.right))

        return height_rec(self.root)

