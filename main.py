import pandas as pd
from playwright.sync_api import sync_playwright
from io import StringIO
import time

def visual_jse_debug():
    url = "https://www.jamstockex.com/trading/trade-quotes/"
    
    with sync_playwright() as p:
        print("🚀 Launching VISUAL Browser (Watch the window!)...")
        # Change headless to False to see what's happening
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(viewport={'width': 1280, 'height': 1000})
        page = context.new_page()
        
        page.goto(url, wait_until="domcontentloaded")

        # 1. Wait for the page to settle
        print("⏳ Waiting for page to settle...")
        time.sleep(5)

        # 2. Try to find the 'Ordinary Shares' heading and scroll to it
        try:
            print("🔍 Searching for 'Ordinary Shares' section...")
            # Using a case-insensitive search
            shares_header = page.get_by_text("ORDINARY SHARES", exact=False)
            shares_header.scroll_into_view_if_needed()
            print("✅ Found header and scrolled.")
        except:
            print("❌ Could not find 'Ordinary Shares' header.")

        # 3. Instead of waiting for visibility, let's just grab the content 
        # after a fixed delay. Sometimes tables are 'visible' to humans but 
        # 'hidden' to Playwright's automated checks.
        print("📸 Taking state snapshot...")
        html_content = page.content()
        
        # Save a new screenshot while the browser is open
        page.screenshot(path="live_debug.png")
        
        browser.close()
        
    try:
        tables = pd.read_html(StringIO(html_content), flavor='lxml')
        print(f"📊 Found {len(tables)} total tables.")
        
        for i, df in enumerate(tables):
            # Check for common JSE columns
            columns_str = " ".join([str(c) for c in df.columns])
            if "Symbol" in columns_str or "Security" in columns_str:
                print(f"🎯 Target Table identified at index {i}!")
                # Clean up headers
                df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
                return df.dropna(subset=['Symbol'])
        
        return None
    except Exception as e:
        print(f"❌ Error during parsing: {e}")
        return None

# Execution
df = visual_jse_debug()
if df is not None:
    print("\n--- JSE DATA DETECTED ---")
    print(df.head(10))