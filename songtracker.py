# This is used to capture a new page with beautiful soup.
# Once the page is captured, upen it and inspect the song title & artist elements
#     to know what to track using beautiful soup


# TODO
#   - add temp bd in case the main one is open in stat viewer
#   - add catches in the staion scrapers in case there is no song
#   - add catch in 

# INSTALLS
# python3 -m pip install beautifulsoup4
# python3 -m pip install requests 

# for getting the date
from datetime import datetime

import sqlite3
from sqlite3 import Error
import traceback

# import the scraper modules
from stations.cities97 import get_cities_97
from stations.jackfm import get_jack_fm
from stations.kqrs import get_kqrs
from stations.thecurrent import get_the_current


DEBUGGER = False
SAVE_WEB_PAGES = False
#SONG_DB_FILE = "./all_stations.db"
SONG_DB_FILE = "./test.db"
# station names that match the db table names
STATION_LIST = ["the_current", "jack_fm", "kqrs", "cities_97"]


LAST_SONGS_CSV_FILENAME = "last_songs.csv"
THE_CURRENT_FILENAME = "the_current.csv"
JACK_FM_FILENAME = "jack_fm.csv"
KQRS_FILENAME = "kqrs.csv"
CITIES_97_FILENAME = "cities_97.csv"


# get the current song from each radio station
def get_current_songs():
    current_songs_dict = {}
    current_songs_dict["the_current"] = get_the_current(DEBUGGER, SAVE_WEB_PAGES)
    current_songs_dict["jack_fm"] = get_jack_fm(DEBUGGER, SAVE_WEB_PAGES)
    current_songs_dict["kqrs"] = get_kqrs(DEBUGGER, SAVE_WEB_PAGES)
    current_songs_dict["cities_97"] = get_cities_97(DEBUGGER, SAVE_WEB_PAGES)
    return current_songs_dict


# get the most recent songs from each table
def get_last_songs(song_db_file):
    if DEBUGGER:
        print("Calling get_last_songs()")

    last_songs_dict = {}

    conn = None
    try:
        conn = sqlite3.connect(song_db_file)
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

    # for each station, select the most recent song from the db
    for station in STATION_LIST:
        # check if the table exists
        c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name=\'''' + station + '''\';''')
        # TODO check that this still works once there exists the table
        if c.fetchone()[0] == 0:
            # dne, set the last song to blank
            if DEBUGGER:
                print('Table "' + station + '" does not exist. Setting last song to "".')
            # TODO also change this once the query is updated to fix [0][0]
            last_song = [[""]]
        else:
            # get the most recent timestamp row
            c.execute('''SELECT song_name FROM ''' + station + ''' ORDER BY timestamp DESC LIMIT 1;''')
            last_song = c.fetchall()
        # TODO fix having to use [0][0] by updating the query
        # catch if the table is empty
        if last_song == []:
            last_songs_dict[station] = ""
        else:
            last_songs_dict[station] = last_song[0][0]
    if DEBUGGER:
        print("Gathered last songs:")
        print("\t" + str(last_songs_dict))

    conn.close()
    return last_songs_dict


# log the songs to the database
def log_songs(song_db_file, songs_dict):
    # get the previous songs
    last_songs_dict = get_last_songs(song_db_file)

    # open db file - will be created if does not exist
    conn = None
    try:
        conn = sqlite3.connect(song_db_file)
        if DEBUGGER:
            print("Connected to db")
    except Error as e:
        if DEBUGGER:
            print("Not connected to db")
            print(e)
            traceback.print_exc()
        return
    c = conn.cursor()

    # loop through the current songs dict and log each song that is new
    for station in songs_dict:
        # compare the current song to the previous song from that station
        if last_songs_dict[station] != songs_dict[station][0]:
            if DEBUGGER:
                print("New song for " + station + ": " + songs_dict[station][0] + " by " + songs_dict[station][1])
            # create a table for the station if one does not exist
            try:
                c.execute(
                    """ CREATE TABLE IF NOT EXISTS """
                    + station +
                    """ ( id integer PRIMARY KEY,
                        station_name text,
                        song_name text,
                        album_name text,
                        artist_name text,
                        datestamp text,
                        timestamp text,
                        radio_show text,
                        dj text ); """
                )
            except Error as e:
                if DEBUGGER:
                    print("Station table creation failed for station: " + station + ".")
                    print(e)

            # add the song to the given station's table
            # current_datetime = datetime.now().isoformat()
            # date and time formats should match what sqlite uses (2021-08-14 and 15:44:06)
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            
            sql_add_song = ''' INSERT INTO ''' + station + ''' (station_name,song_name,artist_name,datestamp,timestamp) VALUES(?,?,?,?,?)''' 
              
            add_song_values = (station, songs_dict[station][0], songs_dict[station][1], current_date, current_time)

            try:
                c.execute(sql_add_song, add_song_values)
                conn.commit()
                if DEBUGGER:
                    print(
                        "added song \"" + songs_dict[station][0] + " by " + songs_dict[station][1] 
                        + " to station " + station + "."
                        )
                    print("last row id = " + str(c.lastrowid))
            except Error as e:
                if DEBUGGER:
                    print("Station table creation failed for station: " + station + ".")
                    print(e)


def main():
    current_songs_dict = get_current_songs()
    log_songs(SONG_DB_FILE, current_songs_dict)

    #update_last_songs(last_songs_dict, current_songs_dict)

    
    
if __name__ == '__main__':
    main()