import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd

st.set_page_config(page_title="Web Scraper", layout="centered")

# Helper function to validate and normalize URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ["http", "https"]
    except:
        return False

# Recursive scraping function
def scrape_website(url, visited):
    if url in visited:
        return []

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return [(url, f"Failed to retrieve content. Status Code: {response.status_code}")]

        visited.add(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract text
        page_text = soup.get_text(separator=' ', strip=True)

        # Find links and recursively scrape subpages
        base = urlparse(url)
        domain = base.netloc
        links = [urljoin(url, tag['href']) for tag in soup.find_all('a', href=True)]
        internal_links = set(link for link in links if urlparse(link).netloc == domain)

        data = [(url, page_text)]

        for link in internal_links:
            if link not in visited:
                data.extend(scrape_website(link, visited))

        return data

    except Exception as e:
        return [(url, f"Error: {str(e)}")]

# Streamlit UI
st.title("🌐 Website Scraper with Subpage Support")
st.markdown("Enter a URL and get a full report of the content (including subpages).")

url_input = st.text_input("Enter the website URL (e.g., https://example.com):")

if st.button("🔍 Start Scraping"):
    if not url_input:
        st.warning("Please enter a valid URL.")
    elif not is_valid_url(url_input):
        st.error("Invalid URL format. Make sure it starts with http:// or https://")
    else:
        st.info("Scraping in progress. Please wait...")
        visited = set()
        scraped_data = scrape_website(url_input, visited)

        df = pd.DataFrame(scraped_data, columns=["URL", "Content"])
        st.success(f"Scraping completed. {len(df)} pages scanned.")

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Full Report (CSV)",
            data=csv,
            file_name="web_scraping_report.csv",
            mime="text/csv"
        )
