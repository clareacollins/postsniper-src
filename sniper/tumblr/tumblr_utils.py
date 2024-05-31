from selenium.webdriver.common.by import By

from sniper import scope

import time

### DRIVER FUNCTIONS ###
# Open URL to blog's archive
def driverGetArchive(driver, user, tag="None"):
    if tag == "None":
        driver.get(f"https://{user}.tumblr.com/archive")
    else:
        driver.get(f"https://{user}.tumblr.com/archive/tagged/{tag}")
    time.sleep(2)    
# Open URL to blog's feed
def driverGetFeed(driver, user, tag="None"):
    if tag == "None":
        driver.get(f"https://tumblr.com/{user}")
    else:
        driver.get(f"https://tumblr.com/{user}/tagged/{tag}")
    time.sleep(2)

### DRIVER INTERACTIONS ###
def clickReadMore(post):
    readMoreEls = post.find_elements(By.CSS_SELECTOR, "div.ZqZ6N button")
    if len(readMoreEls) > 0:
        readMoreEls[0].click()
        time.sleep(.5)
def clickSeeAll(post):
    seeAllEls = post.find_elements(By.CSS_SELECTOR, "div.mwjNz a")
    for el in seeAllEls:
        try:
            if el.text == "… See all":
                el.click()
                time.sleep(.5)
        except:
            continue
def clickOptions(post):
    post.find_element(By.CSS_SELECTOR, "div.u2tXn [aria-label='More options']").click()
    time.sleep(.5)
def clickURL(post):
    post.find_element(By.CSS_SELECTOR, "div.KFWnx").click()
    time.sleep(.5)

### STRING PROCESSING ###
# Passed a tumblrfirst link, returns user and code
def extractUserAndCode(link):
    user = link.split("/")[3]
    code = link.split("/")[4]
    return user, code
# Grabs the code from a tumblr link
def extractSourceCode(url):
    if url != "None" and url != "Error":
        return ""
        # return re.match(r"\/(\d\d\d\d\d\d+)", url)[0]
    return "None"
# passed a tsv line of user and tag, returns user and tag
def extractUserAndTag(tsv):
    user = tsv.split("\t")[0]
    tag = tsv.split("\t")[1]
    return user, tag

### BOOLEAN FUNCTIONS ###
# Detect Lost Posts
def detectLostPosts(driver):
    if driver.current_url == "https://www.tumblr.com/explore/trending":
        return True
    try:
        articles = driver.find_elements(By.CSS_SELECTOR, "article")
        asides = driver.find_elements(By.CSS_SELECTOR, "aside article")
        if len(articles) == len(asides):
            print('Lost Post')
            return True
        else:
            return False
    except:
        return True
# Detect if a image element is a gif
def isGif(element):
    if '.gif' in element.get_attribute("srcset") and '.gifv' not in element.get_attribute("srcset"):
        return True
    return False

### GRABBERS - RETURN ELEMENT(S) ###
# Post Elements
def grabPost(driver):
    return driver.find_elements(By.CSS_SELECTOR, "article")[0]
def grabHeader(post):
    return post.find_elements(By.CSS_SELECTOR, "header")[0]
def grabNotes(post):
    return post.find_elements(By.CSS_SELECTOR, "footer")[0]
def grabText(post):
    return post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.k31gt")
def grabLinks(post):
    return post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.k31gt a")
def grabReblogs(post):
    return post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.u2tXn")
def grabVideos(post):
    return post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.yz4vl source")
def grabAudio(post):
    return post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.vP7cO audio source")
def grabImages(post):
# Images from Ask Posts Come First
    # Imgs inline with Ask Answer
    aim_in = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.XZFs6 div.WIYYp img")
    # Imgs that are the Ask Answer
    aim_but = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 button.TRX6J img")
# Images from Standard Posts
    img_std = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.CQmeg img.RoN4R")
# Compile and Filter
    images = list(set(aim_in) | set(aim_but) | set(img_std))
    return sorted(images, key=lambda x: x.location["y"])
# Archive & Feed Elements
def grabArchiveMonths(driver):
    return driver.find_elements(By.CSS_SELECTOR, "div.hSoZ1")
def grabArchivePosts(month):
    return month.find_elements(By.CSS_SELECTOR, "div.NGc5k")
def grabFeedPosts(driver):
    return driver.find_elements(By.CSS_SELECTOR, "div.zAlrA > div") # direct children of div.zAlrA

### GETTERS - Perform Operations on Element(s) ###
def getImages(post):
    images = []
    gifs = []
    im_all = grabImages(post)
    for image in im_all:
        if isGif(image):
            gifs.append(image)
        else:
            images.append(image)
    return images, gifs

# Return String
def getURL(driver):
    url = driver.find_elements(By.CSS_SELECTOR, "div.iaJAj a")[0].get_attribute("href")
    if url == None:
        return "None"
    return url
def getSourceUser(post, user):
    source = post.find_elements(By.CSS_SELECTOR, "div.sqHC2")
    return source[0].text if len(source) != 0 else user
def getText(post, allBool=False):
    els = grabText(post)
    if not allBool:
        if len(els) == 0:
            return "None"
        return scope.cleanText(els[0].text)
    else:
        text = []
        for el in els:
            text.append(scope.cleanText(el.text))
        return " | ".join(text)
def getCaption(post):
    text = getText(post, allBool=False)
    if text != []:
        caption = scope.cleanFilename(text)[:150].strip()
    if caption == "None":
        caption = None
    return caption
def getTags(post):
    tags = post.find_elements(By.CSS_SELECTOR, "div.mwjNz a")
    tags_text = scope.cleanText(", ".join([x.text for x in tags]))
    return tags_text

def getArchiveLink(post):
    return post.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
def getArchiveTags(post):
    tags = post.find_elements(By.CSS_SELECTOR, "div.d1luu")
    tags_text = "" if len(tags) == 0 else tags[0].get_attribute("innerHTML")
    return scope.cleanText(tags_text)
def getFeedCode(post):
    try:
        code = post.get_attribute("data-cell-id")
        if code.split("==")[1].isdigit():
            return code.split("==")[1]
        return "None"
    except:
        return "None"

### Return Int ###
def getPostEnd(post):
    return grabNotes(post).location["y"]