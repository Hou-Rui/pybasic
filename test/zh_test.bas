LET 循环次数 = 5
DIM 电流(循环次数) AS DECIMAL
FOR 索引 = 1 TO 循环次数
	电流(索引 - 1) = 索引 / 2 + 1
END FOR

V = 180
PRINT V \ 2 - 4, " ", 5

FOR 索引 = 1 TO 循环次数
	PRINT " # ", 电流(索引 - 1)
END FOR
