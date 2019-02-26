''' 

Naming convention followed across the simulator is:

- BigBoard = big_boards[0] + big_boards[1]

- big_board[i] = small_boards[0] + small_boards[1] + small_boards[2] + .... + small_boards[7] + small_boards[8] 

- small_board[i] = cell[0] + cell[1] + cell[2] + .... + cell[7] + cell[8]

'''

import sys
import random
import signal
import time
import copy
import traceback
from math import sqrt, log

TIME = 24
MAX_PTS = 86

class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	#print 'Signal handler called with signal', signum
	raise TimedOutExc()

class Random_Player():
	def __init__(self):
		pass

	def move(self, board, old_move, flg):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		ind = 0
		total_sims = 0
		opp = '.'
		if flg == 'x':
			opp = 'o'
		else: opp = 'x'
		temp_board = copy.deepcopy(board)
		# print temp_board.big_boards_status
		cells = temp_board.find_valid_move_cells(old_move)
		# ucb, index, wins, sims, move, flg: whos turn ?, par
		node_data = []
		INF = 999999999999999999
		root = [INF, 0, 0, 0, old_move, flg, -1]
		node_data.append(root)
		ind = 1
		adj = [[]]
		for cell in cells:
			node_data.append([INF, ind, 0, 0, cell, opp, 0])
			adj[0].append([INF, ind, 0, 0, cell, opp, 0])
			adj.append([])
			ind += 1
		ply = opp
		for i in range(700):

			cur = 0
			temp_board = copy.deepcopy(board)

			# selection
			while len(adj[cur]) != 0:
				for i in range(len(adj[cur])):
					adj[cur][i] = node_data[adj[cur][i][1]]
				adj[cur].sort()
				if ply == flg: ply = opp
				else: ply = flg
				cur = adj[cur][len(adj[cur])-1][1]
				temp_board.big_boards_status[node_data[cur][4][0]][node_data[cur][4][1]][node_data[cur][4][2]] = ply
			
			# expansion
			if node_data[cur][3] != 0:
				cells = temp_board.find_valid_move_cells(node_data[cur][4])
				for cell in cells:
					node_data.append([INF, ind, 0, 0, cell, opp, cur])
					adj[cur].append([INF, ind, 0, 0, cell, opp, cur])
					adj.append([])
					ind += 1
				cur = adj[cur][0][1]

			# simulation
			sim_board = copy.deepcopy(temp_board)
			temp_cur = cur
			prev_move = node_data[temp_cur][4]
			to_break = False
			score = 0
			it=0

			x, status = '', ''
			while not to_break:
				cells = sim_board.find_valid_move_cells(prev_move)
				cell = cells[random.randrange(len(cells))]
				if ply == flg: ply = opp
				else: ply = flg
				sim_board.big_boards_status[cell[0]][cell[1]][cell[2]] = ply
				prev_move = cell
				# print it, sim_board.big_boards_status
				x, status = board.find_terminal_state(sim_board)
				it += 1
				if status == 'WON':
					to_break = True
					score = 10
				elif status == 'DRAW':
					to_break = True
					score = 5

			# back propogation
			total_sims += 1
			to_inc = 1
			while temp_cur is not -1:
				if status == 'WON':
					if to_inc:
						node_data[temp_cur][2] += score
						to_inc = 1 - to_inc
				else:
					node_data[temp_cur][2] += score
				node_data[temp_cur][3] += 1
				temp_cur = node_data[temp_cur][6]

			# update ucb
			for node in node_data:
				if node[3] == 0:
					node[0] = INF
				else:
					node[0] = node[2] / node[3] + 4*sqrt(log(total_sims)/node[3])	

		mx = -1
		ans_ind = -1
		for i in adj[0]:
			i = node_data[i[1]]
			if i[3] and i[2]/i[3] > mx:
				mx = i[2]/i[3]
				ans_ind = i[1]

		return node_data[ans_ind][4]

class BigBoard:

	def __init__(self):
		# big_boards_status is the game board
		# small_boards_status shows which small_boards have been won/drawn and by which player
		self.big_boards_status = ([['-' for i in range(9)] for j in range(9)], [['-' for i in range(9)] for j in range(9)])
		self.small_boards_status = ([['-' for i in range(3)] for j in range(3)], [['-' for i in range(3)] for j in range(3)])

	def print_board(self):
		# for printing the state of the board
		print '================BigBoard State================'
		for i in range(9):
			if i%3 == 0:
				print
			for k in range(2):
				for j in range(9):
					if j%3 == 0:
						print "",
					print self.big_boards_status[k][i][j],
				if k==0:
					print "   ",
			print
		print

		print '==============SmallBoards States=============='
		for i in range(3):
			for k in range(2):
				for j in range(3):
					print self.small_boards_status[k][i][j],
				if k==0:
					print "  ",
			print
		print '=============================================='
		print
		print

	def check_small_board_allowed(self, b):
		players = ['x', 'o']
		for ply in players:
		
			# diagonals
			if (b[0] == b[4] == b[8] == ply) or (b[2] == b[4] == b[6] == ply):
				return False, ply

			# horizontal
			if (b[0] == b[1] == b[2] == ply) or (b[3] == b[4] == b[5] == ply) or (b[6] == b[7] == b[8] == ply):
				return False, ply

			# vertical
			if (b[0] == b[3] == b[6] == ply) or (b[1] == b[4] == b[7] == ply) or (b[2] == b[5] == b[8] == ply):
				return False, ply

		if '-' not in b:
			return False, 'd'
		return True, '-'

	def find_valid_move_cells(self, old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		x = 3*(old_move[1]%3)
		y = 3*(old_move[2]%3)
		small_boards = []
		for k in range(2):
			arr = []
			for i in range(x,x+3):
				for j in range(y,y+3):
					arr.append(self.big_boards_status[k][i][j])
			small_boards.append(arr)
		
		players = ['x', 'o']
		small_board_allowed = [True, True]
		
		for i in range(len(small_boards)):
			small_board_allowed[i], winner = self.check_small_board_allowed(small_boards[i])

		if (small_board_allowed[0] == small_board_allowed[1] == False): # open move
			# print "open"
			for k in range(2):
				for x in range(0, 9, 3):
					for y in range(0, 9, 3):
						b = []
						for i in range(x,x+3):
							for j in range(y,y+3):
								b.append(self.big_boards_status[k][i][j])
						ret, winner = self.check_small_board_allowed(b)
						if ret:
							for i in range(x,x+3):
								for j in range(y,y+3):
									if self.big_boards_status[k][i][j] == '-':
										allowed_cells.append((k, i, j))							

		else:
			# print "close"
			for i in range(len(small_boards)):
				if small_board_allowed[i]:
					b = small_boards[i]
					for j in range(9):
						if b[j] == '-':
							allowed_cells.append((i, x+j/3, y+j%3))

		return allowed_cells

	def find_terminal_state(self, board):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher small_boards in case of a draw
		status = [[['-' for i in range(3)] for j in range(3)] for k in range(2)]
		for k in range(2):
			for x in range(0, 9, 3):
				for y in range(0, 9, 3):
					b = []
					for i in range(x,x+3):
						for j in range(y,y+3):
							b.append(board.big_boards_status[k][i][j])
					ret, winner = self.check_small_board_allowed(b)
					status[k][x/3][y/3] = winner

		# print status[0], status[1]
		reult1, winner1 = self.check_small_board_allowed([j for sub in status[0] for j in sub])
		reult2, winner2 = self.check_small_board_allowed([j for sub in status[1] for j in sub])

		if not reult1:
			return winner1, 'WON'
		if not reult2:
			return winner2, 'WON'
		if ('-' not in [j for sub in status[0] for j in sub]) and ('-' not in [j for sub in status[1] for j in sub]):
			return 'NONE', 'DRAW'
		return 'CONTINUE', '-'

if __name__ == '__main__':

	board = BigBoard()
	my_bot = Random_Player()
	turn = 1 # bot's turn
	old_move = (-1, -1, -1)

	while 1:
		board.print_board()
		print old_move
		if turn == 0:
			turn = 1
			old_move = my_bot.move(board, old_move, 'x')
			board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] = 'x'
		else:
			turn = 0
			a, b, c = raw_input().split()
			old_move = (int(a), int(b), int(c))
			board.big_boards_status[int(a)][int(b)][int(c)] = 'o'
