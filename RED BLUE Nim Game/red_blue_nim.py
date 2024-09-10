import sys

# Function to evaluate the game state for scoring
def evaluate_game_state(num_red, num_blue):
    return num_red == 0 or num_blue == 0

def minmax(num_red, num_blue, depth, alpha, beta, maximizing_player, version):
    if depth == 0 or evaluate_game_state(num_red, num_blue):
        return evaluate_score(num_red, num_blue), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None

        for move in possible_moves(num_red, num_blue, version):
            new_num_red, new_num_blue = apply_move(num_red, num_blue, move)
            eval, _ = minmax(new_num_red, new_num_blue, depth - 1, alpha, beta, False, version)

            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break  

        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None

        for move in possible_moves(num_red, num_blue, version):
            new_num_red, new_num_blue = apply_move(num_red, num_blue, move)
            eval, _ = minmax(new_num_red, new_num_blue, depth - 1, alpha, beta, True, version)

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break  

        return min_eval, best_move

# Calculate the score at the end of the game
def evaluate_score(num_red, num_blue):
    return num_red * 2 + num_blue * 3

# Get all possible moves 
def possible_moves(num_red, num_blue, version):
    moves = []

    if version == 'standard':
        # Standard move ordering
        if num_red >= 2: moves.append((2, 0))  
        if num_blue >= 2: moves.append((0, 2)) 
        if num_red >= 1: moves.append((1, 0))  
        if num_blue >= 1: moves.append((0, 1))  
    else:
        # Misère move ordering 
        if num_blue >= 1: moves.append((0, 1))  
        if num_red >= 1: moves.append((1, 0))  
        if num_blue >= 2: moves.append((0, 2))  
        if num_red >= 2: moves.append((2, 0))  

    return moves


def apply_move(num_red, num_blue, move):
    return num_red - move[0], num_blue - move[1]

# Game class for Red-Blue Nim
class NimGame:
    def __init__(self, num_red, num_blue, version='standard', first_player='computer', depth=None):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.first_player = first_player
        self.depth = depth or 5  
        self.current_player = first_player

    
    def play(self):
        while not evaluate_game_state(self.num_red, self.num_blue):
            if self.current_player == 'human':
                self.human_move()
            else:
                self.computer_move()

            # Check if the game is over after each move
            if evaluate_game_state(self.num_red, self.num_blue):
                break  

            self.current_player = 'computer' if self.current_player == 'human' else 'human'

        self.end_game()

    # Human move function
    def human_move(self):
        print(f"\nYour turn! Red: {self.num_red}, Blue: {self.num_blue}")
        while True:
            try:
                pile = input("Choose a pile (red or blue): ").lower()
                count = int(input("How many marbles to take (1 or 2): "))
                if pile not in ['red', 'blue'] or count not in [1, 2]:
                    raise ValueError("Invalid input. Try again.")
                if pile == 'red' and self.num_red >= count:
                    self.num_red -= count
                    break
                elif pile == 'blue' and self.num_blue >= count:
                    self.num_blue -= count
                    break
                else:
                    print("Not enough marbles in the chosen pile. Try again.")
            except ValueError as e:
                print(e)

    # Computer move function using MinMax
    def computer_move(self):
        print(f"\nComputer's turn. Red: {self.num_red}, Blue: {self.num_blue}")
        _, best_move = minmax(self.num_red, self.num_blue, self.depth, float('-inf'), float('inf'), True, self.version)
        if best_move:
            self.num_red, self.num_blue = apply_move(self.num_red, self.num_blue, best_move)
            print(f"Computer takes {best_move[0]} red and {best_move[1]} blue marbles.")

    # End of game and calculate score
    def end_game(self):
        print("\nGame over!")
        score = evaluate_score(self.num_red, self.num_blue)
        print(f"Final score: {score} points (Red marbles: {self.num_red * 2}, Blue marbles: {self.num_blue * 3})")

        if self.version == 'standard':
            winner = 'human' if self.current_player == 'computer' else 'computer'
        else:
            winner = 'human' if self.current_player == 'human' else 'computer'

        print(f"The {winner} wins the game!")

# Command-line argument parsing
if __name__ == "__main__":
    try:
        num_red = int(sys.argv[1])
        num_blue = int(sys.argv[2])
        version = sys.argv[3] if len(sys.argv) > 3 else 'standard'
        first_player = sys.argv[4] if len(sys.argv) > 4 else 'computer'
        depth = int(sys.argv[5]) if len(sys.argv) > 5 else None

        if version not in ['standard', 'misere']:
            raise ValueError("Invalid game version. Choose 'standard' or 'misere'.")
        if first_player not in ['computer', 'human']:
            raise ValueError("Invalid first player. Choose 'computer' or 'human'.")

        game = NimGame(num_red, num_blue, version, first_player, depth)
        game.play()
    except (IndexError, ValueError) as e:
        print(f"Error: {e}")
        print("Usage: python red_blue_nim.py <num-red> <num-blue> <version> <first-player> [depth]")
