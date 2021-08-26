import sys

from solutions.requirements_group_2_solution.match import Match
from solutions.requirements_group_2_solution.utils import input_with_validation


def play_game() -> None:
    """
    Set up the game and play until it's done.
    :return: None
    """

    wants_to_play = "y"

    while wants_to_play == "y":

        chosen_first_player = int(
            input_with_validation(
                "Pick the first player [1, 2]:",
                validation_func=lambda x: x in ["1", "2"],
                retry=True,
            )
        )
        # Initiliaze stuff
        match = Match(first_player=chosen_first_player)

        # Enter game loop
        while not match.is_finished:
            match.play_turn()

        match.print_closing_info()

        wants_to_play = input_with_validation(
            "Do you want to play again? (y/n)",
            validation_func=lambda x: x in ["y", "n"],
            retry=True,
        )

    input("Press enter to exit")
    sys.exit()


if __name__ == "__main__":
    play_game()
