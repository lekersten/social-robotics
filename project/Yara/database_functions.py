import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_list(conn, lists):
    """
    Create a new list into the lists table
    :param conn:
    :param lists:
    :return: list id
    """
    sql = ''' INSERT INTO lists(name,keywords,begin_date,end_date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, lists)
    conn.commit()
    return cur.lastrowid


def create_step(conn, step):
    """
    Create a new step
    :param conn:
    :param step:
    :return:
    """

    sql = ''' INSERT INTO steps(name,keywords,priority,status_id,list_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, step)
    conn.commit()

    return cur.lastrowid


def update_list(conn, lists):
    """
    update name, keywords, begin_date, and end date of a list
    :param conn:
    :param lists:
    :return: list id
    """
    sql = ''' UPDATE lists
              SET name = ? ,
                  keywords = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, lists)
    conn.commit()


def update_step(conn, step):
    """
    update priority, status_id, and keywords of a task
    :param conn:
    :param step:
    :return: list id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  status_id = ? ,
                  keywords = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, step)
    conn.commit()


def delete_step(conn, id):
    """
    Delete a step by step id
    :param conn:  Connection to the SQLite database
    :param id: id of the step
    :return:
    """
    sql = 'DELETE FROM steps WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def select_step_by_list(conn, lists):
    """
    Query tasks by list
    :param conn: the Connection object
    :param lists:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM steps WHERE list_id=?", (lists,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def get_all_list_keywords(conn, date):
    """
    Query tasks by list
    :param conn: the Connection object
    :param date: the current date
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT id,keywords FROM lists WHERE begin_date<=? AND end_date>=?", (date, date,))

    rows = cur.fetchall()
    return rows


def get_all_current_steps(conn, date):
    # Determine the step in a list that needs to be done first

    cur = conn.cursor()
    cur.execute("SELECT name,priority,end_date FROM steps WHERE status_id=0 AND begin_date<=? AND end_date>=?",
                (date, date,))

    rows = cur.fetchall()
    return rows


if __name__ == '__main__':
    database = r"db\pythonsqlite.db"

    sql_create_lists_table = """ CREATE TABLE IF NOT EXISTS lists (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        keywords text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_steps_table = """CREATE TABLE IF NOT EXISTS steps (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    keywords text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    list_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (list_id) REFERENCES lists (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_lists_table)

        # create tasks table
        create_table(conn, sql_create_steps_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        # create a new project
        lists = ('Vacation to Turkey', 'vacation,turkey,holiday,', '2024-03-19', '2024-03-29');
        list_id = create_list(conn, lists)

        # tasks
        step_1 = ('Pack your bags', 'bag,bags,luggage,suitcase,packing,pack', 1, 0, list_id, '2024-03-25', '2024-03-28')
        step_2 = (
            'Prepare by printing your travel info', 'prepare,preparations', 2, 1, list_id, '2024-03-20', '2024-03-28')
        step_3 = ('You will leave on the 29th of March', 'leave,march,date', 0, 3, list_id, '2024-03-19', '2024-03-29')

        # create tasks
        create_step(conn, step_1)
        create_step(conn, step_2)
        create_step(conn, step_3)

    # with conn:
    #     # name, keywords, begin_date, and end date
    #     update_list(conn, ("Easter visit from your daughter", "easter,visit", '2024-03-28', '2024-04-06', 1))
    #     # priority, status_id, and keywords
    #     update_step(conn, (2, '2015-01-04', '2015-01-06', 2))
