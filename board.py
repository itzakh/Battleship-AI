class Board:

	board_height = 10
	board_width = 10
	boats_left = []
	hits = []
	shots = []

	def __init__(self, board_width = 10, board_height = 10):
		self.board_height = board_height
		self.board_width = board_width

	def set_boat(self, boat_start, boat_end):
		boat_start_x, boat_start_y = self.get_coords(boat_start)
		boat_end_x, boat_end_y = self.get_coords(boat_end)

		min_y = min(boat_start_y, boat_end_y)
		max_y = max(boat_start_y, boat_end_y)
		min_x = min(boat_start_x, boat_end_x)
		max_x = max(boat_start_x, boat_end_x)

		boat = []

		if min_y == max_y:
			for i in range(min_x, max_x + 1):
				boat.append((i, min_y))
		elif min_x == max_x:
			for i in range(min_y, max_y + 1):
				boat.append((min_x, i))
		else:
			return 1

		self.boats_left.append(boat)
		return 0

	def shoot(self, shot):
		coords = self.get_coords(shot)
		self.shots.append(coords)

		for boat in self.boats_left:
			if coords in boat:
				boat.remove(coords)
				self.hits.append(coords)

				if len(boat) == 0:
					# Return 2 for Hit and Sink!
					return 2
				# Return 1 for Hit! no sink
				return 1

		# Return 0 for miss
		return 0


	def get_coords(self, ln_input):
		y = self.letter_to_coord(ln_input[0].upper())
		x = int(ln_input[1:]) - 1
		return (x, y)

	def letter_to_coord(self, letter):
		letter = letter.upper()
		return (ord(letter) - ord('A'))

	def get_boats_left(self):
		return self.boats_left

	def get_board_state(self):
		return self.board_width, self.board_height, self.boats_left, self.shots, self.hits

	def print_board(self, reveal_boats = False):
		board = ['.'* self.board_width] * self.board_height

		for space in self.shots:
			x, y = space
			row = list(board[y])
			row[x] = '-'
			board[y] = "".join(row)

		for space in self.hits:
			x, y = space
			row = list(board[y])
			row[x] = 'X'
			board[y] = "".join(row)

		if reveal_boats:
			for boat in self.boats_left:
				for space in boat:
					x, y = space
					row = list(board[y])
					row[x] = 'B'
					board[y] = "".join(row)

		number_row = "  "
		for i in range(1, self.board_width + 1):
			number_row = number_row + str(i) + " "
		print(number_row)

		for j in range(0, self.board_height):
			row = board[j]
			row_letter = str(chr(ord('A') + j))
			print(row_letter + " " + " ".join(row))


# a = Board()
# a.set_boat('A1', 'A9')
# a.set_boat('B3', 'D3')
# a.shoot('A7')
# a.shoot('A6')
# a.shoot('A5')
# a.shoot('D7')
# a.print_board(True)






