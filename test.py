from bs4 import BeautifulSoup
from urllib.request import urlopen
import json


def main():
    url = 'https://www.kfai.org/'

    try:
        page = urlopen(url)
    except:
        print("page NOT opened for site: ", url)
        return None
    siteSoup = BeautifulSoup(page, 'html.parser')

    # SAVE HTML TO FILE TO BETTER SEE WHAT'S GOING ON
    #saveFile = open('kdwb.html','w')
    #saveFile.write(str(siteSoup.prettify()))
    #saveFile.close()
    #print("saved file")

    # RadioK PARSING
    #song_element = siteSoup.find('div','songblock')
    #print(song_element)
    #song_title = song_element.find('strong').string
    #print("\n")
    #print(song_title)
    #song_artist = song_element.find('br').string.rstrip()
    #print("\n")
    #print(song_artist)
    
    # KFAI PARSING
    song_title_element = siteSoup.find('span','txt')
    song_info = song_title_element.contents[2].split(' - ')
    song_info[1] = song_info[1].rstrip()
    print(song_info)

    # GO 96.3 PARSING
    #song_title_element = siteSoup.find(type="text/javascript")
    #all_song_info = str(song_title_element)
    #all_song_info = all_song_info.split('= [')[-1]
    #print(all_song_info)
    #first_song_info = all_song_info.split(',{')[0]
    #print(first_song_info)
    #song_info = json.loads(first_song_info)
    #print(song_info['title'])

    
    #song_title = song_title_element.contents[0]
    #print(song_title)

    #artistTag = 'div'
    #artistAttr = 'showDescription'
    #song_artist_element = siteSoup.find(artistTag,artistAttr)
    #print(song_artist_element)
    #song_artist = song_artist_element.contents[0]
    #print(song_artist)
    
    #song_artist_element = siteSoup.find('div','player-artist js-update-artist')
    #song_artist = song_artist_element.contents[0]
    #print(song_artist)

main()
