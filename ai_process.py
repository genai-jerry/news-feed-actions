import openai
import feed_reader as feed
import os
import file_utils as util
    
openai.api_key = '<api key>'

def categorize_title(title):
    prompt=f'''Given the title: '{title}', categorize the article into one of the following categories: 
        A. Software Development B. Innovation C. Prediction D. Investment News.'''
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    category = response.choices[0].message.content.strip()
    return category

def summarize_content(content):
    prompt=f'''You are an expert in understanding technology content and skilled at summarising content. 
            I would like you to go through the content and summarise it. The summary should include Brief introduction, 
            Key Impact Areas, Advice to Software Engineers. Also, based on the content rate in a scale of 1 to 10 as to how relevant it is for software engineers.
            Provide the output in the format Rating: <rating> ; Summary: <content>. The input content is: \n\n{content}'''
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    summary = ''
    for choice in response.choices:
        summary = f'{summary} {choice.message.content.strip()}'
    return summary
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

def extract_summary_info(text):
    print(text)
    # Extracting rating value
    rating_pattern = re.compile(r'Rating: (\d+)')
    rating_match = rating_pattern.search(text)
    rating = int(rating_match.group(1)) if rating_match else None

    # Extracting summary content
    summary_pattern = re.compile(r'Summary:(.*?)$', re.DOTALL)
    summary_match = summary_pattern.search(text)
    summary_content = summary_match.group(1).strip() if summary_match else None

    return [rating, summary_content]

def main():
    today = check_folder()
    file_path = f'content/{today}'
    if not util.file_exists(file_path, 'summary.csv'):
        print('Summary does not exist')
        feeds = json.loads(feed.load_feed(today))
        summaries = []
        errors = []
        for content in feeds:
            category = categorize_title(content['title'])
            print(f"Category: {category}")

            try:
                summary = summarize_content(content['article_content'])
                summary_info = extract_summary_info(summary)
                if summary_info is None:
                    errors.append({
                        'title': content['title'],
                        'error': f"{e}"
                    })
                print(f"Rating is {summary_info[0]}")
                print(f"Summary is {summary_info[1]}")
                summaries.append([
                    content['title'],
                    category,
                    summary_info[1],
                    summary_info[0]
                    ]
                )
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

        file_location = f'{file_path}/summary.csv'
        util.write_csv(file_location, summaries)

        error_file_location = f'{file_path}/errors.json'
        error_json_content = json.dumps(errors, indent=4)
        util.write_json(error_file_location, error_json_content)
        print('Stored Summary')
    else:
        print('Summary exists')
        file_location = os.path.join(f'content/{today}', 'summary.csv')

if __name__ == "__main__":
    main()
