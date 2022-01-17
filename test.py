import sqlite3
from sqlite3 import Error

def main():

    # open db file - will be created if does not exist
    conn = None
    try:
        conn = sqlite3.connect("./test2.db")
    except Error as e:
        print("Not connected to db")
        print(e)
        return
    c = conn.cursor()

    # get the current timestamp format
    c.execute(
                """ 
                SELECT timestamp
                FROM the_current_test
                LIMIT 1
                """
                )
    query_results = c.fetchone()
    print(query_results)

    # create a new column
    #alter table emp add column dept_id;
    c.execute(
                """ 
                SELECT timestamp
                FROM the_current_test
                LIMIT 1
                """
                )

main()