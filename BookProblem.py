class Library(object):
    
    def __init__(self):
        self.index = -1
        self.total_books_in_library = 0
        self.bookSet = set()
        self.signup_days = 0
        self.ship_books_per_day = 0
        self.books_score = 0
        self.grade = -1

    def Grading(self, booksShippedperDay, avgScoreLibrary , signUpDaysRequired, maxBooksShippedPerDay, AverageBookScore, maxSignUpDaysRequired):
        priorityScore  = (avgScoreLibrary/AverageBookScore)
        prioritysignup = ((1-(signUpDaysRequired / maxSignUpDaysRequired)))
        priorityshipping = (booksShippedperDay/maxBooksShippedPerDay)
        grade = priorityshipping+prioritysignup+priorityScore
        return grade


#list containing all libraries 
Librarylist = []

maxBooksShippedPerDay = 0
maxSignUpDaysRequired = 0

file = open("b_read_on.txt")

line0 = file.readline()
line0 = line0.split()


#Total Number of books
TotalBooks = eval(line0[0])
total_libraries = eval(line0[1])
total_scanning_days = eval(line0[2])


#Making a universal book set that contains each book
Uni_Book_Set = set()
#Initializing Universal Book Set
for i in range(TotalBooks):
    Uni_Book_Set.add(i)
#books score in order
line = file.readline()
line = line.split()
books_score = line



#following lines calculates Average book
AverageBookScore = 0
for eachItem in books_score:
    AverageBookScore = AverageBookScore + eval(eachItem)
AverageBookScore = AverageBookScore / TotalBooks

line = file.readline()
line = line.split()

for i in range(total_libraries):
    lib_obj = Library()
    lib_obj.index = i
    lib_obj.total_books_in_library = eval(line[0])
    lib_obj.signup_days = eval(line[1])
    lib_obj.ship_books_per_day = eval(line[2])

    if maxBooksShippedPerDay < lib_obj.ship_books_per_day:
        maxBooksShippedPerDay = lib_obj.ship_books_per_day

    if maxSignUpDaysRequired < lib_obj.signup_days:
        maxSignUpDaysRequired = lib_obj.signup_days 

    line = file.readline()
    line = line.split()

    for eachBook in line:
        lib_obj.bookSet.add(eachBook)

    for eachBook in lib_obj.bookSet:
        lib_obj.books_score += eval( books_score[ eval(eachBook) ] )
    
    lib_obj.books_score = lib_obj.books_score/lib_obj.total_books_in_library

    lib_obj.grade =  lib_obj.Grading(lib_obj.ship_books_per_day,lib_obj.books_score,lib_obj.signup_days,maxBooksShippedPerDay,AverageBookScore,maxSignUpDaysRequired)

    Librarylist.append(lib_obj)

    line = file.readline()
    line = line.split()

libraries_to_run = []

def Scheduler():
    
    Librarylist.sort(key=lambda lib_obj: lib_obj.grade, reverse=True)

    for eachItem in Librarylist:
        print("Library " ,eachItem.index," grade ", eachItem.grade)

