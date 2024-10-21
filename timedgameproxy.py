
import random 
import time 
import threading 

class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.turn_score = 0

    def roll(self):
        return random.randint(1, 6)

    def reset_turn(self):
        self.turn_score = 0

    def hold(self):
        self.total_score += self.turn_score
        self.reset_turn()

class Game:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.current_player = self.player1
        self.timeout = 10  # 10 seconds for each turn

    def take_turn(self):
        self.current_player.reset_turn()
        print(f"\nCurrent Scores - Player 1: {self.player1.total_score}, Player 2: {self.player2.total_score}")
        while True:
            roll = self.current_player.roll()
            print(f"{self.current_player.name} rolled a {roll}")
            if roll == 1:
                print("Oops! You rolled a 1. No points this turn.")
                self.current_player.reset_turn()
                break
            else:
                self.current_player.turn_score += roll
                print(f"Turn total: {self.current_player.turn_score}")
                
                hold_action = self.get_timed_player_action() #this is where I added the timed action Professor
                if hold_action == 'h':
                    self.current_player.hold()
                    break

    def get_timed_player_action(self):
        """Get player action with a timeout, default to 'h' (hold) if no input is received."""
        if self.current_player.name == "Player 1":
            action = self.get_input_with_timeout("Do you want to roll again (r) or hold (h)? ", self.timeout, default="h")
        else:
            # Computer decision logic
            if self.current_player.turn_score < 20: 
                action = 'r'
            else:
                action = 'h'
            time.sleep(1)  
        return action

    def get_input_with_timeout(self, prompt, timeout, default):
        """Prompt for user input, but default to 'hold' if timeout expires."""
        print(prompt, end='')

        result = [default]  

        def get_input():
            result[0] = input().strip().lower()

        input_thread = threading.Thread(target=get_input)
        input_thread.start()
        input_thread.join(timeout) 

        if input_thread.is_alive():
            print(f"\nTime's up! Defaulting to '{default}'.")
            input_thread.join()  
        return result[0]

    def play(self):
        while self.player1.total_score < 100 and self.player2.total_score < 100:
            self.take_turn()
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

if __name__ == "__main__":
    game = Game()
    game.play()
