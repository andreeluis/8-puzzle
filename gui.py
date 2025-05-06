import time
import tkinter as tk
from puzzle import Puzzle

class PuzzleGUI:
	def __init__(self):
		self.puzzle = Puzzle()
		self.root = tk.Tk()
		self.root.title("8 Puzzle")
		self.buttons = []
		self.create_widgets()


	def create_widgets(self):
		# Frame for shuffle, solve, and reset buttons
		self.control_frame = tk.Frame(self.root)
		self.control_frame.grid(row=0, column=0, columnspan=3, pady=10)

		self.shuffle_button = tk.Button(self.control_frame, text="Shuffle", command=self.shuffle_config)
		self.shuffle_button.pack(side=tk.LEFT, padx=5)

		self.solve_button = tk.Button(self.control_frame, text="Solve", command=self.solve_config)
		self.solve_button.pack(side=tk.LEFT, padx=5)

		self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_config)
		self.reset_button.pack(side=tk.LEFT, padx=5)

		# Frame for algorithm selection
		self.algorithm_frame = tk.Frame(self.root)
		self.algorithm_frame.grid(row=1, column=0, columnspan=3, pady=10)

		self.algorithm_label = tk.Label(self.algorithm_frame, text="Solve with:")
		self.algorithm_label.pack(side=tk.LEFT, padx=5)
		self.algorithm_var = tk.StringVar(value="BFS")
		self.algorithm_menu = tk.OptionMenu(self.algorithm_frame, self.algorithm_var, "BFS", "Greedy", "A*")
		self.algorithm_menu.pack(side=tk.LEFT, padx=5)
		def update_heuristic_menu(*args):
			if self.algorithm_var.get() == "A*" or self.algorithm_var.get() == "Greedy":
				self.heuristic_label.pack(side=tk.LEFT, padx=5)
				self.heuristic_menu.pack(side=tk.LEFT, padx=5)
			else:
				self.heuristic_label.pack_forget()
				self.heuristic_menu.pack_forget()

		self.heuristic_label = tk.Label(self.algorithm_frame, text="Heuristic:")
		self.heuristic_var = tk.StringVar(value="Manhattan")
		self.heuristic_menu = tk.OptionMenu(self.algorithm_frame, self.heuristic_var, "Manhattan", "Euclidean")

		self.algorithm_var.trace("w", update_heuristic_menu)
		update_heuristic_menu()

		# Frame for the puzzle board
		self.board_frame = tk.Frame(self.root)
		self.board_frame.grid(row=2, column=0, columnspan=3)

		# 3x3 grid of buttons for the puzzle board
		for i in range(3):
			row = []
			for j in range(3):
				btn = tk.Button(self.board_frame, text="", width=6, height=3, command=lambda x=i, y=j: self.tile_clicked(x, y))
				btn.grid(row=i, column=j, padx=0, pady=0)  # Remove padding to make buttons cohesive
				row.append(btn)
			self.buttons.append(row)
		self.update_ui()

		# Frame for displaying information
		self.info_frame = tk.Frame(self.root)
		self.info_frame.grid(row=3, column=0, columnspan=3, pady=10)

		self.visited_nodes_label = tk.Label(self.info_frame, text="Visited Nodes: 0")
		self.visited_nodes_label.pack(side=tk.LEFT, padx=5)

		self.moves_label = tk.Label(self.info_frame, text="Moves: 0")
		self.moves_label.pack(side=tk.LEFT, padx=5)

		self.time_label = tk.Label(self.info_frame, text="Time to Solution: 0.0s")
		self.time_label.pack(side=tk.LEFT, padx=5)


	def shuffle_config(self):
		self.puzzle.shuffle()
		self.update_ui()


	def reset_config(self):
		self.puzzle.reset()

		self.visited_nodes_label.config(text=f"Visited Nodes: 0")
		self.time_label.config(text=f"Time to Solution: 0.0s")
		self.moves_label.config(text=f"Moves: 0")

		self.update_ui()


	def solve_config(self):
		start_time = time.time()
		path, explored_nodes = self.puzzle.solve(self.algorithm_var.get(), self.heuristic_var.get())

		if path is None:
			print("No solution found!")
			return

		end_time = time.time()
		self.visited_nodes_label.config(text=f"Visited Nodes: {explored_nodes}")
		self.time_label.config(text=f"Time to Solution: {end_time - start_time:.2f}s")
		self.moves_label.config(text=f"Moves: {len(path)}")

		for row, col in path:
			self.tile_clicked(row, col)
			self.update_ui()
			self.root.update_idletasks()
			self.root.after(500)  # 500 milliseconds delay


	def tile_clicked(self, row, col):
		if self.puzzle.is_solved():
			return

		self.puzzle.move(row, col)
		self.update_ui()
		if self.puzzle.is_solved():
			print("Congratulations! You solved the puzzle!")


	def update_ui(self):
		for i in range(3):
			for j in range(3):
				val = self.puzzle.state[i][j]
				self.buttons[i][j].config(
					text=str(val) if val != 0 else "",
					state=tk.NORMAL if val != 0 else tk.DISABLED
				)


	def run(self):
		self.root.mainloop()
