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
TIME = 24000
MAX_PTS = 86

class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	#print 'Signal handler called with signal', signum
	raise TimedOutExc()

class Team7():
	def __init__(self):
		self.INF = 99999999999999999999

	def move(self, board, old_move, flag):
		opp = 'o' if flag == 'x' else 'x'
		return self.minimax(board, 0, True, -self.INF, self.INF, old_move, flag, opp)[1]

	def minimax(self, node, depth, is_max_player, alpha, beta, old_move, flag, opp):
		
		if (depth >= 2) or (node.find_terminal_state()[1] is not '-'):
			return self.utility(node, flag, opp), (-1, -1, -1)

		best = 0
		# print depth
		# print old_move
		# print "minimax"
		# print node.print_board()
		cells = node.find_valid_move_cells(old_move)
		# print cells
		# print "over---------"
		best_move = cells[random.randrange(len(cells))]
		
		if is_max_player:
			best = -self.INF
			for c in cells:
				temp = copy.deepcopy(node)
				temp.update(old_move, c, flag)
				val = self.minimax(temp, depth + 1, False, alpha, beta, c, flag, opp)
				if val[0] > best:
					best = val[0]
					best_move = c
				alpha = max(alpha, best)
				del temp
				if beta <= alpha:
					break
				
		else:
			ply = 'o'
			best = self.INF
			for c in cells:
				temp = copy.deepcopy(node)
				temp.update(old_move, c, opp)
				val = self.minimax(node, depth + 1, True, alpha, beta, c, flag, opp)
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
		sf = [[[0 for i in range(3)] for j in range(3)] for k in range(2)]
		for k in range(2):
			bs = board.small_boards_status[k]

			# horizontal
			for i in range(3):
				cx = cd = co = 0
				pd = []
				for j in range(3):	
					if bs[i][j] == flag:
						cx += 1
					elif bs[i][j] == opp:
						co += 1
					else:
						cd += 1
						pd.append(j)
				if cx == 0 and cd == 3:
					for ind in range(3):
						sf[k][i][ind] = max(sf[k][i][ind], abs(random.random()-random.random()))
				elif cx == 1 and cd == 2:
					for ind in pd:
						sf[k][i][ind] = max(sf[k][i][ind], 1)
					value += 100
				elif cx == 2 and cd == 1:
					for ind in pd:
						sf[k][i][ind] = max(sf[k][i][ind], 2)
					value += 700
				elif cx == 3:
					for ind in pd:
						sf[k][i][ind] = max(sf[k][i][ind], 3)
					value += 5000
				elif co == 0 and cd == 3:
					for ind in range(3):
						sf[k][i][ind] = min(sf[k][i][ind], -abs(random.random()-random.random()))
				elif co == 1 and cd == 2:
					for ind in pd:
						sf[k][i][ind] = min(sf[k][i][ind], -1)
					value += -100
				elif co == 2 and cd == 1:
					for ind in pd:
						sf[k][i][ind] = min(sf[k][i][ind], -2)
					value += -700
				elif co == 3:
					for ind in pd:
						sf[k][i][ind] = min(sf[k][i][ind], -3)
					value += -5000

			# vertical
			for i in range(3):
				pd = []
				cx = cd = co = 0
				for j in range(3):
					if bs[j][i] == flag:
						cx += 1
					elif bs[j][i] == opp:
						co += 1
					else:
						pd.append(j)
						cd += 1
				if cx == 0 and cd == 3:
					for ind in range(3):
						sf[k][ind][i] = max(sf[k][ind][i], abs(random.random()-random.random()))
				elif cx == 1 and cd == 2:
					for ind in pd:
						sf[k][ind][i] = max(sf[k][ind][i], 1)
					value += 100
				elif cx == 2 and cd == 1:
					for ind in pd:
						sf[k][ind][i] = max(sf[k][ind][i], 2)
					value += 700
				elif cx == 3:
					for ind in pd:
						sf[k][ind][i] = max(sf[k][ind][i], 3)
					value += 5000
				elif co == 0 and cd == 3:
					for ind in range(3):
						sf[k][ind][i] = min(sf[k][ind][i], -abs(random.random()-random.random()))
				elif co == 1 and cd == 2:
					for ind in pd:
						sf[k][ind][i] = min(sf[k][ind][i], -1)
					value += -100
				elif co == 2 and cd == 1:
					for ind in pd:
						sf[k][ind][i] = min(sf[k][ind][i], -2)
					value += -700
				elif co == 3:
					for ind in pd:
						sf[k][ind][i] = min(sf[k][ind][i], -3)
					value += -5000

			# diagonals
			cx = cd = co = 0
			pd = []
			for i in range(3):
				if bs[i][i] == flag:
					cx += 1
				elif bs[i][i] == opp:
					co += 1
				else:
					pd.append(i)
					cd += 1
			if cx == 0 and cd == 3:
				for ind in pd:
					sf[k][ind][ind] = max(sf[k][ind][ind], abs(random.random()-random.random()))
			elif cx == 1 and cd == 2:
				for ind in pd:
					sf[k][ind][ind] = max(sf[k][ind][ind], 1)
				value += 100
			elif cx == 2 and cd == 1:
				for ind in pd:
					sf[k][ind][ind] = max(sf[k][ind][ind], 2)
				value += 700
			elif cx == 3:
				for ind in pd:
					sf[k][ind][ind] = max(sf[k][ind][ind], 3)
				value += 5000
			elif co == 0 and cd == 3:
				for ind in pd:
					sf[k][ind][ind] = min(sf[k][ind][ind], -abs(random.random()-random.random()))
			elif co == 1 and cd == 2:
				for ind in pd:
					sf[k][ind][ind] = min(sf[k][ind][ind], -1)
				value += -100
			elif co == 2 and cd == 1:
				for ind in pd:
					sf[k][ind][ind] = min(sf[k][ind][ind], -2)
				value += -700
			elif co == 3:
				for ind in pd:
					sf[k][ind][ind] = min(sf[k][ind][ind], -3)
				value += -5000
			i = 0
			j = 2
			cx = cd = co = 0
			pd = []
			for t in range(3):
				if bs[i][j] == flag:
					cx += 1
				elif bs[i][j] == opp:
					co += 1
				else:
					pd.append((i,j))
					cd += 1
				i += 1
				j -= 1
			if cx == 0 and cd == 3:
				for ind in pd:
					sf[k][ind[0]][ind[1]] = max(sf[k][ind[0]][ind[1]], abs(random.random()-random.random()))
			elif cx == 1 and cd == 2:
				for ind in pd:
					sf[k][ind[0]][ind[1]] = max(sf[k][ind[0]][ind[1]], 1)
				value += 100
			elif cx == 2 and cd == 1:
				for ind in pd:
					sf[k][ind[0]][ind[1]] = max(sf[k][ind[0]][ind[1]], 2)
				value += 700
			elif cx == 3:
				for ind in pd:
					sf[k][ind[0]][ind[1]] = max(sf[k][ind[0]][ind[1]], 3)
				value += 5000
			elif co == 0 and cd == 3:
				for ind in pd:
					sf[k][ind[0]][ind[1]] = min(sf[k][ind[0]][ind[1]], -abs(random.random()-random.random()))
			elif co == 1 and cd == 2:
				for ind in pd:
					sf[k][ind[0]][ind[1]] = min(sf[k][ind[0]][ind[1]], -1)
				value += -100
			elif co == 2 and cd == 1:
				for ind in pd:
					sf[k][ind[0]][ind[1]] = min(sf[k][ind[0]][ind[1]], -2)
				value += -700
			elif co == 3:
				for ind in pd:
					sf[k][ind[0]][ind[1]] = min(sf[k][ind[0]][ind[1]], -3)
				value += -5000
			for i in range(3):
				for j in range(3):
					if sf[k][i][j] == 0:
						sf[k][i][j] = abs(random.random()-random.random())

		# print value
		return value

class Manual_Player:
	def __init__(self):
		pass

	def move(self, board, old_move, flag):
		print 'Enter your move: <format:board row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]), int(mvp[2]))

class Random_Player():
	def __init__(self):
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		cells = board.find_valid_move_cells(old_move)
		return cells[random.randrange(len(cells))]

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
		#checks if the move is a free move or not based on the rules
		# print "valiiilk"
		# print old_move
		if old_move == (-1,-1,-1) or (self.small_boards_status[0][allowed_small_board[0]][allowed_small_board[1]] != '-' and self.small_boards_status[1][allowed_small_board[0]][allowed_small_board[1]] != '-'):
			# print "open hai"
			for k in range(2):
				for i in range(9):
					for j in range(9):
						if self.big_boards_status[k][i][j] == '-' and self.small_boards_status[k][i/3][j/3] == '-':
							allowed_cells.append((k,i,j))

		else:
			# print "cloae hai"
			for k in range(2):
				if self.small_boards_status[k][allowed_small_board[0]][allowed_small_board[1]] == "-":
					for i in range(3*allowed_small_board[0], 3*allowed_small_board[0]+3):
						for j in range(3*allowed_small_board[1], 3*allowed_small_board[1]+3):
							if self.big_boards_status[k][i][j] == '-':
								allowed_cells.append((k,i,j))

		return allowed_cells

	def find_terminal_state(self):
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

	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		# print new_move
		if (len(old_move) != 3) or (len(new_move) != 3):
			return False
		for i in range(3):
			if (type(old_move[i]) is not int) or (type(new_move[i]) is not int):
				return False
		if (old_move != (-1,-1,-1)) and (old_move[0] < 0 or old_move[0] > 1 or old_move[1] < 0 or old_move[1] > 8 or old_move[2] < 0 or old_move[2] > 8):
			return False
		cells = self.find_valid_move_cells(old_move)
		return new_move in cells

	def update(self, old_move, new_move, ply):
		#updating the game board and small_board status as per the move that has been passed in the arguements
		if(self.check_valid_move(old_move, new_move)) == False:
			return 'UNSUCCESSFUL', False
		self.big_boards_status[new_move[0]][new_move[1]][new_move[2]] = ply

		x = new_move[1]/3
		y = new_move[2]/3
		k = new_move[0]
		fl = 0

		#checking if a small_board has been won or drawn or not after the current move
		bs = self.big_boards_status[k]
		for i in range(3):
			#checking for horizontal pattern(i'th row)
			if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == ply):
				self.small_boards_status[k][x][y] = ply
				return 'SUCCESSFUL', True
			#checking for vertical pattern(i'th column)
			if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == ply):
				self.small_boards_status[k][x][y] = ply
				return 'SUCCESSFUL', True
		#checking for diagonal patterns
		#diagonal 1
		if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == ply):
			self.small_boards_status[k][x][y] = ply
			return 'SUCCESSFUL', True
		#diagonal 2
		if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == ply):
			self.small_boards_status[k][x][y] = ply
			return 'SUCCESSFUL', True
		#checking if a small_board has any more cells left or has it been drawn
		for i in range(3):
			for j in range(3):
				if bs[3*x+i][3*y+j] =='-':
					return 'SUCCESSFUL', False
		self.small_boards_status[k][x][y] = 'd'
		return 'SUCCESSFUL', False

def player_turn(game_board, old_move, obj, ply, opp, flg):
		temp_big_boards_status = copy.deepcopy(game_board.big_boards_status)
		temp_small_boards_status = copy.deepcopy(game_board.small_boards_status)
		signal.alarm(TIME)
		WINNER = ''
		MESSAGE = ''
		pts = {"P1" : 0, "P2" : 0}
		to_break = False
		p_move = ''

		try:									#try to get player 1's move			
			p_move = obj.move(game_board, old_move, flg)
		except TimedOutExc:					#timeout error
#			print e
			WINNER = opp
			MESSAGE = 'TIME OUT'
			pts[opp] = MAX_PTS
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False
		except Exception as e:
			WINNER = opp
			MESSAGE = "THREW AN EXCEPTION"
			traceback.print_exc()
			pts[opp] = MAX_PTS			
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False
		signal.alarm(0)

		#check if board is not modified and move returned is valid
		if (game_board.small_boards_status != temp_small_boards_status) or (game_board.big_boards_status != temp_big_boards_status):
			WINNER = opp
			MESSAGE = 'MODIFIED THE BOARD'
			pts[opp] = MAX_PTS
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False

		update_status, small_board_won = game_board.update(old_move, p_move, flg)
		if update_status == 'UNSUCCESSFUL':
			WINNER = opp
			MESSAGE = 'INVALID MOVE'
			pts[opp] = MAX_PTS
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False

		status = game_board.find_terminal_state()		#find if the game has ended and if yes, find the winner
		print status
		if status[1] == 'WON':							#if the game has ended after a player1 move, player 1 would win
			pts[ply] = MAX_PTS
			WINNER = ply
			MESSAGE = 'WON'
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False
		elif status[1] == 'DRAW':						#in case of a draw, each player gets points equal to the number of small_boards won
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False

		return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], False, small_board_won

def gameplay(obj1, obj2):				#game simulator

	game_board = BigBoard()
	fl1 = 'x'
	fl2 = 'o'
	old_move = (-1,-1,-1)
	WINNER = ''
	MESSAGE = ''
	pts1 = 0
	pts2 = 0

	game_board.print_board()
	signal.signal(signal.SIGALRM, handler)
	while(1):
		#player 1 turn
		p1_move, WINNER, MESSAGE, pts1, pts2, to_break, small_board_won = player_turn(game_board, old_move, obj1, "P1", "P2", fl1)

		if to_break:
			break

		old_move = p1_move
		game_board.print_board()

		if small_board_won:
			p1_move, WINNER, MESSAGE, pts1, pts2, to_break, small_board_won = player_turn(game_board, old_move, obj1, "P1", "P2", fl1)
		
			if to_break:
				break
		
			old_move = p1_move
			game_board.print_board()			

		#do the same thing for player 2
		p2_move, WINNER, MESSAGE, pts1, pts2, to_break, small_board_won = player_turn(game_board, old_move, obj2, "P2", "P1", fl2)

		if to_break:
			break

		game_board.print_board()
		old_move = p2_move

		if small_board_won:
			p2_move, WINNER, MESSAGE, pts1, pts2, to_break, small_board_won = player_turn(game_board, old_move, obj2, "P2", "P1", fl2)
		
			if to_break:
				break
		
			old_move = p2_move
			game_board.print_board()		

	game_board.print_board()

	print "Winner:", WINNER
	print "Message", MESSAGE

	x = 0
	d = 0
	o = 0
	for k in range(2):
		for i in range(3):
			for j in range(3):
				if game_board.small_boards_status[k][i][j] == 'x':
					x += 1
				if game_board.small_boards_status[k][i][j] == 'o':
					o += 1
				if game_board.small_boards_status[k][i][j] == 'd':
					d += 1
	print 'x:', x, ' o:',o,' d:',d

	if MESSAGE == 'DRAW':
		for k in range(2):
			for i in range(3):
				for j in range(3):
					val = 6
					if is_corner(i,j):
						val = 4
					elif is_centre(i,j):
						val = 3
					if game_board.small_boards_status[k][i][j] == 'x':
						pts1 += val
					if game_board.small_boards_status[k][i][j] == 'o':
						pts2 += val

	return (pts1,pts2)

def is_centre(row, col):
	if row == 1 and col == 1:
		return 1
	return 0

def is_corner(row, col):
	if row == 0 and col == 0:
		return 1
	if row == 0 and col == 2:
		return 1
	if row == 2 and col == 0:
		return 1
	if row == 2 and col == 2:
		return 1
	return 0

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Team7()
		obj2 = Team7()

	elif option == '2':
		obj1 = Random_Player()
		obj2 = Team7()

	elif option == '3':
		obj1 = Manual_Player()
		obj2 = Manual_Player()
	else:
		print 'Invalid option'
		sys.exit(1)

	x = gameplay(obj1, obj2)
	print "Player 1 points:", x[0] 
	print "Player 2 points:", x[1]
