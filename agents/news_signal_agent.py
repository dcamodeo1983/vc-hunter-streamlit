import requests
from bs4 import BeautifulSoup

class NewsSignalAgent:
    def __init__(self, domain):
        self.domain = domain

    def run(self):
        news_data = []
        try:
            base_url = f"https://{self.domain}/news"
            response = requests.get(base_url, timeout=8)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all(['p', 'h2', 'article'])
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 50:
                        news_data.append(text)
        except:
            pass
        return news_data[:5]  # Limit to 5 entries
