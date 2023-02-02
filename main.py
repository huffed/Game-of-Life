# !/usr/bin/env python3

# region Imports
import sys
import select
import os
import pandas as pd
import random
import copy
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)
if sys.platform == "win32":
    import msvcrt as m
    from src.win_simple_term_menu import TerminalMenu
    from inputimeout import inputimeout
else:
    from simple_term_menu import TerminalMenu
    import select
# endregion


def game_func(grid_template, grid_size=36):
    # Generate initial grid
    if type(grid_template) != str:
        grid = normal_grid(grid_template, grid_size)
    else:
        grid = random_grid(grid_size)
    counter = 0
    for i in range(grid_size):
        grid.insert(0, [])
        grid.append([])
        for j in range((grid_size*3)):
        
           grid[0].append(".")
           grid[grid_size+1+counter].append(".")
        counter += 2
    del grid_template, counter  # , i, j
    while True:
        def print_grid(grid):
            # Print grid
            cls()
            print(TITLE)
            for row_index in range(grid_size):
                for place_index in range(grid_size):
                    print(Fore.RESET + grid[row_index+grid_size]
                          [place_index+grid_size], end=" ")
                print("")
            print(stylize_text("PRESS ENTER TO EXIT"))
            # Update grid
            previous_grid = copy.deepcopy(grid)
            grid = update_grid(grid, previous_grid, grid_size)

        def stop():
            if sys.platform != "win32":
                a, b, c = select.select([sys.stdin], [], [], 0.1)
                if (len(a) > 0):
                    del a, b, c
                    start_menu()
                else:
                    del a, b, c
                    print_grid(grid)
            else:
                try:
                    inputimeout(prompt='', timeout=0.02)
                    start_menu()
                except Exception:
                    print_grid(grid)
        stop()

# region Grid generators


def random_grid(grid_size):
    grid = []
    for i in range(grid_size):
        row_values = []
        for j in range(grid_size):
            dead_or_alive = random.randint(1, 100)
            if dead_or_alive > 50:
                row_values.append(".")
            else:
                row_values.append("0")
        for j in range(grid_size):
            row_values.insert(0, ".")
            row_values.append(".")
        grid.append(row_values)
    return grid


def normal_grid(grid_template, grid_size):
    grid = []
    for i, row in grid_template.iterrows():
        row_values = []
        for j in range(grid_size):
            row_values.append(row[j+1])
        for j in range(grid_size):
            row_values.insert(0, ".")
            row_values.append(".")
        grid.append(row_values)
    return grid
# endregion


def timeout_input(timeout, prompt="", timeout_value=None):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    else:
        sys.stdout.write('\n')
        sys.stdout.flush()
        return timeout_value


def lexicon_grid(grid_template, grid_size=36):
    if type(grid_template) != str:
        grid = normal_grid(grid_template, grid_size)
    else:
        grid = random_grid(grid_size)
    counter = 0
    for i in range(grid_size):
        grid.insert(0, [])
        grid.append([])
        for j in range((grid_size*3)):
            grid[0].append(".")
            grid[grid_size+1+counter].append(".")
        counter += 2
    for row_index in range(grid_size):
        for place_index in range(grid_size):
            print(Fore.RESET + grid[row_index+grid_size]
                  [place_index+grid_size], end=" ")
        print("")


def update_grid(grid, previous_grid, grid_size):
    alive_counter = 0
    for i in grid[grid_size:grid_size*2]:
        if "0" in i[grid_size:grid_size*2]:
            alive_counter += 1
        else:
            pass
    if alive_counter > 0:
        for row_index in range(len(grid)):
            for place_index in range(len(grid[row_index])):
                # Identifying neighbors
                neighbor_count = 0
                row = previous_grid[row_index]
                row_above = []
                row_below = []
                if row_index == grid_size*3-1:
                    row_above = previous_grid[row_index-1]
                    if place_index == grid_size*3-1:
                        neighbors = row_above[place_index-1] + \
                            row_above[place_index] + row[place_index]
                    elif place_index == 0:
                        neighbors = row_above[place_index+1] + \
                            row_above[place_index] + row[place_index]
                    else:
                        neighbors = row_above[place_index-1] + row_above[place_index] + \
                            row_above[place_index+1] + \
                            row[place_index-1] + row[place_index+1]
                elif row_index == 0:
                    row_below = previous_grid[row_index+1]
                    if place_index == 0:
                        neighbors = row[place_index+1] + \
                            row_below[place_index] + \
                            row_below[place_index+1]
                    elif place_index == grid_size*3-1:
                        neighbors = row_below[place_index] + \
                            row_below[place_index-1] + row[place_index-1]
                    else:
                        neighbors = row_below[place_index-1] + row_below[place_index] + \
                            row_below[place_index+1] + \
                            row[place_index-1] + row[place_index+1]
                else:
                    neighbors = ""
                    row_above = previous_grid[row_index-1]
                    row_below = previous_grid[row_index+1]
                    if 0 <= place_index <= grid_size*3-1:
                        if place_index == 0:
                            neighbors = row_above[place_index] + row_above[place_index+1] + \
                                row[place_index+1] + row_below[place_index] + \
                                row_below[place_index+1]
                        elif place_index == grid_size*3-1:
                            neighbors = row_above[place_index] + row_above[place_index-1] + \
                                row[place_index-1] + row_below[place_index -
                                                               1] + row_below[place_index]
                        else:
                            neighbors = row_above[place_index-1] + row_above[place_index] + row_above[place_index+1] + row[place_index -
                                                                                                                           1] + row[place_index+1] + row_below[place_index-1] + row_below[place_index] + row_below[place_index+1]
                # Checking rules and updating if necessary
                # If cell is alive
                if row[place_index] == "0":
                    if neighbors.count("0") > 1:
                        neighbor_count += neighbors.count("0")
                        if neighbor_count not in [2, 3]:
                            grid[row_index][place_index] = "."
                    else:
                        grid[row_index][place_index] = "."
                # If cell is dead
                else:
                    if neighbors.count("0") == 3:
                        grid[row_index][place_index] = "0"
    return grid


def press_any_key(msg=""):
    print(msg)
    if sys.platform == "win32":
        m.getch()
    else:
        os.system("read -p '' -n1 -s")


def cls():
    if sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')


def stylize_text(text):
    return f"{Style.BRIGHT}\033[1m{Fore.CYAN}{text}{Fore.RESET}{Style.RESET_ALL}"


def menu(options):
    menu = TerminalMenu(options, menu_cursor_style=("fg_cyan", "bold"))
    menu_choice = menu.show()
    return menu_choice


# Calling game
TITLE = f'''\033[4m{stylize_text("John Conway's Game of Life in Python")}\n'''
MODES = ["random", "dragon", "119P4H1V0",
         "1234", "70P5H2V0", "2 glider mess"]
MODES_DICT = {
    "random": ["random", "The random mode will generate a random grid of living and dead cells with a grid size of your choosing."],
    "dragon": [pd.read_csv('src/templates/dragon.csv'), "This spaceship, discovered by Paul Tooke in April 2000, was the first known c/6 spaceship. With 102 cells, it was the smallest known orthogonal c/6 spaceship until Hartmut Holzwart discovered 56P6H1V0 in April 2009"],
    "119P4H1V0": [pd.read_csv('src/templates/119P4H1V0.csv'), "A spaceship discovered by Dean Hickerson in December 1989, the first spaceship of its kind to be found. Hickerson then found a small tagalong for this spaceship which could be attached to one side or both. These three variants of 119P4H1V0 were the only known c/4 orthogonal spaceships until July 1992 when Hartmut Holzwart discovered a larger spaceship, 163P4H1V0."],
    "1234": [pd.read_csv('src/templates/1234.csv'), ""],
    "70P5H2V0": [pd.read_csv('src/templates/70P5H2V0.csv'), "A spaceship discovered by Hartmut Holzwart on 5 December 1992."],
    "2 glider mess": [pd.read_csv('src/templates/2-glider-mess.csv'), "A constellation made up of eight blinkers, four blocks, a beehive and a ship, plus four emitted gliders, created by the following 2-glider collision."]
}

if __name__ == "__main__":
    def start_menu():
        while True:
            cls()
            # Start game
            print(TITLE)
            print(stylize_text("FASTEST ON MAC!\n"))
            menu_choice = menu(["START", "HELP", "LEXICON", "QUIT"])
            # Start
            if menu_choice == 0:
                while True:
                    cls()
                    try:
                        # Get user's game settings
                        print(TITLE)
                        print(stylize_text("Modes\n"))
                        # Get game mode variable
                        mode = menu(MODES)
                        cls()
                        print(TITLE)
                        # If game mode is random
                        if mode == 0:
                            while True:
                                try:
                                    cls()
                                    print(TITLE)
                                    # Get grid size variable
                                    grid_size = int(
                                        int(input(f"{Fore.RESET}Grid size (10-36): {Style.BRIGHT}\033[1m{Fore.CYAN}")))
                                    if not 10 <= grid_size <= 36:
                                        raise Exception
                                    game_func(
                                        MODES_DICT[MODES[mode]][0], grid_size)
                                except Exception:
                                    pass
                        # If game mode is not random
                        else:
                            game_func(MODES_DICT[MODES[mode]][0])
                    except Exception:
                        pass
            # Help
            elif menu_choice == 1:
                print(f"""
{stylize_text("Explanation")}
The Game of Life is not your typical computer game. It is a cellular automaton, and was invented by Cambridge mathematician John Conway.

This game became widely known when it was mentioned in an article published by Scientific American in 1970. It consists of a grid of cells which, based on a few mathematical rules, can live, die or multiply. Depending on the initial conditions, the cells form various patterns throughout the course of the game.

{stylize_text("Rules")}
For a space that is populated:
Each cell with one or no neighbors dies, as if by solitude.


Each cell with four or more neighbors dies, as if by overpopulation.


Each cell with two or three neighbors survives.


For a space that is empty or unpopulated:
Each cell with three neighbors becomes populated.""")
                press_any_key("\nPress any key to go back to menu...")
            # Lexicon
            elif menu_choice == 2:
                cls()
                print(TITLE)
                # Get lexicon choice
                choice = menu(MODES)
                cls()
                print(TITLE)
                print(f"LEXICON - {stylize_text(MODES[choice])}\n")
                # Show grid description
                print(MODES_DICT[MODES[choice]][1])
                print(f"\n{stylize_text('Example of initial grid state (36):')}")
                # Show grid example
                lexicon_grid(MODES_DICT[MODES[choice]][0])
                press_any_key(
                    f"\nPress any key to return to main menu.")
                start_menu()
            # Quit
            elif menu_choice == 3:
                cls()
                quit()
    start_menu()
