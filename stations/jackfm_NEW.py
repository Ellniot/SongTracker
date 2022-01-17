
import requests
import json

# get song & artist from the current
def get_jack_fm(DEBUGGER=False, SAVE_WEB_PAGES=False):
    request_url = "http://prt.wostreaming.net/prt/nowplaying/2/3/5689/nowplaying.jsonp"
    # HOW TO UPDATE:
    #   - got to https://www.929jack.com/recently-played/
    #   - put a "Break on..." on the Now Playing attribute on subtree modification
    # reload the page
    # the last call in the network tab should be the json now playing call
    if DEBUGGER:
        print("Calling get_jack_fm()")

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
        new_page = open("jack_fm.json", 'w', encoding="utf-8")
        new_page.write(str(json.dumps(parsed_response, indent=2, sort_keys=True)))
        new_page.close()

    # get song
    song = parsed_response['performances'][0]['title']
    if DEBUGGER:
        print("song = " + song)

    # get artist
    artist = parsed_response['performances'][0]['artist']
    if DEBUGGER:
        print("artist = " + artist)

    return [song, artist]