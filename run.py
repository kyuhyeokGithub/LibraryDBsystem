#############################################
#               2018-*****                  #
#############################################

from mysql.connector import connect
from connect_db import *
from msg import *

# Initialize DB once right after executing python run.py
def initialize_database(db_connector):

    db_connector.initialize_db()

    # Print initialization success message
    print('Database successfully initialized\n')
    pass

# Reset DB using ./data.csv
def reset(db_connector):
    
    db_connector.reset_db_with_csv()

    # Print initialization success message
    print('Database successfully initialized\n')
    pass

# Print all information about books in DB
def print_books(db_connector):

    db_connector.print_all_book_info()
    pass

# Print all information about users in DB
def print_users(db_connector):

    db_connector.print_all_user_info()
    pass

# Insert a book with input data
def insert_book(db_connector):
    
    # Get a title, an author as input
    title = input('Book title: ')
    author = input('Book author: ')

    # Try to insert a book
    try :
        success_msg = db_connector.insert_into_book( None, title, author)
        print(str(success_msg)+'\n')
        pass
    # If there is an error mentioned below, insertion is failed and show an error
    except (BookAlreadyExistError, BookAuthorTooLongError, BookTitleTooLongError) as error_msg:
        print(str(error_msg)+'\n')
        pass

# Remove a book with target_book_id(input)
def remove_book(db_connector):
    book_id = input('Book ID: ')
    
    # Try to find out a book with book_id and delete it
    try :
        success_msg = db_connector.delete_from_book(book_id)
        print(str(success_msg)+'\n')
        pass
    
    # If there is an error mentioned below, deletion is failed and show an error
    except (BookNotExistError, BookisLoanedDeleteError) as error_msg:
        print(str(error_msg)+'\n')
        pass

    pass

# Insert an user with input
def insert_user(db_connector):
    name = input('User name: ')
    
    # Try to insert a new user with an input, name
    try :
        success_msg = db_connector.insert_into_user(None, name)
        print(str(success_msg)+'\n')
        pass
    
    # When an error raised (Name is too long to store)
    except (UserNameTooLongError) as error_msg:
        print(str(error_msg)+'\n')
        pass

    pass

# Remove an user with target_user_id(input)
def remove_user(db_connector):
    user_id = input('User ID: ')
    
    # Try to find out an user with user_id and delete it
    try :
        success_msg = db_connector.delete_from_user(user_id)
        print(str(success_msg)+'\n')
        pass

    # If there is an error mentioned below, deletion is failed and show an error
    except (UserNotExistError, UserisLoanedDeleteError) as error_msg:
        print(str(error_msg)+'\n')
        pass

    pass

# To check out(The user(input) borrow the book with book_id(input))
def checkout_book(db_connector):
    book_id = input('Book ID: ')
    user_id = input('User ID: ')

    # Try to store an information about loan
    try :
        success_msg = db_connector.insert_into_loan(book_id, user_id)
        print(str(success_msg)+'\n')
        pass

    # If there is an error mentioned below, show an error
    except (BookNotExistError, UserNotExistError, BookisLoanedError, UserisLoanedError) as error_msg:
        print(str(error_msg)+'\n')
        pass

    pass

# Store information about returning the book and rating about it
def return_and_rate_book(db_connector):
    book_id = input('Book ID: ')
    user_id = input('User ID: ')
    rating = input('Ratings (1~5): ')
    
    # Try to insert a new tuple about rating
    try :
        success_msg = db_connector.insert_into_rate(book_id, user_id, rating)
        print(str(success_msg)+'\n')
        pass

    # If there is an error during the process, show an error
    except (BookNotExistError, UserNotExistError, BookUserNotExistInLoanError, RateRangeError) as error_msg:
        print(str(error_msg)+'\n')
        pass

    pass

# Show borrowing status about the user with an input, user_id
def print_borrowing_status_for_user(db_connector):
    user_id = input('User ID: ')
    
    # Try to print about the user's borrowing status using an input, user_id
    try :
        db_connector.print_borrowing_user(user_id)
        pass

    # If there is an error during the process, show an error
    except (UserNotExistError) as error_msg:
        print(str(error_msg)+'\n')
        pass

    pass

# Search books which contains the query(input)
def search_books(db_connector):
    query = input('Query: ')
    db_connector.search_book(query)
    pass

# Recommend the book based on avg_rating, and popularity for the user(input : user_id)
def recommend_popularity(db_connector):
    
    user_id = input('User ID: ')
    
    # Try to do recommendation process
    try :
        db_connector.recommend_book_with_popularity(user_id)
        pass

    # If there is an error, show an error
    except (UserNotExistError) as error_msg:
        print(str(error_msg)+'\n')
        pass

    pass

# Recommend the book based on CF for the user(input : user_id)
def recommend_item_based(db_connector):
    
    user_id = input('User ID: ')
    
    # Try to do recommendation process
    try :
        db_connector.recommend_book_with_cf(user_id)
        pass

    # If there is an error, show an error
    except (UserNotExistError) as error_msg:
        print(str(error_msg)+'\n')
        pass
    
    pass

# Main function
def main():

    # call the connector implemented in ./connect_db.py
    db_connector = connector()

    # Select your option using number
    while True:
        print('============================================================')
        print('1. initialize database')
        print('2. print all books')
        print('3. print all users')
        print('4. insert a new book')
        print('5. remove a book')
        print('6. insert a new user')
        print('7. remove a user')
        print('8. check out a book')
        print('9. return and rate a book')
        print('10. print borrowing status of a user')
        print('11. search books')
        print('12. recommend a book for a user using popularity-based method')
        print('13. recommend a book for a user using user-based collaborative filtering')
        print('14. exit')
        print('15. reset database')
        print('============================================================')
        menu = int(input('Select your action: '))

        # Depending on an input, menu, db_connector do the process
        if menu == 1:
            initialize_database(db_connector)
        elif menu == 2:
            print_books(db_connector)
        elif menu == 3:
            print_users(db_connector)
        elif menu == 4:
            insert_book(db_connector)
        elif menu == 5:
            remove_book(db_connector)
        elif menu == 6:
            insert_user(db_connector)
        elif menu == 7:
            remove_user(db_connector)
        elif menu == 8:
            checkout_book(db_connector)
        elif menu == 9:
            return_and_rate_book(db_connector)
        elif menu == 10:
            print_borrowing_status_for_user(db_connector)
        elif menu == 11:
            search_books(db_connector)
        elif menu == 12:
            recommend_popularity(db_connector)
        elif menu == 13:
            recommend_item_based(db_connector)
        elif menu == 14:
            print('Bye!')
            break
        elif menu == 15:
            # Have to check one more about initializing DB with ./data.csv
            answer = str(input('Would you like to initialize the database? y/n : '))

            # After checking, if the answer is yes, then do the initialization
            if answer == 'y' or answer == 'Y' :
                reset(db_connector)

        # When people select invalid menu
        else:
            print('Invalid action')

if __name__ == "__main__":
    main()
