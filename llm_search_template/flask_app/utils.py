import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

load_dotenv()

# API Keys
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def search_articles(query):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"q": query}
    response = requests.post(url, json=payload, headers=headers)

    articles = []
    if response.status_code == 200:
        data = response.json()
        for result in data.get("organic", []):
            articles.append({
                "url": result.get("link"),
                "heading": result.get("title"),
                "text": fetch_article_content(result.get("link"))
            })
    return articles

def fetch_article_content(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return ""
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = " ".join([p.get_text() for p in paragraphs if p.get_text()])
        return content.strip()
    except Exception:
        return ""

def concatenate_content(articles):
    content = ""
    for article in articles:
        content += f"Title: {article['heading']}\n{article['text']}\n\n"
    return content

def generate_answer(content, query):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
            {"role": "assistant", "content": content}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating answer: {e}"
