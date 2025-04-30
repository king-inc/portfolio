from Classes.HelperFunctions import *
import numpy as np

rubiks_cube = CreateCube()
rubiks_cube.PrintCube()
#rubiks_cube= ScatterCube(rubiks_cube, 4)
rubiks_cube.PrintCube()
#SolveWithSetMoves(rubiks_cube,reversed(moves))
PerformAction(rubiks_cube,7).PrintCube()
#print(np.shape(rubiks_cube.faces))
#rubiks_cube = SolveCubeRandom(rubiks_cube)

#SuneSolver(rubiks_cube)
#back = rubiks_cube.GetFaceFromPos("back")
#front = rubiks_cube.GetFaceFromPos("front")
#print(rubiks_cube.faces[back].GetColor()) 
#print(rubiks_cube.faces[front].GetColor())
#print(rubiks_cube.faces[back].GetNodes()[0][0].GetColors()[0])
#print(rubiks_cube.faces[front].GetNodes()[0][0].GetColors()[0])
            
            
        