# pylint: disable=import-error
"""Convert Anilist activities to human readable format for volume start date and end date"""
import sys

import curses

from process import process
from file_operations import open_file, write_file, list_files_in_directory
from add_volume import add_volume
from info import info

def display_select_list(options):
    def draw_menu(stdscr, current_row_idx, start_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx in range(start_row_idx, min(start_row_idx + h - 1, len(options))):
            row = str(options[idx]).replace(".json", "")
            x = w // 2 - len(row) // 2
            y = idx - start_row_idx

            if idx == current_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()

    def main(stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        current_row_idx = 0
        start_row_idx = 0

        draw_menu(stdscr, current_row_idx, start_row_idx)

        while True:
            key = stdscr.getch()
            if key == curses.KEY_UP:
                if current_row_idx > 0:
                    current_row_idx -= 1
                    if current_row_idx < start_row_idx:
                        start_row_idx -= 1
            elif key == curses.KEY_DOWN:
                if current_row_idx < len(options) - 1:
                    current_row_idx += 1
                    # pylint: disable=no-member
                    if current_row_idx >= start_row_idx + curses.LINES - 1:
                        start_row_idx += 1
            elif key in [73, 105]:
                return options[current_row_idx], "info"
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return options[current_row_idx], "process"
            elif key == curses.KEY_BACKSPACE:
                return "", "quit"

            draw_menu(stdscr, current_row_idx, start_row_idx)

    return curses.wrapper(main)

def main():
    """Entry point"""
    files = list_files_in_directory("../json/")
    selected, action = display_select_list(files)

    if action == "process":
        process_result = process(selected)
        if process_result == "back":
            main()
            return
    elif action == "info":
        media_id, volumes = open_file(selected)
        last = volumes[-1]
        text = f"{selected.replace(".json", "")}\nAmount of volumes: {len(volumes)}\nLast record: {str(last)}"
        info_result = info(text)
        if info_result == "back":
            main()
            return
        elif info_result == "edit":
            submission, start, end = add_volume()
            if submission == "submit":
                volumes.append({"start": int(start), "end": int(end)})
                write_file(selected, media_id, volumes)
                p_result = process(selected)
                if p_result == "back":
                    main()
                    return
            elif submission == "cancel":
                main()
                return
        elif info_result == "process":
            p_result = process(selected)
            if p_result == "back":
                main()
                return
    elif action == "quit":
        sys.exit()

if __name__ == "__main__":
    main()
