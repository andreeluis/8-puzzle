from puzzle import *
from collections import deque

from puzzle_state import PuzzleState

def solve_with_bfs(puzzle: Puzzle):
	frontier = deque()
	frontier.append((puzzle.state, []))

	explored = set()

	while frontier:
		state, path = frontier.popleft()

		if state.is_solved():
			print("Solved!")
			return path

		if state not in explored:
			for next_state in state.next_states():
				move = state.get_move_to(next_state)
				explored.add(state)
				frontier.append((next_state, path + [move]))

	return None


def solve_with_dfs(puzzle: Puzzle):
	stack = []
	stack.append((puzzle.state, []))

	explored = set()

	while stack:
		state, path = stack.pop()

		if state.is_solved():
			print("Solved!")
			return path

		if state not in explored:
			for next_state in state.next_states():
				move = state.get_move_to(next_state)
				explored.add(state)
				stack.append((next_state, path + [move]))

	return None


def solve_with_a_star(puzzle: Puzzle, heuristic : str):
	from queue import PriorityQueue

	callable_heuristic = manhattan_distance
	if heuristic == "euclidean":
		callable_heuristic = euclidean_distance

	frontier = PriorityQueue()
	frontier.put((0, puzzle.state, []))

	explored = set()

	while not frontier.empty():
		_, state, path = frontier.get()

		if state.is_solved():
			print("Solved!")
			return path

		if state not in explored:
			for next_state in state.next_states():
				move = state.get_move_to(next_state)
				explored.add(state)
				priority = len(path) + callable_heuristic(next_state)
				frontier.put((priority, next_state, path + [move]))

	return None


def manhattan_distance(state: PuzzleState):
	""" Calculate the Manhattan distance heuristic for the A* algorithm """
	distance = 0

	for i in range(3):
		for j in range(3):
			if state.state[i][j] != 0:
				distance += abs(state.state[i][j] - state.goal[i][j])

	return distance


def euclidean_distance(state: PuzzleState):
	""" Calculate the Euclidean distance heuristic for the A* algorithm """
	distance = 0

	for i in range(3):
		for j in range(3):
			if state.state[i][j] != 0:
				distance += ((state.state[i][j] - state.goal[i][j]) ** 2) ** 0.5

	return distance