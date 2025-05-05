class PuzzleState:
	def __init__(self, state = [], goal = []):
		self.state = state
		self.goal = goal


	def __getitem__(self, index):
		return self.state[index]


	def __hash__(self):
		return hash(tuple(tuple(row) for row in self.state))


	def __eq__(self, other):
		if self.state == other.state:
			return True
		return False


	def __lt__(self, other):
		"""Define less-than for PuzzleState based on heuristic or state comparison."""
		return self.state < other.state


	def set_state(self, state):
		self.state = [state[i][:] for i in range(3)]


	def is_solved(self):
		return self.state == self.goal


	def is_solvable(self):
		inversions = 0

		flat_state = [self.state[i][j] for i in range(3) for j in range(3) if self.state[i][j] != 0]
		for i in range(len(flat_state)):
			for j in range(i + 1, len(flat_state)):
				if flat_state[i] > flat_state[j]:
					inversions += 1

		return inversions % 2 == 0


	def shuffle(self):
		import random
		flat_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

		while True:
			random.shuffle(flat_state)
			shuffled_state = [flat_state[i:i + 3] for i in range(0, len(flat_state), 3)]
			if PuzzleState(state=shuffled_state, goal=self.goal).is_solvable():
				self.state = shuffled_state
				break


	def move(self, row, col):
		if (row > 0 and self.state[row - 1][col] == 0):
			# up
			self.state[row - 1][col] = self.state[row][col]
			self.state[row][col] = 0
		elif (row < 2 and self.state[row + 1][col] == 0):
			# down
			self.state[row + 1][col] = self.state[row][col]
			self.state[row][col] = 0
		elif (col > 0 and self.state[row][col - 1] == 0):
			# left
			self.state[row][col - 1] = self.state[row][col]
			self.state[row][col] = 0
		elif (col < 2 and self.state[row][col + 1] == 0):
			# right
			self.state[row][col + 1] = self.state[row][col]
			self.state[row][col] = 0


	def next_states(self):
		""" Return the next states of the puzzle """
		next_states = []
		for i in range(3):
			for j in range(3):
				if self.state[i][j] == 0:
					if i > 0:
						# up
						new_state = [row[:] for row in self.state]
						new_state[i - 1][j], new_state[i][j] = new_state[i][j], new_state[i - 1][j]
						next_states.append(PuzzleState(new_state, self.goal))
					if i < 2:
						# down
						new_state = [row[:] for row in self.state]
						new_state[i + 1][j], new_state[i][j] = new_state[i][j], new_state[i + 1][j]
						next_states.append(PuzzleState(new_state, self.goal))
					if j > 0:
						# left
						new_state = [row[:] for row in self.state]
						new_state[i][j - 1], new_state[i][j] = new_state[i][j], new_state[i][j - 1]
						next_states.append(PuzzleState(new_state, self.goal))
					if j < 2:
						# right
						new_state = [row[:] for row in self.state]
						new_state[i][j + 1], new_state[i][j] = new_state[i][j], new_state[i][j + 1]
						next_states.append(PuzzleState(new_state, self.goal))

					return next_states


	def get_move_to(self, next_state):
		""" Return the move to reach the next state """
		for i in range(3):
			for j in range(3):
				if self.state[i][j] == 0:
					if i > 0 and next_state.state[i - 1][j] == self.state[i][j]:
						return (i - 1, j)
					elif i < 2 and next_state.state[i + 1][j] == self.state[i][j]:
						return (i + 1, j)
					elif j > 0 and next_state.state[i][j - 1] == self.state[i][j]:
						return (i, j - 1)
					elif j < 2 and next_state.state[i][j + 1] == self.state[i][j]:
						return (i, j + 1)