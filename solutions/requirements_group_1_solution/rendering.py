"""
Functions for presenting the state of the game visually.
"""


from typing import List

from solutions.requirements_group_1_solution.board import Board, Cell


def render_board(board: Board) -> str:
    """
    Build a visual representation of the state of the board, with the contents
    of the cells being their marks or, if they are empty, their number id.
    :param board: the board object.
    :return: an ASCII art-style representation of the board.
    """

    cells_by_position = board.cells_by_position

    rendered_board = _render_divider_row(column_count=board.column_count)

    for row in cells_by_position:
        rendered_board += "\n" + (_render_cell_row(row))
        rendered_board += "\n" + (_render_divider_row(column_count=board.column_count))

    return rendered_board


def _render_cell_row(row: List[Cell]) -> str:
    return "|" + "".join([f" {_render_cell(cell)} |" for cell in row])


def _render_cell(cell: Cell) -> str:
    return cell.number_id if cell.is_empty else cell.contents


def _render_divider_row(column_count: int) -> str:
    return "-" + "-" * (column_count * 4)
