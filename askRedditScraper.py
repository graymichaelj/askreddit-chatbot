import praw
import pandas as pd
import json
import requests
import pickle

# Read-only instance
r = praw.Reddit(client_id="25D1-1jhyUso2IB9NEpfhw",         # client id
                client_secret="ZoyIh3zITNB3Ac4H2Ji1r4w_eMZTfA",      # client secret
                user_agent="mgray55uncc")        # user agent

with open("post_urls", "rb") as fp:   # Unpickling
    post_urls = pickle.load(fp)

comment_list = []
# I manually change this based on where the script left off, if it stops for some reason
left_off_at = 1001

# get only the top comment of each post using their urls
for i in range(left_off_at, len(post_urls)):
    # looping through each post URL to get the top comment for each post, one at a time
    url = post_urls[i]
    submission = r.submission(url=url)
    # sort comments of a post (submission) by top voted
    submission.comment_sort = "top"
    try:
        # get the text of the first post
        comment_list.append(submission.comments[0].body)
    except:
        # very rarely we get an empty comment list for some reason
        print('an error occured, probably the comment list was empty')
        # still have to append something in the comment_list otherwise it will become out of sync with the post_list
        comment_list.append('error')

    if i % 100 == True:
        # print every 100 submissions to know the script is working
        print(str(i)+' submissions processed.')
    if i % 1000 == True:
        filename = "coment_list_"+str(left_off_at)+"_to_"+str(i)
        # save a pickle file every 1000 submissions in case the script crashes
        with open(filename, "wb") as fp:
            pickle.dump(comment_list, fp)
