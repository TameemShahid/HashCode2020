# HashCode2020 Solution

# Current High Score
5,822,921

# Scenarios:
a) A library can take a very large number of days to sign up and have the lowest scoring books
b) A library can take a very large number of days to sign up BUT have the best scoring books 
c) A library can have the best scoring books but can ship only 1 book per day whereas the library with minimum scoring books
   can ship large number of books per day resulting in more score per day than the largest scoring book library
d) And many more scenarios similar to this

# Basic Algorithm
The most prominent factors that effect the scoring are:
1) Each library signup day
2) Average score of the books of each library
3) Books a library can ship each day

With these factors assign each library a grade based on these factors (maximum grade value is 3, where the best 
possible result in each factor will contribute 1 to the grade):
1) Lower the signup days for a library the better
2) Higher the average score of books for a library the better
3) Higher the amount of books a library can ship per day the better

With a grade assigned to each library schedule each library according to its grade in descending order so the library with the 
best grade signs up first and so. 
