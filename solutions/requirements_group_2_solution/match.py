from solutions.requirements_group_2_solution.board import Board
from solutions.requirements_group_2_solution.rendering import render_board


class Match:
    """
    The state of the match and the actions to play each turn and finish the
    game.
    """

    def __init__(self, first_player: int):
        """
        Set up initial state.
        :param first_player: the number of the player who moves first.
        """
        self._board = Board()
        self._players_by_number = {
            1: Player(number=1, mark="X"),
            2: Player(number=2, mark="O"),
        }
        self._players_by_mark = {
            player.mark: player for player in self._players_by_number.values()
        }
        self._current_player = self._players_by_number[first_player]

    def play_turn(self) -> None:
        """
        Flow of a turn.
        :return: None
        """
        print(render_board(self._board))
        print(f"Next move: Player {self._current_player.number}")

        input_is_valid = False
        while not input_is_valid:
            chosen_cell = int(input("Which cell to mark?[1-9]"))
            if not 1 <= chosen_cell <= 9:
                print("That's not a valid cell number.")
                print("Try again")
                continue

            try:
                self._board.write_mark_on_cell_if_empty(
                    cell_number=chosen_cell, mark=self._current_player.mark
                )
                input_is_valid = True
            except ValueError:
                print("Can't write on that cell, it already has a mark.")
                print("Try again")
                continue

        self._switch_current_player()
        print("/////////////////////////////")

    @property
    def is_finished(self) -> bool:
        """
        Check if the match is done, either because there is a winner of because
        a stalemate has been reached.
        :return: True if so, False otherwise.
        """
        return self._board.there_is_winning_combo or self._board.there_is_stalemate

    def _switch_current_player(self) -> None:
        if self._current_player.number == 1:
            self._current_player = self._players_by_number[2]
            return
        if self._current_player.number == 2:
            self._current_player = self._players_by_number[1]
            return

    def print_closing_info(self) -> None:
        """
        Print the final state of the board and announce the result of the
        match.
        :return: None
        """
        print(render_board(board=self._board))

        if self._board.there_is_winning_combo:
            winning_mark = self._board.get_winning_mark()
            winning_player = self._players_by_mark[winning_mark]
            print(f"Player {winning_player.number_id} has won!!!!!!!!!!!!!!!!!!!!!!")
        if self._board.there_is_stalemate:
            print("Stalemate. Nobody wins this time!")


class Player:
    """
    A player in the match.
    """

    def __init__(self, number: int, mark: str):
        """
        Identify the player with a number and assign which mark he will use on
        the board.
        :param number: the player's number
        :param mark: the mark to use on the board.
        """
        self.number = number
        self.mark = mark
