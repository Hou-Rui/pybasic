USE BCURSES
S$ = "HELLO, WORLD"
LOCATE (XMAX() - LEN$(S$)) \ 2, YMAX() \ 2
PRINTUDL S$
PAUSE
CRSEXIT