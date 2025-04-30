from Classes.Face import Face

ROW = 3

class Cube:
    def __init__(self, faces):
        self.faces = faces
        self.all_colors = ["red","blue","yellow","green","white","orange"]
        self.color_pos = {"front":"red",
                        "back":"orange",
                        "top":"blue",
                        "bottom":"green",
                        "left":"yellow",
                        "right":"white"}
        self.FRONT = self.GetFaceFromPos("front")
        self.BACK = self.GetFaceFromPos("back")
        self.TOP = self.GetFaceFromPos("top")
        self.BOTTOM = self.GetFaceFromPos("bottom")
        self.LEFT = self.GetFaceFromPos("left")
        self.RIGHT = self.GetFaceFromPos("right")

    def __eq__(self, _cube):
        output = True
        for i in range(len(self.faces)):
            output = output and self.faces[i] == _cube.GetFaces()[i]
            if not output:
                break
        return output

    def GetMatrixFaces(self):
        matrix = []
        keys = {"red":0,
                "blue":1,
                "yellow":2,
                "green":3,
                "white":4,
                "orange":5}
        
        for i in range(len(self.faces)):
            face = []
            for j in range(ROW):
                line = []
                for k in range(ROW):
                    line.append(keys[self.faces[i].GetNodes()[j][k].GetColors()[0]])
                face.append(line)
            matrix.append(face)
        return matrix
    def GetFaces(self):
        return self.faces
    def SetFaces(self, faces):
        self.faces = faces
    def ChangeFront(self, color):
        output = self.color_pos.copy()
        for key in self.color_pos:
            if self.color_pos[key] == color:
                #print(key)
                #print("pre change: ",self.color_pos)
                if key == "front":
                    return output
                if key == "bottom":
                    output["front"],output["back"],output["top"],output["bottom"] = output["bottom"],output["top"],output["front"],output["back"]
                elif key == "top":
                    output["front"],output["back"],output["top"],output["bottom"] = output["top"],output["bottom"],output["back"],output["front"]
                elif key == "right":
                    output["front"],output["back"],output["left"],output["right"] = output["right"],output["left"],output["front"],output["back"]
                elif key == "left":
                    output["front"],output["back"],output["left"],output["right"] = output["left"],output["right"],output["back"],output["front"]
                elif key == "back":
                    output["front"],output["back"],output["top"],output["bottom"] = output["back"],output["front"],output["bottom"],output["top"]
                break
        return output
            
    def GetFaceFromPos(self,pos):
        for key in self.color_pos:
            if key == pos:
                for i in range(len(self.faces)):
                    if self.faces[i] != 0 and self.color_pos[key] == self.faces[i].GetColor():
                        return i
                return False
    def PrintCube(self):
        print_pos = {}
        curr_face = 0
        for key in self.color_pos:
            #find the right face
            for i in range(len(self.faces)):
                if self.faces[i].GetColor() == self.color_pos[key]:
                    curr_face = i
            face_string = []
            for i in range(ROW):
                face_string.append(self.faces[curr_face].GetNodes()[i][0].GetColors()[0] + " | " + self.faces[curr_face].GetNodes()[i][1].GetColors()[0] + " | " + self.faces[curr_face].GetNodes()[i][2].GetColors()[0])
                if i<2:
                    face_string.append("--- + --- + ---")
            print_pos.update({key:face_string})

        output = []
        first_line = ""
        sec_line = ""
        third_line = ""
        #j is elements in self.color_pos key
        for j in range(5):
            if j<1:
                first_line += print_pos["back"][j] + " | " + print_pos["top"][j]
                sec_line += print_pos["left"][j] + " | " + print_pos["front"][j] + " | " + print_pos["right"][j]
                third_line += "                 " + " | " + print_pos["bottom"][j] + " | "
            else:
                first_line += "\n" + print_pos["back"][j] + " | " + print_pos["top"][j]
                sec_line += "\n" +print_pos["left"][j] + " | " + print_pos["front"][j] + " | " + print_pos["right"][j]
                third_line += "\n                 " + " | " + print_pos["bottom"][j] + " | "
        output = [first_line,sec_line,third_line]
        output_str = ""
        for i in range(len(output)):
            if i < 1:
                output_str += output[i]
            else:
                output_str += "\n" +output[i]
            if i<2:
                output_str += "\n--- + --- + --- + --- + --- + --- + --- + --- + ---"
        print(output_str)

    def RotateLU(self, key):
        #key is the face to be turned
        if key =="front" or key =="back" or key =="top" or key=="bottom":
            front_line = self.faces[self.FRONT].GetLineNodes("L")
            top_line = self.faces[self.TOP].GetLineNodes("L")
            bottom_line = self.faces[self.BOTTOM].GetLineNodes("L")
            back_line = self.faces[self.BACK].GetLineNodes("L")

            self.faces[self.FRONT].ChangeLine(bottom_line, "L")
            self.faces[self.TOP].ChangeLine(front_line, "L")
            self.faces[self.BACK].ChangeLine(top_line, "L")
            self.faces[self.BOTTOM].ChangeLine(back_line,"L")

            self.faces[self.LEFT].RotateFace("R")
        
        elif key=="left":
            top_line = self.faces[self.TOP].GetLineNodes("U")
            bottom_line = self.faces[self.BOTTOM].GetLineNodes("D")
            left_line = self.faces[self.LEFT].GetLineNodes("L")
            right_line = self.faces[self.RIGHT].GetLineNodes("R")

            self.faces[self.LEFT].ChangeLine(bottom_line, "L")
            self.faces[self.TOP].ChangeLine(left_line, "U")
            self.faces[self.RIGHT].ChangeLine(top_line, "R")
            self.faces[self.BOTTOM].ChangeLine(right_line,"D")

            self.faces[self.BACK].RotateFace("R")
        
        elif key=="right":
            top_line = self.faces[self.TOP].GetLineNodes("D")
            bottom_line = self.faces[self.BOTTOM].GetLineNodes("U")
            left_line = self.faces[self.LEFT].GetLineNodes("R")
            right_line = self.faces[self.RIGHT].GetLineNodes("L")

            self.faces[self.RIGHT].ChangeLine(bottom_line, "L")
            self.faces[self.TOP].ChangeLine(right_line, "D")
            self.faces[self.LEFT].ChangeLine(top_line, "R")
            self.faces[self.BOTTOM].ChangeLine(left_line,"U")

            self.faces[self.FRONT].RotateFace("R")

    def RotateLD(self, key):
        if key =="front" or key =="back" or key =="top" or key=="bottom":
            front_line = self.faces[self.FRONT].GetLineNodes("L")
            top_line = self.faces[self.TOP].GetLineNodes("L")
            bottom_line = self.faces[self.BOTTOM].GetLineNodes("L")
            back_line = self.faces[self.BACK].GetLineNodes("L")

            self.faces[self.FRONT].ChangeLine(top_line, "L")
            self.faces[self.TOP].ChangeLine(back_line, "L")
            self.faces[self.BACK].ChangeLine(bottom_line, "L")
            self.faces[self.BOTTOM].ChangeLine(front_line,"L")

            self.faces[self.LEFT].RotateFace("L")
        
        elif key=="left":
            top_line = self.faces[self.TOP].GetLineNodes("U")
            bottom_line = self.faces[self.BOTTOM].GetLineNodes("D")
            left_line = self.faces[self.LEFT].GetLineNodes("L")
            right_line = self.faces[self.RIGHT].GetLineNodes("R")

            self.faces[self.LEFT].ChangeLine(top_line, "L")
            self.faces[self.TOP].ChangeLine(right_line, "U")
            self.faces[self.RIGHT].ChangeLine(bottom_line, "R")
            self.faces[self.BOTTOM].ChangeLine(left_line,"D")

            self.faces[self.BACK].RotateFace("L")
        
        elif key=="right":
            top_line = self.faces[self.TOP].GetLineNodes("D")
            bottom_line = self.faces[self.BOTTOM].GetLineNodes("U")
            left_line = self.faces[self.LEFT].GetLineNodes("R")
            right_line = self.faces[self.RIGHT].GetLineNodes("L")

            self.faces[self.RIGHT].ChangeLine(top_line, "L")
            self.faces[self.TOP].ChangeLine(left_line, "D")
            self.faces[self.LEFT].ChangeLine(bottom_line, "R")
            self.faces[self.BOTTOM].ChangeLine(right_line,"U")

            self.faces[self.FRONT].RotateFace("R")
        
    def RotateRU(self, key):
        if key =="front" or key =="back" or key =="top" or key=="bottom":
            front_line = self.faces[self.FRONT].GetLineNodes("R")
            top_line = self.faces[self.TOP].GetLineNodes("R")
            bottom_line = self.faces[self.BOTTOM].GetLineNodes("R")
            back_line = self.faces[self.BACK].GetLineNodes("R")

            self.faces[self.FRONT].ChangeLine(bottom_line, "R")
            self.faces[self.TOP].ChangeLine(front_line, "R")
            self.faces[self.BACK].ChangeLine(top_line, "R")
            self.faces[self.BOTTOM].ChangeLine(back_line,"R")

            self.faces[self.RIGHT].RotateFace("R")
        
        elif key=="left":
            self.RotateLD("right")
        
        elif key=="right":
            self.RotateLD("left")

    def RotateRD(self, key):
        if key =="front" or key =="back" or key =="top" or key=="bottom":
            front_line = self.faces[self.FRONT].GetLineNodes("R")
            top_line = self.faces[self.TOP].GetLineNodes("R")
            bottom_line = self.faces[self.BOTTOM].GetLineNodes("R")
            back_line = self.faces[self.BACK].GetLineNodes("R")

            self.faces[self.FRONT].ChangeLine(top_line, "R")
            self.faces[self.TOP].ChangeLine(back_line, "R")
            self.faces[self.BACK].ChangeLine(bottom_line, "R")
            self.faces[self.BOTTOM].ChangeLine(front_line,"R")

            self.faces[self.RIGHT].RotateFace("L")
        
        elif key=="left":
            self.RotateLU("right")
        
        elif key=="right":
            self.RotateLU("left")

    def RotateUL(self, key):
        #key is the face to be turned
        if key =="front" or key =="back" or key =="left" or key=="right":
            front_line = self.faces[self.FRONT].GetLineNodes("U")
            left_line = self.faces[self.LEFT].GetLineNodes("U")
            right_line = self.faces[self.RIGHT].GetLineNodes("U")
            back_line = self.faces[self.BACK].GetLineNodes("D")

            self.faces[self.FRONT].ChangeLine(right_line, "U")
            self.faces[self.LEFT].ChangeLine(front_line, "U")
            self.faces[self.BACK].ChangeLine(left_line, "D")
            self.faces[self.RIGHT].ChangeLine(back_line,"U")

            self.faces[self.TOP].RotateFace("L")
        
        elif key=="top":
            self.RotateLU("left")
        elif key=="bottom":
            self.RotateLU("right")

    def RotateUR(self, key):
        #key is the face to be turned
        if key =="front" or key =="back" or key =="left" or key=="right":
            front_line = self.faces[self.FRONT].GetLineNodes("U")
            left_line = self.faces[self.LEFT].GetLineNodes("U")
            right_line = self.faces[self.RIGHT].GetLineNodes("U")
            back_line = self.faces[self.BACK].GetLineNodes("D")

            self.faces[self.FRONT].ChangeLine(left_line, "U")
            self.faces[self.LEFT].ChangeLine(back_line, "U")
            self.faces[self.BACK].ChangeLine(right_line, "D")
            self.faces[self.RIGHT].ChangeLine(front_line,"U")

            self.faces[self.TOP].RotateFace("R")
        
        elif key=="top":
            self.RotateLD("left")
        elif key=="bottom":
            self.RotateLD("right")
    
    def RotateDL(self, key):
        #key is the face to be turned
        if key =="front" or key =="back" or key =="left" or key=="right":
            front_line = self.faces[self.FRONT].GetLineNodes("D")
            left_line = self.faces[self.LEFT].GetLineNodes("D")
            right_line = self.faces[self.RIGHT].GetLineNodes("D")
            back_line = self.faces[self.BACK].GetLineNodes("U")

            self.faces[self.FRONT].ChangeLine(right_line, "D")
            self.faces[self.LEFT].ChangeLine(front_line, "D")
            self.faces[self.BACK].ChangeLine(left_line, "U")
            self.faces[self.RIGHT].ChangeLine(back_line,"D")

            self.faces[self.BOTTOM].RotateFace("L")
        
        elif key=="top" or key=="bottom":
            self.RotateLD("right")
        elif key=="bottom":
            self.RotateLD("left")

    def RotateDR(self, key):
        #key is the face to be turned
        if key =="front" or key =="back" or key =="left" or key=="right":
            front_line = self.faces[self.FRONT].GetLineNodes("D")
            left_line = self.faces[self.LEFT].GetLineNodes("D")
            right_line = self.faces[self.RIGHT].GetLineNodes("D")
            back_line = self.faces[self.BACK].GetLineNodes("U")

            self.faces[self.FRONT].ChangeLine(left_line, "D")
            self.faces[self.LEFT].ChangeLine(back_line, "D")
            self.faces[self.BACK].ChangeLine(right_line, "U")
            self.faces[self.RIGHT].ChangeLine(front_line,"D")

            self.faces[self.BOTTOM].RotateFace("R")
        
        elif key=="top":
            self.RotateLU("right")
        elif key=="bottom":
            self.RotateLU("left")

    def RotateFaceL(self, key):
        if key=="front":
            self.RotateLU("right")
        elif key== "back":
            self.RotateLU("left")
        elif key=="left":
            self.RotateLU("front")
        elif key=="right":
            self.RotateRD("front")
        elif key=="top":
            self.RotateUL("front")
        elif key=="bottom":
            self.RotateDL("front")

    def RotateFaceR(self, key):
        if key=="front":
            self.RotateLD("right")
        elif key== "back":
            self.RotateLD("left")
        elif key=="left":
            self.RotateLD("front")
        elif key=="right":
            self.RotateRU("front")
        elif key=="top":
            self.RotateUL("front")
        elif key=="bottom":
            self.RotateDR("front")
