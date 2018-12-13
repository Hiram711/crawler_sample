import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
host = 'https://www.zhihu.com'
params = {'offset': 15, 'type': 'day'}
params_json = json.dumps(params)
r = requests.get("https://www.zhihu.com/node/ExploreAnswerListV2?params=%s" % params_json, headers=headers)
print(r.status_code)
print(r.url)
soup = BeautifulSoup(r.text, 'html5lib')
answer_list = soup.select('.explore-feed.feed-item')
for answer in answer_list:
    question = answer.find(attrs={'data-za-element-name': 'Title'}).text.strip()
    question_url = urljoin(host,answer.find(attrs={'data-za-element-name': 'Title'}).attrs['href'])
    author = answer.find(attrs={'class': 'author-link'}).text
    author_url = urljoin(host,answer.find(attrs={'class': 'author-link'}).attrs['href'])
    answer_content = answer.find('textarea', class_='content').text
    answer_url = urljoin(host,answer.find('a', class_='answer-date-link meta-item').attrs['href'])
    answer_output = (question, question_url, author, author_url, answer_url)
    print(answer_output)
