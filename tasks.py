from celery import Celery


# @app.task # registering the task to the app
# def add(x, y):
# 	return x + y

import requests  # pulling data
from bs4 import BeautifulSoup  # xml parsing
import json  # exporting files
from datetime import datetime
from celery.schedules import crontab  # scheduler


app = Celery('tasks')  # defining app name used in our flag
url = 'https://news.google.com/news/rss'
article_list = []

# save function

@app.task
def save_function(articles_list):
    # timestamp and filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = 'articles-{}.json'.format(timestamp)
    # creating our articles file with timestamp
    with open(filename, 'w').format(timestamp) as outfile:
        json.dump(article_list, outfile)
# scarping function


# scraping function
@app.task
def googlenews_news_rss():
    article_list = []
    try:
        # execute my request, parse the data using the XML 
        # parser in BS4
        r = requests.get('https://news.google.com/news/rss')
        soup = BeautifulSoup(r.content, features='xml')
        # select only the "items" I want from the data      
        articles = soup.findAll('item')
        # for each "item" I want, parse it into a list
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            # create an "article" object with the data
            # from each "item"
            article = {
                'title': title,
                'link': link,
                'published': published,
                'created_at':datetime.now(),
                }
            # append my "article_list" with each "article" object
            article_list.append(article)
        # after the loop, dump my saved objects into a .txt file
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)

app.conf.beat_sheduler = {
	# executes every minute
	'scraping-task-ne-minute':{
	'task':'tasks.googlenews_rss',
	'shedule':crontab()
	}
}
