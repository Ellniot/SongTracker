# this script shows info about the songs collected
# IDEAS:
#   - top songs / week & month
#   - top new songs / week (played > 1)
#   - new songs
#   - top artists / week & month

import sqlite3
from sqlite3 import Error
import traceback


DEBUGGER = True
SONG_DB_FILE = "./all_stations.db"

# get the most frequent songs from the given date range
def get_top_songs(cur, station, begin, end, count):
    sql_query = 'SELECT song_name,artist_name FROM ' + station + ' WHERE timestamp > ' + begin + 'AND timestamp < ' + end + ' ORDER BY timestamp DESC LIMIT ' + str(count) + ';'
    if DEBUGGER:
        print("getting top " + str(count) + " songs from " + station + " from " + begin + " - " + end)
        print("query = " + sql_query)
    cur.execute(sql_query)
    rows = cur.fetchall()
    print(rows)

# get the songs that only appear in the given date range and not prior
def get_new_songs(cur, station, begin, end, count):
    ''' SONGS WITH ONLY ONE PLAY
    Select song_name, count(*) as freq
    From the_current
    Group By song_name
    HAVING freq = 1
    '''

    '''
    SELECT * FROM the_current as T1
    WHERE T1.timestamp > '2021-05-00T16:34:40.336198'
    AND NOT EXISTS
    (SELECT * FROM the_current as T2
    WHERE T2.timestamp < '2021-05-00T16:34:40.336198'
    AND T1.song_name=T2.song_name and T1.artist_name=T2.artist_name)
    '''
    
    sql_query = 'SELECT song_name,artist_name FROM ' + station + ' WHERE timestamp > ' + begin + 'AND timestamp < ' + end + ' ORDER BY timestamp DESC LIMIT ' + str(count) + ';'
    if DEBUGGER:
        print("getting new songs from " + station + " from " + begin + " - " + end)
    '''
    SELECT TOP count song_name, artist_name
    FROM [station]
    WHERE timestamp > from
    AND timestamp < to;
    '''

# get the most frequent artists from the given date range
def get_top_artists(cur, station, begin, to, end):
    if DEBUGGER:
        print("getting top artists from " + station + " from " + begin + " - " + end)
    '''
    SELECT TOP count song_name, artist_name
    FROM [station]
    WHERE timestamp > from
    AND timestamp < to;
    '''

# get songs that exist in the given date range but not prior & exist more than once
def get_new_non_unique(cur, station, begin, end, count):
    if DEBUGGER:
        print("getting top new non-unique songs from " + station + " from " + begin + " - " + end)
    '''
    SELECT TOP count song_name, artist_name
    FROM [station]
    WHERE timestamp > from
    AND timestamp < to;
    '''


def main():
    # connect to the db
    conn = None
    try:
        conn = sqlite3.connect(SONG_DB_FILE)
        if DEBUGGER:
            print("Connected to db")
    except Error as e:
        if DEBUGGER:
            print("Not connected to db")
            print(e)
            traceback.print_exc()
        # if unable to connect to the db, return
        return
    c = conn.cursor()

    # TODO Check if db exists
    # TODO Check if table exists
    get_top_songs(c, "the_current", "'2021-05-10T16:34:40.336198'", "'now'", 3)

if __name__ == '__main__':

    main()