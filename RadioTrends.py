# TODO:
#   - remove/escape commas and other escape chars
#   - change time function to not have milliseconds


from datetime import datetime, date
import time
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup
# BEAUTIFUL SOUP RESOURCES
# https://www.pythoncentral.io/python-beautiful-soup-example-yahoo-finance-scraper/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children


# open config file, load in station and tag data
# name, url, title obj, artist obj
def loadStations():
    try:
        config_file = open('config.txt', 'r')
    except:
        file_name = 'config.txt'
        config_file = open(file_name, 'w')
        config_file.close()
        print("No config file")
        return None
    config_list = config_file.readlines()
    station_list = []
    for line in config_list:
        temp_line = line.split(',')
        temp_line[-1] = temp_line[-1].replace("\n", "")
        station_list.append(temp_line)
    return station_list
    

# open website and return value from tag
# used for The Current and Jack FM
def getSongAndArtist(url,titleTag,titleAttr,artistTag,artistAttr):
    try:
        page = urlopen(url)
    except:
        print("page NOT opened for site: ", url)
        return None
    siteSoup = BeautifulSoup(page, 'html.parser')
    
    song_title_element = siteSoup.find(titleTag,titleAttr)
    song_title = song_title_element.contents[0]

    song_artist_element = siteSoup.find(artistTag,artistAttr)
    song_artist = song_artist_element.contents[0]
    return [song_title,song_artist]

# For 95.3 GO & 96.3 GO 
def getSongAndArtistJSON(stationData):
    url = stationData[1]
    try:
        page = urlopen(url)
    except:
        print("page NOT opened")
        return None
    siteSoup = BeautifulSoup(page, 'html.parser')

    # GO 9_.3 PARSING
    song_title_element = siteSoup.find_all(type="text/javascript")[-1]
    all_song_info = str(song_title_element)
    all_song_info = all_song_info.split('= [')[-1]
    first_song_info = all_song_info.split(',{')[0]
    song_info = json.loads(first_song_info)
    return [song_info['title'],song_info['artist']]
    
def getSongAndAristKFAI(stationData):
    url = stationData[1]
    try:
        page = urlopen(url)
    except:
        print("page NOT opened")
        return None
    siteSoup = BeautifulSoup(page, 'html.parser')

    song_info_element = siteSoup.find('span','txt')
    song_info = song_info_element.contents[2].split(' - ')
    song_info[1] = song_info[1].rstrip()
    return song_info
    

def getSongAndArtistRadioK(stationData):
    url = stationData[1]

    try:
        page = urlopen(url)
    except:
        print("page NOT opened for site: ", url)
        return None
    siteSoup = BeautifulSoup(page, 'html.parser')
    song_element = siteSoup.find('div','songblock')
    song_title = song_element.find('strong').string
    song_artist = song_element.find('br').string.rstrip()
    return [song_title,song_artist]
    

# open save file,
# check if most resent entry is same as new
# write date, time, title, artist, station
def writeData(station, title, artist):
    file_name = 'songFiles\\'
    file_name += station
    file_name += '.csv'
    last_written_song = ''
    try:
        # see if the file exists, get last song to compare
        song_file = open(file_name, 'r')
        song_file_lines = song_file.readlines()
        last_written_song = song_file_lines[-1].split(',')[2]
        song_file.close()
    except:
        print("No songfile for station: ", station, ". Creating file...")
        open_file = open(file_name, 'w')
        open_file.close()

    print(station)
    print("\tlast song:    ", last_written_song)
    print("\tcurrent song: ", title)
    if(last_written_song == title):
            return None
    song_file = open(file_name, 'a')
    # get and format date
    d = date.today()
    formatted_date = d.isoformat()
    song_file.write(formatted_date)
    song_file.write(',')
    
    # get and format time
    t = datetime.now().time()
    formatted_time = t.isoformat()
    song_file.write(formatted_time)
    song_file.write(',')

    song_file.write(title)
    song_file.write(',')
    song_file.write(artist)
    song_file.write(',')
    song_file.write(station)
    song_file.write(',\n')
    
    song_file.close()
    print(station,'\t\t',title,'\t\t',artist)

    
# loop through station list
def loopStations(station_list):
    current_song_artist = []
    for station in station_list:
        if (station[0].startswith('Go')):
            try:
                current_song_artist = getSongAndArtistJSON(station)
            except:
                print("ERROR - ",station[0])
        elif (station[0] == 'KFAI'):
            try:
                current_song_artist = getSongAndAristKFAI(station)
            except:
                print("ERROR - ",station[0])
        elif (station[0] == 'RadioK'):
            try:
                current_song_artist = getSongAndArtistRadioK(station)
            except:
                print("ERROR - ",station[0])
        else:
            try:
                current_song_artist = getSongAndArtist(station[1],station[2],station[3],station[4],station[5])
            except:
                print("ERROR - ",station[0])
        if(current_song_artist != None):            
            writeData(station[0],current_song_artist[0], current_song_artist[1])


def main():
    while(True):
        stationInfo = loadStations()
        loopStations(stationInfo)
        time.sleep(60)
    
    
    
main()
#writeData('The Current', 'Lonely Boy', 'The Black Keys')
