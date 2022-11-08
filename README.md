# Redifine_Challenge

The code gets as input one argument which is the  timestamp (TS) and finds the index of the block by the rule tbN < T S < tbN+1.
In order to avoid as many api calls as possible, we first found an evaluated index of the block and then we divided into two cases:
If the time of the index we got is greater than the input and if it is less than the input.
In any case, we reduced our search range and recalculated the average according to the number of blocks in the new range.
