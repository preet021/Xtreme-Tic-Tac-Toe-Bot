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
		temp_board = board
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
		cur = 0
		for i in range(10):

			while len(adj[cur]) != 0:
				for i in adj[cur]:
					i = node_data[i[1]]
				adj[cur].sort()
				if ply == flg: ply = opp
				else: ply = flg
				cur = adj[cur][len(adj[cur])-1][1]
				temp_board.big_boards_status[node_data[cur][4][0]][node_data[cur][4][1]][node_data[cur][4][2]] = ply

			if node_data[cur][3] != 0:  # expand
				cells = temp_board.find_valid_move_cells(node_data[cur][4])
				for cell in cells:
					node_data.append([INF, ind, 0, 0, cell, opp, cur])
					adj[cur].append([INF, ind, 0, 0, cell, opp, cur])
					adj.append([])
					ind += 1
				cur = adj[cur][0][1]

			# run simulation
			sim_board = temp_board
			temp_cur = cur
			prev_move = node_data[temp_cur][4]
			to_break = False
			score = 0

			while not to_break:
				cells = sim_board.find_valid_move_cells(prev_move)
				if len(cells) == 0:
					sim_board.print_board()
				cell = cells[random.randrange(len(cells))]
				if ply == flg: ply = opp
				else: ply = flg
				# update temp board
				sim_board.big_boards_status[cell[0]][cell[1]][cell[2]] = ply
				prev_move = cell
				x, status = board.find_terminal_state(sim_board)
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
				if to_inc:
					node_data[temp_cur][2] += score
					to_inc = 1 - to_inc
				node_data[temp_cur][3] += 1
				temp_cur = node_data[temp_cur][6]

			# update ucb
			for node in node_data:
				if node[3] == 0:
					node[0] = INF
				else:
					node[0] = node[2] / node[3] + sqrt(2*log(total_sims)/node[3])	

		mx = -1
		ans_ind = -1
		for i in adj[0]:
			i = node_data[i[1]]
			if i[0] > mx:
				mx = i[0]
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

	def find_valid_move_cells(self, old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		allowed_small_board = [old_move[1]%3, old_move[2]%3]
		
		

		return allowed_cells

	def find_terminal_state(self, board):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher small_boards in case of a draw

		cntx = 0
		cnto = 0
		cntd = 0
	
		for k in range(2):
			bs = self.small_boards_status[k]
			for i in range(3):
				for j in range(3):
					if bs[i][j] == 'x':
						cntx += 1
					if bs[i][j] == 'o':
						cnto += 1
					if bs[i][j] == 'd':
						cntd += 1
			for i in range(3):
				row = bs[i]
				col = [x[i] for x in bs]
				#print row,col
				#checking if i'th row or i'th column has been won or not
				if (row[0] =='x' or row[0] == 'o') and (row.count(row[0]) == 3):	
					return (row[0],'WON')
				if (col[0] =='x' or col[0] == 'o') and (col.count(col[0]) == 3):
					return (col[0],'WON')
			#check diagonals
			if(bs[0][0] == bs[1][1] == bs[2][2]) and (bs[0][0] == 'x' or bs[0][0] == 'o'):
				return (bs[0][0],'WON')
			if(bs[0][2] == bs[1][1] == bs[2][0]) and (bs[0][2] == 'x' or bs[0][2] == 'o'):
				return (bs[0][2],'WON')

		if cntx+cnto+cntd < 18:		#if all small_boards have not yet been won, continue
			return ('CONTINUE', '-')
		elif cntx+cnto+cntd == 18:							#if game is drawn
			return ('NONE', 'DRAW')

if __name__ == '__main__':

	board = BigBoard()
	big_boards = (board.big_boards_status)
	small_boards = (board.small_boards_status)
	my_bot = Random_Player()
	turn = 0 # bot's turn
	old_move = (-1, -1, -1)

	while 1:
		board.print_board()
		if turn == 0:
			turn = 1
			old_move = my_bot.move(board, old_move, 'x')
		else:
			a, b, c = raw_input().split()
			old_move = (int(a), int(b), int(c))
			big_boards[a][b][c] = 'o'
		board.big_boards_status = big_boards
		board.small_boards_status = small_boards
