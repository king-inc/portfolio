from z3 import *


# Define puzzle dimensions
ROWS = 3
COLS = 3

# Define edge colors
TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3

# Create Z3 solver
solver = Solver()

#instance puzzle to be solved
instance = [[[4,2,8,9],[2,8,6,3],[2,3,8,2]],
            [[5,8,2,7],[5,7,4,8],[8,8,7,0]],
            [[6,9,7,1],[8,3,0,8],[7,0,2,9]]]

# Define 3x3x4 matrix of integer variables
X = [[[ Int("x_%s_%s_%s" % (i, j, k)) for k in range(4) ]
      for j in range(COLS) ]
      for i in range(ROWS)
    ]

# condition that each variable is within 0-9
cell_conds = [ And(0 <= X[i][j][k], X[i][j][k] <= 9)
               for k in range(4) for j in range(COLS) for i in range(ROWS)
             ]
#constraint that edges must match (up to down, left to right)
#only top to bottom and right to left are constrained because they are the same as their opposite
edge_conds = []

# to create the constraint we loop through entire puzzle (columns and rows)
for i in range(ROWS):
  for j in range (COLS):
		#if not the first row in the puzzle
    if i>0:
      #add constraint to edge_conds to ensure top is equal to bottom
      edge_conds.append(X[i][j][TOP] == X[i-1][j][BOTTOM])
    #if not the last column in the puzzle
    if j<COLS-1:
			#add constraint to edge_conds to ensure right is equal to left
      edge_conds.append(X[i][j][RIGHT] == X[i][j+1][LEFT])

#constraint to ensure blocks from instance puzzle to be the same as in solved puzzle 
block_conds = []

#loop through entire puzzle
for i in range(ROWS):
	for j in range(COLS):
		#create an array to store each blocks of the instance condition with each blocks of the solving puzzle
		each_block_conds = []
		#loop through the puzzle again to compare each block in instance puzzle to all blocks of the solving puzzle
		for k in range(ROWS):
			for l in range(COLS):
				#add condition where they are all the same as the instance block
				each_block_conds.append(And(X[k][l][TOP] == instance[i][j][TOP],X[k][l][RIGHT] == instance[i][j][RIGHT],X[k][l][BOTTOM] == instance[i][j][BOTTOM],X[k][l][LEFT] == instance[i][j][LEFT] ))
		#append to block_conds with Or to ensure only one block in the instance puzzle would be the same assolved puzzle
		block_conds.append(Or(each_block_conds))

#add conditions to the solver
solver.add(cell_conds + edge_conds + block_conds)
#print(solver)
if solver.check() == sat:
  model = solver.model()
  solution = [[[model.evaluate(X[i][j][k]) for k in range(4)] for j in range(COLS)] for i in range(ROWS)]
  print ("Given Instance ")
	#print instance
  for i in range(ROWS):
      print("  " + str(instance[i][0][TOP])+ "   |   " + str(instance[i][1][TOP])+ "   |   " + str(instance[i][2][TOP]) + "  ")
      print(str(instance[i][0][LEFT]) + "   " + str(instance[i][0][RIGHT]) + " | " +str(instance[i][1][LEFT])+"   "+str(instance[i][1][RIGHT])+ " | " +str(instance[i][2][LEFT])+"   "+str(instance[i][2][RIGHT]))
      print("  " + str(instance[i][0][BOTTOM])+ "   |   " + str(instance[i][1][BOTTOM])+ "   |   " + str(instance[i][2][BOTTOM]) + "  ")
      print("----------------------")

  
  print ("Solution found: ")
	#print solution
  for i in range(ROWS):
      print("  " + str(solution[i][0][TOP])+ "   |   " + str(solution[i][1][TOP])+ "   |   " + str(solution[i][2][TOP]) + "  ")
      print(str(solution[i][0][LEFT]) + "   " + str(solution[i][0][RIGHT]) + " | " +str(solution[i][1][LEFT])+"   "+str(solution[i][1][RIGHT])+ " | " +str(solution[i][2][LEFT])+"   "+str(solution[i][2][RIGHT]))
      print("  " + str(solution[i][0][BOTTOM])+ "   |   " + str(solution[i][1][BOTTOM])+ "   |   " + str(solution[i][2][BOTTOM]) + "  ")
      print("----------------------")

else:
    print("No solution found")

