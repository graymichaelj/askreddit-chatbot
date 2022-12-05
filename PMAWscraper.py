import pandas as pd
from pmaw import PushshiftAPI
import pickle

api = PushshiftAPI()

# function to filter posts retrieved to have > 10 comments (getting rid of junk posts)


def fxn(item):
    return item['num_comments'] > 5


# get the posts. search through 3.3million posts, filtering by >10 comments
posts = api.search_submissions(
    subreddit="AskReddit", limit=1000000, filter_fn=fxn)
print(f'{len(posts)} posts retrieved from Pushshift')

post_list = [post for post in posts]  # make a list of post objects
# make a list of post titles (this is most important for us)
post_titles = [post['title'] for post in post_list]
# make a list of post URLs to use for getting comments with PRAW
post_urls = [post['url'] for post in post_list]

with open("post_list", "wb") as fp:  # Pickling
    pickle.dump(post_list, fp)

with open("post_titles", "wb") as fp:  # Pickling
    pickle.dump(post_titles, fp)

with open("post_urls", "wb") as fp:  # Pickling
    pickle.dump(post_urls, fp)
