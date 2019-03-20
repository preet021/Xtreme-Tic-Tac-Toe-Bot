import time
import random
import copy

class Team7():
	def __init__(self):
		self.INF = 99999999999999999999
		self.t = 0

	def move(self, board, old_move, flag):
		opp = 'o' if flag == 'x' else 'x'
		self.t = time.time()
		return self.minimax(board, 0, True, -self.INF, self.INF, old_move, flag, opp, 5)[1]

	def minimax(self, node, depth, is_max_player, alpha, beta, old_move, flag, opp, max_depth):

		if (depth >= max_depth) or (node.find_terminal_state()[1] is not '-') or (time.time() - self.t > 23.9):
			return self.utility(node, flag, opp), (-1, -1, -1)

		best = 0
		cells = node.find_valid_move_cells(old_move)
		best_move = cells[random.randrange(len(cells))]
		
		if len(cells) > 18:
			max_depth = depth + 1
		
		if is_max_player:
			best = -self.INF
			for c in cells:
				temp = copy.deepcopy(node)
				temp.update(old_move, c, flag)
				val = self.minimax(temp, depth + 1, False, alpha, beta, c, flag, opp, max_depth)
				if val[0] > best:
					best = val[0]
					best_move = c
				alpha = max(alpha, best)
				del temp
				if beta <= alpha:
					break
				
		else:
			best = self.INF
			for c in cells:
				temp = copy.deepcopy(node)
				temp.update(old_move, c, opp)
				val = self.minimax(temp, depth + 1, True, alpha, beta, c, flag, opp, max_depth)
				if best > val[0]:
					best = val[0]
					best_move = c
				beta = min(beta, best)
				del temp
				if beta <= alpha:
					break

		return best, best_move

	def utility(self, board, flag, opp):
		value = 0
		for k in range(2):
			
			bs = board.small_boards_status[k]

			# horizontal
			for i in range(3):
				cx = cd = co = 0
				for j in range(3):	
					if bs[i][j] == flag:
						cx += 1
					elif bs[i][j] == opp:
						co += 1
					else:
						cd += 1
				if cx == 1 and cd == 2:
					value += 200
				elif cx == 2 and cd == 1:
					value += 1000
				elif cx == 2 and co == 1:
					value += -10000
				elif cx == 3:
					value += 500000
				elif co == 1 and cd == 2:
					value += -200
				elif co == 2 and cd == 1:
					value += -1500
				elif co == 2 and cx == 1:
					value += 20000
				elif co == 3:
					value += -500000

			# vertical
			for i in range(3):
				cx = cd = co = 0
				for j in range(3):
					if bs[j][i] == flag:
						cx += 1
					elif bs[j][i] == opp:
						co += 1
					else:
						cd += 1
				if cx == 1 and cd == 2:
					value += 200
				elif cx == 2 and cd == 1:
					value += 1000
				elif cx == 2 and co == 1:
					value += -10000
				elif cx == 3:
					value += 500000
				elif co == 1 and cd == 2:
					value += -200
				elif co == 2 and cd == 1:
					value += -1500
				elif co == 2 and cx == 1:
					value += 20000
				elif co == 3:
					value += -500000

			# diagonals
			cx = cd = co = 0
			for i in range(3):
				if bs[i][i] == flag:
					cx += 1
				elif bs[i][i] == opp:
					co += 1
				else:
					cd += 1
			if cx == 1 and cd == 2:
				value += 200
			elif cx == 2 and cd == 1:
				value += 1000
			elif cx == 2 and co == 1:
					value += -10000
			elif cx == 3:
				value += 500000
			elif co == 1 and cd == 2:
				value += -200
			elif co == 2 and cd == 1:
				value += -1500
			elif co == 2 and cx == 1:
					value += 20000
			elif co == 3:
				value += -50000

			i = 0
			j = 2
			cx = cd = co = 0
			for t in range(3):
				if bs[i][j] == flag:
					cx += 1
				elif bs[i][j] == opp:
					co += 1
				else:
					cd += 1
				i += 1
				j -= 1
			if cx == 1 and cd == 2:
				value += 200
			elif cx == 2 and cd == 1:
				value += 1000
			elif cx == 2 and co == 1:
					value += -10000
			elif cx == 3:
				value += 500000
			elif co == 1 and cd == 2:
				value += -200
			elif co == 2 and cd == 1:
				value += -1500
			elif co == 2 and cx == 1:
					value += 20000
			elif co == 3:
				value += -500000

			bs = board.big_boards_status[k]
			for x in range(0,9,3):
				for y in range(0,9,3):

					# horizontal
					for i in range(x,x+3):
						cx = co = cd = 0
						for j in range(y,y+3):
							if bs[i][j] == flag:
								cx += 1
							elif bs[i][j] == opp:
								co += 1
							else:
								cd += 1
						if cx == 2 and cd == 1:
							value += 5
						elif cx == 2 and co == 1:
							value += -20
						elif co == 2 and cd == 1:
							value += -20
						elif co == 2 and cx == 1:
							value += 20

					# vertical
					for i in range(x,x+3):
						cx = cd = co = 0
						for j in range(y,y+3):
							if bs[j][i] == flag:
								cx += 1
							elif bs[j][i] == opp:
								co += 1
							else:
								cd += 1
						if cx == 2 and cd == 1:
							value += 5
						elif cx == 2 and co == 1:
							value += -20
						elif co == 2 and cd == 1:
							value += -20
						elif co == 2 and cx == 1:
							value += 20

					# diagonals
					cx = cd = co = 0
					i = x
					j = y
					for t in range(3):
						if bs[i][j] == flag:
							cx += 1
						elif bs[i][j] == opp:
							co += 1
						else:
							cd += 1
						i += 1
						j += 1
					if cx == 2 and cd == 1:
						value += 5
					elif cx == 2 and co == 1:
						value += -20
					elif co == 2 and cd == 1:
						value += -20
					elif co == 2 and cx == 1:
						value += 20

					cx = cd = co = 0
					i = x
					j = y + 2
					for t in range(3):
						if bs[i][j] == flag:
							cx += 1
						elif bs[i][j] == opp:
							co += 1
						else:
							cd += 1
						i += 1
						j -= 1
					if cx == 2 and cd == 1:
						value += 5
					elif cx == 2 and co == 1:
						value += -20
					elif co == 2 and cd == 1:
						value += -20
					elif co == 2 and cx == 1:
						value += 20

		return value
