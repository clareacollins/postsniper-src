from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from sniper import scope

import time

### DRIVER FUNCTIONS ###
# Closes the App Popup
def closeAppPopup(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "div.izfzeJ button.erLepC").click()
        time.sleep(.5)
    except:
        pass
# Closes the Membership Popup
def closeMembershipPopup(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "div.hlCuMM button").click()
        time.sleep(.5)
    except:
        pass

def findButton(driver, keyword):
    buttons = driver.find_elements(By.CSS_SELECTOR, "div.dAYgYF button.hjwRvq")
    for button in buttons:
        if keyword == button.text:
            return button
    return None

def selectFilter(driver, keyword, subelement):
    findButton(driver, keyword).click()
    buttons = driver.find_elements(By.CSS_SELECTOR, subelement)
    option_tuples = [(0, "All")] + [(buttons.index(button) + 1, button.text) for button in buttons]
    userSelect = input(scope.userSelectMssg(option_tuples, keyword))
    if userSelect != "0":
        buttons[int(userSelect) - 1].click()
        time.sleep(1)
        value = f"{option_tuples[int(userSelect)][1].split(' (')[0]}"
    else:
        driver.find_element(By.CSS_SELECTOR, "div.dAYgYF button.hjwRvq").send_keys(Keys.ESCAPE)
        time.sleep(1)
        value = None
    return value

def toggleOrder(driver):
    driver.find_element(By.CSS_SELECTOR, "div.dAYgYF button.kjazmo").click()
    time.sleep(1)
    buttons = driver.find_elements(By.CSS_SELECTOR, "a.iQxAKa")
    userSelect = input("Select Order:\n[0] Newest to oldest\n[1] Oldest to newest\n")
    if userSelect == "1":
        buttons[1].click()
        time.sleep(1)
        return " ASC"
    else:
        driver.find_element(By.CSS_SELECTOR, "div.dAYgYF button.hjwRvq").send_keys(Keys.ESCAPE)
        return ""

### STRING PROCESSING ### 
def extractUser(target, driver):
    if "/" in target:
        return driver.find_element(By.CSS_SELECTOR, "div.hLKCev").text
    else:
        return target
def extractCode(target):
    return target.split("/")[-1].split("-")[-1]

### Grab
def grabPost(driver):
    return driver.find_element(By.CSS_SELECTOR, "div.sc-kLwhqv")
def grabImages(post):
    return post.find_elements(By.CSS_SELECTOR, "div.bmhuBL img")
def grabLightboxImage(driver):
    return driver.find_element(By.CSS_SELECTOR, "div.hFYGny img")
def grabExpandButtons(driver):
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.fofpnM")
    return [button for button in buttons if button.text == "Load more"]
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

def getSrc(image, driver):
    try:
        image.click()
        time.sleep(2)
        src = grabLightboxImage(driver).get_attribute("src")
    except:
        src = image.get_attribute("src")
    return src