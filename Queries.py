"""
Samira Omerovic
CYBR-260-40
Week 7: Final Project
July 1, 2022

This class is used to execute queries to the database
"""

import Connect


def get_single_query(query: str, value: str) -> str or None:
    """
    This function fetches 1 single value in the table (i.e.: query[0] == "Value").
    This function uses prepare statements, if not needed pass None in value.
    :param query: The query to be executed with placeholders for the prepare statement
    :param value: The value needed to be parsed into the query in the prepare statement.
    :return: The result if found, None otherwise
    """
    try:
        if Connect.connect_exists() and query is not None and query != "":
            sql = Connect.getSQL()
            mycursor = sql.cursor(prepared=True)

            if value is not None:
                mycursor.execute(query, (value,))
            else:
                mycursor.execute(query)

            result = mycursor.fetchone()

            if result is not None:
                return result[0]
    except Exception as e:
        print(e)

    return None


def get_all_query(query: str, value: str) -> [] or None:
    """
    This function fetches all the values in the table as an array with the use of prepare statements.
    :param query: The query to be executed with placeholders for the prepare statement
    :param value: The value needed to be parsed into the query in the prepare statement.
    :return: The results if found as an array, None otherwise
    """
    try:
        if Connect.connect_exists() and query is not None and query != "":
            sql = Connect.getSQL()
            mycursor = sql.cursor(prepared=True)

            if value is not None:
                mycursor.execute(query, (value,))
            else:
                mycursor.execute(query)

            result = mycursor.fetchall()

            sql.commit()

            # Put the results in the array and return it
            if result is not None:
                array = []
                for row in result:
                    array.append(row)

                return array
    except Exception as e:
        print(e)

    return None


def execute_query(query: str, tuple: ()) -> bool:
    """
    This function executes a given query with the use of prepare statements.
    :param query: The query to be executed with placeholders for the prepare statement
    :param tuple: Always give a tuple as second argument!
    :return: True if successful, False otherwise
    """
    try:
        if Connect.connect_exists() and query is not None and query != "":
            sql = Connect.getSQL()
            mycursor = sql.cursor(prepared=True)

            if tuple is not None:
                mycursor.execute(query, tuple)
            else:
                mycursor.execute(query)

            sql.commit()

            return True
    except Exception as e:
        print(e)

    return False
