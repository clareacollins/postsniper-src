from selenium.webdriver.common.by import By
import re

def extractUser(target):
    if "/" in target:
        return target.split("/")[3]
    else:
        return target

def extractCode(target):
    if "/" in target:
        return target.split("/")[5]
    else:
        return None

def getPost(driver):
    return driver.find_element(By.CSS_SELECTOR, "article")

def getPostPFP(post):
    return post.find_element(By.CSS_SELECTOR, "div[data-testid='Tweet-User-Avatar']")

def getUserName(post):
    user_names = post.find_elements(By.CSS_SELECTOR, "div[data-testid='User-Name'] a span")
    return user_names[0].text, user_names[1].text

def getPostText(post):
    return post.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']")

def getPostImages(post):
    return post.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetPhoto'] img")

def getPostDate(post):
    return post.find_element(By.CSS_SELECTOR, "time")

def getPostEnd(post):
    return post.find_element(By.CSS_SELECTOR, "article div.r-qklmqi").location["y"]

# Archive
def getMedia(driver):
    return driver.find_elements(By.CSS_SELECTOR, "li a")

def getSrc(image, driver=None):
    return re.sub("\?format=jpg&name=[\d|\w]*", "?format=jpg&name=large", image.get_attribute("src"))