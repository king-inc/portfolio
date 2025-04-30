from Classes.Node import Node

ROW = 3

class Face: 
    def __init__(self, nodes, color):
        self.nodes = nodes
        self.color = color

    def __eq__(self, _face):
        #output is true by default because its used in and operations
        output = True
        #print(_face)
        if _face == 0:
            return False
        if self.color == _face.GetColor():
            for i in range(ROW):
                for j in range(ROW):
                    output = output and self.nodes[i][j] == _face.GetNodes()[i][j]
                    if not output:
                        break
                if not output:
                    break
        else:
            output = False

        return output
    
    def GetNodes(self):
        return self.nodes
    def SetNodes(self, nodes):
        self.nodes = nodes
    def GetColor(self):
        return self.color
    def CompareLines(self, line, ex_line):
        output = True
        if line == "L":
            for i in range(ROW):
                output = output and self.nodes[i][0] == ex_line.nodes[i][0]
        elif line == "R":
            for i in range(ROW):
                output = output and self.nodes[i][2] == ex_line.nodes[i][2]
        elif line == "MV":
            for i in range(ROW):
                output = output and self.nodes[i][1] == ex_line.nodes[i][1]
        elif line == "MH":
            output = output and self.nodes[1] == ex_line.nodes[1]
        elif line == "U":
            output = output and self.nodes[0] == ex_line.nodes[0]
        elif line == "D":
            output = output and self.nodes[2] == ex_line.nodes[2]
        return output
    
    def GetLineNodes(self, line):
        nodes = []
        if line == "L":
            for i in range(ROW):
                nodes.append(self.nodes[i][0])
        elif line == "R":
            for i in range(ROW):
                nodes.append(self.nodes[i][2])
        elif line == "U":
            nodes = self.nodes[0]
        elif line == "D":
            nodes = self.nodes[2]
        return nodes
    
    def ChangeLine(self,nodes, line):
        if line == "L":
            for i in range(ROW):
                self.nodes[i][0] = nodes[i]
        elif line == "R":
            for i in range(ROW):
                self.nodes[i][2] = nodes[i]
        elif line == "U":
            self.nodes[0] = nodes
        elif line == "D":
            self.nodes[2] = nodes
        
    def RotateFace(self,direction):
        if direction == "L":
            self.nodes[0][0], self.nodes[0][1], self.nodes[0][2],self.nodes[1][2], self.nodes[2][2], self.nodes[2][0],self.nodes[2][1], self.nodes[1][0] = self.nodes[2][0], self.nodes[1][0], self.nodes[0][0],self.nodes[0][1],self.nodes[0][2],self.nodes[2][2],self.nodes[1][2],self.nodes[2][1]
        elif direction == "R":
            self.nodes[0][0], self.nodes[0][1], self.nodes[0][2],self.nodes[1][2], self.nodes[2][2], self.nodes[2][0],self.nodes[2][1], self.nodes[1][0] = self.nodes[0][2],self.nodes[1][2],self.nodes[2][2],self.nodes[2][1],self.nodes[2][0],self.nodes[0][0],self.nodes[1][0],self.nodes[0][1]
