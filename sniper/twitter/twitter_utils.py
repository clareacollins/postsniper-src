from selenium.webdriver.common.by import By


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

# Archive
def getMedia(driver):
    return driver.find_elements(By.CSS_SELECTOR, "li a")