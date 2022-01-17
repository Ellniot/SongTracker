
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

    # return blank if unable to gather song from station
    if parsed_response == []:
        return ["",""]

    # get song
    song = parsed_response[0]["song"]
    if DEBUGGER:
        print("song = " + song)

    # get artist
    artist = parsed_response[0]["artist"]
    if DEBUGGER:
        print("artist = " + artist)

    return [song, artist]