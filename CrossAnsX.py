#MinMax based AI Agent for Tic Tac toe game
#Author: Bhavya Saraf
#The program has been written for an arbitrary n dimensional game
#A  Heuristic has been written to predict the utility of a non terminal state
#with precision. The use of heuristic is to prevent the AI agent from taking 
#Very large amount of time

import math

board = [[2,2,2] for i in range(3)]
dimension = 3
depthLimit = 0
maxIterations = 100000

#Note:
#if board[i][j] == 0: the corresponding coordinates contain 'x'
#if board[i][j] == 1: the corresponding coordinates contain 'o'
#if board[i][j] == 2: the corresponding coordinates contain ' '

#Use to draw board with given dimensions on the console
def DrawBoard(board, dimension):
	adjustment = dimension - 1
	dimension = len(board)
	for i in range(dimension):
		for j in range(4*dimension + adjustment):
			print('_', end='')
		print()
		for j in range(dimension):
			if board[i][j] == 0:
				print(" x | ", end="")
			elif board[i][j] == 1:
				print(" o | ", end="")
			else:
				print("   | ", end="")

		for j in range(dimension):
			print(i,end='')
			print(j,end=' ')

		print()
	for j in range(4*dimension + adjustment):
	 	print('_', end='')
	print()

#Take coordinates from the human player
def PlayerMove():
	global board
	global dimension
	print("Enter the coordinates in the ")
	while True:
		inputCoordinates = list(map(int, input().split()))
		if len(inputCoordinates) != 2:
			print('Please Enter Valid numbers!')
			continue
		if inputCoordinates[0] < 0 or inputCoordinates[1] < 0:
			print('Please Enter Valid numbers!')
			continue
		if inputCoordinates[0] >= dimension or inputCoordinates[1] >= dimension:
			print('Please Enter Valid numbers!')
			continue
		if board[inputCoordinates[0]][inputCoordinates[1]] != 2:
			print('Please Enter in an unfilled cell')
			continue
		board[inputCoordinates[0]][inputCoordinates[1]] = 0
		break

#To determine if any of the player has won, tie or no termination as of now
#Returns 0 if 'x' or human agent has won
#Returns 1 if 'o' or AI agent has won
#Returns -1 if draw
#Returns 2 if game not yet terminated
def IsVictory(board, dimension):
	numUnfilled = 0
	ctr = [0 for i in range(9)]
	for i in range(dimension):
		ctr[1] = 0
		ctr[2] = 0
		ctr[3] = 0
		ctr[4] = 0
		for j in range(dimension):

			if board[i][j] == 2:
				numUnfilled = numUnfilled + 1

			if board[i][j] == 0:
				ctr[1] = ctr[1] + 1

			if board[i][j] == 1:
				ctr[2] = ctr[2] + 1

			if board[j][i] == 0:
				ctr[3] = ctr[3] + 1

			if board[j][i] == 1:
				ctr[4] = ctr[4] + 1

		if board[i][i] == 0:
			ctr[5] = ctr[5] + 1

		if board[i][i] == 1:
			ctr[6] = ctr[6] + 1

		if board[i][dimension-i-1] == 0:
			ctr[7] = ctr[7] + 1

		if board[i][dimension-i-1] == 1:
			ctr[8] = ctr[8] + 1

		if ctr[1] == dimension or ctr[3] == dimension or ctr[5] == dimension or ctr[7] == dimension:
			return 0
		if ctr[2] == dimension or ctr[4] == dimension or ctr[6] == dimension or ctr[8] == dimension:
			return 1
	if numUnfilled == 0:
		return -1
	return 2

#Heuristic function
#Returns probable utility, maxScore and minScore (in the same order)
#If minScore > maxScore, utility = -1 (Bad for the AI agent hence negative)
#If minScore < maxScore, utility =  1 (Good for the AI agent hence positive)
#if minScore == maxScore, utility = 0 (Assuming tie)
def Heuristic(board, dimension, chance):
	winStatus = IsVictory(board, dimension)
	if winStatus == 0: return -1,0,10000
	if winStatus == 1: return 1,10000,0
	if winStatus == -1: return 0,0,0

	scoreMinAgent = 0
	scoreMaxAgent = 0

	ctr = [0 for i in range(9)]

	for i in range(dimension):
		
		ctr[1] = 0
		ctr[2] = 0
		ctr[3] = 0
		ctr[4] = 0
		
		for j in range(dimension):
			if board[i][j] == 0:
				ctr[1] = ctr[1] + 1
			if board[i][j] == 1:
				ctr[2] = ctr[2] + 1

			if board[j][i] == 0:
				ctr[3] = ctr[3] + 1
			if board[j][i] == 1:
				ctr[4] = ctr[4] + 1

		if board[i][i] == 0:
			ctr[5] = ctr[5] + 1
		if board[i][i] == 1:
			ctr[6] = ctr[6] + 1
		if board[i][dimension-i-1] == 0:
			ctr[7] = ctr[7] + 1
		if board[i][dimension-i-1] == 1:
			ctr[8] = ctr[8] + 1

		if ctr[1] + ctr[2] != dimension:
			#If a row consists of only x's
			if ctr[1] != 0 and ctr[2] == 0:
				#Obvious win condition for 'x'
				if chance == 0 and dimension - ctr[1] == 1: return -1,0,10000
				scoreMinAgent = scoreMinAgent + ctr[1]
			if ctr[1] == 0 and ctr[2] != 0:
				#Obvious win condition for 'o'
				if chance == 1  and dimension - ctr[2] == 1: return 1,10000,0
				scoreMaxAgent = scoreMaxAgent + ctr[2]
		if ctr[3] + ctr[4] != dimension:
			if ctr[3] != 0 and ctr[4] == 0:
				#Obvious win condition for 'x'
				if chance == 0 and dimension - ctr[3] == 1: return -1,0,10000
				scoreMinAgent = scoreMinAgent + ctr[3]
			if ctr[3] == 0 and ctr[4] != 0:
				#Obvious win condition for 'o'
				if chance == 1  and dimension - ctr[4] == 1: return 1,10000,0
				scoreMaxAgent = scoreMaxAgent + ctr[4]
	if ctr[5] + ctr[6] != dimension:
		if ctr[5] != 0 and ctr[6] == 0:
			#Obvious win condition for 'x'
			if chance == 0 and dimension - ctr[5] == 1: return -1,0,10000
			scoreMinAgent = scoreMinAgent + ctr[5]
		if ctr[5] == 0 and ctr[6] != 0:
			#Obvious win condition for 'o'
			if chance == 1  and dimension - ctr[6] == 1: return 1,10000,0
			scoreMaxAgent = scoreMaxAgent + ctr[6]
	if ctr[7] + ctr[8] != dimension:
		if ctr[7] != 0 and ctr[8] == 0:
			#Obvious win condition for 'x'
			if chance == 0 and dimension - ctr[7] == 1: return -1,0,10000
			scoreMinAgent = scoreMinAgent + ctr[7]
		if ctr[7] == 0 and ctr[8] != 0:
			#Obvious win condition for 'o'
			if chance == 1  and dimension - ctr[8] == 1: return 1,10000,0
			scoreMaxAgent = scoreMaxAgent + ctr[8]

	if scoreMaxAgent > scoreMinAgent: return 1, scoreMaxAgent, scoreMinAgent
	elif scoreMaxAgent < scoreMinAgent: return -1, scoreMaxAgent, scoreMinAgent
	else: return 0, scoreMaxAgent, scoreMinAgent

#Changes depth of the minMax according to number of unfilled cells
def DynamicDepth(state, dimension):
	global depthLimit
	numUnfilled = 1
	for i in range(dimension):
		for j in range(dimension):
			if state[i][j] == 2:
				numUnfilled = numUnfilled + 1
	depthLimit = math.ceil(math.log(maxIterations)/math.log(numUnfilled))
	print(depthLimit)

#Returns the optimum utility and the best possible move for the minAgent
def MinAgent(state, dimension, depth):
	#If the given state is terminal state
	terminalUtitilty = IsVictory(state, dimension)
	if terminalUtitilty == 0:
		return -1, state
	if terminalUtitilty == 1:
		return 1, state
	if terminalUtitilty == -1:
		return 0, state

	#Use heuristic in case of depthLimit
	if depth >= depthLimit:
		tmpMin = 10000
		tmpMinScore = 100000
		tmpMaxScore = 100000
		probState = state
		for i in range(dimension):
			for j in range(dimension):
				if state[i][j] == 2:
					state[i][j] = 0
					judgement, maxScore, minScore = Heuristic(state, dimension, 0)
					if judgement <= tmpMin:
						tmpMin = judgement
						if tmpMaxScore >= maxScore:
							tmpMaxScore = maxScore
							if tmpMinScore <= minScore:
								tmpMinScore = minScore
								probState = [[state[i][j] for j in range(dimension)] for i in range(dimension)]
					state[i][j] = 2 
		return tmpMin, probState

	#Choose the move which has the least possible utilty 
	minVal = 1000
	requiredMove = state
	for i in range(dimension):
		for j in range(dimension):
			if state[i][j] == 2:
				state[i][j] = 0
				maxVal, otherState = MaxAgent(state, dimension, depth + 1)
				if maxVal < minVal:
					minVal = maxVal
					requiredMove = [[state[i][j] for j in range(dimension)] for i in range(dimension)]
				state[i][j] = 2
	return minVal, requiredMove

#Returns the optimum utility and the best possible move for the maxAgent 
def MaxAgent(state, dimension, depth):
	#If the given state is terminal state
	terminalUtitilty = IsVictory(state, dimension)
	if terminalUtitilty == 0:
		return -1, state
	if terminalUtitilty == 1:
		return 1, state
	if terminalUtitilty == -1:
		return 0, state

	#Use heuristic in case of depthLimit
	if depth >= depthLimit:
		tmpMax = -10000
		tmpMinScore = 100000
		tmpMaxScore = -100000
		probState = state
		for i in range(dimension):
			for j in range(dimension):
				if state[i][j] == 2:
					state[i][j] = 1
					judgement, maxScore, minScore = Heuristic(state, dimension, 1)
					if judgement >= tmpMax:
						tmpMax = judgement
						if tmpMinScore >= minScore:
							tmpMinScore = minScore
							if tmpMaxScore <= maxScore:
								tmpMaxScore = maxScore
								probState = [[state[i][j] for j in range(dimension)] for i in range(dimension)]
					state[i][j] = 2 
		return tmpMax, probState

	#Choose the move which has the best possible utilty 
	maxVal = -1000
	requiredMove = state
	for i in range(dimension):
		for j in range(dimension):
			if state[i][j] == 2:
				state[i][j] = 1
				minVal, otherState = MinAgent(state, dimension, depth + 1)
				if maxVal < minVal:
					maxVal = minVal
					requiredMove = [[state[i][j] for j in range(dimension)] for i in range(dimension)]
				state[i][j] = 2
	return maxVal, requiredMove	

#Invokes maxAgent method
def ComputerMove():
	global board
	global dimension
	tmpBoard = board
	print('Computer moves:')
	val, move = MaxAgent(tmpBoard, dimension, 0)
	board = move

#Game play
def GamePlay():
	global board
	global dimension
	dimension = int(input('Enter the dimension of play:'))
	board = [[2 for i in range(dimension)] for j in range(dimension)]
	chanceCounter = 1
	DrawBoard(board, dimension)
	while IsVictory(board, dimension) == 2:
		if chanceCounter%2 == 0:
			PlayerMove()
			DrawBoard(board, dimension)
		else:
			ComputerMove()
			DrawBoard(board, dimension)
		chanceCounter = chanceCounter + 1
	winStatus = IsVictory(board, dimension)
	if winStatus == -1:
		print('Tie')
	elif winStatus == 0:
		print('You Win')
	else:
		print('Computer Wins')

#Method for debugging purposes
def Tester():
	board = [[1,1,1,1,0],
			 [1,0,1,1,2],
			 [2,2,2,2,0],
			 [2,2,2,2,0],
			 [2,2,2,2,0]]
	
	dimension = 4
	DrawBoard(board, dimension)
	x,y,z = Heuristic(board, dimension, 0)
	print(x,y,z)
	val, selectedState = MaxAgent(board, dimension, 0)
	print(val)
	DrawBoard(selectedState, dimension)

GamePlay()