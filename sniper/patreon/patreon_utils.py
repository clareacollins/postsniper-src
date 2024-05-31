from selenium.webdriver.common.by import By

from sniper import scope

import time

### DRIVER FUNCTIONS ###
# Closes the Membership Popup
def closeMembershipPopup(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "div.hlCuMM button").click()
        time.sleep(.5)
    except:
        pass
# Closes the App Popup
def closeAppPopup(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "div.izfzeJ button.erLepC").click()
        time.sleep(.5)
    except:
        pass

def clickPostType(driver):
    driver.find_elements(By.CSS_SELECTOR, "div.dAYgYF button.hjwRvq")[0].click()
    time.sleep(1)
def clickPostTier(driver):
    driver.find_element(By.CSS_SELECTOR, "div.dAYgYF button.hjwRvq")[1].click()
    time.sleep(1)
def clickPostDate(driver):
    driver.find_element(By.CSS_SELECTOR, "div.dAYgYF button.hjwRvq")[2].click()
    time.sleep(1)
def clickPostOrder(driver):
    driver.find_element(By.CSS_SELECTOR, "div.dAYgYF button.hjwRvq")[3].click()
    time.sleep(1)

def clickAllPosts(driver):
    driver.find_element(By.CSS_SELECTOR, "div.cQjDCC").click()
    time.sleep(1)

### STRING PROCESSING ### 
def extractCode(target):
    return target.split("/")[-1].split("-")[-1]
def extractUser(target):
    return target.split("/")[-2]

### Grab
def grabPost(driver):
    return driver.find_element(By.CSS_SELECTOR, "div.sc-kLwhqv")
def grabImages(post):
    return post.find_elements(By.CSS_SELECTOR, "div.bmhuBL img")
def grabLightboxImage(driver):
    return driver.find_element(By.CSS_SELECTOR, "div.hFYGny img")
def grabExpandButtons(driver):
    return driver.find_elements(By.CSS_SELECTOR, "button.fofpnM")
def grabFeedPosts(driver):
    return driver.find_elements(By.CSS_SELECTOR, "ul.jTaBgR span.hxhWXn a")
### Get
def getPostTitle(post):
    return post.find_element(By.CSS_SELECTOR, "span.eGFfXM").text
def getPostDate(post):
    return post.find_element(By.CSS_SELECTOR, "div.dXpjXs a").text
def getPostText(post):
    return scope.cleanText(post.find_element(By.CSS_SELECTOR, "div.ckzGeP").text)
def getPostTags(post):
    tags = post.find_elements(By.CSS_SELECTOR, "p.lbLzWd")
    return ", ".join([scope.cleanText(x.text) for x in tags])


def getPostEnd(post):
    return post.find_element(By.CSS_SELECTOR, "div.hHwPVy").location["y"]