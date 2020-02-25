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



def Sorting_Acc_Score(library_object: Library):
    print("Sorting library " ,library_object.index," books according to score")
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
            elif eval( books_score[ eval(library_object.bookSet[j]) ] ) == prev_max and not library_object.books_in_score_order.__contains__(library_object.bookSet[j]):
                library_object.books_in_score_order[i] = library_object.bookSet[j]
                curr_max = eval( books_score[ eval(library_object.bookSet[j]) ] )

        
        prev_max = curr_max
    print("Library: ", library_object.index, " books in score order: ", library_object.books_in_score_order)
    print("Sorting Done!")

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
    
    print("Scheduling Libraries")

    libraries_to_run = sorted(Librarylist, key=lambda lib_obj: lib_obj.grade, reverse=True)

    print("Scheduling Done!")
    return libraries_to_run

def Scan_Books(days=1):
    print("Scanning Books!")
    for j in range(days):
        for eachItem in signed_libs:
            eachItem.books_in_score_order = set(eachItem.books_in_score_order)
            books_to_scan = eachItem.books_in_score_order.difference(scanned_books)

            for i in range(eachItem.ship_books_per_day):
                try:
                    book = books_to_scan.pop()
                    scanned_books.update(book)
                    eachItem.books_scanned_of_lib.append(book)
                except KeyError:
                    pass
    print("Scanning Books Done!")

def Working():
    print("Started Actual Work!")
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
    print("Work Done!")

def PrintScannedBooks():
    print("Scanned books: ",(scanned_books))
    print("Signed up libraries: ", len(signed_libs))

def CountScore():
    score = 0
    for eachItem in scanned_books:
        score = score + eval(books_score[ eval(eachItem) ])

    print("FINAL SCORE: ", score)

def GenerateOutput():
    outputFile = open("output.txt", "w")

    #printing the total libraries signed up
    outputFile.writelines( str(len(signed_libs)) + "\n" )

    for eachItem in signed_libs:
        #printing library index and the count of books it scanned
        outputFile.writelines( str( eachItem.index ) + " " + str( len( eachItem.books_scanned_of_lib ) ) + "\n" )
        
        #printing every book that is scanned by the library
        for i in range( len(eachItem.books_scanned_of_lib) ):
            outputFile.writelines( eachItem.books_scanned_of_lib[i] + " " )
        outputFile.writelines("\n")

    outputFile.close()

def CheckLibScannedBooks():
    for eachItem in signed_libs:
        print("Library: ", eachItem.index, "Scanned Books: ", eachItem.books_scanned_of_lib)


libraries_to_run = Scheduler()
# Working()
#PrintScannedBooks()
CountScore()
CheckLibScannedBooks()
# GenerateOutput()