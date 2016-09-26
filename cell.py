# -*- coding: utf-8 -*-

# Game of Life
# According to the Wikipedia's article: "The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970."
# Given a board with m by n cells, each cell has an initial state live (1) or dead (0). 
# Each cell interacts with its eight neighbors (horizontal, vertical, diagonal) using the following four rules (taken from the above Wikipedia article):
# Any live cell with fewer than two live neighbors dies, as if caused by under-population.
# Any live cell with two or three live neighbors lives on to the next generation.
# Any live cell with more than three live neighbors dies, as if by over-population..
# Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
# Write a function to compute the next state (after one update) of the board given its current state.

class Solution:

	def gameOfLife(self, board):
		dx = (1, 1, 1, 0, 0, -1, -1, -1)
		dy = (1, 0, -1, 1, -1, 1, 0, -1)
		for x in range(len(board)):
			for y in range(len(board[0])):
				lives = 0
				for z in range(8):
					nx, ny = x + dx[z], y + dy[z]
					lives += self.getCellStatus(board, nx, ny)
				if lives + board[x][y] == 3 or lives == 3:
					board[x][y] |= 2
		for x in range(len(board)):
			for y in range(len(board[0])):
				board[x][y] >>= 1

	def getCellStatus(self, board, x, y):
		if x < 0 or y < 0 or x >= len(board) or y >= len(board[0]):
			return 0
		return board[x][y] & 1
