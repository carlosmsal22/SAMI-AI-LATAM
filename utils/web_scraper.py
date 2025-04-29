import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Sample fallback data
SAMPLE_DATA = {
    "Secureonix": [
        {"comment": "Secureonix SIEM platform is powerful but hard to configure.", "source": "Reddit", "date": "2023-11-12"},
        {"comment": "Customer support for Secureonix could be better.", "source": "Trustpilot", "date": "2023-12-01"},
        {"comment": "Good experience working at Secureonix.", "source": "Glassdoor", "date": "2023-10-15"},
        {"comment": "Secureonix offers innovative security solutions.", "source": "Google", "date": "2023-11-20"}
    ]
}

def scrape_reddit(keyword, max_posts=5):
    print(f"Attempting to scrape Reddit for: {keyword}")
    try:
        url = f"https://api.pushshift.io/reddit/search/submission/?q={keyword}&size={max_posts}"
        response = requests.get(url, timeout=10)
        data = response.json()['data']
        return pd.DataFrame([{
            'comment': post['title'],
            'source': 'Reddit',
            'date': datetime.fromtimestamp(post['created_utc']).strftime("%Y-%m-%d")
        } for post in data])
    except Exception as e:
        print(f"Fallback to sample Reddit data due to: {e}")
        sample = [d for d in SAMPLE_DATA.get(keyword, []) if d['source'] == 'Reddit']
        return pd.DataFrame(sample[:max_posts])

def scrape_trustpilot(keyword, max_reviews=5):
    print(f"Attempting to scrape Trustpilot for: {keyword}")
    try:
        domain = {
            'apple': 'apple.com',
            'nike': 'nike.com',
            'secureonix': 'secureonix.com'
        }.get(keyword.lower())
        if not domain:
            raise ValueError("Brand not mapped to Trustpilot domain")
        
        url = f"https://www.trustpilot.com/review/{domain}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        reviews = []
        for review in soup.select('article.review')[:max_reviews]:
            reviews.append({
                'comment': review.select_one('.review-content__text').get_text(strip=True),
                'source': 'Trustpilot',
                'date': review.select_one('time')['datetime']
            })
        return pd.DataFrame(reviews)
    except Exception as e:
        print(f"Fallback to sample Trustpilot data due to: {e}")
        sample = [d for d in SAMPLE_DATA.get(keyword, []) if d['source'] == 'Trustpilot']
        return pd.DataFrame(sample[:max_reviews])

def scrape_glassdoor(keyword, max_reviews=5):
    print(f"Attempting to scrape Glassdoor for: {keyword}")
    try:
        search_query = f"{keyword} site:glassdoor.com"
        search_url = f"https://www.google.com/search?q={search_query}"
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for g in soup.select('div.tF2Cxc')[:max_reviews]:
            title = g.select_one('h3').text if g.select_one('h3') else "No title"
            results.append({
                'comment': title,
                'source': 'Glassdoor (via Google)',
                'date': datetime.now().strftime("%Y-%m-%d")
            })
        return pd.DataFrame(results)
    except Exception as e:
        print(f"Fallback to sample Glassdoor data due to: {e}")
        sample = [d for d in SAMPLE_DATA.get(keyword, []) if d['source'] == 'Glassdoor']
        return pd.DataFrame(sample[:max_reviews])

def scrape_google_search(keyword, max_results=5):
    print(f"Attempting to scrape Google News/Blogs for: {keyword}")
    try:
        search_query = f"{keyword} news OR blog"
        search_url = f"https://www.google.com/search?q={search_query}"
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for g in soup.select('div.tF2Cxc')[:max_results]:
            title = g.select_one('h3').text if g.select_one('h3') else "No title"
            results.append({
                'comment': title,
                'source': 'Google News/Blogs',
                'date': datetime.now().strftime("%Y-%m-%d")
            })
        return pd.DataFrame(results)
    except Exception as e:
        print(f"Fallback to sample Google data due to: {e}")
        sample = [d for d in SAMPLE_DATA.get(keyword, []) if d['source'] == 'Google']
        return pd.DataFrame(sample[:max_results])

def hybrid_scrape(keyword, max_results_per_source=5):
    print(f"Running enhanced hybrid scrape for: {keyword}")
    reddit_data = scrape_reddit(keyword, max_posts=max_results_per_source)
    trustpilot_data = scrape_trustpilot(keyword, max_reviews=max_results_per_source)
    glassdoor_data = scrape_glassdoor(keyword, max_reviews=max_results_per_source)
    google_data = scrape_google_search(keyword, max_results=max_results_per_source)
    combined = pd.concat([reddit_data, trustpilot_data, glassdoor_data, google_data], ignore_index=True)
    return combined
