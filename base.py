import sys

class Node:
    '''Basic AST node'''
    def __init__(self, *children):
        '''Create an AST node.

        Parameters:
          - *children: the children of the node.
        '''
        self.children = children

    def toDot(self, ID, out):
        '''Print node and its children in Graphviz DOT format.

        Parameters:
          - ID: the numerical ID of the parent, used as a DOT ID;
          - out: the output stream.

        Return value:
            The ID of the last printed node; used for the recursion.
        '''
        ID += 1
        myID = ID
        print("\t{} [label = {}]".format(myID, self.__class__.__name__),
              file=out)
        for c in self.children:
            print("\t{} -> {}".format(myID, ID + 1), file=out)
            ID = c.toDot(ID, out)
        return ID

def mkTree(node, out=sys.stdout):
    '''Turn an AST into dot format.

    Parameters:
        - node: the root Node of the AST;
        - out: the output stream (default: sys.stdout).
    '''
    print("digraph {", file=out)
    node.toDot(-1, out)
    print("}", file=out)

def dictToTrie(dic):
    '''Turn a dict into a dict of dicts of dicts... in the shape of a trie.

    Parameters:
        - dic: the dict to turn into a trie.

    Precondictions: no key of dic must be a prefix of another.
    '''
    root = dict()
    # For each string that leads to a value
    for k in dic.keys():
        cur = root
        # For each character in the key (except the last one)
        for c in k[:-1]:
            if c not in cur.keys():
                # Create a dict
                cur[c] = dict()
            cur = cur[c]
        # For the last character, put the value
        cur[k[-1:]] = dic[k]
    return root
