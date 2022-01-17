
import requests
import json

# get song & artist from the current
def get_the_current(DEBUGGER=False, SAVE_WEB_PAGES=False):
    request_url = "https://nowplaying.publicradio.org/the-current/playlist"
    if DEBUGGER:
        print("Calling get_the_current()")

    # make the get request
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    if DEBUGGER:
        print(json.dumps(parsed_response, indent=2, sort_keys=True))

     # return blank if unable to gather song from station
    if parsed_response == []:
        return ["",""]

    # save the page as an html - utf-8 so special chars don't cause a crash
    #   this is only to inspect the respose, not necessary for song capture
    if SAVE_WEB_PAGES:
        new_page = open("the_current.json", 'w', encoding="utf-8")
        new_page.write(str(json.dumps(parsed_response, indent=2, sort_keys=True)))
        new_page.close()

    # get song
    song = parsed_response['data']["songs"][0]['title']
    if DEBUGGER:
        print("song = " + song)

    # get artist
    artist = parsed_response['data']["songs"][0]['album']
    if DEBUGGER:
        print("artist = " + artist)

    return [song, artist]