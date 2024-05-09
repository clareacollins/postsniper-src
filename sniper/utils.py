from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import urllib.request

import time, re

import scope, dir

# Detect Lost Posts
def detectLostPosts(driver):
    try:
        articles = driver.find_elements(By.CSS_SELECTOR, "article")
        asides = driver.find_elements(By.CSS_SELECTOR, "aside article")
        if len(articles) == len(asides):
            print('Lost Post')
            return True
        return False
    except:
        return True

def grabImages(post):
# Images from Ask Posts Come First
    # Imgs inline with Ask Answer
    aim_in = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.XZFs6 div.WIYYp img")
    # Imgs that are the Ask Answer
    aim_but = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 button.TRX6J img")
# Images from Standard Posts
    img_std = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.CQmeg img.RoN4R")
# Compile
    images = []
    for image in aim_in:
        if image not in images:
            images.append(image)
    for image in aim_but:
        if image not in images:
            images.append(image)
    for image in img_std:
        if image not in images:
            images.append(image)
    #print(len(images))
    return images

# Detect Post Type
def detectPostType(post):
# Detect Images in Post
    all_images = grabImages(post)
    # Separate Gifs from Images
    images = []
    gifs = []
    for image in all_images:
        if scope.grabSrc(image, "MAX").split(".")[-1] != "gifv":
            images.append(image)
        else:
            gifs.append(image)
# Detect Other Media
    # Video
    videos = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.yz4vl source")
    video_links = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.ypwxx iframe")
    # Audio
    audio = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.vP7cO audio source")
    contents = [(images, "png"), (gifs, "gif"), (videos, "mp4"), (audio, "mp3")]
    # Determine Type
    if len(audio) > 0:
        return "audio", contents
    elif len(videos) > 0 or len(video_links) > 0:
        return "video", contents
    elif len(gifs) > 0:
        return "gif", contents
    elif len(images) > 0:
        return "img", contents
    else:
        return "text", contents

def grabPostText(post, delimiter="|", allBool=False):
    text_els = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.k31gt")
    final_text = "None"
    if len(text_els) != 0:
        final_text = ""
        if not allBool:
            final_text = text_els[0].text
        else:
            for text_el in text_els:
                final_text += text_el.text + delimiter
    final_text = re.sub(r"\n|@", " ", final_text)
    return final_text

def grabSourceCode(driver, post, source):
    try:
        post.find_element(By.CSS_SELECTOR, "div.u2tXn [aria-label='More options']").click()
        time.sleep(.5)
        source_code = driver.find_elements(By.CSS_SELECTOR, "div.iaJAj a")[0].get_attribute("href")
        if source not in source_code:
            source_code = "None"
        return source_code
    except:
        return "None"

# Open Post
def openPost(driver):
# Grab Post
    post = driver.find_elements(By.CSS_SELECTOR, "article")[0]
# If Read More, Click Read More
    if len(post.find_elements(By.CSS_SELECTOR, "div.ZqZ6N button")) > 0:
        post.find_elements(By.CSS_SELECTOR, "div.ZqZ6N button")[0].click()
        time.sleep(.5)
# Expand Tags if Possible
    for tag in post.find_elements(By.CSS_SELECTOR, "div.mwjNz a"):
        try:
            if tag.text == "… See all":
                tag.click()
                time.sleep(.5)
        except:
            continue
# Scroll to Post and Move Cursor
    driver.execute_script(f"window.scrollTo(0, 0);")
    ActionChains(driver).move_to_element(driver.find_elements(By.CSS_SELECTOR, "header")[0]).perform()
    time.sleep(.5)
    return post, post.find_elements(By.CSS_SELECTOR, "footer")[0]

# Assemble Post
def assemblePost(driver, filename, post, fitBool=False):
    dest = f'{dir.root}\\extract\\temp\\'
    images = grabImages(post)

# Handle No Images
    if len(images) == 0:
        scope.captureElement(driver, filename, post, bottom=post.find_elements(By.CSS_SELECTOR, "footer")[0].location["y"])
        return TypeError
# Generate Image Element Location Tuples
    img_tuples = []
    for image in images:
        src = scope.grabSrc(image, " 540w")
        if not fitBool:
            src = scope.grabSrc(image, " 1280w")
        # print(src)
        # [0] element, [1] link, [2] top coord, [3] bottom coord
        img_tuples.append((image, src, image.location["y"], image.location["y"] + image.size["height"]))
# Screenshot from Top of Post to Top of First Image
    capture = scope.captureElement(driver, filename, post, bottom=img_tuples[0][2])
# Add Image
    for image_tup in img_tuples:
        # Download Image, add to Capture
        urllib.request.urlretrieve(image_tup[1], f"{dest}Temp - 1.png")
        scope.combine(filename, f"{dest}Temp - 1.png", fitBool=fitBool)
    # Between Images (and not after the last image)
        if image_tup != img_tuples[-1] and img_tuples[img_tuples.index(image_tup) + 1][2] - image_tup[3] > 20:
            driver.execute_script(f"window.scrollTo(0, 0);")
            scope.captureElement(driver, f"{dest}Temp - 1", post,
                                             top=image_tup[3], 
                                             bottom=img_tuples[img_tuples.index(image_tup) + 1][2])
            scope.combine(filename, f"{dest}Temp - 1.png")
            # Screenshot from Bottom of Last Image to Top of Notes (Post Footer)
    driver.execute_script(f"window.scrollTo(0, 0);")
    scope.captureElement(driver, f"{dest}Temp - 1", post, 
                                               top=img_tuples[-1][3],
                                               bottom=post.find_elements(By.CSS_SELECTOR, "footer")[0].location["y"])
    scope.combine(filename, f"{dest}Temp - 1.png")