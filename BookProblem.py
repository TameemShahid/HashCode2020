import threading

#Library class 
class Library(object):
    
    def __init__(self):
        self.index = -1
        self.total_books_in_library = 0
        self.bookSet = set()
        self.signup_days = 0
        self.ship_books_per_day = 0
        self.books_score = 0
        self.grade = -1
        self.books_in_score_order = []
        self.books_scanned_of_lib = []

    def Grading(self, booksShippedperDay, avgScoreLibrary , signUpDaysRequired, maxBooksShippedPerDay, AverageBookScore, maxSignUpDaysRequired):
        priorityScore  = (avgScoreLibrary/AverageBookScore)
        prioritysignup = ((1-(signUpDaysRequired / maxSignUpDaysRequired)))
        priorityshipping = (booksShippedperDay/maxBooksShippedPerDay)
        grade = priorityshipping+prioritysignup+priorityScore
        return grade


class Book(object):

    def __init__(self):
        self.index = -1
        self.score = -1


#list containing all libraries 
Librarylist = []

maxBooksShippedPerDay = 0
maxSignUpDaysRequired = 0

file = open("a_example.txt")

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



def Sorting_Acc_Score(library_object: Library):
    library_object.bookSet = list(library_object.bookSet)
    library_object.bookSet = sorted(library_object.bookSet)

    prev_max = eval(max(books_score)) + 1

    for i in range( len(library_object.bookSet) ):
        curr_max = 0
        for j in range( len(library_object.bookSet) ):
            # library_object.books_in_score_order[i] = library_object.bookSet[j]

            if eval( books_score[ eval(library_object.bookSet[j]) ] ) > curr_max and eval( books_score[ eval(library_object.bookSet[j]) ] ) < prev_max:
                library_object.books_in_score_order[i] = library_object.bookSet[j]
                curr_max = eval( books_score[ eval(library_object.bookSet[j]) ] )

        
        prev_max = curr_max

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
        # book_obj = Book()
        # book_obj.index = eachBook
        # book_obj.score = books_score[eval(eachBook)]
        lib_obj.books_in_score_order.append(eachBook)

    Sorting_Acc_Score(lib_obj)
    #lib_obj.books_in_score_order.sort(key=lambda book_obj: book_obj.score, reverse=True)

    for eachBook in lib_obj.bookSet:
        lib_obj.books_score += eval( books_score[ eval(eachBook) ] )
    
    lib_obj.books_score = lib_obj.books_score/lib_obj.total_books_in_library

    lib_obj.grade =  lib_obj.Grading(lib_obj.ship_books_per_day,lib_obj.books_score,lib_obj.signup_days,maxBooksShippedPerDay,AverageBookScore,maxSignUpDaysRequired)

    Librarylist.append(lib_obj)



    line = file.readline()
    line = line.split()

libraries_to_run = []
scanned_books = set()
signed_libs = []


def Scheduler():
    
    libraries_to_run = sorted(Librarylist, key=lambda lib_obj: lib_obj.grade, reverse=True)
    for eachItem in libraries_to_run:
        print("library: ", eachItem.index, " grade: ", eachItem.grade)
    
    print("TOTAL LIBRARIES: ", len(libraries_to_run))
    return libraries_to_run

def Scan_Books(days=1):
    for j in range(days):
        for eachItem in signed_libs:
            eachItem.books_in_score_order = set(eachItem.books_in_score_order)
            books_to_scan = eachItem.books_in_score_order.difference(scanned_books)

            print("books to scan: ", len(books_to_scan))
            for i in range(eachItem.ship_books_per_day):
                try:
                    scanned_books.update(books_to_scan.pop())
                    # books_to_scan.remove(books_to_scan[0])
                except KeyError:
                    pass

def Working():
    scanned_books = set()

    remaining_days = total_scanning_days
    i = 0
    while remaining_days > 0:
        if len(libraries_to_run) > i:
            remaining_days -= libraries_to_run[i].signup_days
            Scan_Books( libraries_to_run[i].signup_days )
            signed_libs.append(libraries_to_run[i])
            print("remaining days: ", remaining_days)
        else:
            Scan_Books()
            remaining_days -= 1
            print("remaining days: ", remaining_days)

        # i = i+1
        try:
            libraries_to_run.pop(0)
        except IndexError:
            pass

def PrintScannedBooks():
    print("Scanned books: ",(scanned_books))
    print("Signed up libraries: ", len(signed_libs))

def CountScore():
    score = 0
    for eachItem in scanned_books:
        score = score + eval(books_score[ eval(eachItem) ])

    print("FINAL SCORE: ", score)

outputFile = open("output.txt", "w")

libraries_to_run = Scheduler()
Working()
PrintScannedBooks()
CountScore()

outputFile.close()