import sqlite3


def connect():
    """
    Quick access function to connect to the mirrorData database with sqlite3
    @rtype: Cursor, Connection
    @return: the connection and cursor to the database
    """
    conn = sqlite3.connect("/Users/kevingarcia/Desktop/algorithmfiles/repository/mirrorData.db")
    cur = conn.cursor()
    return cur, conn


def findPartNumber():
    file = open("arduinoOutput.txt", 'r')
    xLength = file.readline()
    yLength = file.readline()
