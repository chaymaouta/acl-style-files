"""Simple command-line Tic-Tac-Toe (X/O) game.

This module provides a minimal yet friendly command-line implementation
of Tic-Tac-Toe.  Players X and O take turns choosing positions on a
3x3 grid until one claims three in a row or the board fills up.  The
module can be imported in other scripts or executed directly with
``python xo_game.py`` to play in the terminal.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


WINNING_COMBINATIONS: List[Tuple[int, int, int]] = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


@dataclass
class TicTacToeGame:
    """Encapsulates the state and rules of a Tic-Tac-Toe game."""

    board: List[str] = field(default_factory=lambda: [" "] * 9)
    current_player: str = "X"

    def display_board(self) -> str:
        """Return a string representation of the board for printing."""

        rows = [" | ".join(self.board[i : i + 3]) for i in range(0, 9, 3)]
        separator = "\n---------\n"
        return separator.join(rows)

    def make_move(self, position: int) -> None:
        """Attempt to place the current player's mark at ``position``.

        Parameters
        ----------
        position:
            The board slot from 1-9 (counted left to right, top to
            bottom).

        Raises
        ------
        ValueError
            If ``position`` is outside 1-9 or already occupied.
        """

        index = position - 1
        if index < 0 or index >= len(self.board):
            raise ValueError("Position must be between 1 and 9.")
        if self.board[index] != " ":
            raise ValueError("That position is already taken.")

        self.board[index] = self.current_player

    def switch_player(self) -> None:
        """Change the active player from X to O or vice versa."""

        self.current_player = "O" if self.current_player == "X" else "X"

    def winner(self) -> Optional[str]:
        """Return the winning player's symbol, or ``None`` if no winner."""

        for combo in WINNING_COMBINATIONS:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        return None

    def is_draw(self) -> bool:
        """Return ``True`` if the board is full and nobody has won."""

        return all(cell != " " for cell in self.board) and self.winner() is None

    def reset(self) -> None:
        """Reset the board and start a new game with player X."""

        self.board = [" "] * 9
        self.current_player = "X"


def prompt_move(game: TicTacToeGame) -> int:
    """Prompt the current player for their move and return the choice."""

    while True:
        raw = input(f"Player {game.current_player}, choose a position (1-9): ")
        try:
            position = int(raw)
        except ValueError:
            print("Please enter a number between 1 and 9.")
            continue

        try:
            game.make_move(position)
        except ValueError as err:
            print(err)
            continue

        return position


def play_cli() -> None:
    """Run a full command-line Tic-Tac-Toe game loop."""

    game = TicTacToeGame()
    print("Welcome to Tic-Tac-Toe! Players take turns as X and O.\n")

    while True:
        print(game.display_board())
        prompt_move(game)

        winner = game.winner()
        if winner:
            print(game.display_board())
            print(f"Congratulations! Player {winner} wins!")
            break

        if game.is_draw():
            print(game.display_board())
            print("It's a draw!")
            break

        game.switch_player()


if __name__ == "__main__":
    try:
        play_cli()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
