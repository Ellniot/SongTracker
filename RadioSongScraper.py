# This is used to capture a new page with beautiful soup.
# Once the page is captured, upen it and inspect the song title & artist elements
#     to know what to track using beautiful soup


# for reading/writing csv files
import csv

# for checking if the sonfile dir exists
import os

# for getting the date
from datetime import date, datetime

from urllib.request import urlopen
from bs4 import BeautifulSoup
# BEAUTIFUL SOUP RESOURCES
# https://www.pythoncentral.io/python-beautiful-soup-example-yahoo-finance-scraper/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children

# for api http get requests
import requests

# for handling/printing json (response from KQRS)
import json

DEBUGGER = True
SAVE_WEB_PAGES = False
LAST_SONGS_CSV_FILENAME = "last_songs.csv"
THE_CURRENT_FILENAME = "the_current.csv"
JACK_FM_FILENAME = "jack_fm.csv"
KQRS_FILENAME = "kqrs.csv"
CITIES_97_FILENAME = "cities_97.csv"

def get_last_songs():
    if DEBUGGER:
        print("Calling get_last_songs()")
    # open the last_songs.csv file
    try:
        with open(LAST_SONGS_CSV_FILENAME) as last_songs_file:
            last_songs_list = csv.reader(last_songs_file, delimiter=',')
            last_songs_dict = {}
            for row in last_songs_list:
                # add each row to the dictionary
                #   {Station : [song, artist]}
                last_songs_dict[row[0]] = [row[1], row[2]]
            if DEBUGGER:
                print("loaded last songs successfully")
    except:
        if DEBUGGER:
            print("last_songs.csv does not exist")
        last_songs_dict = {}
    
    # add any missing keys in case they are not yet saved
    key_list = ["The Current", "Jack FM", "KQRS", "Cities 97"]
    for key in key_list:
        if not (key in last_songs_dict):
            last_songs_dict[key] = ["", ""]

    return last_songs_dict


# log the given song in the specified file
#   files are located in the songfiles folder
def log_song(file_name, song, artist):
    if DEBUGGER:
        print("Calling log_song()")
    # define the row to be written
    output_row = [song, artist]
    # add the date and time
    today = date.today()
    output_row.append(today.strftime("%d/%m/%Y"))
    now = datetime.now()
    output_row.append(now.strftime("%H:%M:%S"))
    if DEBUGGER:
        print(str(output_row))

    # check if the gonsfiles dir exists
    songfiles_dir_path = "./songfiles"
    if not (os.path.isdir(songfiles_dir_path)):
        # create the dir if it does not exist
        new_dir_path = os.path.join("./", "songfiles")
        os.mkdir(new_dir_path)

    # add the folder to the filename
    full_file_name = "songfiles/" + file_name

    # open the given csv file in append mode
    with open(full_file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(output_row)


# get song & artist from the current
def get_the_current(last_song):
    url = "https://www.thecurrent.org/listen"
    if DEBUGGER:
        print("Calling get_the_current()")

    try:
        page = urlopen(url)
    except:
        print("page NOT opened for site: ", url)
        return None
    siteSoup = BeautifulSoup(page, 'html.parser')

    # save the page as an html - utf-8 so special chars don't cause a crash
    #   this is only to inspec the webpage, not necessary for song capture
    if SAVE_WEB_PAGES:
        new_page = open("the_current.html", 'w', encoding="utf-8")
        new_page.write(str(siteSoup))
        new_page.close()


    # get the song
    song_frag = siteSoup.find(class_="player-title js-update-title")
    if DEBUGGER:
        print("song_frag = " + str(song_frag))
    song = song_frag.get_text()
    if DEBUGGER:
        print("Song title = " + song)

    # get the artist
    artist_frag = siteSoup.find(class_="player-artist js-update-artist")
    if DEBUGGER:
        print("artist_frag = " + str(artist_frag))
    artist = artist_frag.get_text()
    if DEBUGGER:
        print("Artist title = " + artist)


    # TODO - pull this block out of each station into its own function
    # check if the song is new and log it
    if ((song != last_song[0]) or (artist != last_song[1])):
        if DEBUGGER:
            print("The Current: " + song + " - " + artist)
            print("The Current song is new, logging...")
        log_song(THE_CURRENT_FILENAME, song, artist)
    else:
        if DEBUGGER:
            print("The Current - no new song")

    return [song, artist]

        
# get song & artist from jack FM
def get_jack_fm(last_song):
    request_url = "https://www.radio.com/_components/station-recently-played/instances/default.html?stationId=529&ignore_resolve_media=true"
    if DEBUGGER:
        print("Calling get_jack_fm()")

    # make the get request
    response = requests.get(request_url)
    # TODO - check if the request returned a blank list of songs

    # save the page as an html - utf-8 so special chars don't cause a crash
    #   this is only to inspec the webpage, not necessary for song capture
    if SAVE_WEB_PAGES:
        if DEBUGGER:
            print("Saving the response for jackFM api call")
        new_page = open("jack_fm.html", 'w', encoding="utf-8")
        new_page.write(str(response.text))
        new_page.close()

    # use bs4 to scrape the currently playing
    siteSoup = BeautifulSoup(response.text, 'html.parser')
    # get the CURRENTLY PLAYING section of the song history
    currently_playing_frag = siteSoup.find(class_="details__time--on-air")
    if currently_playing_frag == None:
        if DEBUGGER:
            print("siteSoup is NoneType - skipping Jack FM")
        return ["", ""]
    # then get the parent fragment
    parent_div = currently_playing_frag.find_parent("div")
    if DEBUGGER:
        print("parent_div = " + str(parent_div))

    
    # get the song
    song = parent_div.find(class_="details__title").get_text()
    if DEBUGGER:
        print("song = " + song)
    # get the artist
    artist = parent_div.find(class_="details__artist").get_text()
    if DEBUGGER:
        print("artist = " + artist)

    # check if the song is new and log it
    if ((song != last_song[0]) or (artist != last_song[1])):
        if DEBUGGER:
            print("Jack FM: " + song + " - " + artist)
            print("Jack FM song is new, logging...")
        log_song(JACK_FM_FILENAME, song, artist)
    else:
        if DEBUGGER:
            print("The Current - no new song")

    return [song, artist]


# get song & artist from KQRS
def get_kqrs(last_song):
    request_url = "https://api.tunegenie.com/v2/brand/nowplaying/?apiid=m2g_bar&b=kqrs&count=1"
    if DEBUGGER:
        print("Calling get_kqrs()")


    # make the get request
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    if DEBUGGER:
        print(json.dumps(parsed_response, indent=2, sort_keys=True))

    # get song
    song = parsed_response[0]["song"]
    if DEBUGGER:
        print("song = " + song)

    # get artist
    artist = parsed_response[0]["artist"]
    if DEBUGGER:
        print("artist = " + artist)

    # check if the song is new and log it
    if ((song != last_song[0]) or (artist != last_song[1])):
        if DEBUGGER:
            print("KQRS: " + song + " - " + artist)
            print("KQRS song is new, logging...")
        log_song(KQRS_FILENAME, song, artist)
    else:
        if DEBUGGER:
            print("The Current - no new song")

    return [song, artist]


# get song & artist from Cities 97
def get_cities_97(last_song):
    url = "https://cities971.iheart.com/music/recently-played/"
    if DEBUGGER:
        print("Calling get_cities_97()")

    try:
        page = urlopen(url)
    except:
        print("page NOT opened for site: ", url)
        return None
    siteSoup = BeautifulSoup(page, 'html.parser')

    # save the page as an html - utf-8 so special chars don't cause a crash
    #   this is only to inspec the webpage, not necessary for song capture
    if SAVE_WEB_PAGES:
        new_page = open("cities_97.html", 'w', encoding="utf-8")
        new_page.write(str(siteSoup))
        new_page.close()

    # look for the "LIVE" icon
    live_icon_frag = siteSoup.find(class_="svg-icon icon-live")
    if live_icon_frag == None:
        return ["", ""]
    
    # get the parent song fragment
    parent_frag = live_icon_frag.find_parent(class_="component-track-display type-recentlyplayed")
    if parent_frag == None:
        return ["", ""]

    # get the song
    song_frag = parent_frag.find(class_="track-title")
    if DEBUGGER:
        print("song_frag = " + str(song_frag))
    song = song_frag.get_text()
    if DEBUGGER:
        print("Song title = " + song)

    # get the artist
    artist_frag = parent_frag.find(class_="track-artist")
    if DEBUGGER:
        print("artist_frag = " + str(artist_frag))
    artist = artist_frag.get_text()
    if DEBUGGER:
        print("Artist title = " + artist)
    
    # check if the song is new and log it
    if ((song != last_song[0]) or (artist != last_song[1])):
        if DEBUGGER:
            print("Cities 97: " + song + " - " + artist)
            print("cities97 song is new, logging...")
        log_song(CITIES_97_FILENAME, song, artist)
    else:
        if DEBUGGER:
            print("The Current - no new song")

    return [song, artist]


def update_last_songs(last_songs_dict, current_songs_dict):
    if DEBUGGER:
        print("Calling update_last_songs()")
        print("last_songs_dict = " + str(last_songs_dict))
        print("current_songs_dict = " + str(current_songs_dict))

    # TODO - move this, bad practive to have const here/ at all
    key_list = ["The Current", "Jack FM", "KQRS", "Cities 97"]
    # make sure not to replace existing songs with ""
    for key in key_list:
        # check if unable to get the current song
        if current_songs_dict == "":
            # set it to the last known song
            current_songs_dict[key] = last_songs_dict[key]
        

    # write the dictionary to the csv file
    with open(LAST_SONGS_CSV_FILENAME, 'w', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        print(str(current_songs_dict.keys()))
        for key in current_songs_dict.keys():
            output_row = []
            output_row.append(key)
            output_row.append(current_songs_dict[key][0])
            output_row.append(current_songs_dict[key][1])
            if DEBUGGER:
                print("writting row: " + str(output_row))
            # Add contents of list as last row in the csv file
            csv_writer.writerow(output_row)

    

def main():
    last_songs_dict = get_last_songs()
    current_songs_dict = {}
    current_songs_dict["The Current"] = get_the_current(last_songs_dict["The Current"])
    current_songs_dict["Jack FM"] = get_jack_fm(last_songs_dict["Jack FM"])
    current_songs_dict["KQRS"] = get_kqrs(last_songs_dict["KQRS"])
    current_songs_dict["Cities 97"] = get_cities_97(last_songs_dict["Cities 97"])
    update_last_songs(last_songs_dict, current_songs_dict)

    
    
main()
