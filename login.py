from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep

def tumblrLogin(driver):
    driver.get("https://www.tumblr.com/login")
    # REDACTED
    sleep(5)

def patreonLogin(driver):
    driver.get("https://www.patreon.com/login")
    # REDACTED
    sleep(5)

def twitterLogin(driver):
    driver.get("https://twitter.com/login")
    # REDACTED
    sleep(5)
    

def reload(type='tumblr'):
    print("Reloading Driver")
    sleep(5)
    driver = webdriver.Chrome()
    if type == 'tumblr':
        tumblrLogin(driver)
    elif type == 'patreon':
        patreonLogin(driver)
    elif type == 'twitter':
        twitterLogin(driver)
    return driver
