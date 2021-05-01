import sys

from solutions.requirements_group_2_solution.match import Match


def play_game() -> None:
    """
    Set up the game and play until it's done.
    :return: None
    """

    # Initiliaze stuff
    match = Match()

    # Enter game loop
    while not match.is_finished:
        match.play_turn()

    match.print_closing_info()

    print("Press enter to exit")
    sys.exit()


if __name__ == "__main__":
    play_game()
