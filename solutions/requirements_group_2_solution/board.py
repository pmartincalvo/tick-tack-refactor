"""
Classes related to the state of the board and the cells contained in it.
"""

from typing import Dict, List, Set


class Cell:
    """
    The state of a cell within the board.
    """

    def __init__(self, x_position: int, y_position: int, number_id: int):
        """
        Set initial state.
        :param x_position: the x coordinate within the board.
        :param y_position: the y coordinate within the board.
        :param number_id: an id number for the cell.
        """

        self.x_position = x_position
        self.y_position = y_position
        self.number_id = number_id
        self.contents = None

    @property
    def is_empty(self) -> bool:
        """
        Check if the cell has any content.
        :return: True if empty, False otherwise.
        """
        if self.contents is None:
            return True
        return False


class CellGroup:
    """
    A group of cells.
    """

    def __init__(self, cells: List[Cell]):
        """
        Receive cells.
        :param cells: The cells that form the group.
        """
        self._cells = cells

    @property
    def all_cells_are_empty(self) -> bool:
        """
        Check if all cells in the group are empty.
        :return: True if all are empty, False otherwise.
        """
        return all((cell.is_empty for cell in self._cells))

    @property
    def all_cells_have_mark(self) -> bool:
        """
        Check if all cells have some content.
        :return: True if all have content, False otherwise.
        """
        return all((not cell.is_empty for cell in self._cells))

    @property
    def present_marks(self) -> Set[str]:
        """
        Retrieve the unique set of different marks present within the cells in
        the group.
        :return: The set of unique marks.
        """
        all_marks = [cell.contents for cell in self._cells]
        unique_marks = set(all_marks)

        return unique_marks

    @property
    def there_is_only_one_mark_type(self) -> bool:
        """
        Check that there is only one mark type in the group.
        :return: True if so, False otherwise.
        """
        unique_mark_count = len(self.present_marks)

        return unique_mark_count == 1


class Board:
    """
    The state of the board, along with methods to explore the structure of the
    contents.
    """

    column_count = 3
    row_count = 3
    shape = (column_count, row_count)

    def __init__(self):
        """
        Generate a blank board with no contents and make an internal data
        structure to keep the cells by their number id.
        """
        self.cells_by_position = self._generate_empty_board()
        self._cells_by_number = self._structure_cells_by_number(self.cells_by_position)

    def write_mark_on_cell_if_empty(self, cell_number: int, mark: str) -> None:
        """
        Try to write a mark on a cell, raise an error if it's not empty.
        :param cell_number: The number id of the cell to write into.
        :param mark: The mark to write in the cell.
        :return: None
        """
        target_cell = self._cells_by_number[cell_number]

        if not target_cell.is_empty:
            raise ValueError("Can't write on cell, it has contents")

        self._write_mark_on_cell(cell=target_cell, mark=mark)

    @property
    def there_is_winning_combo(self) -> bool:
        """
        Check all the lines on the board to find any winning combination of
        cells.
        :return: True if there is a winning line of cells, False otherwise.
        """
        for line in self._all_possible_lines_in_board:
            if self._group_of_cells_is_winning_combo(line):
                return True
        return False

    def get_winning_mark(self) -> str:
        """
        Find out what is the mark present in the winning group of cells.
        :return: The winning mark.
        """
        winning_cells = self._get_winning_cells()
        winning_mark = min(
            winning_cells.present_marks
        )  # Set with only one value, use min to get the value

        return winning_mark

    @property
    def there_is_stalemate(self) -> bool:
        """
        Check if the board contains a stalemate situation.
        :return: True if so, False otherwise.
        """
        return not self.there_is_winning_combo and self._all_cells_have_marks

    @property
    def _all_cells_have_marks(self) -> bool:
        """
        Check if all cells in the board have contents.
        :return: True if so, False otherwise.
        """
        return all((not cell.is_empty for cell in self._cells_by_number.values()))

    @staticmethod
    def _write_mark_on_cell(cell: Cell, mark: str) -> None:
        """
        Write a mark on a cell.
        :param cell: the cell to put the mark on.
        :param mark: the mark to write.
        :return: None
        """
        cell.contents = mark

    @staticmethod
    def _generate_empty_board() -> List[List[Cell]]:
        """
        Create all the cells that compose an empty board, in a data structure
        that replicates their coordinates position.
        :return: all the empty cells, correctly placed in a 2D grid.
        """
        cells_by_position = []

        generated_cells_counter = 1
        for row in range(0, Board.shape[0]):
            row_contents = Board._generate_row_of_cells(generated_cells_counter, row)
            cells_by_position.append(row_contents)
            generated_cells_counter += Board.row_count

        return cells_by_position

    @staticmethod
    def _generate_row_of_cells(
        generated_cells_count: int, row_index: int
    ) -> List[Cell]:
        """
        Create a row of empty cells, assigning them sequential number ids.
        :param generated_cells_count: the number to start assigning numbers
        from.
        :param row_index: the row index.
        :return: a row of empty cells.
        """
        row_contents = []
        for cell_in_row in range(0, Board.row_count):
            row_contents.append(
                Cell(
                    x_position=row_index,
                    y_position=cell_in_row,
                    number_id=generated_cells_count,
                )
            )
            generated_cells_count += 1

        return row_contents

    @staticmethod
    def _structure_cells_by_number(
        cells_by_position: List[List[Cell]],
    ) -> Dict[int, Cell]:
        """
        Create a dict structure where cells are keyed by their number id.
        :param cells_by_position: a grid of cells representing the board.
        :return: The same cells, keyed by their number id.
        """
        flat_list_of_cells = [cell for row in cells_by_position for cell in row]

        cells_by_number = {cell.number_id: cell for cell in flat_list_of_cells}

        return cells_by_number

    def _there_is_vertical_winning_combo(self) -> bool:
        """
        Check if there is any vertical winning combination.
        :return: True if so, False otherwise.
        """
        for column_index in range(0, Board.column_count):
            if self._column_has_winning_combo(column_index):
                return True
        return False

    def _there_is_horizontal_winning_combo(self) -> bool:
        """
        Check if there is any horizontal winning combination.
        :return: True if so, False otherwise.
        """
        for row_index in range(0, Board.row_count):
            if self._row_has_winning_combo(row_index):
                return True
        return False

    def _there_is_diagonal_winning_combo(self) -> bool:
        """
        Check if there is any diagonal winning combination.
        :return: True if so, False otherwise.
        """
        for diagonal_index in (1, 2):  # There are 2 diagonals
            if self._diagonal_has_winning_combo(diagonal_index):
                return True
        return False

    def _column_has_winning_combo(self, column_index: int) -> bool:
        """
        Check if a specific column, selected by index, has a winning
        combination.
        :param column_index: the index of the column to check.
        :return: True if so, False otherwise.
        """
        cells_to_check = self._get_cells_in_line("vertical", index=column_index)
        return self._group_of_cells_is_winning_combo(cells_to_check)

    def _row_has_winning_combo(self, row_index: int) -> bool:
        """
        Check if a specific row, selected by index, has a winning
        combination.
        :param row_index: the index of the row to check.
        :return: True if so, False otherwise.
        """
        cells_to_check = self._get_cells_in_line("horizontal", index=row_index)
        return self._group_of_cells_is_winning_combo(cells_to_check)

    def _diagonal_has_winning_combo(self, diagonal_index: int):
        """
        Check if a specific diagonal, selected by index, has a winning
        combination.
        :param diagonal_index: the index of the diagonal to check.
        :return: True if so, False otherwise.
        """
        cells_to_check = self._get_cells_in_line("diagonal", index=diagonal_index)
        return self._group_of_cells_is_winning_combo(cells_to_check)

    def _get_cells_in_line(self, way: str, index: int) -> CellGroup:
        """
        Fetch the group of cells that exist in a line.
        :param way: str indicating if a column, row or diagonal should be
        fetched.
        :param index: the index of the line.
        :return: the cells in the specified line.
        """
        ways_to_functions_mapping = {
            "horizontal": self._get_cells_in_column,
            "vertical": self._get_cells_in_row,
            "diagonal": self._get_cells_in_diagonal,
        }

        cell_getter_function = ways_to_functions_mapping[way]

        return cell_getter_function(index)

    def _get_cells_in_column(self, column_index: int) -> CellGroup:
        """
        Get the group of cells that compose a column.
        :param column_index: the column to get the cells from.
        :return: the cells in that column.
        """
        return CellGroup(
            cells=[
                self.cells_by_position[column_index][row_index]
                for row_index in range(0, Board.row_count)
            ]
        )

    def _get_cells_in_row(self, row_index: int) -> CellGroup:
        """
        Get the group of cells that compose a row.
        :param row_index: the row to get the cells from.
        :return: the cells in that row.
        """
        return CellGroup(
            cells=[
                self.cells_by_position[column_index][row_index]
                for column_index in range(0, Board.column_count)
            ]
        )

    def _get_cells_in_diagonal(self, diagonal_index: int) -> CellGroup:
        """
        Get the group of cells that compose a diagonal.
        :param diagonal_index: the diagonal to get the cells from.
        :return: the cells in that diagonal.
        """
        positions_by_index = {
            1: {  # Iterate top-bottom, left-right
                "x_positions": range(0, Board.column_count),
                "y_positions": range(0, Board.row_count),
            },
            2: {  # Iterate top-bottom, right-left
                "x_positions": range(Board.column_count - 1, -1, -1),
                "y_positions": range(0, Board.row_count),
            },
        }

        positions_to_use = positions_by_index[diagonal_index]

        return CellGroup(
            cells=[
                self.cells_by_position[column_index][row_index]
                for column_index, row_index in zip(
                    positions_to_use["x_positions"], positions_to_use["y_positions"]
                )
            ]
        )

    @staticmethod
    def _group_of_cells_is_winning_combo(cells_to_check: CellGroup) -> bool:
        """
        Check if a group of cells is a winning combination.
        :param cells_to_check: the group of cells to check.
        :return: True if so, False otherwise.
        """
        return (
            cells_to_check.all_cells_have_mark
            and cells_to_check.there_is_only_one_mark_type
        )

    def _get_winning_cells(self) -> CellGroup:
        """
        Search the board to find the winning group of cells and return it.
        :return: the winning group of cells.
        :raises ValueError: if no winning combination is found on the board.
        """
        for line in self._all_possible_lines_in_board:
            if self._group_of_cells_is_winning_combo(line):
                return line
        raise ValueError("There is no winning line in the board.")

    @property
    def _all_possible_lines_in_board(self) -> List[CellGroup]:
        """
        Get all the lines on the board.
        :return: All the lines on the board.
        """

        all_possible_lines = []

        for column_index in range(0, Board.column_count):
            all_possible_lines.append(
                self._get_cells_in_line(way="vertical", index=column_index)
            )

        for row_index in range(0, Board.row_count):
            all_possible_lines.append(
                self._get_cells_in_line(way="horizontal", index=row_index)
            )

        for diagonal_index in [1, 2]:
            all_possible_lines.append(
                self._get_cells_in_line(way="diagonal", index=diagonal_index)
            )

        return all_possible_lines
