#!/usr/bin/python

class Board:
	def __init__(self):
		self.board_state = {"height": 10, "width": 10, "boats_left": [], "hits": [], "shots": []}

	def set_boat(self, boat_start, boat_end):
		boat_start_x, boat_start_y = self.letter_number_to_coords(boat_start)
		boat_end_x, boat_end_y = self.letter_number_to_coords(boat_end)

		min_y = min(boat_start_y, boat_end_y)
		max_y = max(boat_start_y, boat_end_y)
		min_x = min(boat_start_x, boat_end_x)
		max_x = max(boat_start_x, boat_end_x)

		boat = []
		invalid_choices = sum(self.board_state["boats_left"], [])

		if min_y == max_y:
			for i in range(min_x, max_x + 1):
				if self.coord_to_letter_number((i, min_y)) in invalid_choices:
					return 1
				boat.append(self.coord_to_letter_number((i, min_y)))

		elif min_x == max_x:
			for i in range(min_y, max_y + 1):
				if self.coord_to_letter_number((min_x, i)) in invalid_choices:
					return 1
				boat.append(self.coord_to_letter_number((min_x, i)))
		else:
			return 1

		self.board_state["boats_left"].append(boat)
		return 0

	def shoot(self, letter_number_shot):
		self.board_state["shots"].append(letter_number_shot)

		for boat in self.board_state["boats_left"]:
			if letter_number_shot in boat:
				boat.remove(letter_number_shot)
				self.board_state["hits"].append(letter_number_shot)

				if len(boat) == 0:
					# Return 2 for Hit and Sink!
					return 2
				# Return 1 for Hit! no sink
				return 1

		# Return 0 for miss
		return 0

	def is_valid_starting_boat_pos(self, letter_number):
		coord = self.letter_number_to_coords(letter_number)
		invalid_choices = sum(self.board_state["boats_left"], [])
		return self.is_coord_valid(coord, invalid_choices)

	def boat_correct_length(self, boat_start, boat_end, length):
		boat_start_x, boat_start_y = self.letter_number_to_coords(boat_start)
		boat_end_x, boat_end_y = self.letter_number_to_coords(boat_end)

		min_y = min(boat_start_y, boat_end_y)
		max_y = max(boat_start_y, boat_end_y)
		min_x = min(boat_start_x, boat_end_x)
		max_x = max(boat_start_x, boat_end_x)

		boat = []

		if min_y == max_y and (max_x - min_x) == (length - 1):
			return True
		elif min_x == max_x and (max_y - min_y) == (length - 1):
			return True

		return False

	def is_coord_valid(self, coord, invalid_choices):
		x, y = coord
		if x < 0 or x >= self.board_state["width"]:
			return False
		elif y < 0 or y >= self.board_state["height"]:
			return False

		if self.coord_to_letter_number(coord) in invalid_choices:
			return False

		return True

	def letter_number_to_coords(self, ln_input):
		y = self.letter_to_coord(ln_input[0].upper())
		x = int(ln_input[1:]) - 1
		return (x, y)

	def coord_to_letter_number(self, coord):
		x, y = coord
		letter = str(chr(y + ord('A')))
		number = str(x + 1)
		return letter + number

	def letter_to_coord(self, letter):
		letter = letter.upper()
		return (ord(letter) - ord('A'))

	def get_boats_left(self):
		return self.board_state["boats_left"]

	def get_board_state(self):
		board_state = {}
		return self.board_state

	def print_board(self, reveal_boats = False):
		board = ['.'* self.board_state["width"]] * self.board_state["height"]

		for space in self.board_state["shots"]:
			x, y = self.letter_number_to_coords(space)
			row = list(board[y])
			row[x] = '-'
			board[y] = "".join(row)

		for space in self.board_state["hits"]:
			x, y = self.letter_number_to_coords(space)
			row = list(board[y])
			row[x] = 'X'
			board[y] = "".join(row)

		if reveal_boats:
			for boat in self.board_state["boats_left"]:
				for space in boat:
					x, y = self.letter_number_to_coords(space)
					row = list(board[y])
					row[x] = 'b'
					board[y] = "".join(row)

		number_row = "  "
		for i in range(1, self.board_state["width"] + 1):
			number_row = number_row + str(i) + " "
		print(number_row)

		for j in range(0, self.board_state["height"]):
			row = board[j]
			row_letter = str(chr(ord('A') + j))
			print(row_letter + " " + " ".join(row))


# a = Board()
# a.set_boat('A1,A9')
# a.set_boat('B3,D3')
# a.shoot('A7')
# a.shoot('A6')
# a.shoot('A5')
# a.shoot('D7')
# a.print_board(True)
# print(a.get_board_state())


# bb = Board()
# bb.set_boat('G1,G9')
# bb.set_boat('B8,D8')
# bb.shoot('A1')
# bb.shoot('H8')
# bb.shoot('F4')
# bb.shoot('D4')
# bb.print_board(True)
# print(bb.get_board_state())
# print(isinstance(bb, Board))
# print(isinstance(a, Board))
# print(a.get_board_state() == bb.get_board_state())




