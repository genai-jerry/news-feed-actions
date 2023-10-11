import requests
from bs4 import BeautifulSoup

def extract_article_content(url):
    """
    Connect to the article URL and extract the content.

    Parameters:
    url (str): The URL of the article.

    Returns:
    str: The extracted content of the article.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
    }

    try:
        # Sending a request to the webpage
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        print(f"Error connecting to {url}: {e}")
        return None

    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all paragraph tags and extract the text
    paragraphs = soup.find_all('p')
    article_content = ' '.join(paragraph.text for paragraph in paragraphs)

    return article_content

# Example usage
article_url = 'https://example.com/article-link'
article_content = extract_article_content(article_url)
print(article_content)
