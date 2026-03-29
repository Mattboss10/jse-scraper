jse-scraper 🇯🇲

A robust, headless-browser Python library designed to extract real-time market data from the Jamaica Stock Exchange (JSE).

Because the JSE website uses dynamic JavaScript rendering and modern bot-protection, standard scrapers often fail. jse-scraper utilizes Playwright to mimic human browsing patterns, ensuring reliable data ingestion for your financial models.

🚀 Key Features

Dynamic Rendering: Automatically handles JavaScript-heavy tables that requests cannot see.

Stealth Mode: Mimics human behavior (scrolling, viewport management) to avoid firewall triggers.

Pandas Native: Returns data directly as a DataFrame for immediate quantitative analysis.

Auto-Cleanup: Sanitizes headers, removes currency symbols ($), and standardizes "Ordinary Shares" tables.

📦 Installation

Ensure you have a virtual environment active, then install the package and its browser dependencies:

# Install the library (once published to PyPI)
pip install jse-scraper

# Install the necessary Chromium browser for Playwright
playwright install chromium


🛠️ Quick Start

from jse_scraper import JSEScraper

# Initialize the scraper
# Set headless=False if you want to watch the 'Searcher' work in a window
scraper = JSEScraper(headless=True)

print("📡 Fetching Market Data from JSE...")
df = scraper.get_trade_quotes()

if df is not None:
    # The library cleans headers automatically
    print(df[['Symbol', 'Last Traded Price', 'Volume']].head(10))
else:
    print("❌ Failed to retrieve data. Check your internet connection.")


📊 Why use a Headless Browser?

Most Caribbean stock exchange websites do not provide free public APIs. They rely on "Server-Side Rendering" or "Hydrated States" where data is injected into the page after it loads.

jse-scraper solves this by:

Launching a headless Chromium instance.

Navigating to the Trade Quotes page.

Waiting for the "Ordinary Shares" section to fully render.

Capturing the DOM and parsing it via lxml for maximum speed.

🏗️ Project Structure (src-layout)

jse_scraper/
├── src/
│   └── jse_scraper/
│       ├── __init__.py    # Package entry point
│       └── scraper.py     # Core Playwright & Pandas logic
├── pyproject.toml         # Build system & dependencies
└── README.md              # Documentation


⚖️ Disclaimer

This project is an independent open-source tool and is not affiliated with, authorized, or endorsed by the Jamaica Stock Exchange. This library is intended for educational and research purposes. Users must ensure their usage complies with the JSE's Terms of Service and data redistribution policies.

👨‍💻 Author

Developed by a Matthew Cohen
Building the data infrastructure for the next generation of Caribbean Fintech.