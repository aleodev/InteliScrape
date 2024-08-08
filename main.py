from reddit_scraper import run as run_reddit
from vantage_scraper import run as run_vantage
import curses


def run_option_function(func):
    # Temporarily exit curses mode to run the function and print its output
    curses.endwin()  # End curses mode to allow printing to the terminal
    func()  # Call the external function
    input("Press Enter to return to the menu...")  # Wait for user input


def print_menu(stdscr, selected_row_idx):
    menu = ["REDDIT SCRAPER", "VANTAGE SCRAPER", "EXIT"]

    stdscr.clear()
    stdscr.addstr(0, 0, "=" * 30)
    stdscr.addstr(1, 0, "         Scraper         ")
    stdscr.addstr(2, 0, "=" * 30)

    for idx, row in enumerate(menu):
        x = 7
        y = 4 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, row)

    stdscr.addstr(y + 2, 0, "=" * 30)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.keypad(True)  # Enable keypad mode to capture special keys
    current_row = 0
    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < 2:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                run_option_function(run_reddit)
                # No need to call curses.wrapper here; the function is handled
            elif current_row == 1:
                run_option_function(run_vantage)
                # No need to call curses.wrapper here; the function is handled
            elif current_row == 2:
                break  # Exit the menu loop and end the program

        print_menu(stdscr, current_row)


if __name__ == "__main__":
    curses.wrapper(main)
