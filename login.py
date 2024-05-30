from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep

def tumblrLogin(driver):
    driver.get("https://www.tumblr.com/login")
    sleep(1)
    form = driver.find_elements(By.TAG_NAME, "form")[0]
    form.find_element(By.NAME, "email").send_keys("REDACTED")
    sleep(.5)
    form.find_element(By.NAME, "password").send_keys("REDACTED")
    sleep(.5)
    form.find_element(By.TAG_NAME, "button").click()
    sleep(5)

def patreonLogin(driver):
    driver.get("https://www.patreon.com/login")
    sleep(1)
    driver.find_element(By.NAME, "email").send_keys("REDACTED")
    sleep(.5)
    driver.find_element(By.CSS_SELECTOR, "button.gWqiec").click()
    # wait = input("Press Enter to Continue")
    sleep(1)
    driver.find_element(By.NAME, "current-password").send_keys("REDACTED")
    sleep(.5)
    driver.find_element(By.CSS_SELECTOR, "button.gWqiec").click()
    sleep(5)

def twitterLogin(driver):
    driver.get("https://twitter.com/login")
    sleep(1)
    driver.find_element(By.NAME, "session[username_or_email]").send_keys("REDACTED")
    sleep(.5)
    driver.find_element(By.NAME, "session[password]").send_keys("REDACTED")
    sleep(.5)
    driver.find_element(By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button']").click()
    sleep(5)
    

def reload(type='tumblr'):
    print("Reloading Driver")
    sleep(5)
    driver = webdriver.Chrome()
    if type == 'tumblr':
        tumblrLogin(driver)
    elif type == 'patreon':
        patreonLogin(driver)
    driver.set_window_size(1024, 1940)
    return driver
