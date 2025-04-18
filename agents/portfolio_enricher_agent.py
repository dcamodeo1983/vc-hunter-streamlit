import requests
from bs4 import BeautifulSoup

class PortfolioEnricherAgent:
    def __init__(self, portfolio_links):
        self.links = portfolio_links

    def run(self):
        company_data = []
        for url in self.links[:10]:  # Limit for safety
            try:
                response = requests.get(url, timeout=8)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    text = soup.get_text(separator=" ", strip=True)
                    company_data.append(text[:3000])
            except:
                continue
        return "\n".join(company_data)
