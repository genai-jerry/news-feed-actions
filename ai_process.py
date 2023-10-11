import openai
import feed_reader as feed
import os
import file_utils as util
    
openai.api_key = '<API-KEY>'

def categorize_title(title):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Given the title: '{title}', categorize the article into one of the following categories: A. Software Development B. Innovation C. Prediction D. Investment News.",
        temperature=0,
        max_tokens=60
    )
    category = response.choices[0].text.strip()
    return category

def summarize_content(content):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"You are an expert in understanding technology content and skilled at summarising content. I would like you to go through the content and summarise it. The summary should include Brief introduction, Key Impact Areas, Advice to Software Engineers. The content is: \n\n{content}",
        temperature=0.5
    )
    summary = response.choices[0].text.strip()
    return summary

def podcast_content(content):
    prompt = f"You are an expert podcast content creator. Read through the article text and generate a 5 minute long script for a podcast on Generative AI that will appeal to Software Professionals. The podcast will be a monologue. Also as an expert rate this topic between 1 to 10 in terms of appeal to the target audience that is experienced software professionals. The podcast should have an introduction, a deeper analysis of issue and a call to action. The podcast is named GenAI People. Provide response in the format <rating>:<value>, <podcast>:<content>. The input article is: \n\n{content}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0.5
    )
    podcast = ''
    for choice in response.choices:
        podcast = podcast + ' ' + choice.message.content.strip()
    return podcast

from datetime import datetime

def check_folder():
    # Get today's date in 'YYYY-MM-DD' format
    today = datetime.now().strftime('%Y-%m-%d')

    # Set the path to the 'content' folder and today's folder within it
    content_folder = 'content'
    today_folder = os.path.join(content_folder, today)

    # Create the 'content' folder and today's folder within it, if they don't exist
    os.makedirs(today_folder, exist_ok=True)
    return today

import json
import re

def extract_podcast_info(text):
    print(text)
    # Extracting rating value
    rating_pattern = re.compile(r'Rating: (\d+)')
    rating_match = rating_pattern.search(text)
    rating = int(rating_match.group(1)) if rating_match else None

    # Extracting podcast content
    podcast_pattern = re.compile(r'Podcast:\n\n(.*?)$', re.DOTALL)
    podcast_match = podcast_pattern.search(text)
    podcast_content = podcast_match.group(1).strip() if podcast_match else None

    return [rating, podcast_content]


def main():
    today = check_folder()
    file_path = 'content/' + today
    if not util.file_exists(file_path, 'podcast.json'):
        print('Podcast does not exist')
        feeds = json.loads(feed.load_feed(today))
        podcasts = []
        errors = []
        for content in feeds:
            category = categorize_title(content['title'])
            print(f"Category: {category}")

            try:
                podcast = podcast_content(content['article_content'])
                podcast_info = extract_podcast_info(podcast)
                if podcast_info is None:
                    errors.append({
                        'title': content['title'],
                        'error': f"{e}"
                    })
                print(f"Rating is {podcast_info[0]}")
                print(f"Podcast is {podcast_info[1]}")
                podcasts.append({
                    'title': content['title'],
                    'category': category,
                    'podcast': podcast_info[1],
                    'rating': podcast_info[0]
                })
            except openai.error.OpenAIError as e:
                errors.append({
                    'title': content['title'],
                    'error': f"{e}"
                })
            except Exception as e:
                errors.append({
                    'title': content['title'],
                    'error': f"{e}"
                })

        file_location = file_path + '/podcast.json'
        json_content = json.dumps(podcasts, indent=4)
        util.write_json(file_location, json_content)

        error_file_location = file_path + '/errors.json'
        error_json_content = json.dumps(errors, indent=4)
        util.write_json(error_file_location, error_json_content)
        print('Returning Podcast')
        return json_content
    else:
        print('Podcast exists')
        file_location = os.path.join('content/' + today, 'podcast.json')
        print('Returning Podcast')
        return util.load_json(file_location)

if __name__ == "__main__":
    main()
