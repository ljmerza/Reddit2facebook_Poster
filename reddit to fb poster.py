# Reddit to Facebook Poster
# Created by: Leonardo Merza
# Date: 5/24/14

# Imports
import facebook, time
import re, praw, requests, os, glob, sys
from bs4 import BeautifulSoup
import collections

# Values to change
minScore = 80 # the minimum score needed to post
targetSubreddits = ['', '', ''] # the subreddits to search
# facebook token key
fbKey = ''
numberOfPosts = 1 # number of posts to make on facebook
botName = '' # name of bot for reddit

array = []
counterPosts = 0
currentHighScore = 0
postDict = {}
postDict2 = {}
graph = facebook.GraphAPI(fbKey)
imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')
divider = "---------------------------------------------------------------------"

print "reddit to facebook poster version 0.76"
print divider

if not os.path.exists('storage.txt'):
    open('storage.txt', 'w').close()

def downloadImage(imageUrl, wallMessage):
    global array, counterPosts, numberOfPosts
    if not(imageUrl in array):
        counterPosts = counterPosts+1
        if counterPosts > numberOfPosts:
            newWallMessage = wallMessage.replace("&amp;", "&")
            newWallMessage2 = newWallMessage.replace("[OC]", "")
            newWallMessage3 = newWallMessage2.split('[x-post')[0]
            newWallMessage4 = newWallMessage3.split('x-post')[0]
            newWallMessage5 = newWallMessage4.replace("[infographic]", "&").encode('ascii', 'ignore')
            print "Image URL: " + imageUrl
            print "Image Title: " + newWallMessage5
            print divider
            graph.put_object("me", "feed", link=imageUrl, picture=imageUrl, message=newWallMessage5)
            array.append(imageUrl)

            with open('storage.txt', 'w') as fileText:
                for item in array:
                    fileText.write("%s\n" % item)
            fileText.close()

with open('storage.txt', 'r') as fileText:
    for line in fileText:
        array.append(line.rstrip())
    fileText.close()
print "The array: ", array
print divider


for targetSubreddit in targetSubreddits:

    r = praw.Reddit(user_agent=botName)
    submissions = r.get_subreddit(targetSubreddit).get_top_from_week(limit=25)
    time.sleep(2)
        

    for submission in submissions:
        if submission.score < minScore:
            continue
        postDict[submission.score] = submission.url
        postDict2[submission.score] = submission.title

reverseKeys = list(reversed(sorted(postDict.keys())))
print reverseKeys 
print divider
print postDict
print divider

for highKey in reverseKeys:
    if counterPosts > numberOfPosts:
        break

    subHigh = postDict.get(highKey)
    wallMessage = postDict2.get(highKey)

    if 'http://imgur.com/a/' in subHigh:
        albumId = submission.url[len('http://imgur.com/a/'):]
        htmlSource = requests.get(subHigh).text
        soup = BeautifulSoup(htmlSource)
        matches = soup.select('.album-view-image-link a')
        for match in matches:
            imageUrl = match['href']
            if '?' in imageUrl:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
            else:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:]
            downloadImage('http:' + match['href'], wallMessage)

    elif 'http://i.imgur.com/' in subHigh:
        mo = imgurUrlPattern.search(subHigh)
        imgurFilename = mo.group(2)
        if '?' in imgurFilename:
            imgurFilename = imgurFilename[:imgurFilename.find('?')]
        downloadImage(subHigh, wallMessage)

    elif 'http://imgur.com/' in subHigh:
        htmlSource = requests.get(subHigh).text
        soup = BeautifulSoup(htmlSource)
        imageUrl = soup.select('.image img')[0]['src']
        if imageUrl.startswith('//'):
            imageUrl = 'http:' + imageUrl
            imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]

        if '?' in imageUrl:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
        else:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:]
        downloadImage(imageUrl, wallMessage)
    elif '.jpg' in subHigh:
        downloadImage(subHigh, wallMessage)
    elif '.png' in subHigh:
        downloadImage(subHigh, wallMessage)

print "The new array: ", array
print divider
print "Done."
