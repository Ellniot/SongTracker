
from urllib.request import urlopen
from bs4 import BeautifulSoup
# BEAUTIFUL SOUP RESOURCES
# https://www.pythoncentral.io/python-beautiful-soup-example-yahoo-finance-scraper/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children


# get song & artist from the current
def get_the_current(DEBUGGER=False, SAVE_WEB_PAGES=False):
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


    # # TODO - pull this block out of each station into its own function
    # # check if the song is new and log it
    # if ((song != last_song[0]) or (artist != last_song[1])):
    #     if DEBUGGER:
    #         print("The Current: " + song + " - " + artist)
    #         print("The Current song is new, logging...")
    #     log_song(THE_CURRENT_FILENAME, song, artist)
    # else:
    #     if DEBUGGER:
    #         print("The Current - no new song")

    return [song, artist]