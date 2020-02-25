import threading

#Library class 
class Library(object):
    
    def __init__(self):
        #Index to know which library it is
        self.index = -1
        self.total_books_in_library = 0
        self.bookSet = set()
        self.signup_days = 0
        self.ship_books_per_day = 0
        #Average book score of the library
        self.books_score = 0
        #Grade of the library based on three factors defined in Grading function of library
        self.grade = -1
        #list containing books index in order of score (descending) (highest score book index is at the first index)
        self.books_in_score_order = []
        #list containing all the scanned books of the library to print in the output file
        self.books_scanned_of_lib = []

    def Grading(self, booksShippedperDay, avgScoreLibrary , signUpDaysRequired, maxBooksShippedPerDay, AverageBookScore, maxSignUpDaysRequired):
        """ Assigns each library a grade based on 3 factors, therefore the best library will have a grade
            closest to 3 and the worst library will have a grade closest to 0. The three factors are: 
            1) How many books library can ship per day (Higher the better)
            2) Average book score of the library (Total Book Score of library / Number of books in library) (Higher the better) 
            3) Days required to sign up the library (lower the better) 
            
            The starting 3 parameters are for a specific library, the last 3 parameters are global
            1) MaxBooksShippedPerDay = Highest number of books possible that can be shipped a day
            2) AverageBookScore = The average book score of ALL the books (not of a library but universally)
            3) MaxSignUpDaysRequired = Highest number of signup days out of all library """

        priorityScore  = (avgScoreLibrary/AverageBookScore)
        prioritysignup = ((1-(signUpDaysRequired / maxSignUpDaysRequired)))
        priorityshipping = (booksShippedperDay/maxBooksShippedPerDay)
        grade = priorityshipping+prioritysignup+priorityScore
        return grade
    
#**********************************************************************************************************************#

class Book(object):
    #Book class made with the thought of otimizing the code. Can be used effectively
    def __init__(self):
        self.index = -1
        self.score = -1

#**********************************************************************************************************************#

#list containing all libraries 
Librarylist = []

maxBooksShippedPerDay = 0
maxSignUpDaysRequired = 0

#**********************************************************************************************************************#

file = open("b_read_on.txt")

#read the first line (0th) to pick up total number of books, libraries and scanning days
line0 = file.readline()
line0 = line0.split()


#Total Number of books, libraries, and scanning days
TotalBooks = eval(line0[0])
total_libraries = eval(line0[1])
total_scanning_days = eval(line0[2])


#Making a universal book set that contains each book
Uni_Book_Set = set()
#Initializing Universal Book Set
for i in range(TotalBooks):
    Uni_Book_Set.add(i)

#read the second line(1th)
#books_score is a list containing score of every book, in the format [a] = b where "a" = book and "b" = score
line = file.readline()
line = line.split()
books_score = line

#**********************************************************************************************************************#

def Sorting_Acc_Score(library_object: Library):

    """ Function that sorts all the books in the library according to their score
        (Highest scoring book is at the first index). Its time complexity is O(n^2).
        Book class can be used to reprsent books and then python build in function
        sorted(key=lambda book_obj: book_obj.score, reverse=True) for I think more
        optimized sort"""

    print("Sorting library " ,library_object.index," books according to score")

    #converting BookSet of library to list and then sorting the books in ascending order for easier management 
    # of books (we will know for sure that 0th book is on 0th index and we can easily map 0th index book to
    # 0th index of book score for easier retrieval of score  )
    library_object.bookSet = list(library_object.bookSet)
    library_object.bookSet = sorted(library_object.bookSet)

    #variable used to keep track of previous highest score (for example if previous book had a score of 50
    # then we need to find a book with a score less than 50 but have the highest score than the remaining)
    # Initially prev_max is set to 1 greater than the book with the highest score
    prev_max = eval(max(books_score)) + 1

    for i in range( len(library_object.bookSet) ):
        #variable used to find the highest scoring book in the current iteration
        curr_max = 0
        for j in range( len(library_object.bookSet) ):
            #if book score is greater than current max score found but less than the previous iteration highest score than 
            #it is the current highest scoring book 
            if eval( books_score[ eval(library_object.bookSet[j]) ] ) > curr_max and eval( books_score[ eval(library_object.bookSet[j]) ] ) < prev_max:
                library_object.books_in_score_order[i] = library_object.bookSet[j]
                curr_max = eval( books_score[ eval(library_object.bookSet[j]) ] )

            #if an event occurs where current highest book score is equal to previous iteration highest book score
            #for example (2 books have the same score that is 100) then put the book in the next index
            elif eval( books_score[ eval(library_object.bookSet[j]) ] ) == prev_max and not library_object.books_in_score_order.__contains__(library_object.bookSet[j]):
                library_object.books_in_score_order[i] = library_object.bookSet[j]
                curr_max = eval( books_score[ eval(library_object.bookSet[j]) ] )

        #set prev_max to the current max after each iteration of inner loop
        prev_max = curr_max
    print("Library: ", library_object.index, " books in score order: ", library_object.books_in_score_order)
    print("Sorting Done!")

#following lines calculates Average book score of all books
AverageBookScore = 0
for eachItem in books_score:
    AverageBookScore = AverageBookScore + eval(eachItem)
AverageBookScore = AverageBookScore / TotalBooks

#**********************************************************************************************************************#



#read the third line (2th) containing number of books, signup days, and shipment of books per day of the library
line = file.readline()
line = line.split()

for i in range(total_libraries):
    #make a library object and fill the relevant data read from the line of file
    lib_obj = Library()
    lib_obj.index = i
    lib_obj.total_books_in_library = eval(line[0])
    lib_obj.signup_days = eval(line[1])
    lib_obj.ship_books_per_day = eval(line[2])

    #if the library has shipment per day greater than global max books shipped per day than update
    if maxBooksShippedPerDay < lib_obj.ship_books_per_day:
        maxBooksShippedPerDay = lib_obj.ship_books_per_day

    #if the library has signup days greater than global max books signup days than update
    if maxSignUpDaysRequired < lib_obj.signup_days:
        maxSignUpDaysRequired = lib_obj.signup_days 

    #read the next line to get the books in the library
    line = file.readline()
    line = line.split()

    #add each book in the read line to the bookset of library and also in the books in score order list 
    #which will be sorted later
    for eachBook in line:
        lib_obj.bookSet.add(eachBook)
        # book_obj = Book()
        # book_obj.index = eachBook
        # book_obj.score = books_score[eval(eachBook)]
        lib_obj.books_in_score_order.append(eachBook)


    #sort the books of the library in score order
    Sorting_Acc_Score(lib_obj)
    #lib_obj.books_in_score_order.sort(key=lambda book_obj: book_obj.score, reverse=True)


    #find the average book score of the library
    for eachBook in lib_obj.bookSet:
        lib_obj.books_score += eval( books_score[ eval(eachBook) ] )
    lib_obj.books_score = lib_obj.books_score/lib_obj.total_books_in_library

    #find the grade of the library
    lib_obj.grade =  lib_obj.Grading(lib_obj.ship_books_per_day,lib_obj.books_score,lib_obj.signup_days,maxBooksShippedPerDay,AverageBookScore,maxSignUpDaysRequired)

    #add the library to the list of libraries
    Librarylist.append(lib_obj)

    #IF YOU WANT TO PARTIALLY GENERATE A ACCEPTABLE OUTPUT THAT WILL HAVE A SCORE AND NOT FOR THE WHOLE FILE, UNCOMMENT THE FOLLOWING LINES 
    # ans = input("Continue? [y/n]..")
    # if ans == "n":
    #     break
    # else:
    #     pass

    #read the next line to get info for the next library
    line = file.readline()
    line = line.split()
#************************************************************************************************************************#


#list containing the libraries to run in order of grade (descending) (Highest grade library is first)
libraries_to_run = []
#set containing all the scanned books
scanned_books = set()
#list containing those libraries that have been signed up and now can scan their books
signed_libs = []




def Scheduler():

    """ Functions that schedules or sort the libraries in the order of their grade (descending) """

    print("Scheduling Libraries")

    libraries_to_run = sorted(Librarylist, key=lambda lib_obj: lib_obj.grade, reverse=True)

    print("Scheduling Done!")
    return libraries_to_run



def Scan_Books(days=1):

    """ Functions that will scan the books of all signed up libraries for the number of days 
        some library is signing up for. For example: library 5 takes 3 days to sign up, this 
        function will scan the books of all the already signed up library for 3 days, and when
        all the libraries are signed up this function will run for 1 day """

    print("Scanning Books!")
    for j in range(days):
        #for every library that has been signed up
        for eachItem in signed_libs:
            #Every library remaining books_to_scan is found by subtracting the already scanned books 
            #from the books_in_score_order to make sure all the highest scoring books are scanned first
            eachItem.books_in_score_order = set(eachItem.books_in_score_order)
            books_to_scan = eachItem.books_in_score_order.difference(scanned_books)

            #This loop ensures that each library can scan only the amount of books it can ship per day
            for i in range(eachItem.ship_books_per_day):
                try:
                    book = books_to_scan.pop()
                    scanned_books.update(book)
                    eachItem.books_in_score_order.remove(book)
                    eachItem.books_scanned_of_lib.append(book)
                except KeyError:
                    pass
    print("Scanning Books Done!")



def Working():

    """ Function that runs for the total days available and calls the ScanBooks() to scan the books.
        If some library is signing up call the ScanBooks() for that number of days else just call the function 
        for one day """

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

        try:
            libraries_to_run.pop(0)
        except IndexError:
            pass
    print("Work Done!")



def PrintScannedBooks():

    """ Function that prints all the books that have scanned along with the total number of libraries signed up """

    print("Scanned books: ",(scanned_books))
    print("Signed up libraries: ", len(signed_libs))




def CountScore():

    """ Function to check the score generated rather than to submit the file and see some error related to 
        output file """

    score = 0
    for eachItem in scanned_books:
        score = score + eval(books_score[ eval(eachItem) ])

    print("FINAL SCORE: ", score)




def GenerateOutput():

    """ Function to generate the text in the output file """

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

    """ Check the scanned books of each library """

    for eachItem in signed_libs:
        print("Library: ", eachItem.index, "Scanned Books: ", eachItem.books_scanned_of_lib)


libraries_to_run = Scheduler()
Working()
#PrintScannedBooks()
CountScore()
CheckLibScannedBooks()
GenerateOutput()