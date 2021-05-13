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
def get_top_songs(cur, station, from, to, count):
    if DEBUGGER:
        print("getting top songs from " + station + " from " + from + " - " + to)
    '''
    SELECT TOP count song_name, artist_name
    FROM [station]
    WHERE timestamp > from
    AND timestamp < to;
    '''

# get the songs that only appear in the given date range and not prior
def get_new_songs(cur, station, from, to, count):
    if DEBUGGER:
        print("getting new songs from " + station + " from " + from + " - " + to)
    '''
    SELECT TOP count song_name, artist_name
    FROM [station]
    WHERE timestamp > from
    AND timestamp < to;
    '''

# get the most frequent artists from the given date range
def get_top_artists(cur, station, from, to, count):
    if DEBUGGER:
        print("getting top artists from " + station + " from " + from + " - " + to)
    '''
    SELECT TOP count song_name, artist_name
    FROM [station]
    WHERE timestamp > from
    AND timestamp < to;
    '''

# get songs that exist in the given date range but not prior & exist more than once
def get_new_non_unique(cur, station, from, to, count):
    if DEBUGGER:
        print("getting top new non-unique songs from " + station + " from " + from + " - " + to)
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

    top_songs_last_week = get_top_songs()

if __name__ == '__main__':
    main()