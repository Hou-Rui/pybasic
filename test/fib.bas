DIM FIB(100) AS INTEGER
FIB(1) = 1
FIB(2) = 1
FOR X = 3 TO 100
    FIB(X) = FIB(X - 1) + FIB(X - 2)
NEXT X
FOR X = 1 TO 100
    PRINT FIB(X)
NEXT X