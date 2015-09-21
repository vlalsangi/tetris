#! /usr/bin/python

#by Vaishak Lalsangi
#vnl

from Tkinter import *
import random

def run(row, col, mult = 10, offset = 20, tc = 1000):
	root = Tk()
	global canvas

	h = ((row) * mult) + (2 * offset) #defines height of board
	w = ((col) * mult) + (2 * offset) #defines width of board

	canvas =  Canvas(root, width = w, height = h) 
	canvas.pack()
	root.resizable(width = 0, height = 0)
	class Struct : pass
	canvas.data = Struct()
	canvas.focus_set()
	canvas.bind("<Up>", keyPressedUp)
	canvas.bind("<Down>", keyPressedDown)
	canvas.bind("<Left>", keyPressedLeft)
	canvas.bind("<Right>", keyPressedRight)
	canvas.bind("r", keyPressedR)
	canvas.bind()
	#storing global vars/constants here
	canvas.data.row = row
	canvas.data.col = col
	canvas.data.count = 0
	canvas.data.h = h
	canvas.data.w = w
	canvas.data.mult = mult
	canvas.data.offset = offset
	canvas.data.timeconstant = tc
	pieceTypes()
	init()
	canvas.after(canvas.data.timeconstant, timerFired)
	root.mainloop()

def init():
	
	canvas.data.score = 0
	canvas.data.isGameOver = False #defines gamestate
	canvas.data.emptyColor = "blue" #defines empty color for board

	canvas.data.board = [[canvas.data.emptyColor for i in range(canvas.data.col)] for j in range(canvas.data.row)] #fills with emptycolor
	redrawAll()

def pieceTypes():
	#Seven "standard" pieces (tetrominoes)
	iPiece = [
		[ True,  True,  True,  True]
	]
	  
	jPiece = [
		[ True, False, False ],
		[ True, True,  True]
	]
	  
	lPiece = [
		[ False, False, True],
		[ True,  True,  True]
	]
	  
	oPiece = [
		[ True, True],
		[ True, True]
	]
	  
	sPiece = [
		[ False, True, True],
		[ True,  True, False ]
	]
	  
	tPiece = [
		[ False, True, False ],
		[ True,  True, True]
	]

	zPiece = [
		[ True,  True, False ],
		[ False, True, True]
	]

	canvas.data.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
	canvas.data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]

def redrawAll():

	canvas.delete(ALL) #clears canvas to avoid performance issues
	removeFullRows() #checks for rows to remove
	drawGame() #draws objects on canvas
	drawBoard() #refreshes board
	if (canvas.data.count < 1):
		newFallingPiece() #first piece of game set
		canvas.data.count += 1
	drawFallingPiece() #draws fallingpiece
	removeFullRows() #checks for rows to remove again

def drawGame():
	
	offset = canvas.data.offset
	canvas.create_rectangle(0, 0, canvas.data.w, canvas.data.h, fill = "orange") #draws canvas
	canvas.create_rectangle(offset, offset, (canvas.data.w - offset + 1), (canvas.data.h - offset + 1), fill = "black") #draws border under board
	canvas.create_text((canvas.data.w - 1.25 * offset), (offset/2), text = "Score: " + str(canvas.data.score), fill = "purple", font = "Helvetica 12 bold") #draws score widget
	if (canvas.data.isGameOver):
		canvas.create_text((2 * offset), (offset/2), text = "GAME OVER", fill = "purple", font = "Helvetica 12 bold") #draws gameover
		canvas.create_text((4 * offset), (canvas.data.h - offset/2), text = "Press 'r' to restart!", fill = "purple", font = "Helvetica 12 bold") #draws helper

def drawBoard(): #iterates through board and redraws it
	board = canvas.data.board
	offset = canvas.data.offset
	mult = canvas.data.mult

	for x in range (0, len(board)):
		for y in range (0, len(board[x])):
			
			x0 = offset + (y * mult) + 1
			y0 = offset + (x * mult) + 1
			
			drawCell(x0, y0, canvas.data.board[x][y])

def drawCell(x0, y0, color): #draws a cell at x0, y0
	xy0off = canvas.data.mult - 1
	canvas.create_rectangle(x0, y0, x0 + xy0off, y0 + xy0off, fill = color)

def newFallingPiece(): #creates a new falling piece
	rand = random.randint(0, 6) #random piece
	mult = canvas.data.mult
	cent = int(canvas.data.col / 2) - 1 #dependent on cols
	canvas.data.fallingPiece = canvas.data.tetrisPieces[rand]
	rand = random.randint(0, 6) #random color
	canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[rand]
	canvas.data.fallingPieceRow = canvas.data.offset + 1
	canvas.data.fallingPieceCol = canvas.data.offset + (mult * cent) + 1 #picks col dependent on multiplier

def drawFallingPiece(): #draws falling piece
	fallpiece = canvas.data.fallingPiece
	mult = canvas.data.mult
	x0 = canvas.data.fallingPieceCol
	y0 = canvas.data.fallingPieceRow
	color = canvas.data.fallingPieceColor

	for x in fallpiece: #calls drawcell such that all "true" cells in fallpiece are painted
		for y in x:
			if (y):
				drawCell(x0, y0, color)
			x0 = x0 + mult
		y0 = y0 + mult
		x0 = canvas.data.fallingPieceCol	

def keyPressedUp(event): #rotates
  	if (canvas.data.isGameOver == False):
		rotateFallingPiece()
		redrawAll()

def keyPressedDown(event): #shifts down
  	if (canvas.data.isGameOver == False):
		moveFallingPiece(0, canvas.data.mult)
		redrawAll()

def keyPressedLeft(event): #shifts up
 	if (canvas.data.isGameOver == False):
		moveFallingPiece(-canvas.data.mult, 0)
		redrawAll()

def keyPressedRight(event): #shifts right
  	if (canvas.data.isGameOver == False):
		moveFallingPiece(canvas.data.mult, 0)
		redrawAll()

def keyPressedR(event): #restarts game immediately
	canvas.data.isGameOver = False
	canvas.after(100, timerFired)
	init()

def moveFallingPiece(dx, dy): #moves fallingpiece and checks if legal or not
	
	mult = canvas.data.mult

	row = (canvas.data.fallingPieceRow - canvas.data.offset - 1) / mult
	col = (canvas.data.fallingPieceCol - canvas.data.offset - 1) / mult

	nrow = row + (dy / mult)
	ncol = col + (dx / mult)

	canvas.data.fallingPieceRow = (nrow * mult) + canvas.data.offset + 1
	canvas.data.fallingPieceCol = (ncol * mult) + canvas.data.offset + 1

	if (fallingPieceIsLegal(nrow, ncol) == False):

		canvas.data.fallingPieceRow = (row * mult) + canvas.data.offset + 1
		canvas.data.fallingPieceCol = (col * mult) + canvas.data.offset + 1

		return False

	return True

def fallingPieceIsLegal(nrow, ncol): #checks if piece is legal or not
	
	fallp = canvas.data.fallingPiece
	board = canvas.data.board
	ocol = ncol

	for x in fallp:
		for y in x:
			if y:
				try:
					if (board[nrow][ncol] != canvas.data.emptyColor):
						return False
				except IndexError: #upper bound checking is not necessary, as checking color will throw an IndexError anyway
					return False
				if (nrow < 0): #negative bound checking is necessary, as python can iterate through negative list indexes
					return False
				if (ncol < 0):
					return False
			ncol += 1
		nrow += 1
		ncol = ocol

	return True
	
def rotateFallingPiece(): #rotates and checks if legal or not
	
	fallPiece = canvas.data.fallingPiece
	mult = canvas.data.mult
	newfallPiece = list(zip(*fallPiece))
	canvas.data.fallingPiece = list(reversed(newfallPiece))

	row = (canvas.data.fallingPieceRow - canvas.data.offset - 1) / mult
	col = (canvas.data.fallingPieceCol - canvas.data.offset - 1) / mult

	if (fallingPieceIsLegal(row, col) == False):
		canvas.data.fallingPiece = fallPiece

def timerFired(): #timing for entire program
	redrawAll()
	mult = canvas.data.mult
	if (moveFallingPiece(0, mult) == False): #if placing piece is imeediately illegal, flag gameover
		placeFallingPiece()
		redrawAll()
		if (moveFallingPiece(0, mult) == False):
			canvas.data.isGameOver = True
	if (canvas.data.isGameOver == False):
		canvas.after(canvas.data.timeconstant, timerFired) #time constant can be changed
	redrawAll()

def placeFallingPiece():
	
	fallpiece = canvas.data.fallingPiece
	board = canvas.data.board
	color = canvas.data.fallingPieceColor
	mult = canvas.data.mult
	y0 = canvas.data.fallingPieceRow
	x0 = canvas.data.fallingPieceCol
	row = (y0 - canvas.data.offset - 1) / mult
	col = (x0 - canvas.data.offset - 1) / mult
	ocol = col

	for x in fallpiece:
		for y in x:
			if (y):
				canvas.data.board[row][col] = color
			col += 1
		row += 1
		col = ocol

	newFallingPiece() #after placing, new fallingpiece is generated

def removeFullRows(): #removes row and awards points
	
	board = canvas.data.board
	emp = [canvas.data.emptyColor] * canvas.data.col
	score = 0
	c = 0

	for x in board:
		for y in x:
			if (y == canvas.data.emptyColor):
				c = c + 1
		if (c == 0):
				score = score + 1
				board.remove(x)
				board.insert(0, emp)
		c = 0

	canvas.data.score = canvas.data.score + (score ** 2) #more rows cleared at one time, the better

#checks for file, if none found, then defaults

try:
	f = open("tetris-pref.txt")
	args = f.readline()
	largs = args.split(", ")
	liargs = []
	while (len(largs) > 5):
		largs.pop()
	for y in largs:
		liargs = liargs + [int(y)]
	
	run(*liargs)

except IOError:
	run(15, 10) #row, col, multiplier (size of board), offset (side offsets), timeconstant (timerfired freq)