#!/usr/bin/python
from board import Board
from ai import AI
import time

class Session:
	def __init__(self):
		pass

	def play_game(self):
		player_board = Board()
		ai_board = Board()

		ai = AI(ai_board.get_board_state())

		#######
		self.set_human_board(player_board)
		# human_ai = AI(player_board.get_board_state())
		# self.set_ai_board(human_ai, player_board)
		#######
		self.set_ai_board(ai, ai_board)
		self.print_boards(player_board, ai_board)

		print("\nLet's Play!")

		while True:
			#####
			self.take_human_turn(ai_board)
			# self.take_AI_turn(human_ai, ai_board)
			#####
			if self.has_no_boats(ai_board):
				self.print_boards(player_board, ai_board, True)
				print("YOU WIN!!!")
				break

			self.take_AI_turn(ai, player_board)
			if self.has_no_boats(player_board):
				self.print_boards(player_board, ai_board, True)
				print("You Lost :( \nThe AI takeover is coming...")
				break

			self.print_boards(player_board, ai_board)

		play_again = self.take_input("Play again? [Y/n]: ")
		if "Y" in play_again.upper():
			self.play_game()

	def set_human_board(self, board):
		print("We are going to place 5 boats of varying length on the board.")

		do_random_board = self.take_input("Do you want a random board? [Y/n]: ")
		if "Y" in do_random_board.upper():
			human_ai = AI(board.get_board_state())
			self.set_ai_board(human_ai, board)
			return

		print ("OK, we will enter the boats manually.\n" +
			"For all boats enter in the starting and ending positions surround by quotes and separated by a ','\n" +
			"e.x. \"A1,A5\"\n")

		self.set_human_boat_safe(board, 5)
		self.set_human_boat_safe(board, 4)
		self.set_human_boat_safe(board, 3)
		self.set_human_boat_safe(board, 3)
		self.set_human_boat_safe(board, 2)

	def set_human_boat_safe(self, board, size):
		start_end = self.take_input("\nEnter boat of length " + str(size) + ": ")
		try:
			start, end = start_end.split(",")
			invalid_spaces = sum(board.board_state["boats_left"], [])
			if not(board.is_valid_letter_num(start, invalid_spaces)) or not(board.is_valid_letter_num(end, invalid_spaces)):
				raise Exception("Boat input included illegal coordinates")
			if not(board.boat_correct_length(start, end, size)):
				raise(Exception("Boat of incorrect length"))

			if board.set_boat([start, end]):
				raise(Exception("Could not place boat there"))
			board.print_board(True)

		except Exception as error:
			print("Error: " + str(error))
			print("Could not understand input. Enter in the starting and ending positions surround by quotes and separated by a ','\n" +
			"e.x. \"A1,A5\"\n")

			return self.set_human_boat_safe(board, size)


	def set_ai_board(self, ai, board):
		board.set_boat(ai.set_boat(5, board.get_board_state()))
		board.set_boat(ai.set_boat(4, board.get_board_state()))
		board.set_boat(ai.set_boat(3, board.get_board_state()))
		board.set_boat(ai.set_boat(3, board.get_board_state()))
		board.set_boat(ai.set_boat(2, board.get_board_state()))

	def take_human_turn(self, target_board):
		try:
			next_shot = self.take_input("\nSelect space on opponents board to target (e.x. \"A1\"): ")
			if not(target_board.is_valid_letter_num(next_shot, target_board.board_state["shots"])):
				raise(Exception("Invalid shot selection."))
			result = target_board.shoot(next_shot)
			self.print_shot_result(next_shot, result)

		except Exception as error:
			print("Error: " + str(error))
			self.take_human_turn(target_board)

	def take_AI_turn(self, ai, target_board):
		print("\nAI taking turn.")
		next_shot = ai.shoot()
		result = target_board.shoot(next_shot)
		ai.record_shot_results(result, target_board.get_board_state())
		self.print_shot_result(next_shot, result)

	def print_shot_result(self, shot, result):
		if result == 0:
			print(shot + " Miss!")
		elif result == 1:
			print(shot + " Hit!")
		elif result == 2:
			print(shot + " Hit and Sink!")

		time.sleep(1)

	def has_no_boats(self, board):
		return len(sum(board.get_board_state()["boats_left"], [])) <= 0

	def print_boards(self, player_board, opponent_board, show_ai_board = False):
		print("\n\nYour Board")
		player_board.print_board(True)

		print("\n\nOpponents Board")
		opponent_board.print_board(show_ai_board)

	def take_input(self, text):
		try:
			result = input(text)
		except:
			print("Sorry, could not understand input. Try surrounding it in quotation marks \"\"")
			return self.take_input(text)
		return result

a = Session()
a.play_game()





