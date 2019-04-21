X = INPUT() AS INTEGER
DO
    IF X MOD 2 = 1 THEN
        X = X * 3 + 1
    ELSE
        X = X \ 2
    END IF
    WRITE X + " "
LOOP UNTIL X = 4
PRINT "2 1 ..."
