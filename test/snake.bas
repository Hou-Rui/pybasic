USE BCURSES
USE BQUEUE

FUNCTION PAIR(X, Y)
    THIS = STRUCT()
    THIS.X = X
    THIS.Y = Y
    RETURN THIS
END FUNCTION

SNAKE = QUEUE()
TOP = PAIR(0, 0)
MOVE = PAIR(1, 0)
APPLE = PAIR(-1, 0)
DIM WINCHARS(XMAX() * YMAX()) as integer
FOR i = 0 TO XMAX() * YMAX()
    WINCHARS(i) = ASC("!")
NEXT i

SUB SNKINIT()
    SETWAIT 0.5
    FOR X = 1 TO 10
        Y = YMAX() \ 2
        PUSH SNAKE, PAIR(X, Y)
        TOP = PAIR(X, Y)
        LOCATE X, Y
        WINCHARS(X * YMAX() + Y) = ASC("*")
        CRSPRINT "*"
    NEXT X
END SUB

SUB SNKMOVE()
    TOP = PAIR(TOP.X + MOVE.X, TOP.Y + MOVE.Y)
    SNKJUDGE(TOP)
    IF APPLE.X <> -1 THEN
        OLD = POP(SNAKE)
        LOCATE OLD.X, OLD.Y
        WINCHARS(OLD.X * YMAX() + OLD.Y) = ASC(" ")
        CRSPRINT " "

        LOCATE APPLE.X, APPLE.Y
        WINCHARS(APPLE.X * YMAX() + APPLE.Y) = ASC("@")
        CRSPRINT "@"
    END IF
    PUSH SNAKE, TOP
    LOCATE TOP.X, TOP.Y
    WINCHARS(TOP.X * YMAX() + TOP.Y) = ASC("*")
    CRSPRINT "*"
END SUB

SUB SNKJUDGE(NXT)
    'CRSPRINT NXT.X, NXT.Y
    'LOCATE 1, 2
    'CRSPRINT XMAX(), YMAX()
    IF NXT.X < 0 OR NXT.X >= XMAX() OR NXT.Y < 0 OR NXT.Y >= YMAX() THEN
        GAMEOVER
    END IF
    ' C = CHARAT(NXT.X, NXT.Y)
    C = CHR$(WINCHARS(NXT.X * YMAX() + NXT.Y))
    LOCATE 2, 2
    CRSPRINT C
    IF C = "*" THEN
        GAMEOVER
    END IF
    IF C = "@" THEN
        APPLE.X = -1
    END IF
END SUB

SUB GAMEOVER()
    ' CLS
    LOCATE XMAX() \ 2 - 4, YMAX() \ 2
    CRSPRINT "GAME OVER!"
    PAUSE
    CRSEXIT
    END
END SUB

SUB SNKINPUT()
    C = GETCH()
    IF C = ASC("w") OR C = ASC("W") THEN
        MOVE = PAIR(0, -1)
    ELSEIF C = ASC("s") OR C = ASC("S") THEN
        MOVE = PAIR(0, 1)
    ELSEIF C = ASC("a") OR C = ASC("A") THEN
        MOVE = PAIR(-1, 0)
    ELSEIF C = ASC("d") OR C = ASC("D") THEN
        MOVE = PAIR(1, 0)
    END IF
END SUB

SUB RNDAPPLE()
    IF APPLE.X = -1 THEN
        APPLE.X = RANDINT(0, XMAX() - 1)
        APPLE.Y = RANDINT(0, YMAX() - 1)
    END IF
END SUB

SUB PLAYGAME()
    DO
        RNDAPPLE
        SNKMOVE
        SNKINPUT
    LOOP
END SUB

'    PRINT XMAX() \ 2 - 4, YMAX() \ 2
' C = GETCH()
SNKINIT
PLAYGAME
CRSEXIT
PRINT "PROG END"