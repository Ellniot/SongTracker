

from urllib.request import urlopen
from bs4 import BeautifulSoup
# BEAUTIFUL SOUP RESOURCES
# https://www.pythoncentral.io/python-beautiful-soup-example-yahoo-finance-scraper/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children


# get song & artist from Cities 97
def get_cities_97(DEBUGGER=False, SAVE_WEB_PAGES=False):
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

    # look for the "track-title" classes
    track_title_html = siteSoup.find(class_="track-title")
    song = track_title_html.find("span").text.strip()

    # look for the "track-artist" classes
    track_artist_html = siteSoup.find(class_="track-artist")
    artist = track_artist_html.find("span").text.strip()

    
    # # check if the song is new and log it
    # if ((song != last_song[0]) or (artist != last_song[1])):
    #     if DEBUGGER:
    #         print("Cities 97: " + song + " - " + artist)
    #         print("cities97 song is new, logging...")
    #     log_song(CITIES_97_FILENAME, song, artist)
    # else:
    #     if DEBUGGER:
    #         print("The Current - no new song")

    return [song, artist]