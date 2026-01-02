from Game.gamestate import GameState
import random

def main():
    state = GameState()
    move_number = 1
    moves_played = []

    print("Initial board:")
    print(state.board)
    print("Current player:", state.current_player)
    print("Valid moves:", state.generate_valid_moves())

    # Play a game, tracking moves
    while not state.game_over:
        valid_moves = state.generate_valid_moves()
        if not valid_moves:
            print("No more valid moves. Game is a draw.")
            break
        move = random.choice(valid_moves)
        moves_played.append(move)
        print(f"\nMove {move_number}: Player {state.current_player} plays column {move}")
        state.move(move)
        print("Board:")
        print(state.board)
        print("Current player:", state.current_player)
        print("Valid moves:", state.generate_valid_moves())
        move_number += 1

    if state.winner is not None:
        print(f"Game over. Player {state.winner} wins!")
    else:
        print("Game over. No winner (draw).")

    print("---------------------------------------")
    print("---------------------------------------")
    print("---------------------------------------")
    print("---------------------------------------")
    print("---------------------------------------")

    # Unmove all moves to return to the initial state
    print("\nUnmoving all moves to restore initial board:")
    while moves_played:
        last_move = moves_played.pop()
        print(f"Unmoving column {last_move}")
        state.unmove(last_move)
        print("Board:")
        print(state.board)
        print("Current player (should have switched back):", state.current_player)

    print("\nFinal board after all unmoves (should match initial board):")
    print(state.board)
    print("Current player:", state.current_player)
    print("Valid moves:", state.generate_valid_moves())


if __name__ == "__main__":
    main()
