import curses
from pybasic import global_table

stdscr = curses.initscr()
stdscr.keypad(1)
curses.cbreak()
curses.noecho()

@global_table.reflect('XMAX')
def curses_xmax():
    return stdscr.getmaxyx()[1]

@global_table.reflect('YMAX')
def curses_ymax():
    return stdscr.getmaxyx()[0]

@global_table.reflect('XNOW')
def curses_xnow():
    return stdscr.getyx()[1]

@global_table.reflect('YNOW')
def curses_ynow():
    return stdscr.getyx()[0]

@global_table.reflect('LOCATE')
def curses_locate(x, y):
    stdscr.addstr(y, x, '')
    stdscr.refresh()

@global_table.reflect('CHARAT')
def curses_charat(x, y):
    stdscr.getch(y, x)

@global_table.reflect('PRINT')
def curses_print(s):
    stdscr.addstr(s)
    stdscr.refresh()

@global_table.reflect('PRINTBOLD')
def curses_printbold(s):
    stdscr.addstr(s, curses.A_BOLD)

@global_table.reflect('PRINTUDL')
def curses_print_underline(s):
    stdscr.addstr(s, curses.A_UNDERLINE)

@global_table.reflect('SETWAIT')
def curses_setwait(x):
    return curses.halfdelay(int(x * 10))

@global_table.reflect('GETCH')
def curses_getch():
    return stdscr.getch()

@global_table.reflect('PAUSE')
def curses_pause():
    stdscr.getch()

@global_table.reflect('CLS')
def curses_cls():
    stdscr.clear()

@global_table.reflect('CRSEXIT')
def curses_exit():
    stdscr.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()
