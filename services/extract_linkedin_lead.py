from pickle import NONE
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from linkedin_scraper import Person, actions
from .LSTM.test import compare

def get_linkedin_user_profile(url):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    email = "harishd_30@ymail.com"
    password = "ammuda19"
    actions.login(browser, email, password) # if email and password isnt given, it'll prompt in terminal
    person = Person(url, driver=browser)
    return person

def extract_from_linkedin(task, url, context, mode="shallow"):
    try:
        user = get_linkedin_user_profile(url)
        check = compare(user.about[0], context)
    except Exception as e:
        print(e)
        return None
    if check > 0.35:
        return user
    else:
        return None
