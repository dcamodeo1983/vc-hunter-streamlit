import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMSummarizerAgent:
    def __init__(self, homepage, internal, company, news):
        self.homepage = homepage
        self.internal = internal
        self.company = company
        self.news = news

    def build_prompt(self):
        news_text = "\n".join(self.news)[:2000]
        return f"""
You're an expert analyst. Given this content, extract the firm's core investment behavior:

1. Investment thesis
2. Core sectors / verticals
3. Preferred stages, geographies
4. Strategic posture (bold vs cautious, thesis-driven vs opportunistic)
5. Co-investment behavior
6. Public signals and sentiment

--- HOMEPAGE ---
{self.homepage[:3000]}

--- INTERNAL PAGES ---
{self.internal[:3000]}

--- PORTFOLIO COMPANY TEXT ---
{self.company[:4000]}

--- NEWS & SIGNALS ---
{news_text}
"""

    def run(self):
        try:
            prompt = self.build_prompt()
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ LLM summarization failed: {e}")
            return ""
