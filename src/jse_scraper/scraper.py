import pandas as pd
from playwright.sync_api import sync_playwright
from io import StringIO
import time

class JSEScraper:
    def __init__(self, headless=True):
        self.url = "https://www.jamstockex.com/trading/trade-quotes/"
        self.headless = headless

    def get_trade_quotes(self):
        """Fetches the main market ordinary shares table."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(self.url, wait_until="networkidle")
            
            # Use the 'Human-like' wait we discovered earlier
            time.sleep(5) 
            page.get_by_text("ORDINARY SHARES", exact=False).scroll_into_view_if_needed()
            
            html_content = page.content()
            browser.close()
            
        return self._parse_html(html_content)

    def _parse_html(self, html):
        """Internal helper to clean up JSE tables."""
        tables = pd.read_html(StringIO(html), flavor='lxml')
        for df in tables:
            if 'Symbol' in df.columns or 'Security' in df.columns:
                # Standardize headers for the user
                df.columns = [str(c).replace('\n', ' ').replace(' ($)', '').strip() for c in df.columns]
                return df.dropna(subset=['Symbol'])
        return None