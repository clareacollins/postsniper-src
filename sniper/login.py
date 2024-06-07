from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from sniper import dir

import time

def tumblrLogin(driver):
    driver.get("https://www.tumblr.com/login")
    time.sleep(1)
    form = driver.find_elements(By.TAG_NAME, "form")[0]
    form.find_element(By.NAME, "email").send_keys(dir.LoginData["tumblr"]["email"])
    time.sleep(.5)
    form.find_element(By.NAME, "password").send_keys(dir.LoginData["tumblr"]["password"])
    time.sleep(.5)
    form.find_element(By.TAG_NAME, "button").click()
    time.sleep(5)

def patreonLogin(driver):
    driver.get("https://www.patreon.com/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys(dir.LoginData["patreon"]["email"])
    time.sleep(.5)
    driver.find_element(By.CSS_SELECTOR, "button.gWqiec").click()
    time.sleep(1)
    driver.find_element(By.NAME, "current-password").send_keys(dir.LoginData["patreon"]["password"])
    time.sleep(.5)
    driver.find_element(By.CSS_SELECTOR, "button.gWqiec").click()
    time.sleep(5)

def twitterLogin(driver):
    driver.get("https://x.com/i/flow/login")
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys(dir.LoginData["twitter"]["email"])
    time.sleep(.5)
    driver.find_element(By.CSS_SELECTOR, "button.r-13qz1uu").click()
    time.sleep(1)
    # If you have 2FA
    label_input = driver.find_element(By.CSS_SELECTOR, "label span").text
    if label_input == "Phone or username":
        driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys(dir.LoginData["twitter"]["username"])
        time.sleep(.5)
        driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys(Keys.ENTER)
        time.sleep(1)
    time.sleep(.5)
    driver.find_element(By.CSS_SELECTOR, "input.r-homxoj").send_keys(dir.LoginData["twitter"]["password"])
    time.sleep(.5)
    driver.find_element(By.CSS_SELECTOR, "button.r-19yznuf").click()
    time.sleep(5)

def loginType(driver, type='tumblr'):
    print(f"Logging into {type}...")
    if type == 'tumblr':
        tumblrLogin(driver)
    elif type == 'patreon':
        patreonLogin(driver)
    elif type == 'twitter':
        twitterLogin(driver)

def reload(type='tumblr'):
    print("Reloading Driver")
    time.sleep(5)
    driver = webdriver.Chrome()
    if type == 'tumblr':
        tumblrLogin(driver)
    elif type == 'patreon':
        patreonLogin(driver)
    elif type == 'twitter':
        twitterLogin(driver)
    return driver