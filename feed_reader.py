import feedparser
import requests
from bs4 import BeautifulSoup
import json
import file_utils as util
import os

def extract_article_content(url):
	headers = {
	    "User-Agent": "Mozilla/5.0"
	}
	try:
	    response = requests.get(url, headers=headers)
	    response.raise_for_status()
	except requests.RequestException as e:
	    print(f"Error connecting to {url}: {e}")
	    return None

	soup = BeautifulSoup(response.text, 'html.parser')
	paragraphs = soup.find_all('p')
	print(paragraphs)
	article_content = ' '.join(paragraph.text for paragraph in paragraphs)
	print(article_content)

	return article_content

def load_feed(today):
	file_path = f'content/{today}'
	if not util.file_exists(file_path, 'feed.json'):
		print('Feed does not exist')
		feed_url = 'https://rss.app/feeds/tY4l5k6Ggv1doN3i.xml'
		feed = feedparser.parse(feed_url)

		unique_titles = set()
		is_unique_title = lambda title: not (title in unique_titles or unique_titles.add(title))

		unique_entries = filter(lambda entry: is_unique_title(entry.title), feed.entries)
		articles = []
		for entry in unique_entries:
			article_title = entry.title
			article_url = entry.link
			article_content = extract_article_content(article_url)
			articles.append({
			    'title': article_title,
			    'article_url': article_url,
			    'article_content': article_content
			})

		file_location = f'{file_path}/feed.json'
		json_content = json.dumps(articles, indent=4)
		util.write_json(file_location, json_content)
		print('Returning Feed')
		return json_content
	else:
		print('Feed exists')
		file_location = os.path.join(f'content/{today}', 'feed.json')
		print('Returning Feed')
		return util.load_json(file_location)