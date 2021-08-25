"""
Functions for presenting the state of the game visually.
"""


from typing import Any, List, Union

from solutions.requirements_group_2_solution.board import Board, Cell, CellGroup

NEW_LINE_IN_STRING = "\n"
COLUMN_DIVIDER_STRING = "|"
ROW_DIVIDER_STRING = "-"


class BaseCellFilter:
    """
    Cell filters are used to filter out cells depending on some condition.
    """

    def keep(self, cell: Cell) -> bool:
        """
        Tells whether the cell should be kept.
        :param cell: the cell to assess.
        :return: true if it should be kept, false otherwise.
        """
        raise NotImplementedError()

    def filter(self, cell: Cell, default_value: Any = None) -> Union[Cell, Any]:
        """
        Pass a cell through the filter, returning it if it should be kept or
        returning a default value instead if it should not be kept.
        :param cell: the cell to assess.
        :param default_value: the default value to return if the cell should
        not be kept.
        :return: the cell if it should be kept, the default value otherwise.
        """
        if self.keep(cell):
            return cell
        return default_value


class SpecificCellsFilter(BaseCellFilter):
    """
    Filters cells to only keep those that are in a predefined cell group.
    """

    def __init__(self, cells_to_keep: CellGroup):
        """
        Receive the predefined cells.
        :param cells_to_keep: a cell group with the cells to keep.
        """
        self.cells_to_keep = cells_to_keep

    def keep(self, cell: Cell) -> bool:
        """
        Check if the cell is in the group and if so, keep it.
        :param cell: the cell to assess.
        :return: true if the cell is in the predefined group, false otherwise.
        """
        if cell in self.cells_to_keep:
            return True
        return False


class BoardRenderer:
    """
    Renders a board, with some flexibility on how to do so.
    """

    def __init__(self, board: Board):
        """
        Receive the board to render.
        :param board: the board to render.
        """
        self._board = board

    def render(self, active_filter: Union[BaseCellFilter, None] = None) -> str:
        """
        Render the entire board, including cell contents.
        :param active_filter: an optional filter to only show the contents of
        certain cells.
        :return: a string visualizing the state of the board.
        """
        cells_by_position = self._board.cells_by_position

        rendered_board = self._render_divider_row()

        for row in cells_by_position:
            rendered_board += NEW_LINE_IN_STRING + (
                self._filter_and_render_cell_row(row, active_filter)
            )
            rendered_board += NEW_LINE_IN_STRING + (self._render_divider_row())

        return rendered_board

    def _filter_and_render_cell_row(
        self, row: CellGroup, active_filter: BaseCellFilter
    ) -> str:
        """
        Filter the cells of a row with the active filter and the render the
        row.
        :param row: the cells in the row to filter and render.
        :param active_filter: an optional filter to only show the contents of
        certain cells.
        :return: the rendered contents after filtering.
        """
        content_to_render = self._filter_cell_row(row, active_filter)
        render = self._render_cell_row(content_to_render)
        return render

    @staticmethod
    def _render_cell_row(content_to_render: List[str]) -> str:
        """
        Renders a cell row with the passed contents.
        :param content_to_render: the contents of the row cells, as strings.
        :return: a single string representing the entire row.
        """
        return COLUMN_DIVIDER_STRING + "".join(content_to_render)

    def _filter_cell_row(
        self, row: CellGroup, filter_to_apply: BaseCellFilter
    ) -> List[str]:
        """
        Apply a filter to a row of cells and return the content to render.
        :param row: the row of cells.
        :param filter_to_apply: the filter to apply.
        :return: the content to render.
        """
        content_to_render = [
            f" {self._render_cell(cell, filter_to_apply)} " + COLUMN_DIVIDER_STRING
            for cell in row
        ]
        return content_to_render

    @staticmethod
    def _render_cell(cell: Cell, filter_to_apply: BaseCellFilter = None) -> str:
        """
        Render the contents of a cell.
        :param cell: the cell to render.
        :param filter_to_apply: an optional filter to only show the contents of
        certain cells.
        :return: the representation of this cell to render.
        """
        if filter_to_apply is not None:
            cell_should_not_be_kept = not filter_to_apply.keep(cell)
            if cell_should_not_be_kept:
                return " "
        if cell.is_empty:
            return str(cell.number_id)
        return str(cell.contents)

    def _render_divider_row(self) -> str:
        """
        Render a divider row.
        :return: a string representing the division between rows.
        """
        return ROW_DIVIDER_STRING + ROW_DIVIDER_STRING * (self._board.column_count * 4)
