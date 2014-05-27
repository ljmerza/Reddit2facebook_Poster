REDDIT TO FACEBOOK POSTER VERSION 0.6

This python program will search each reddit you specify in the 'targetsubreddits' list and find the highest scoring post in the past week of all subreddits searched. It will then check to see if that post is a single image file from imgur or a single png/jpg and if it is, attempt to post it onto the facebook account with the given kiey in the 'fbkey' variable.

It will attempt to look into the 'storage.txt' file to see if it has already posted this image and if it has not, it will post the image to facebook with the reddit post's title else it will skip to the next highest scoring image found.

The 'numberOfPosts' variable tells the program how many times to post to facebook and is set default as one.  The program uses the 'storage.txt' file in order to keep track of the URLs of each image that it has already posted. The 'minScore' variable allows to filter out image posts that are below this threshold score (default is 80).

The 'botName' variable is to access the reddit API using PRAW and can be any string as long as it is unique to reddit. So far in version 0.6, the program will strip out [OC] and replace '&amp;' with '&' for the post title.