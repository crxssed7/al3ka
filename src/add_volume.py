import curses

def add_volume():
    def draw_input_screen(stdscr, current_field, input1, input2):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Labels and input fields positions
        label1 = "Start: "
        label2 = "End: "
        input1_y, input1_x = h//2 - 2, w//2 - len(label1)//2
        input2_y, input2_x = h//2, w//2 - len(label2)//2
        submit_y, submit_x = h//2 + 2, w//2 - len("Submit")//2

        stdscr.addstr(input1_y, input1_x, label1)
        stdscr.addstr(input2_y, input2_x, label2)

        if current_field == 0:
            stdscr.attron(curses.color_pair(1))
        stdscr.addstr(input1_y, input1_x + len(label1), input1)
        if current_field == 0:
            stdscr.attroff(curses.color_pair(1))

        if current_field == 1:
            stdscr.attron(curses.color_pair(1))
        stdscr.addstr(input2_y, input2_x + len(label2), input2)
        if current_field == 1:
            stdscr.attroff(curses.color_pair(1))

        if current_field == 2:
            stdscr.attron(curses.color_pair(1))
        stdscr.addstr(submit_y, submit_x, "Submit")
        if current_field == 2:
            stdscr.attroff(curses.color_pair(1))

        stdscr.refresh()

    def main(stdscr):
        curses.curs_set(1)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        input1 = ""
        input2 = ""
        current_field = 0  # 0: input1, 1: input2, 2: submit button

        draw_input_screen(stdscr, current_field, input1, input2)

        while True:
            key = stdscr.getch()

            if key == curses.KEY_UP:
                if current_field > 0:
                    current_field -= 1
            elif key == curses.KEY_DOWN:
                if current_field < 2:
                    current_field += 1
            elif key == curses.KEY_BACKSPACE or key == 127:
                if current_field == 0 and len(input1) > 0:
                    input1 = input1[:-1]
                elif current_field == 1 and len(input2) > 0:
                    input2 = input2[:-1]
            elif key in (10, 13):  # Enter key
                if current_field == 2:
                    return "submit", input1, input2
                else:
                    current_field += 1
            elif key in (curses.KEY_ENTER, ord('\n')):
                if current_field == 2:
                    return "submit", input1, input2
                else:
                    current_field += 1
            elif key == 27: # ESCAPE
                return "cancel", "", ""
            else:
                if current_field == 0:
                    input1 += chr(key)
                elif current_field == 1:
                    input2 += chr(key)

            draw_input_screen(stdscr, current_field, input1, input2)

    return curses.wrapper(main)
