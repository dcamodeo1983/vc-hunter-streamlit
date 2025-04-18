import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class VCWebsiteScraperAgent:
    def __init__(self, url):
        self.url = url
        self.domain = url.replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
        self.session = requests.Session()

    def fetch_page(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = self.session.get(url, timeout=10, headers=headers)
            if response.status_code == 200 and "text/html" in response.headers.get("Content-Type", ""):
                return response.text
        except Exception as e:
            print(f"❌ Failed to load {url}: {e}")
        return ""

    def find_internal_links(self, soup, keyword_list):
        links = []
        for link_tag in soup.find_all("a", href=True):
            href = link_tag['href']
            text = link_tag.get_text(strip=True).lower()
            if any(k in href.lower() or k in text for k in keyword_list):
                full_url = urljoin(self.url, href)
                if self.domain in full_url:
                    links.append(full_url)
        return list(set(links))

    def scrape(self):
        homepage_html = self.fetch_page(self.url)
        soup = BeautifulSoup(homepage_html, "html.parser")
        homepage_text = soup.get_text(separator=" ", strip=True)

        portfolio_links = self.find_internal_links(soup, ["portfolio", "companies", "investments"])
        internal_texts = []
        all_company_links = []

        for link in portfolio_links[:5]:  # Limit to 5
            internal_html = self.fetch_page(link)
            if internal_html:
                internal_soup = BeautifulSoup(internal_html, "html.parser")
                internal_texts.append(internal_soup.get_text(separator=" ", strip=True))
                external_links = self.find_internal_links(internal_soup, [".com"])
                for e in external_links:
                    if self.domain not in e:
                        all_company_links.append(e)

        return {
            "homepage": homepage_text,
            "internal": "\n\n".join(internal_texts),
            "portfolio_links": list(set(all_company_links))
        }
