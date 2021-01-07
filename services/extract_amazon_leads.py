from bs4 import BeautifulSoup
import requests
import json

def extract_from_amazon(site_url):
    reviews = []
    review_return = []
    for i in range(0,10):
        arr = site_url.split('&')
        my_str = arr[0] + '&' + arr[1] + '&' +arr[2] + '&pageNumber=' + str(i+1) + '#reviews-filter-bar'
        result = requests.get(my_str)
        src = result.content
        soup = BeautifulSoup(src,'lxml')
        for tag in soup.find_all('div',{'class':'a-section review aok-relative'}):
            reviews.append(tag)
        print(my_str)

    for review in reviews:
        review_dict = {'name':'','title':'','rating':'','content':''}
        review = str(review)
        soup = BeautifulSoup(review,'lxml')

        for tag in soup.findAll('span',{'class':'a-profile-name'}):
            review_dict['name'] = str(tag.text)

        for tag in soup.findAll('a',{'class':'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'}):
            review_dict['title'] = str(tag.span.text)

        for tag in soup.findAll('i',{'class':'a-icon a-icon-star a-star-1 review-rating'}):
            rating = str(tag.span.text)
            rating = rating.split('.')
            review_dict['rating'] = str(rating[0])

        for tag in soup.findAll('span',{'class':'a-size-base review-text review-text-content'}):
            review_dict['content'] = str(tag.span.text)

        review_return.append(review_dict)


    json_formatted_str = json.dumps(review_return, indent=2)
    json_loader = json.loads(json_formatted_str)

    return json.dumps(json_loader)
