from puzzle_state import PuzzleState

class Puzzle:
	def __init__(self):
		self.initial_state = PuzzleState(goal=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
		self.state = PuzzleState(goal=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
		self.shuffle()


	def is_solved(self):
		return self.state.is_solved()


	def move(self, row, col):
		if (row < 0 or row > 2 or col < 0 or col > 2):
			print("Invalid move!")
			return

		self.state.move(row, col)


	def shuffle(self):
		""" Shuffle the puzzle state for a new initial state """
		self.initial_state.shuffle()

		self.reset()


	def reset(self):
		""" Reset the puzzle state to the initial state """
		self.state.set_state(self.initial_state)


	def solve(self, algorithm, heuristic=None):
		""" Solve the puzzle using the specified algorithm """
		from solve import solve_with_bfs, solve_with_greedy, solve_with_a_star

		if algorithm == "BFS":
			return solve_with_bfs(self)
		elif algorithm == "Greedy":
			return solve_with_greedy(self, heuristic)
		elif algorithm == "A*":
			return solve_with_a_star(self, heuristic)
		else:
			print("Invalid algorithm!")
			return None