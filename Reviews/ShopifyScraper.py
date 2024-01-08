import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_reviews(url, num_pages):
    data = {'Review': [], 'Date': [], 'Company': [], 'Country': [], 'App Usage': [], 'Stars': []}

    for page in range(1, num_pages + 1):
        page_url = f"{url}&page={page}"

        response = requests.get(page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            review_containers = soup.find_all('div', {'data-merchant-review': True})

            for review_container in review_containers:
                review_content = review_container.find('p', {'class': 'tw-break-words'}).text.strip()

                date = review_container.find('div', {'class': 'tw-text-body-xs'}).text.strip()

                metadata_container = review_container.find('div', {'class': 'tw-order-2'})
                company = metadata_container.find('div', {'class': 'tw-text-fg-primary'}).text.strip()
                country = metadata_container.find_all('div')[1].text.strip()
                app_usage = metadata_container.find_all('div')[2].text.strip()

                stars = len(review_container.find_all('svg', {'class': 'tw-fill-fg-primary'}))

                data['Review'].append(review_content)
                data['Date'].append(date)
                data['Company'].append(company)
                data['Country'].append(country)
                data['App Usage'].append(app_usage)
                data['Stars'].append(stars)

        else:
            print(f"Error: Unable to fetch page {page}. Status code {response.status_code}")

    df = pd.DataFrame(data)

    df.to_excel('biteScraperXLS.xlsx', index=False)

if __name__ == "__main__":
    base_url = "https://apps.shopify.com/bitespeed-fb-messenger-chatbot/reviews?sort_by=newest&ratings%5B%5D=5"

    num_pages = 25

    scrape_reviews(base_url, num_pages)

# pip install beautifulsoup4 requests pandas
