import requests
from bs4 import BeautifulSoup
import json


url = 'https://news.google.com/news/rss'
article_list = []


def save_function(article_list):
	with open('articles.txt', 'w') as f:
		json.dump(article_list, f)





def goooglenews_rss(url):
	try:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, features='xml')
		# return print("The scraping job done:", r.status_code, "\n", soup)
		articles = soup.findAll('item')

		for a in articles:
			title = a.find('title').text
			link = a.find('link').text
			published = a.find('pubDate').text

			article ={"title": title, "link": link, "published": published}
			article_list.append(article)

		return print(article_list), save_function(article_list)	
	except Exception as e:
		return print(f"The scrape job failed:", e)



print("Start Scrapping")
goooglenews_rss(url)
print("Finish Scrapping")