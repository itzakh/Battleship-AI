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
				print("YOU WIN!!!")
				break

			self.take_AI_turn(ai, player_board)
			if self.has_no_boats(player_board):
				print("You Lost :( \nThe AI takeover is coming...")
				break

			self.print_boards(player_board, ai_board)

		play_again = input("Play again? [Y/n]: ")
		if "Y" in play_again.upper():
			self.play_game()

	def set_human_board(self, board):
		print("We are going to place 5 boats of varying length on the board.")

		do_random_board = input("Do you want a random board? [Y/n]: ")
		if "Y" in do_random_board.upper():
			human_ai = AI(board.get_board_state())
			self.set_ai_board(human_ai, board)
			return

		print ("OK, we will enter the boats manually.\n" +
			"For all boats enter in the starting and ending positions surround by quotes and separated by a ','\n" +
			"e.x. \"A1,A5\"\n")

		board.print_board(True)
		start_end_pos_5 = input("\nEnter boat of length 5: ")
		board.set_boat(start_end_pos_5)
		board.print_board(True)
		start_end_pos_4 = input("\nEnter boat of length 4: ")
		board.set_boat(start_end_pos_4)
		board.print_board(True)
		start_end_pos_3a = input("\nEnter boat of length 3: ")
		board.set_boat(start_end_pos_3a)
		board.print_board(True)
		start_end_pos_3b = input("\nEnter another boat of length 3: ")
		board.set_boat(start_end_pos_3b)
		board.print_board(True)
		start_end_pos_2 = input("\nEnter boat of length 2: ")
		board.set_boat(start_end_pos_2)
		board.print_board(True)

	def set_ai_board(self, ai, board):
		board.set_boat(ai.set_boat(5, board.get_board_state()))
		board.set_boat(ai.set_boat(4, board.get_board_state()))
		board.set_boat(ai.set_boat(3, board.get_board_state()))
		board.set_boat(ai.set_boat(3, board.get_board_state()))
		board.set_boat(ai.set_boat(2, board.get_board_state()))

	def take_human_turn(self, target_board):
		next_shot = input("\nSelect space on opponents board to target (e.x. \"A1\"): ")
		result = target_board.shoot(next_shot)
		self.print_shot_result(next_shot, result)

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

	def print_boards(self, player_board, opponent_board):
		print("\n\nOpponents Board")
		opponent_board.print_board()

		print("\n\nYour Board")
		player_board.print_board(True)

a = Session()
a.play_game()





