#############################################
#               2018-*****                  #
#############################################

# SQL for creating the table
sql_create_table_book = "\
    CREATE TABLE book(\
        book_id INT NOT NULL AUTO_INCREMENT,\
        book_title VARCHAR(50),\
        author VARCHAR(30),\
        PRIMARY KEY (book_id),\
        UNIQUE (book_title, author)\
    );\
"

# SQL for creating the table
sql_create_table_user = "\
    CREATE TABLE user(\
        user_id INT NOT NULL AUTO_INCREMENT,\
        name VARCHAR(10),\
        PRIMARY KEY (user_id)\
    );\
"

# SQL for creating the table
sql_create_table_loan = "\
    CREATE TABLE loan(\
        book_id INT NOT NULL,\
        user_id INT NOT NULL,\
        PRIMARY KEY (book_id, user_id),\
        FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,\
        FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE\
    );\
"

# SQL for creating the table
sql_create_table_rate = "\
    CREATE TABLE rate(\
        book_id INT NOT NULL,\
        user_id INT NOT NULL,\
        rate INT NOT NULL,\
        PRIMARY KEY (book_id, user_id),\
        FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,\
        FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,\
        CHECK (rate BETWEEN 1 and 5)\
    );\
"

# SQL for count # of tables
sql_check_schema_ready = f"""\
    SELECT COUNT(*)\
    FROM information_schema.tables\
    WHERE table_schema = "{"DB2018_10786"}";
"""

# SQL for dropping the table
sql_drop_table_book = 'DROP TABLE book;'
sql_drop_table_user = 'DROP TABLE user;'
sql_drop_table_loan = 'DROP TABLE loan;'
sql_drop_table_rate = 'DROP TABLE rate;'

# SQL for inserting the tuple
sql_insert_into_book_with_id = "\
    INSERT INTO book\
    VALUES (%s, %s, %s);\
"

# SQL for inserting the tuple
sql_insert_into_user_with_id = "\
    INSERT INTO user\
    VALUES (%s, %s);\
"

# SQL for inserting the tuple
sql_insert_into_book = "\
    INSERT INTO book (book_title, author)\
    VALUES (%s, %s);\
"

# SQL for inserting the tuple
sql_insert_into_user = "\
    INSERT INTO user (name)\
    VALUES (%s);\
"

# SQL for inserting the tuple
sql_insert_into_loan = "\
    INSERT INTO loan (book_id, user_id)\
    VALUES (%s, %s);\
"

# SQL for inserting the tuple
sql_insert_into_rate = "\
    INSERT INTO rate (book_id, user_id, rate)\
    VALUES (%s, %s, %s);\
"

# SQL for select all info from book
sql_select_all_info_from_book = "\
    SELECT book.book_id, book.book_title, book.author, ROUND(AVG(rate.rate),3) as avg_rate, (1-COUNT(DISTINCT loan.user_id)) as n_avail\
    FROM book\
    LEFT OUTER JOIN rate ON book.book_id = rate.book_id\
    LEFT OUTER JOIN loan ON book.book_id = loan.book_id\
    GROUP BY book.book_id\
    ORDER BY book.book_id;\
"

# SQL for selecting all info from user
sql_select_all_info_from_user = "\
    SELECT user_id, name\
    FROM user\
    ORDER BY user_id;\
"

# SQL for deletion
sql_delete_from_book = "\
    DELETE FROM book\
    WHERE book_id = (%s);\
"

# SQL for checking the book with b_id is in DB
sql_check_book_exist = "\
    SELECT COUNT(*) as cnt\
    FROM book\
    WHERE book_id = (%s);\
"

# SQL for count the number of books loaned
sql_count_book_loaned = "\
    SELECT COUNT(*) as cnt\
    FROM loan\
    WHERE loan.book_id = (%s);\
"

# SQL for deletion
sql_delete_from_user = "\
    DELETE FROM user\
    WHERE user_id = (%s);\
"

# SQL for checking user exists in DB
sql_check_user_exist = "\
    SELECT COUNT(*) as cnt\
    FROM user\
    WHERE user_id = (%s);\
"

# SQL for counting how many books the user loan
sql_count_user_loaned = "\
    SELECT COUNT(*) as cnt\
    FROM loan\
    WHERE loan.user_id = (%s);\
"

# SQL for selecting all information from table <loan>
sql_select_all_info_from_loan = "\
    SELECT *\
    FROM loan\
    ORDER BY book_id, user_id;\
"

# SQL for checking whether the pair exists in loan table or not
sql_check_book_user_exist_in_loan = "\
    SELECT COUNT(*) as cnt\
    FROM loan\
    WHERE book_id = (%s)\
    and user_id = (%s);\
"

# SQL for checking whether the pair exists in rate table or not
sql_check_book_user_exist_in_rate = "\
    SELECT COUNT(*) as cnt\
    FROM rate\
    WHERE book_id = (%s)\
    and user_id = (%s);\
"

# SQL for update the rate
sql_update_rate = "\
    UPDATE rate\
    SET rate.rate = (%s)\
    WHERE book_id = (%s)\
    and user_id = (%s);\
"

# SQL for deletion
sql_delete_from_loan = "\
    DELETE FROM loan\
    WHERE book_id = (%s)\
    and user_id = (%s);\
"

# SQL for selecting borrowing info for the user
sql_select_borrowing_info_for_user = "\
    SELECT loan.book_id as id, book.book_title as title, book.author as author\
    FROM loan\
    JOIN book ON loan.book_id = book.book_id\
    WHERE loan.user_id = (%s)\
    GROUP BY loan.book_id\
    ORDER BY loan.book_id;\
"

# SQL for find the book which contains the query in its title
sql_select_book_with_query = "\
    SELECT book.book_id, book.book_title, book.author, ROUND(AVG(rate.rate),3) as avg_rate, (1-COUNT(DISTINCT loan.user_id)) as n_avail\
    FROM book\
    LEFT OUTER JOIN rate ON book.book_id = rate.book_id\
    LEFT OUTER JOIN loan ON book.book_id = loan.book_id\
    WHERE book.book_title LIKE CONCAT('%', %s, '%')\
    GROUP BY book.book_id\
    ORDER BY book.book_id;\
"

# SQL for find the best avg_rate book for the user
sql_recommend_book_with_popularity_rate = "\
    SELECT A.book_id, B.book_title, B.author, B.avg_rate, B.n_avail\
    FROM (\
        SELECT book.book_id\
        FROM book\
        WHERE NOT EXISTS (\
            SELECT rate.book_id\
            FROM rate\
            WHERE rate.user_id = (%s)\
            AND book.book_id = rate.book_id)\
        ) AS A,(\
        SELECT book.book_id, book.book_title, book.author, ROUND(AVG(rate.rate),3) AS avg_rate, (1-COUNT(DISTINCT loan.user_id)) as n_avail\
        FROM book\
        LEFT OUTER JOIN rate ON book.book_id = rate.book_id\
        LEFT OUTER JOIN loan ON book.book_id = loan.book_id\
        GROUP BY book.book_id\
        ORDER BY book.book_id\
        ) AS B\
    WHERE A.book_id = B.book_id\
    ORDER BY B.avg_rate desc, A.book_id\
    LIMIT 1;\
"

# SQL for find the most # of rates book for the user
sql_recommend_book_with_popularity_num = "\
    SELECT C.book_id, C.book_title, C.author, C.avg_rate, C.n_avail\
    FROM (\
        SELECT A.book_id, B.book_title, B.author, B.avg_rate, B.n_avail, B.num_rate\
        FROM (\
            SELECT book.book_id\
            FROM book\
            WHERE NOT EXISTS (\
                SELECT rate.book_id\
                FROM rate\
                WHERE rate.user_id = (%s)\
                AND book.book_id = rate.book_id)\
            ) AS A,(\
            SELECT book.book_id, book.book_title, book.author, ROUND(AVG(rate.rate),3) AS avg_rate, COUNT(rate.rate) AS num_rate, (1-COUNT(DISTINCT loan.user_id)) as n_avail\
            FROM book\
            LEFT OUTER JOIN rate ON book.book_id = rate.book_id\
            LEFT OUTER JOIN loan ON book.book_id = loan.book_id\
            GROUP BY book.book_id\
            ORDER BY book.book_id\
            ) AS B\
        WHERE A.book_id = B.book_id\
        ORDER BY B.num_rate desc, A.book_id\
        LIMIT 1\
        ) AS C\
"

# SQL for selecting all user ids
sql_select_all_ids_from_user = "\
    SELECT user_id\
    FROM user\
    ORDER BY user_id;\
"

# SQL for selecting all book ids
sql_select_all_ids_from_book = "\
    SELECT book_id\
    FROM book\
    ORDER BY book_id;\
"

# SQL for selecting all rate info
sql_select_all_info_from_rate = "\
    SELECT user_id, book_id, rate\
    FROM rate\
    ORDER BY user_id, book_id;\
"

# SQL for selecting info about a specific book (w/ quantity)
sql_select_info_from_book = "\
    SELECT book.book_id, book.book_title, book.author, ROUND(AVG(rate.rate),3) as avg_rate, (1-COUNT(DISTINCT loan.user_id)) as n_avail\
    FROM book\
    LEFT OUTER JOIN rate ON book.book_id = rate.book_id\
    LEFT OUTER JOIN loan ON book.book_id = loan.book_id\
    WHERE book.book_id = (%s)\
    GROUP BY book.book_id\
    ORDER BY book.book_id;\
"

# SQL for selecting info about a specific book (w/o quantity)
sql_select_info_from_book_recommend = "\
    SELECT book.book_id, book.book_title, book.author, ROUND(AVG(rate.rate),3) as avg_rate\
    FROM book\
    LEFT OUTER JOIN rate ON book.book_id = rate.book_id\
    WHERE book.book_id = (%s)\
    GROUP BY book.book_id\
    ORDER BY book.book_id;\
"

