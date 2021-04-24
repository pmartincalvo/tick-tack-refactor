import sys

from solutions.requirements_group_1_solution.match import Match


def play_game():

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
