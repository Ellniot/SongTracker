
import requests
import json

# get song & artist from KQRS
def get_kqrs(DEBUGGER=False, SAVE_WEB_PAGES=False):
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

    # # check if the song is new and log it
    # if ((song != last_song[0]) or (artist != last_song[1])):
    #     if DEBUGGER:
    #         print("KQRS: " + song + " - " + artist)
    #         print("KQRS song is new, logging...")
    #     log_song(KQRS_FILENAME, song, artist)
    # else:
    #     if DEBUGGER:
    #         print("The Current - no new song")

    return [song, artist]