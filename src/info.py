import curses

def info(text):
    def draw_textbox(stdscr, text, start_line):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Display only the portion of text that fits in the window
        lines = text.splitlines()
        for idx in range(start_line, min(start_line + h, len(lines))):
            # Calculate the x-coordinate to center the text horizontally
            x = w // 2 - len(lines[idx]) // 2
            stdscr.addstr(idx - start_line, x, lines[idx])

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
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return "process"
            elif key == curses.KEY_BACKSPACE:
                return "back"
            elif key == ord("e"):
                return "edit"
            draw_textbox(stdscr, text, start_line)

    return curses.wrapper(main)
