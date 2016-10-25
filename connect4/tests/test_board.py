import context

from src import board
import unittest
import nose

class TestBoard(unittest.TestCase):

	def setUp(self):
		self.board = board.Board()

	def testNumCols(self):
		self.assertEqual(len(self.board.state), 7)

	def testNumRows(self):
		self.assertEqual(len(self.board.state[4]), 6)

	def testAdd(self):
		''' Test cases for the Board.add() function'''
		self.board.add(0, 1)
		self.board.add(2, 2)
		self.board.add(4, 1)
		self.board.add(4, 2)
		self.board.add(4, 1)
		#####################
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 1 0 0 ###
		### 0 0 0 0 2 0 0 ###
		### 1 0 2 0 1 0 0 ###
		#####################

		#Check values were added correctly
		self.assertEqual(self.board.state[0][0], 1)
		self.assertEqual(self.board.state[2][0], 2)
		self.assertEqual(self.board.state[4][0], 1)
		self.assertEqual(self.board.state[4][1], 2)
		self.assertEqual(self.board.state[4][2], 1)

		#Check still zero
		self.assertEqual(self.board.state[0][1], 0)
		self.assertEqual(self.board.state[1][0], 0)
		self.assertEqual(self.board.state[2][1], 0)
		self.assertEqual(self.board.state[3][0], 0)
		self.assertEqual(self.board.state[4][3], 0)
		self.assertEqual(self.board.state[5][0], 0)
		self.assertEqual(self.board.state[6][0], 0)

	def testReset(self):
		self.board.reset()
		self.assertEqual(self.board.state, board.Board().state)

	def testCheckValue(self):
		''' Test cases for the _checkValue() function'''
		self.board.reset()
		for col in range(3):
			self.board.add(col, 1)
		for row in range(2):
			self.board.add(1, 1)

		self.assertTrue(self.board._checkValue((1, 0),1))
		self.assertFalse(self.board._checkValue((0, 1),1))

		self.assertTrue(self.board._checkValue((1, 0),1))
		self.assertFalse(self.board._checkValue((2, 1),1))

		self.assertTrue(self.board._checkValue((1, 0),1))
		self.assertFalse(self.board._checkValue((0, 1),1))

		self.assertTrue(self.board._checkValue((2, 0),1))
		self.assertFalse(self.board._checkValue((2, 2),1))

		self.assertFalse(self.board._checkValue((-1, -1),1))

	def testWinVert(self):
		self.board.reset()
		for row in range(4):
			self.board.add(0, 1)

		#####################
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 0 0 0 ###
		### 1 0 0 0 0 0 0 ###
		### 1 0 0 0 0 0 0 ###
		### 1 0 0 0 0 0 0 ###
		### 1 0 0 0 0 0 0 ###
		#####################

		self.assertTrue(self.board.hasWon(1))
		self.assertFalse(self.board.hasWon(2))

	def testWinDiag(self):
		self.board.reset()
		self.board.add(0,1)
		self.board.add(1,2)
		self.board.add(1,1)
		self.board.add(2,2)
		self.board.add(2,2)
		self.board.add(2,1)

		#Making sure a sequence of 3 does not trigger hasWon() == Truself
		.assertFalse(self.board.hasWon(1))

		self.board.add(3,2)
		self.board.add(3,2)
		self.board.add(3,2)
		self.board.add(3,1)

		#####################
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 1 0 0 0 ###
		### 0 0 1 2 0 0 0 ###
		### 0 1 2 2 0 0 0 ###
		### 1 2 2 2 0 0 0 ###
		#####################

		self.assertTrue(self.board.hasWon(1))
		self.assertFalse(self.board.hasWon(2))

	def testWinHoriz(self):
		self.board.reset()
		for col in range(4):
			self.board.add(col, 1)

		#####################
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 0 0 0 ###
		### 0 0 0 0 0 0 0 ###
		### 1 1 1 1 0 0 0 ###
		#####################

		self.assertTrue(self.board.hasWon(1))
		self.assertFalse(self.board.hasWon(2))

nose.runmodule()
