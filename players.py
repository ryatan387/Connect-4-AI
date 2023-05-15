import random
import time
import pygame
import math

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):
	def checkTerminal(self, env, player):
		#horizontal
		for r in range(ROW_COUNT):
			row_arr = [int(i) for i in list(env.board[r,:])]
			for c in range(COLUMN_COUNT-3):
				grouping_four = row_arr[c:c+4]
				if grouping_four.count(player) == 4:
					return True
		#vertical
		for c in range(COLUMN_COUNT):
			col_arr = [int(i) for i in list(env.board[:,c])]
			for r in range(ROW_COUNT-3):
				grouping_four = col_arr[r:r+4]
				if grouping_four.count(player) == 4:
					return True
		#slope pos
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				grouping_four = [env.board[r+i][c+i] for i in range(4)]
				if grouping_four.count(player) == 4:
					return True
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				grouping_four = [env.board[r+3-i][c+i] for i in range(4)]
				if grouping_four.count(player) == 4:
					return True
		return False

	def scoring(self, grouping_four, env):
		switch = {1:2,2:1}
		opp_position = switch[self.position]
		score=0
		if grouping_four.count(self.position) == 4:
			score+=100
		elif grouping_four.count(self.position) == 3 and grouping_four.count(0) == 1:
			score+=5	
		elif grouping_four.count(self.position) == 2 and grouping_four.count(0) == 2:
			score+=2
		if grouping_four.count(opp_position) == 3 and grouping_four.count(0) == 1:
			score-=6
		elif grouping_four.count(opp_position) == 2 and grouping_four.count(0) == 2:
			score-=3
		return score

	def eval_func(self, env):
		score=0
		#center pref
		center_array = [int(i) for i in list(env.board[:, COLUMN_COUNT//2])]
		center_count = center_array.count(self.position)
		score+= center_count*6.5
		#horizontal
		for r in range(ROW_COUNT):
			row_arr = [int(i) for i in list(env.board[r,:])]
			for c in range(COLUMN_COUNT-3):
				grouping_four = row_arr[c:c+4]
				score+=self.scoring(grouping_four, env)
		#vertical
		for c in range(COLUMN_COUNT):
			col_arr = [int(i) for i in list(env.board[:,c])]
			for r in range(ROW_COUNT-3):
				grouping_four = col_arr[r:r+4]
				score+=self.scoring(grouping_four, env)
		#slope pos
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				grouping_four = [env.board[r+i][c+i] for i in range(4)]
				score+=self.scoring(grouping_four, env)
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				grouping_four = [env.board[r+3-i][c+i] for i in range(4)]
				score+=self.scoring(grouping_four, env)
		return score

	def minimax(self , env, depth, maximizingPlayer):
		#possible moves
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		#check if terminal node
		switch = {1:2,2:1}
		opp_position = switch[self.position]
		terminalNode=self.checkTerminal(env, self.position) or self.checkTerminal(env, opp_position)
		if depth == 0 or terminalNode or not indices:
			if terminalNode:
				if self.checkTerminal(env ,opp_position):
					return (None, -1000000)
				elif self.checkTerminal(env ,self.position):
					return (None, 1000000)
				else:
					return (None, 0)
			else:
				return (None, self.eval_func(env))
		if maximizingPlayer:
			optimalCol = random.choice(indices)
			value = -math.inf
			for col in indices:
				#simulate move
				temp_env=env.getEnv()
				temp_env.board[env.topPosition[col]][col] = self.position
				temp_env.topPosition[col] -= 1
				temp_env.history[0].append(col)
				heuristicValue = self.minimax(temp_env, depth-1, False)[1]
				if heuristicValue > value:
					value = heuristicValue
					optimalCol = col
			return optimalCol, value
		else: #min
			optimalCol = random.choice(indices)
			value = math.inf
			for col in indices:
				#simulate move
				temp_env=env.getEnv()
				temp_env.board[env.topPosition[col]][col] = opp_position
				temp_env.topPosition[col] -= 1
				temp_env.history[0].append(col)
				heuristicValue = self.minimax(temp_env, depth-1, True)[1]
				if heuristicValue < value:
					value = heuristicValue
					optimalCol = col
			return optimalCol, value

	def play(self, env, move):
		temp_env= env.getEnv()
		col=self.minimax(temp_env, 2, True)[0]
		move[:] = [col]

class alphaBetaAI(connect4Player):
	def checkTerminal(self, env, player):
		#horizontal
		for r in range(ROW_COUNT):
			row_arr = [int(i) for i in list(env.board[r,:])]
			for c in range(COLUMN_COUNT-3):
				grouping_four = row_arr[c:c+4]
				if grouping_four.count(player) == 4:
					return True
		#vertical
		for c in range(COLUMN_COUNT):
			col_arr = [int(i) for i in list(env.board[:,c])]
			for r in range(ROW_COUNT-3):
				grouping_four = col_arr[r:r+4]
				if grouping_four.count(player) == 4:
					return True
		#slope pos
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				grouping_four = [env.board[r+i][c+i] for i in range(4)]
				if grouping_four.count(player) == 4:
					return True
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				grouping_four = [env.board[r+3-i][c+i] for i in range(4)]
				if grouping_four.count(player) == 4:
					return True
		return False

	def eval_func(self, env):
		score=0
		switch = {1:2,2:1}
		opp_position = switch[self.position]
		#center pref
		center_array = [int(i) for i in list(env.board[:, COLUMN_COUNT//2])]
		center_count = center_array.count(self.position)
		score+= center_count*6.5
		#horizontal
		for r in range(ROW_COUNT):
			row_arr = [int(i) for i in list(env.board[r,:])]
			for c in range(COLUMN_COUNT-3):
				grouping_four = row_arr[c:c+4]
				if grouping_four.count(self.position) == 3 and grouping_four.count(0) == 1:
					score+=5
				elif grouping_four.count(self.position) == 2 and grouping_four.count(0) == 2:
					score+=2
				if grouping_four.count(opp_position) == 3 and grouping_four.count(0) == 1:
					score-=6
				elif grouping_four.count(opp_position) == 2 and grouping_four.count(0) == 2:
					score-=3
		#vertical
		for c in range(COLUMN_COUNT):
			col_arr = [int(i) for i in list(env.board[:,c])]
			for r in range(ROW_COUNT-3):
				grouping_four = col_arr[r:r+4]
				if grouping_four.count(self.position) == 3 and grouping_four.count(0) == 1:
					score+=5	
				elif grouping_four.count(self.position) == 2 and grouping_four.count(0) == 2:
					score+=2
				if grouping_four.count(opp_position) == 3 and grouping_four.count(0) == 1:
					score-=6
				elif grouping_four.count(opp_position) == 2 and grouping_four.count(0) == 2:
					score-=3
		#positive diagonals
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				grouping_four = [env.board[r+i][c+i] for i in range(4)]
				if grouping_four.count(self.position) == 3 and grouping_four.count(0) == 1:
					score+=5	
				elif grouping_four.count(self.position) == 2 and grouping_four.count(0) == 2:
					score+=2
				if grouping_four.count(opp_position) == 3 and grouping_four.count(0) == 1:
					score-=6
				elif grouping_four.count(opp_position) == 2 and grouping_four.count(0) == 2:
					score-=3
		#negative diagonals
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				grouping_four = [env.board[r+3-i][c+i] for i in range(4)]
				if grouping_four.count(self.position) == 3 and grouping_four.count(0) == 1:
					score+=5	
				elif grouping_four.count(self.position) == 2 and grouping_four.count(0) == 2:
					score+=2
				if grouping_four.count(opp_position) == 3 and grouping_four.count(0) == 1:
					score-=6
				elif grouping_four.count(opp_position) == 2 and grouping_four.count(0) == 2:
					score-=3
		return score

	def alphabeta(self, env, depth, alpha, beta, maximizingPlayer):
		#possible moves
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		#check if terminal node
		switch = {1:2,2:1}
		opp_position = switch[self.position]
		terminalNode=self.checkTerminal(env, self.position) or self.checkTerminal(env, opp_position)
		if depth == 0 or terminalNode or not indices:
			if terminalNode:
				if self.checkTerminal(env ,opp_position):
					return (None, -10000000)
				elif self.checkTerminal(env ,self.position):
					return (None, 10000000)
				else:
					return (None, 0)
			else:
				return (None, self.eval_func(env))
		#successor function
		successor = []
		while len(indices) != 0:
			successor.append(indices[math.floor(len(indices)/2)])
			indices.remove(indices[math.floor(len(indices)/2)])
		if maximizingPlayer:
			optimalCol = random.choice(successor)
			value = -math.inf
			#succesor function
			for col in successor:
				#simulate move
				temp_env=env.getEnv()
				temp_env.board[env.topPosition[col]][col] = self.position
				temp_env.topPosition[col] -= 1
				temp_env.history[0].append(col)
				heuristicValue = self.alphabeta(temp_env, depth-1, alpha, beta, False)[1]
				if heuristicValue > value:
					value = heuristicValue
					optimalCol = col
				if value >= beta:
					break
				alpha = max(alpha,value)
			return optimalCol, value
		else: #min
			optimalCol = random.choice(successor)
			value = math.inf
			#succesor function
			for col in successor:
				#simulate move
				temp_env=env.getEnv()
				temp_env.board[env.topPosition[col]][col] = opp_position
				temp_env.topPosition[col] -= 1
				temp_env.history[0].append(col)
				heuristicValue = self.alphabeta(temp_env, depth-1, alpha, beta, True)[1]
				if heuristicValue < value:
					value = heuristicValue
					optimalCol = col
				if value <= alpha:
					break
				beta = min(beta,value)
			return optimalCol, value

	def play(self, env, move):
		temp_env= env.getEnv()
		if env.topPosition[3]==5:
			move[:]=[3]
			return
		col=self.alphabeta(temp_env, 4, -math.inf, math.inf, True)[0]	
		move[:] = [col]

SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)





