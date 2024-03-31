import sqlite3


# TODO: update the connection string
def connect():
    """
    Quick access function to connect to the mirrorData database with sqlite3
    @rtype: Cursor, Connection
    @return: the connection and cursor to the database
    """
    conn = sqlite3.connect("/Users/kevingarcia/Desktop/algorithmfiles/repository/mirrorData.db")
    cur = conn.cursor()
    return cur, conn


def verifyInput(postData):
    """
    Makes sure that the given dictionary in the POST function has all of the required keys, and makes sure
    that the values are not Null.
    @param postData: dictionary containing the database columns as keys and the column values-to-input as values.
    @rtype: Boolean
    @return: True if the inputted data is valid, False otherwise
    """
    requiredKeys = ["id", "coordinates", "mirrorPartNum", "distortionLevel", "runDate", "result"]
    for key in requiredKeys:
        if key not in postData:
            print(f'{key} not found as key in PostData')
            return False
        if postData[key] is None:
            print(f'value for key: {key} is None')
            return False
    return True


def POST(postData):
    """
    Publishes the inputted data to the database
    @param postData: dictionary containing the database columns as keys and the column values-to-input as values.

    """
    cur, conn = connect()  # connect to database
    if not verifyInput(postData):  # verify that the inputted data is valid
        return
    cur.execute(
        f"""
            INSERT INTO mirrorData (id, coordinates, mirrorPartNum, distortionLevel, runDate, result, runTime)
            VALUES ("{postData["id"]}", "{postData["coordinates"]}", "{postData["mirrorPartNum"]}", 
                    {postData["distortionLevel"]}, "{postData["runDate"]}", "{postData["result"]}",
                    "{postData["distortionLevel"]}");
        """)
    conn.commit()
    cur.close()
    print("POSTED")


def GET(startDate, endDate, mirrorPartNumber):
    """
    Queries data from mirrorData.db where the measurements occur between the startDate and endDate and the measurement
    was done on the given mirrorPartNumber.
    @param startDate: the start date of when the measurements have to be between
    @param endDate: the end date of when the measurements have to be between
    @param mirrorPartNumber: the mirror part number to query for
    @rtype: list (Array)
    @return: the query results
    """
    cur, conn = connect()
    cur.execute(
        f"""
            SELECT * FROM mirrorData 
            WHERE mirrorPartNum = "{mirrorPartNumber}"
            AND (runDate BETWEEN "{startDate}" and "{endDate}");
        """
    )
    queryResults = cur.fetchall()
    cur.close()
    return queryResults


def GETALL():
    """
    Get all the data in the database
    @rtype: list (Array)
    @return: a list of all the data entries in the database
    """
    cur, conn = connect()
    cur.execute(
        f"""
            SELECT * FROM mirrorData
        """
    )
    queryResults = cur.fetchall()
    cur.close()
    return queryResults
