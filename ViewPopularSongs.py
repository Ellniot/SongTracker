#Developed by Elliot Carson
#Last Updated: 7/25/17
#must run with IDLE 2.7.9

#imports
import re

#global variables


#UI

#algorythms

#main
def main():
    allSongFile1 = open("storefile_TheCurrent.txt",'r')
    allSongFile2 = open("storefile_TheCurrent.txt",'r')
    print("SongFile Loaded!")
    #monthSongFile = open("storefile_monthly", 'r')

    #importing data as arrays
    height,w,h = 0,0,0
    for i in allSongFile1:
        height = height + 1
        #print (i)
    print(height)
    songMatrix = [["blank" for x in range(4)] for y in range(height)]
    print("Matrix initialized!")
    for j in allSongFile2:
        i = str(j)
        songMatrix[h][0] = i[0:1]
        l1,l2,l3 = 0,0,0
        l1 = j.find("\t", 3)
        songMatrix[h][1] = i[3:l1]
        l1 = l1 + 1
        l2 = j.find("\t", l1)
        songMatrix[h][2] = i[l1:l2]
        l2 = l2 + 1
        l3 = j.find("\t", l2)
        songMatrix[h][3] = i[l2:l3]
        h = h +1
        
    print(songMatrix)
    print("done")


main()
