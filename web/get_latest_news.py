# filename: get_latest_news.py
import requests
from bs4 import BeautifulSoup

def parse_headlines(url):
    headline_list = []
    page = requests.get(url)
    
    soup = BeautifulSoup(page.content, 'html.parser')  # Use beautiful soup to get info from the webpage
    
    for item in soup.find_all('h3', class_='article-headline'):
        headline = str(item).lower()
        if 'latest' or 'top' in headline:
            headline_list.append(str(item))
            
    return headline_list
    
if __name__ == "__main__":  # The code only runs when run as a script, not imported
    url='https://www.bbc.co.uk/news' # Set the URL for news collection. Feel free to change it for different sources or categories of News.
    newest_headlines = parse_headlines(url)  # Run the function and store the parsed data in a variable
    
    print("Latest Headline:", end=' ')
    if newest_headlines:   # Check whether there are headlines extracted from the news page or not
        print("\n".join([x.strip() for x in newest_headlines]))  # Print the collected latest news headlines without any extra spacing between each line if it's successful or show an error message otherwise
    else:
        print("No News Headline found.")