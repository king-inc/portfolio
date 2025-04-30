class Node:
    def __init__(self, _colors, _node_type):
        self.colors = _colors
        self.node_type = _node_type

    def __eq__(self, _node):
        return self.node_type == _node.node_type and sorted(self.colors) == sorted(_node.GetColors())
    def GetColors(self):
        return self.colors
    def GetType(self):
        return self.node_type