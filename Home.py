import requests
from bs4 import BeautifulSoup
import json
from flask import Flask


app = Flask(__name__)


def get_latest_stories():
    url = "https://time.com"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the elements containing the latest stories
        story_elements = soup.find_all('div', class_='partial latest-stories')
        
        # Extract and print the titles of the latest stories
        #print(story_elements)
        titles_array = []
        links_array = []
        for story_element in story_elements:
            titles = story_element.find_all('h3', class_='latest-stories__item-headline')
            for title in titles:
                titles_array.append(title.text)
                #print(title.text)

            for a in story_element.find_all('a', href=True):
              links_array.append("https://time.com" + a['href'])
              #print(a['href'])

            score_titles = [{"title": t, "link": s} for t, s in zip(titles_array, links_array)]
            return json.dumps(score_titles)


                
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

@app.route('/getTimeStories', methods=['GET'])
def get_Time_Stories():   
    return get_latest_stories()

if __name__ == '__main__':
    app.run(debug=True)
