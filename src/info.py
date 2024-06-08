import curses

def info(text):
    def draw_textbox(stdscr, text, start_line):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Display only the portion of text that fits in the window
        lines = text.splitlines()
        for idx in range(start_line, min(start_line + h, len(lines))):
            stdscr.addstr(idx - start_line, 0, lines[idx])

        stdscr.refresh()

    def main(stdscr):
        curses.curs_set(0)
        start_line = 0

        draw_textbox(stdscr, text, start_line)

        while True:
            key = stdscr.getch()
            if key == curses.KEY_UP and start_line > 0:
                start_line -= 1
            elif key == curses.KEY_DOWN and start_line < len(text.splitlines()) - 1:
                start_line += 1
            elif key == curses.KEY_ENTER:
                return "process"
            elif key == curses.KEY_BACKSPACE:
                return "back"
            elif key == ord("e"):
                return "edit"
            draw_textbox(stdscr, text, start_line)

    return curses.wrapper(main)
