#############################################
#               2018-*****                  #
#############################################

from mysql.connector import connect, Error, errorcode
from SQL import *
from msg import *
import csv
import numpy as np

# Connector class to do various operations with a database
class connector():
    def __init__(self) -> None:
        
        # information to connect the DB
        self.connection = connect(
            host = "astronaut.snu.ac.kr",
            port = "7001",
            user = "DB2018_10786",
            password = "DB2018_10786",
            database = "DB2018_10786",
            charset = "utf8"
        )

        # no table schema, yet
        self.schema_ready = False

    # initialize DB (execute once after executing run.py)
    def initialize_db(self):

        with self.connection.cursor(dictionary=True) as cursor :

            # check how many schemas are in DB
            cursor.execute(sql_check_schema_ready)
            cnt = list(cursor.fetchone().values())[0]

            # Check whether there are at least 4 schemas(book, user, rate, loan) (maybe accurately 4)
            self.schema_ready = cnt >= 4

            # There are no schema in DB and have to create 4 schema for table book, user, loan, rate
            if self.schema_ready == False :
                
                # Create schema for tables
                cursor.execute(sql_create_table_book)
                cursor.execute(sql_create_table_user)
                cursor.execute(sql_create_table_loan)
                cursor.execute(sql_create_table_rate)
                self.schema_ready = True

                # Don't forget, I have to commit for save schema
                self.connection.commit()

            # Load ./data.csv
            f = open('./data.csv', 'r', encoding='cp949')
            csvReader = csv.reader(f)

            # Pass the first row, which means column name
            next(csvReader)

            # Loop for each tuple in csv file
            for row in csvReader:
  
                b_id, b_title, b_author, u_id, u_name, b_u_rating = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip()
                
                # Insert new tuple into the table book
                try:
                    self.insert_into_book(b_id, b_title, b_author)
                # If there is the book with the same title and author, raise an error
                except BookAlreadyExistError:
                    pass
                
                # Insert new tuple into the table user
                try :
                    self.insert_into_user(u_id, u_name) 
                except Error as e :
                    pass

                # Insert new tuple into the table rate
                try :
                    cursor.execute(sql_insert_into_rate, (b_id, u_id, b_u_rating))
                    self.connection.commit()
                except Error as e :
                    pass
        
        # After success initialization, return True
        return True
            
    # Insert the new tuple about the book into the table <book>
    def insert_into_book(self, b_id, b_title, b_author):

        # get cursor
        cursor = self.connection.cursor()

        # Integrity check
        try :
            # If book_id is not explicitly mentioned, insert the tuple and commit
            if b_id is None :
                cursor.execute(sql_insert_into_book, (b_title, b_author))
                self.connection.commit()
            # If book_id is explicitly mentioned, insert the tuple and commit
            else :
                cursor.execute(sql_insert_into_book_with_id, (b_id, b_title, b_author))
                self.connection.commit()

        # If there is an error about integrity
        except Error as e :
            # If the book already exists (same title, same author)
            if e.errno == errorcode.ER_DUP_ENTRY :
                raise BookAlreadyExistError(b_title, b_author)
            # If book title or author is too long, raise an appropriate error
            if e.errno == errorcode.ER_DATA_TOO_LONG :
                column_name = e.msg.split("'")[1]
                if column_name == 'book_title' :
                    raise BookTitleTooLongError()
                elif column_name == 'author' :
                    raise BookAuthorTooLongError()
        
        # return success with success message
        return BookInsertSuccess()
    
    # Insert the new tuple about the user into the table <user>
    def insert_into_user(self, u_id, u_name):

        # get cursor
        cursor = self.connection.cursor()

        # Integrity check
        try :
            # If user_id is not explicitly mentioned, insert the tuple and commit
            if u_id is None :
                cursor.execute(sql_insert_into_user, (u_name, ))
            # If user_id is explicitly mentioned, insert the tuple and commit
            else :
                cursor.execute(sql_insert_into_user_with_id, (u_id, u_name))
        
        # If there is an error about integrity
        except Error as e :
            # If the user already exists (same id)
            if e.errno == errorcode.ER_DUP_ENTRY :
                pass
            # If user name is too long, raise an appropriate error
            if e.errno == errorcode.ER_DATA_TOO_LONG :
                raise UserNameTooLongError()
        
        # save it using commit
        self.connection.commit()

        # return success with message
        return UserInsertSuccess()

    # print all book information in DB
    def print_all_book_info(self):

        with self.connection.cursor(dictionary=True) as cursor :
            # get all book information using SQL
            cursor.execute(sql_select_all_info_from_book)

            # result : <type> list
            # element = dictionary = one tuple for data
            result = cursor.fetchall()

            # call the print function with column name and result(list of dictionary)
            self.print_with_format(['id', 'title', 'author', 'avg.rating', 'quantity'], result)
        
        return True

    # print all user information in DB
    def print_all_user_info(self):

        with self.connection.cursor(dictionary=True) as cursor :
            # get all user information using SQL
            cursor.execute(sql_select_all_info_from_user)

            # result : <type> list
            # element = dictionary = one tuple for data
            result = cursor.fetchall()

            # call the print function with column name and result(list of dictionary)
            self.print_with_format(['id', 'name'], result)

        return True

    # print with format using column names and data list
    def print_with_format(self, col_name_list, data_list):
        
        # Check column name to know how many spaces are needed
        space_format = [max(len(col_name) + 2, 8) for col_name in col_name_list]

        # for each data, alternate its type to string or 'None'
        for data in data_list :
            for idx, (key, value) in enumerate(data.items()):
                if value is None :
                    temp = 'None'
                else :
                    temp = str(value)
                
                # Also, check how many spaces are needed for each column to express the tuple
                space_format[idx] = max(space_format[idx], len(temp)+2)
        
        # count how many '-' are needed
        L = max(sum(space_format), 80)

        result = ''

        # first line
        result += '-' * L + '\n'

        # column names
        for i in range(len(space_format)) :
            result += col_name_list[i] + ' ' * (space_format[i] - len(col_name_list[i]))
        result += '\n'

        # add a line
        result += '-' * L + '\n'

        # print each tuple with new line
        for data in data_list :
            for idx, (key, value) in enumerate(data.items()):

                if value is None :
                    temp = 'None'
                else :
                    temp = str(value)
                result += (temp + ' ' * (space_format[idx] - len(temp)))
            result += '\n'
        
        # last line
        result += '-' * L + '\n'

        # PRINT !
        print(result)

    # delete the tuple in table <book> using book_id
    def delete_from_book(self, b_id):

        with self.connection.cursor(dictionary=True) as cursor :

            # check input book_id is valid
            cursor.execute(sql_check_book_exist, (b_id,))
            result = cursor.fetchall()

            # if there is no book with the input book_id
            if result[0]['cnt'] == 0 :
                # raise an error
                raise BookNotExistError(b_id)

            # Check whether the book is already borrowed or not
            cursor.execute(sql_count_book_loaned, (b_id,))
            result = cursor.fetchall()

            # If someone already borrowed the book, you can't delete information about the book
            if result[0]['cnt'] > 0 :
                raise BookisLoanedDeleteError()

            # Execute deletion of the book
            cursor.execute(sql_delete_from_book, (b_id,))

            # save it
            self.connection.commit()
        
        # return success with the message
        return BookDeleteSuccess()

    # delete the tuple in table <user> using user_id
    def delete_from_user(self, u_id):

        with self.connection.cursor(dictionary=True) as cursor :

            # check input user_id is valid
            cursor.execute(sql_check_user_exist, (u_id,))
            result = cursor.fetchall()

            # if there is no user with the input user_id
            if result[0]['cnt'] == 0 :
                raise UserNotExistError(u_id)

            # Check whether the user already borrow the book or not
            cursor.execute(sql_count_user_loaned, (u_id,))
            result = cursor.fetchall()

            # If the user already borrowed a book, you can't delete information about the user
            if result[0]['cnt'] > 0 :
                raise UserisLoanedDeleteError()

            # Execute deletion of the book
            cursor.execute(sql_delete_from_user, (u_id,))

            # save it
            self.connection.commit()

        # return success with the message
        return UserDeleteSuccess()


    # Insert the new tuple about borrowing into the table <loan>
    def insert_into_loan(self, b_id, u_id):
        
        with self.connection.cursor(dictionary=True) as cursor :

            # Check whether the book with b_id exists in the DB
            cursor.execute(sql_check_book_exist, (b_id,))
            result = cursor.fetchall()

            # If the book with b_id does not exist in DB
            if result[0]['cnt'] == 0 :
                raise BookNotExistError(b_id)
            
            # Check whether the user with u_id exists in the DB
            cursor.execute(sql_check_user_exist, (u_id,))
            result = cursor.fetchall()

            # If the user with u_id does not exist in DB
            if result[0]['cnt'] == 0 :
                raise UserNotExistError(u_id)

            # Check whether the book with b_id is loaned
            cursor.execute(sql_count_book_loaned, (b_id,))
            result = cursor.fetchall()

            # If the book is loaned right now, you can't borrow it
            if result[0]['cnt'] > 0 :
                raise BookisLoanedError()
            
            # Check whether the user is borrowing too many books
            cursor.execute(sql_count_user_loaned, (u_id,))
            result = cursor.fetchall()

            # If the user exceed a limit of the number of borrowing books
            if result[0]['cnt'] >= 2 :
                raise UserisLoanedError(u_id)

            # Execute loan and store the information in the table <loan>
            cursor.execute(sql_insert_into_loan, (b_id, u_id))
        
        # save it
        self.connection.commit()

        # return success with the message
        return LoanSuccess()

    # Insert the new tuple about rating into the table <rate>
    def insert_into_rate(self, b_id, u_id, rate):
        
        with self.connection.cursor(dictionary=True) as cursor :

            # Check whether the book with b_id exists in the DB
            cursor.execute(sql_check_book_exist, (b_id,))
            result = cursor.fetchall()

            # If the book with b_id does not exist in DB
            if result[0]['cnt'] == 0 :
                raise BookNotExistError(b_id)
            
            # Check whether the user with u_id exists in the DB
            cursor.execute(sql_check_user_exist, (u_id,))
            result = cursor.fetchall()

            # If the user with u_id does not exist in DB
            if result[0]['cnt'] == 0 :
                raise UserNotExistError(u_id)

            # Check whether the user is borrowing the book
            cursor.execute(sql_check_book_user_exist_in_loan, (b_id, u_id))
            result = cursor.fetchall()

            # If the user is not related to the book
            if result[0]['cnt'] == 0 :
                raise BookUserNotExistInLoanError()

            # Check whether the user with u_id exists in the DB
            cursor.execute(sql_check_book_user_exist_in_rate, (b_id, u_id))
            result = cursor.fetchall()

            # If the user already rated about the book
            if result[0]['cnt'] > 0 :
                try :
                    # Check rate is integer or not
                    int_rate = int(rate)
                except :
                    # If it is not an integer, raise an error
                    raise RateRangeError()
                try :
                    # Update the rate using rate, b_id, and u_id through SQL UPDATE
                    cursor.execute(sql_update_rate, (rate, b_id, u_id))
                except Error as e :
                    # If there is an error about rate
                    if e.errno == errorcode.ER_CHECK_CONSTRAINT_VIOLATED :
                        raise RateRangeError()
                    
            # If the user didn't rate about the book
            else :
                try :
                    # Check rate is integer or not
                    int_rate = int(rate)
                except :
                    # If it is not an integer, raise an error
                    raise RateRangeError()
                try :
                    # Insert the rate using rate, b_id, and u_id through SQL INSERT
                    cursor.execute(sql_insert_into_rate, (b_id, u_id, rate))
                except Error as e :
                    # If there is an error about rate
                    if e.errno == errorcode.ER_CHECK_CONSTRAINT_VIOLATED :
                        raise RateRangeError()
            
            # delete the tuple in loan
            cursor.execute(sql_delete_from_loan, (b_id, u_id))

        # save it
        self.connection.commit()

        # return success with the message
        return ReturnRateSuccess()

    # Print borrowing status for the user with u_id
    def print_borrowing_user(self, u_id):

        with self.connection.cursor(dictionary=True) as cursor :
            
            # Check whether the user with u_id exists in the DB
            cursor.execute(sql_check_user_exist, (u_id,))
            result = cursor.fetchall()

            # If the user with u_id does not exist in DB
            if result[0]['cnt'] == 0 :
                raise UserNotExistError(u_id)
            
            # Load borrowing status about the user
            cursor.execute(sql_select_borrowing_info_for_user, (u_id,))
            result = cursor.fetchall()

            # print it with these column names using the print_with_format function
            self.print_with_format(['id', 'title', 'author'], result)
        
        # return success
        return True
    
    # Search books which contain a query in their titles
    def search_book(self, query):

        with self.connection.cursor(dictionary=True) as cursor :

            # Load all books which contain a query in their titles using LIKE
            cursor.execute(sql_select_book_with_query, (query,))
            result = cursor.fetchall()

            # print it with these column names using the print_with_format function
            self.print_with_format(['id', 'title', 'author', 'avg.rating', 'quantity'], result)
        
        # return success
        return True
    
    # Reset the database with ./data.csv
    def reset_db_with_csv(self):

        with self.connection.cursor(dictionary=True) as cursor :

            # Drop existing tables with this order(considering foreign dependency)
            # This is because inserting new data from csv file should be start with id=1
            cursor.execute(sql_drop_table_rate)
            cursor.execute(sql_drop_table_loan)
            cursor.execute(sql_drop_table_user)
            cursor.execute(sql_drop_table_book)
            self.connection.commit()

            # Create schema for these four tables (Keep this order due to foreign dependency)
            cursor.execute(sql_create_table_book)
            cursor.execute(sql_create_table_user)
            cursor.execute(sql_create_table_loan)
            cursor.execute(sql_create_table_rate)
            self.connection.commit()
            
            # load the csv file
            f = open('./data.csv', 'r', encoding='cp949')
            csvReader = csv.reader(f)

            # Jump the column name
            next(csvReader)

            # For each row(each tuple)
            for row in csvReader:

                # extract values of each attribute
                b_id, b_title, b_author, u_id, u_name, b_u_rating = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip()
                
                try:
                    # Insert new tuple into the table <book>
                    self.insert_into_book(b_id, b_title, b_author)
                except BookAlreadyExistError:
                    # If the book already exists, raise an error
                    pass
                
                try :
                    # Insert new tuple into the table <user>
                    self.insert_into_user(u_id, u_name) 
                except Error as e :
                    pass

                try :
                    # Insert new tuple into the table <rate>
                    cursor.execute(sql_insert_into_rate, (b_id, u_id, b_u_rating))
                    self.connection.commit()
                except Error as e :
                    # Dealing with an error
                    pass

        # return success
        return True
    
    # Recommend a book based on avg.rate and number of rate
    def recommend_book_with_popularity(self, u_id) :

        with self.connection.cursor(dictionary=True) as cursor :

            # Check whether the user with u_id exists in the DB
            cursor.execute(sql_check_user_exist, (u_id,))
            result = cursor.fetchall()

            # If the user with u_id does not exist in DB
            if result[0]['cnt'] == 0 :
                raise UserNotExistError(u_id)
            
            # Recommend a book based on avg.rate
            cursor.execute(sql_recommend_book_with_popularity_rate, (u_id,))
            result1 = cursor.fetchall()

            # Recommend a book based on the number of rate
            cursor.execute(sql_recommend_book_with_popularity_num, (u_id,))
            result2 = cursor.fetchall()

            # print it with these column names using the print_with_format_recommend function
            self.print_with_format_recommend(['id', 'title', 'author', 'avg.rating', 'quantity'], result1, result2, 'Rating-based', 'Popularity-based')
        
        # return success
        return True

    # Similar to the other print function, but you have to consider the line to match the format
    def print_with_format_recommend(self, col_name_list, data_list_1, data_list_2, title1, title2):
        
        # Check column name to know how many spaces are needed
        space_format = [max(len(col_name) + 2, 8) for col_name in col_name_list]

        # For a recommended book based on avg.rate, check space format
        for data in data_list_1 :
            for idx, (key, value) in enumerate(data.items()):
                
                if value is None :
                    # If value is NULL, we should print it as 'None'
                    temp = 'None'
                else :
                    # we have to change the value as str to print well
                    temp = str(value)
                
                space_format[idx] = max(space_format[idx], len(temp)+2)
        
        # For a recommended book based on # of rates, check space format
        for data in data_list_2 :
            for idx, (key, value) in enumerate(data.items()):

                if value is None :
                    # If value is NULL, we should print it as 'None'
                    temp = 'None'
                else :
                    # we have to change the value as str to print well
                    temp = str(value)
                
                space_format[idx] = max(space_format[idx], len(temp)+2)
        
        # Calculate how many '-'s are needed
        L = max(sum(space_format), 80)

        # Start with the new line
        result = ''
        result += '-' * L + '\n'
        
        # print the title and the line
        result += title1 + '\n'
        result += '-' * L + '\n'

        # print the column name
        for i in range(len(space_format)) :
            result += col_name_list[i] + ' ' * (space_format[i] - len(col_name_list[i]))
        result += '\n'

        # print the line
        result += '-' * L + '\n'

        # print the recommended book based on avg.rate
        for data in data_list_1 :
            for idx, (key, value) in enumerate(data.items()):

                if value is None :
                    # print it if the value is NULL
                    temp = 'None'
                else :
                    # you have to change the value to str to print well
                    temp = str(value)
                result += (temp + ' ' * (space_format[idx] - len(temp)))
            result += '\n'
        
        # print new line
        result += '-' * L + '\n'

        # print the title and the line
        result += title2 + '\n'
        result += '-' * L + '\n'

        # print the column name
        for i in range(len(space_format)) :
            result += col_name_list[i] + ' ' * (space_format[i] - len(col_name_list[i]))
        result += '\n'

        # print the line
        result += '-' * L + '\n'

        # print the recommended book based on # of rates
        for data in data_list_2 :
            for idx, (key, value) in enumerate(data.items()):

                if value is None :
                    # print it if the value is NULL
                    temp = 'None'
                else :
                    # you have to change the value to str to print well
                    temp = str(value)
                result += (temp + ' ' * (space_format[idx] - len(temp)))
            result += '\n'
        
        # print the last line
        result += '-' * L + '\n'

        # print !
        print(result)
        
        # return success
        return True

    # Recommend a book based on User-based Collaborative Filtering
    def recommend_book_with_cf(self, u_id) :

        # Function for calculating cosine_similarity
        def cosine_similarity(u1_vec, u2_vec):

            # Calculate dot product and each norm for cosine similarity
            dot_product = np.dot(u1_vec, u2_vec)
            norm_v1 = np.linalg.norm(u1_vec)
            norm_v2 = np.linalg.norm(u2_vec)

            # To handle the case with zero vector
            if norm_v1 == 0 or norm_v2 == 0:
                return 0 
            
            # else, return cosine similarity value
            return dot_product / (norm_v1 * norm_v2)


        with self.connection.cursor(dictionary=True) as cursor :

            # Check whether the user with u_id exists in the DB
            cursor.execute(sql_check_user_exist, (u_id,))
            result = cursor.fetchall()

            # If the user with u_id does not exist in DB
            if result[0]['cnt'] == 0 :
                raise UserNotExistError(u_id)
            
            # get all book ids
            cursor.execute(sql_select_all_ids_from_book)
            result1 = cursor.fetchall()

            # get all user ids
            cursor.execute(sql_select_all_ids_from_user)
            result2 = cursor.fetchall()

            # get all rate information
            cursor.execute(sql_select_all_info_from_rate)
            result3 = cursor.fetchall()

            # user_dic
            # user_dic[user_id] = user_index (in the returned list)
            user_dic, user_id_list = {}, []

            # Fill user_id_list and user_dic
            for idx in range(len(result2)) :
                d = result2[idx]
                user_id_list.append(int(d['user_id']))
                user_dic[int(d['user_id'])] = idx

            # book_dic
            # book_dic[book_id] = book_index (in the returned list)
            book_dic, book_id_list = {}, []

            # Fill book_id_list and book_dic
            for idx in range(len(result1)) :
                d = result1[idx]
                book_id_list.append(int(d['book_id']))
                book_dic[int(d['book_id'])] = idx

            # N = # of users, M = # of books
            N, M = len(user_id_list), len(book_id_list)

            # make an initial matrix about rate (0 means that there is no rate between the user and the book)
            user_book_matrix = np.zeros((N, M))
            
            # Fill the user_book_matrix based on a real rate
            for d in result3 :
                u, b, r = int(d['user_id']), int(d['book_id']), int(d['rate'])
                user_book_matrix[user_dic[u], book_dic[b]] = r

            # make UB_mat which will include user average rate instead of 0
            UB_mat = np.copy(user_book_matrix)

            # for each user
            for u in range(UB_mat.shape[0]):
                row = UB_mat[u]

                # extract non_zero rate(real rate)
                non_zero = row[row > 0]

                # If user has rated at least a book
                # calculate a mean of rates and fill it instead of 0
                if non_zero.shape[0] > 0:
                    user_mean = non_zero.mean()
                    row[row == 0] = user_mean

            # similarity matrix[i][j] : cosine_similarity value between user i and user j
            similarity_matrix = np.zeros((N, N))
            for i in range(N):
                for j in range(N):
                    similarity_matrix[i,j] = cosine_similarity(UB_mat[i,:], UB_mat[j,:])

            # find the target user index
            user_index = user_dic[int(u_id)]

            # Get the similarity scores for the target user
            my_similarity_score = similarity_matrix[user_index]

            # for the user, there are M books including rated books 
            # Already rated books will have -1 as an value, 
            # so it is hard to recommend rated books except he or she didn't rate any book.
            predicted_ratings = -np.ones(M)

            # count how many books can be recommended
            cnt_candidate = 0

            for book_index in range(M):
                # For each book, add weighted_sum and cos_similarity sum for user loop
                weighted_sum = 0
                cos_similarity_sum = 0

                # If the user already rated the book, stop the process
                if user_book_matrix[user_index, book_index] > 0 :
                    continue
                
                # this book(w/ book_index) can be recommended because the user didn't rate
                cnt_candidate += 1

                for u_idx in range(N):
                    # Consider different users, not target user
                    if u_idx != user_index:

                        # Get weight(similarity) and original rate(including esitmated rate) and Add them
                        R = UB_mat[u_idx, book_index]
                        W = my_similarity_score[u_idx]
                        weighted_sum += W * R
                        cos_similarity_sum += W

                # Fill the estimated socre in predicted_ratings
                if cos_similarity_sum != 0:
                    predicted_ratings[book_index] = weighted_sum / cos_similarity_sum

                # Since the user didn't rate any book, coos_similarity_sum == 0
                # So we just fill the value 0
                else:
                    predicted_ratings[book_index] = 0
            
            # When the user rated all books in DB
            if cnt_candidate == 0 :
                # Don't recommend
                self.print_with_format(['id', 'title', 'author', 'avg.rating', 'exp.rating'], [])

                # return success
                return True
            
            # Find the maximum estimated value's index
            # Using np.argmax, find the first index if there are more than one maximums
            recommended_book_index = np.argmax(predicted_ratings)

            # Get book_id from the index mentioned above
            recommended_book_id = book_id_list[recommended_book_index]

            # Load the information about the recommended book
            cursor.execute(sql_select_info_from_book_recommend, (recommended_book_id,))
            result = cursor.fetchall()

            # Add the information using format string
            result[0]['exp.rating'] = f'{np.max(predicted_ratings):.3f}'

            # Print it with these column names
            self.print_with_format(['id', 'title', 'author', 'avg.rating', 'exp.rating'], result)

        # return success
        return True


            
            




