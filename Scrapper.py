import requests
from bs4 import BeautifulSoup
import os

file_dir = "D:\Other Stuff\MTG Card Discord BOt\MTGCards"

url = "https://www.mtggoldfish.com/sets/The+Lord+of+the+Rings+Tales+of+Middle+Earth#online"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

with open(os.path.join(file_dir, 'LOTR.txt'), 'w') as f:
    for a_tag in soup.find_all('a', {'data-full-image': True}):
        image_link = a_tag['data-full-image']
        f.write(image_link + '\n')