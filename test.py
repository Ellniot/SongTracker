#Developed by Elliot Carson
#Last Updated: 7/25/17
#Developed on python 2.7.9

#MODULE IMPORTS
from bs4 import BeautifulSoup
from urllib import urlopen
from time import sleep
from datetime import datetime

#GLOBAL VARIABLES
trackerIsOn = True

#GET WEBPAGES
def getCurrentSoup():
    url = 'http://www.thecurrent.org/listen'
    streamPage = urlopen(url)
    soup = BeautifulSoup(streamPage, "html5lib")
    return soup

def getJackFMSoup():
    url = 'http://player.radio.com/listen/station/1041-jack-fm'
    streamPage = urlopen(url)
    soup = BeautifulSoup(streamPage, "html5lib")
    return soup


#SONG + ARTIST CHECKS
def getTheCurrentSong(soup):
    titleClass = "player-title js-update-title"
    tempSong = str(soup.findAll('div', attrs={'class': titleClass}))
    tempStr = tempSong[43:-7]
    return tempStr

def getTheCurrentArtist(soup):
    artistClass = "player-artist js-update-artist"
    tempArtist = str(soup.findAll('div', attrs={'class': artistClass}))
    tempStr = tempArtist[45:-7]
    return tempStr

def getJackFMSong(soup):
    titleClass = "track-name"
    tempSong = str(soup.findAll('div', attrs={'class': titleClass}))
    tempStr = tempSong
    print(type(tempSong))
    return tempStr

def getJackFMArtist(soup):
    artistClass = "track-artist"
    tempArtist = str(soup.findAll('div', attrs={'class': artistClass}))
    tempStr = tempArtist
    return tempStr

    
#LOAD LAST SONG FROM FILE AS LASTSONG
def checkLastSong():
    storefile0 = open("/home/pi/Desktop/SongTracker/storefile_TheCurrent.txt",'r')
    storefile1 = open("/home/pi/Desktop/SongTracker/storefile_TheCurrent.txt",'r')
    height,counter = 0,0
    tempSong = "d_song"
    for i in storefile0:
        height = height + 1
    fileStr = str(storefile1.read())
    tempArr = fileStr.split("\n", (height - 1))
    tempStr = tempArr[-1]
    l1 = tempStr.find("\t", 20)
    l1 = l1 + 1
    l2 = tempStr.find("\t", l1)
    oldSong = tempStr[l1:l2]
    return oldSong
    
#MAIN TRACKER LOOP
def startTracker(): 
    oldCurrentSong = "default_song"
    oldCurrentSong = checkLastSong()
    print("Last song on file: " + oldCurrentSong)
    while trackerIsOn:
        song, artist = "default_song", "default_artist"
        soup = getJackFMSoup()
        song = getJackFMSong(soup)
        artist = getJackFMArtist(soup)
        print(song)
        print(artist)
        if song != oldCurrentSong:
            print("New Song! - " + song + " " + str(datetime.now()))
            storefile = open("/home/pi/Desktop/SongTracker/storefile_TheCurrent.txt",'a')
            #storefile.write("1" + '\t' + str(datetime.now()) + '\t' + song + '\t' + artist + '\n')
            storefile.close()
        else:
            print("No new song. - " + song + " " + str(datetime.now()))
        oldCurrentSong = song
        sleep(119)
    
def main():
    trackerIsOn = True
    startTracker() 

main()
