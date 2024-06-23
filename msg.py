#############################################
#               2018-*****                  #
#############################################


################# SUCCESS ###################
#
#
#
# Success and an appropriate message
class BookInsertSuccess():
    def __init__(self):
        self.msg = 'One book successfully inserted'

    def __str__(self):
        return self.msg
    
# Success and an appropriate message
class UserInsertSuccess():
    def __init__(self):
        self.msg = 'One user successfully inserted'

    def __str__(self):
        return self.msg
    
# Success and an appropriate message
class BookDeleteSuccess():
    def __init__(self):
        self.msg = 'One book successfully removed'

    def __str__(self):
        return self.msg
    
# Success and an appropriate message
class UserDeleteSuccess():
    def __init__(self):
        self.msg = 'One user successfully removed'

    def __str__(self):
        return self.msg
    
# Success and an appropriate message
class LoanSuccess():
    def __init__(self):
        self.msg = 'Book successfully checked out'

    def __str__(self):
        return self.msg
    
# Success and an appropriate message
class ReturnRateSuccess():
    def __init__(self):
        self.msg = 'Book successfully returned and rated'

    def __str__(self):
        return self.msg


################## ERROR ####################
#
#
#
# Error and an appropriate message
class BookAlreadyExistError(Exception):
    def __init__(self, title, author) :
        self.msg = f'Book ({title}, {author}) already exists'
    
    def __str__(self) :
        return self.msg

# Error and an appropriate message
class BookTitleTooLongError(Exception):
    def __init__(self) :
        self.msg = 'Title length should range from 1 to 50 characters'
    
    def __str__(self) :
        return self.msg
    
# Error and an appropriate message
class BookAuthorTooLongError(Exception):
    def __init__(self) :
        self.msg = 'Author length should range from 1 to 30 characters'
    
    def __str__(self) :
        return self.msg

# Error and an appropriate message
class UserNameTooLongError(Exception):
    def __init__(self) :
        self.msg = 'Username length should range from 1 to 10 characters'
    
    def __str__(self) :
        return self.msg

# Error and an appropriate message
class BookNotExistError(Exception):
    def __init__(self, b_id) :
        self.msg = f'Book {b_id} does not exist'
    
    def __str__(self) :
        return self.msg
    
# Error and an appropriate message
class BookisLoanedDeleteError(Exception):
    def __init__(self) :
        self.msg = 'Cannot delete a book that is currently borrowed'
    
    def __str__(self) :
        return self.msg
    
# Error and an appropriate message
class UserNotExistError(Exception):
    def __init__(self, u_id) :
        self.msg = f'User {u_id} does not exist'
    
    def __str__(self) :
        return self.msg
    
# Error and an appropriate message
class UserisLoanedDeleteError(Exception):
    def __init__(self) :
        self.msg = 'Cannot delete a user with borrowed books'
    
    def __str__(self) :
        return self.msg
    
# Error and an appropriate message
class BookisLoanedError(Exception):
    def __init__(self) :
        self.msg = 'Cannot check out a book that is currently borrowed'
    
    def __str__(self) :
        return self.msg
    
# Error and an appropriate message
class UserisLoanedError(Exception):
    def __init__(self, u_id) :
        self.msg = f'User {u_id} exceeded the maximum borrowing limit'
    
    def __str__(self) :
        return self.msg
    
# Error and an appropriate message
class BookUserNotExistInLoanError(Exception):
    def __init__(self) :
        self.msg = 'Cannot return and rate a book that is not currently borrowed for this year'
    
    def __str__(self) :
        return self.msg
    
# Error and an appropriate message
class RateRangeError(Exception):
    def __init__(self) :
        self.msg = 'Rating should range from 1 to 5.'
    
    def __str__(self) :
        return self.msg