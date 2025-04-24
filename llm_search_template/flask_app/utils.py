import os
import requests
from bs4 import BeautifulSoup
import openai

# Load API keys from environment variables
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


def search_articles(query):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.
    """
    search_url = f"https://serper.com/search?q={query}"
    headers = {"Authorization": f"Bearer {SERPER_API_KEY}"}
    response = requests.get(search_url, headers=headers)
    articles = []
    
    if response.status_code == 200:
        data = response.json()
        for result in data.get("results", []):
            articles.append({
                "url": result.get("url"),
                "heading": result.get("title"),
                "text": fetch_article_content(result.get("url"))
            })
    return articles


def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text.
    """
    response = requests.get(url)
    if response.status_code != 200:
        return ""
    
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = " ".join([para.get_text() for para in paragraphs if para.get_text()])
    return content.strip()


def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    """
    full_text = ""
    for article in articles:
        full_text += f"Title: {article['heading']}\n{article['text']}\n\n"
    return full_text


def generate_answer(content, query):
    # Structure the prompt as a conversation with roles (system, user, assistant)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query},
        {"role": "assistant", "content": content}
    ]
    
    try:
        # Make the API call to OpenAI for text generation using the new Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4" if needed
            messages=messages,
            max_tokens=150,  # Adjust based on your needs
            temperature=0.7  # Control randomness in the response (0 to 1)
        )
        
        # Return the generated answer from the assistant
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"Error generating answer: {e}"