import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def roll_die(self):
        return random.randint(1, 6)

    def update_score(self, points):
        self.score += points


class HumanPlayer(Player):
    def take_turn(self):
        turn_total = 0
        while True:
            roll = self.roll_die()
            print(f"{self.name} rolled a {roll}")
            if roll == 1:
                print("Oops! You rolled a 1. No points this turn.")
                return 0
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}")
                action = input("Do you want to roll again (r) or hold (h)? ").lower()
                if action == 'h':
                    self.update_score(turn_total)
                    print(f"{self.name}'s total score is now {self.score}")
                    return turn_total


class ComputerPlayer(Player):
    def take_turn(self):
        turn_total = 0
        while True:
            roll = self.roll_die()
            print(f"{self.name} rolled a {roll}")
            if roll == 1:
                print("Oops! Computer rolled a 1. No points this turn.")
                return 0
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}")
                if turn_total >= min(25, 100 - self.score):
                    print(f"{self.name} decides to hold.")
                    self.update_score(turn_total)
                    print(f"{self.name}'s total score is now {self.score}")
                    return turn_total


class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player_index = 0

    def play(self):
        while all(player.score < 100 for player in self.players):
            current_player = self.players[self.current_player_index]
            print(f"\nCurrent Scores - {self.players[0].name}: {self.players[0].score}, {self.players[1].name}: {self.players[1].score}")
            current_player.take_turn()
            self.current_player_index = (self.current_player_index + 1) % 2  # Switch players

        self.declare_winner()

    def declare_winner(self):
        winner = max(self.players, key=lambda player: player.score)
        print(f"\n{winner.name} wins with a score of {winner.score}!")


if __name__ == "__main__":
    player1_type = input("Choose player 1 (human/computer): ").lower()
    player2_type = input("Choose player 2 (human/computer): ").lower()

    player1 = PlayerFactory.create_player(player1_type, "Player 1")
    player2 = PlayerFactory.create_player(player2_type, "Player 2")

    game = Game(player1, player2)
    game.play()


