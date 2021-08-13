# this script shows info about the songs collected
# IDEAS:
#   - top songs / week & month
#   - top new songs / week (played > 1)
#   - new songs
#   - top artists / week & month

from os import stat
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

# open the sql script and run the query
def query_db(c, station, view, duration, count):
    sql_script_file = open(view, 'r')
    sql_script = sql_script_file.read()
    # insert the variables into the sql
    new_sql_script = sql_script%station, duration, count

    print(new_sql_script)


def main():
    # TODO Check if db exists
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


    # TODO get the station list from the db
    # TODO format this list to capitalize and replace the _ with a space
    station_list = ["the_current", "jack_fm", "kqrs", "cities_97", "the_current_test"]

    # prompt the user to select a station
    # TODO add support for "(0) All Stations" selection
    station_prompt_str = "Please type and enter a station number:\n\t(0) All Stations"
    for i, s in enumerate(station_list):
        station_prompt_str = station_prompt_str + "\n\t(%d) %s"%(i+1,s)
    # TODO add pagination to staion selection list

    # check for valid station input
    valid_input = False
    while not valid_input:
        station_selection = input(station_prompt_str+"\n")
        if station_selection.isnumeric():
            valid_input = int(station_selection) >= 0 and int(station_selection) <= len(station_list)
        print("Please enter a number shown below, or press \"Ctrl+C\" to escape this program.")

    # process the user's station input
    # deincriment staion_selection since the user-prompt incremented it
    station_selection = station_list[int(station_selection)-1]


    # get list of views
    # TODO pull this dynamically from somewhere?
    # TODO format these lists to replace the _ with a space or vice versa
    view_list = ["Top_Songs", "New_Songs", "Latest_Songs", "Top_Artists", "New_Artists", "Latest_Artists",]

    # TODO pull repetitive code into function
    # prompt the user to select a view
    view_prompt_str = "Please type and enter a view number:"
    for i, s in enumerate(view_list):
        view_prompt_str = view_prompt_str + "\n\t(%d) %s"%(i+1,s)
    # TODO add pagination to staion selection list

    # check for valid view input
    valid_input = False
    while not valid_input:
        view_selection = input(view_prompt_str+"\n")
        if view_selection.isnumeric():
            valid_input = int(view_selection) >= 0 and int(view_selection) <= len(view_list)
        print("Please enter a number shown below, or press \"Ctrl+C\" to escape this program.")

    # process the user's view selection
    # deincrement view_selection since the prompt 
    view_selection = "./sql/" + view_list[int(view_selection)-1] + ".sql"


    # TODO get max number of months dynamically
    # ask the user for the duration
    valid_input = False
    while not valid_input:
        duration = input("Please enter the number of past months to include (1-4):\n")
        if duration.isnumeric():
            valid_input = int(duration) >= 1 and int(duration) <= 4
        print("Please enter a number, 1-4, or press \"Ctrl+C\" to escape this program.")

    print(station_selection + " " + view_selection + " " + duration)

    # defaulting count variable to 10
    # TODO update this
    count = 10

    query_db(c, station_selection, view_selection, duration, count)
    # TODO Check if table exists - shouldnt be necessary if tables are pulled dynamically
    #get_top_songs(c, "the_current", "'2021-05-10T16:34:40.336198'", "'now'", 3)

if __name__ == '__main__':

    main()