#!/usr/bin/python
import random

class AI:
	def __init__(self, board_state):
		self.board_state = board_state
		self.next_shot_leads = []
		self.last_shot = "00"
		self.last_hits = []
		self.last_shot_result = 0

	def set_boat(self, boat_length, board_state):
		self.board_state = board_state

		# We cannot put a boat on a space where a boat already exists
		invalid_spaces = sum(self.board_state["boats_left"], [])

		# Randomly get the first two corrdinates for the boat
		starting_pos = self.pick_new_valid_random_letter_number([], invalid_spaces)
		possible_next_pos = self.get_surrounding_valid_letter_nums(starting_pos, invalid_spaces)

		# If we cannot grow the boat from where we are, start over
		if len(possible_next_pos) == 0:
			return self.set_boat(boat_length, self.board_state)

		next_pos = self.pick_new_valid_random_letter_number(possible_next_pos, invalid_spaces)
		current_boat = [starting_pos, next_pos]

		while len(current_boat) < boat_length:
			next_potential_boat_coords = self.get_smart_next_boat_coords(current_boat, invalid_spaces)

			# If we cannot keep building the boat, start from scratch
			if len(next_potential_boat_coords) == 0:
				return self.set_boat(boat_length, self.board_state)

			current_boat.append(self.pick_new_valid_random_letter_number(next_potential_boat_coords, invalid_spaces))

		boat_start, boat_end = self.get_min_max_letter_nums(current_boat)

		return [boat_start, boat_end]

	def shoot(self):
		self.last_shot = self.pick_new_valid_random_letter_number(self.next_shot_leads, self.board_state["shots"])
		return self.last_shot

	def record_shot_results(self, result, board_state):
		self.board_state = board_state
		self.last_shot_result = result

		# If we missed the last shot do nothing
		if result == 0:
			self.next_shot_leads = self.get_smart_next_boat_coords(self.last_hits, self.board_state["shots"])
		# If we hit the last shot then find all valid surrounding locations and add them to hit list
		elif result == 1:
			self.last_hits.append(self.last_shot)
			self.next_shot_leads = self.get_smart_next_boat_coords(self.last_hits, self.board_state["shots"])
		# If we sank a ship on the last shot then clear out the hit list
		elif result == 2:
			self.last_hits = []
			self.next_shot_leads = []

	def get_smart_next_boat_coords(self, cur_boat, invalid_choices):
		if len(cur_boat) == 1:
			return self.get_surrounding_valid_letter_nums(cur_boat[0], invalid_choices)

		# Find the direction the boat is heading
		min_letter_num, max_letter_num = self.get_min_max_letter_nums(cur_boat)
		min_x, min_y = self.letter_number_to_coords(min_letter_num)
		max_x, max_y = self.letter_number_to_coords(max_letter_num)

		smart_next_coords = []
		# We know the boat is heading north, south
		if max_x == min_x:
			# north
			north_coord = (max_x, min_y - 1)
			if self.is_coord_valid(north_coord, invalid_choices):
				smart_next_coords.append(self.coord_to_letter_num(north_coord))
			# south
			south_coord = (max_x, max_y + 1)
			if self.is_coord_valid(south_coord, invalid_choices):
				smart_next_coords.append(self.coord_to_letter_num(south_coord))

		# We know the boat is heading east, west
		elif max_y == min_y:
			# east
			east_coord = (max_x + 1, max_y)
			if self.is_coord_valid(east_coord, invalid_choices):
				smart_next_coords.append(self.coord_to_letter_num(east_coord))
			# west
			west_coord = (min_x - 1, max_y)
			if self.is_coord_valid(west_coord, invalid_choices):
				smart_next_coords.append(self.coord_to_letter_num(west_coord))

		return smart_next_coords

	def get_min_max_letter_nums(self, letter_nums):
		max_x = 0
		min_x = self.board_state["width"]
		max_y = 0
		min_y = self.board_state["height"]

		for letter_num in letter_nums:
			x, y = self.letter_number_to_coords(letter_num)
			if x > max_x:
				max_x = x
			if x < min_x:
				min_x = x

			if y > max_y:
				max_y = y
			if y < min_y:
				min_y = y

		min_letter_num = self.coord_to_letter_num((min_x, min_y))
		max_letter_num = self.coord_to_letter_num((max_x, max_y))
		return (min_letter_num, max_letter_num)

	def get_surrounding_valid_letter_nums(self, letter_number, invalid_choices):
		x, y = self.letter_number_to_coords(letter_number)
		north_coords = (x, y - 1)
		south_coords = (x, y + 1)
		east_coords = (x + 1, y)
		west_coords = (x - 1, y)

		surrounding_coords = [north_coords, south_coords, east_coords, west_coords]
		surrounding_valid_letter_nums = []

		for coord in surrounding_coords:
			if self.is_coord_valid(coord, invalid_choices):
				near_letter_number = self.coord_to_letter_num(coord)
				surrounding_valid_letter_nums.append(near_letter_number)

		return surrounding_valid_letter_nums

	def is_coord_valid(self, coord, invalid_choices):
		x, y = coord
		if x < 0 or x >= self.board_state["width"]:
			return False
		elif y < 0 or y >= self.board_state["height"]:
			return False

		if self.coord_to_letter_num(coord) in invalid_choices:
			return False

		return True

	def pick_new_valid_random_letter_number(self, choices, invalid_choices):
		letter_number = self.pick_random_letter_num(choices)
		while letter_number in invalid_choices:
			letter_number = self.pick_random_letter_num(choices)

		return letter_number

	def pick_random_letter_num(self, choices):
		# If we have choices to pick between use them
		if len(choices) > 0:
			return random.choice(choices)

		# Get a completely random choice if necessary
		return self.coord_to_letter_num(self.pick_random_coord())

	def pick_random_coord(self):
		x = random.randint(0, self.board_state["width"] - 1)
		y = random.randint(0, self.board_state["height"] - 1)
		return (x, y)

	def coord_to_letter_num(self, coord):
		x, y = coord
		letter = str(chr(y + ord('A')))
		number = str(x + 1)
		return letter + number

	def letter_number_to_coords(self, ln_input):
		y = self.letter_to_coord(ln_input[0].upper())
		x = int(ln_input[1:]) - 1
		return (x, y)

	def letter_to_coord(self, letter):
		letter = letter.upper()
		return (ord(letter) - ord('A'))


# board_state = {"height": 10, "width": 10, "boats_left": [], "hits": [], "shots": []}
# a = AI(board_state)
# print(a.coord_to_letter_num(a.pick_random_coord()))
# print(a.get_surrounding_valid_letter_nums("J9", []))
# print(a.get_surrounding_valid_letter_nums("A1", []))
# print(a.get_surrounding_valid_letter_nums("D5", []))
# print(a.shoot())
# a.record_shot_results(0, board_state)
# print(a.next_shot_leads)
# print(a.shoot())
# a.record_shot_results(1, board_state)
# print(a.next_shot_leads)
# print(a.shoot())
# a.record_shot_results(1, board_state)
# print(a.next_shot_leads)
# print(a.coord_to_letter_num((0,0)))
# print(a.letter_number_to_coords(a.coord_to_letter_num((0,0))))
# print(a.coord_to_letter_num((9,9)))
# print(a.letter_number_to_coords(a.coord_to_letter_num((9,9))))
# print(a.set_boat(5, board_state))
# print(a.set_boat(4, board_state))
# print(a.set_boat(3, board_state))
# print(a.set_boat(2, board_state))

