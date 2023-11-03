import random

class Node:
    def __init__(self, keys, par = None):
        self.keys = list([keys])
        self.parent = par
        self.child = list()
    
    def __lt__(self, node):
        return self.keys[0] < node.keys[0]

    def _isLeaf(self):
        return len(self.child) == 0

    def _insertIntoNode(self, new_node):
        for child in new_node.child:
            child.parent = self
        self.keys.extend(new_node.keys)
        self.keys.sort()
        self.child.extend(new_node.child)
        if len(self.child) > 1:
            self.child.sort()
        if len(self.keys) > 3:
            self._split()


    def _insert(self, new_node):
        if self._isLeaf():
            self._insertIntoNode(new_node)
        elif new_node.keys[0] > self.keys[-1]:
            self.child[-1]._insert(new_node)
        else:
            for i in range(0, len(self.keys)):
                if new_node.keys[0] < self.keys[i]:
                    self.child[i]._insert(new_node)
                    break

    def _split(self):
        left_child = Node(self.keys[0], self)
        right_child = Node(self.keys[2], self)
        right_child.keys.append(self.keys[3])

        if self.child:
            self.child[0].parent = left_child
            self.child[1].parent = left_child
            self.child[2].parent = right_child
            self.child[3].parent = right_child
            self.child[4].parent = right_child

            left_child.child = [self.child[0], self.child[1]]
            right_child.child = [self.child[2], self.child[3],self.child[4]]

        self.child = [left_child]
        self.child.append(right_child)
        self.keys = [self.keys[1]]

        if self.parent:
            if self in self.parent.child:
                self.parent.child.remove(self)
            self.parent._insertIntoNode(self)
        else:
            left_child.parent = self
            right_child.parent = self

    def _preorder(self):
        print (self.keys)
        for child in self.child:
            child._preorder()

    def _remove(self, key):
        if key in self.keys:
            if self._isLeaf() and len(self.keys) > 1:
                self.keys.remove(key)
                return True
            elif not self._isLeaf():
                index = self.keys.index(key)
                if len(self.child[index].keys) > 1:
                    predecessor = self._getPredecessor(index)
                    self.keys[index] = predecessor
                    self.child[index]._remove(predecessor)
                    return True
                elif len(self.child[index + 1].keys) > 1:
                    successor = self._getSuccessor(index)
                    self.keys[index] = successor
                    self.child[index + 1]._remove(successor)
                    return True
                else:
                    self._mergeChildren(index)
                    if len(self.keys) == 0:
                        return True

        if self._isLeaf():
            return False

        index = 0
        while index < len(self.keys) and key > self.keys[index]:
            index += 1

        if self.child[index]._remove(key):
            if len(self.child[index].keys) == 0:
                self._mergeChildren(index)
                if len(self.keys) == 0:
                    return True
            return True
        return False

    def _getPredecessor(self, index):
        current = self.child[index]
        while not current._isLeaf():
            current = current.child[-1]
        return current.keys[-1]

    def _getSuccessor(self, index):
        current = self.child[index + 1]
        while not current._isLeaf():
            current = current.child[0]
        return current.keys[0]

    def _mergeChildren(self, index):
        left_child = self.child[index]
        right_child = self.child[index + 1]
        left_child.keys.append(self.keys[index])
        left_child.keys.extend(right_child.keys)
        left_child.child.extend(right_child.child)
        self.keys.pop(index)
        self.child.pop(index + 1)



class Tree234:
    def __init__(self):
        self.root = None

    def insert(self, elem):
        print("Inserindo: " + str(elem))
        if self.root is None:
            self.root = Node(elem)
        else:
            self.root._insert(Node(elem))
            while self.root.parent:
                self.root = self.root.parent
        return True

    def preorder(self):
        print('\n Impressao em pre-ordem\n')
        if self.root:
            self.root._preorder()

    def visualize(self):
        print('\n Estrutura de arvore (visual em largura)')
        this_level = [self.root]
        
        while this_level:
            next_level = list()
            print('\n')
            
            for n in this_level:
                if n:
                    print (str(n.keys), end = ' ')
                    
                    for child in n.child:
                        next_level.append(child)
                    this_level = next_level


    def remove(self, key):
        print("Removendo ", key, "\n")
        if self.root is None:
            return False
        if len(self.root.keys) == 1 and len(self.root.child) == 0:
            if self.root.keys[0] == key:
                self.root = None
                return True
            return False

        # Call the remove function starting from the root
        result = self.root._remove(key)

        if len(self.root.keys) == 0:
            self.root = self.root.child[0]  # Update the root if it's empty

        return result

        

def main():
    tree = Tree234()
    
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    
    tree.visualize()
    tree.preorder()
    
    tree.remove(10)

    tree.visualize()
    tree.preorder()

main()
