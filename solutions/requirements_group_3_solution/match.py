from solutions.requirements_group_3_solution.board import Board
from solutions.requirements_group_3_solution.rendering import (
    BoardRenderer,
    SpecificCellsFilter,
)
from solutions.requirements_group_3_solution.utils import input_with_validation


class Match:
    """
    The state of the match and the actions to play each turn and finish the
    game.
    """

    def __init__(self, first_player: int, board_size: int):
        """
        Set up initial state.
        :param first_player: the number of the player who moves first.
        :param board_size: indicates the size of the board.
        """
        self._board = Board(size=board_size)
        self._board_renderer = BoardRenderer(self._board)
        self._players_by_number = {
            1: Player(number_id=1, mark="X"),
            2: Player(number_id=2, mark="O"),
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
        print(self._board_renderer.render())
        print(f"Next move: Player {self._current_player.number_id}")

        while True:
            chosen_cell = int(
                input_with_validation(
                    prompt=f"Which cell to mark?[{self._board.first_cell_id}"
                    f"-{self._board.last_cell_id}]",
                    validation_func=lambda x: self._board.first_cell_id
                    <= int(x)
                    <= self._board.last_cell_id,
                    retry=True,
                )
            )
            try:
                self._board.write_mark_on_cell_if_empty(
                    cell_number=chosen_cell, mark=self._current_player.mark
                )
                break
            except ValueError:
                print("Can't write on that cell, it already has a mark.")
                print("Try again")

        self._switch_current_player()
        print("/////////////////////////////")

    @property
    def is_finished(self) -> bool:
        """
        Check if the match is done, either because there is a winner or because
        a stalemate has been reached.
        :return: True if so, False otherwise.
        """
        return self._board.there_is_winning_combo or self._board.there_is_stalemate

    def _switch_current_player(self) -> None:
        if self._current_player.number_id == 1:
            self._current_player = self._players_by_number[2]
            return
        if self._current_player.number_id == 2:
            self._current_player = self._players_by_number[1]
            return

    def print_closing_info(self) -> None:
        """
        Print the final state of the board and announce the result of the
        match.
        :return: None
        """

        if self._board.there_is_winning_combo:
            print(
                self._board_renderer.render(
                    SpecificCellsFilter(cells_to_keep=self._board.get_winning_cells())
                )
            )
            winning_mark = self._board.get_winning_mark()
            winning_player = self._players_by_mark[winning_mark]
            print(f"Player {winning_player.number_id} has won!!!!!!!!!!!!!!!!!!!!!!")
        if self._board.there_is_stalemate:
            print(self._board_renderer.render())
            print("Stalemate. Nobody wins this time!")


class Player:
    """
    A player in the match.
    """

    def __init__(self, number_id: int, mark: str):
        """
        Identify the player with a number and assign which mark he will use on
        the board.
        :param number_id: the player's number
        :param mark: the mark to use on the board.
        """
        self.number_id = number_id
        self.mark = mark
