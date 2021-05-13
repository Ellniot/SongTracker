
import requests
from bs4 import BeautifulSoup
# BEAUTIFUL SOUP RESOURCES
# https://www.pythoncentral.io/python-beautiful-soup-example-yahoo-finance-scraper/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children


# get song & artist from jack FM
def get_jack_fm(DEBUGGER=False, SAVE_WEB_PAGES=False):
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

    # # check if the song is new and log it
    # if ((song != last_song[0]) or (artist != last_song[1])):
    #     if DEBUGGER:
    #         print("Jack FM: " + song + " - " + artist)
    #         print("Jack FM song is new, logging...")
    #     log_song(JACK_FM_FILENAME, song, artist)
    # else:
    #     if DEBUGGER:
    #         print("The Current - no new song")

    return [song, artist]