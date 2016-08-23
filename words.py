from base import Node

class Cmavo(Node):
    '''Abstract class for cmavo.'''
    pass

class Brivla(Node):
    '''Abstract class for brivla.'''
    _functions = []
    def toDot(self, ID, out):
        ID += 1
        myID = ID
        print("\t{} [label = {}]".format(ID, self.__class__.__name__),
              file=out)
        print("\t{} -> {} [label = x1]".format(myID, ID + 1), file=out)
        ID = self.children[0].toDot(ID, out)
        if 1 < len(self.children):
            ID += 1
            print("\t{} -> {} [color = white]".format(myID, ID),
                  "\t{} [color = white, label = \"\"]".format(ID),
                  sep="\n", file=out)
            for c, f in zip(self.children[1:], self._functions):
                print("\t{} -> {} [label = \"{}\"]".format(myID, ID + 1, f),
                      file=out)
                ID = c.toDot(ID, out)
        return ID

class Sumti(Node):
    '''Abstract class for sumti.'''
    pass
