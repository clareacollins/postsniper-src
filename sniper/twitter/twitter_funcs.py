from sniper.twitter import twitter_utils as utils

from sniper import scope

import time, requests, re

def downloadImages(images, filename):
    num = 1
    for image in images:
        src = image.get_attribute("src")
        src = re.sub("\?format=jpg&name=[\d|\w]*", "?format=jpg&name=large", src)
        if src != "https://":
            r = requests.get(src)
            with open(f"{filename} - {num}.png", "wb") as f:
                f.write(r.content)
            num += 1

def commandMedia(driver):
    # Grab Media
    post_list = []
    data_tuples = []
    # Process Posts while scrolling
    last_height = scope.getScroll(driver)
    while True:
        new_height = scope.scrollScreen(driver)
        if new_height != last_height:
            time.sleep(10)
            # Grab Posts
            new_posts = []
            posts = utils.getMedia(driver)
            for post in posts:
                if post not in post_list:
                    post_list.append(post)
                    new_posts.append(post)
            for post in new_posts:
                data_tuples.append((post.get_attribute("href")))
            last_height = scope.getScroll(driver)
        else:
            break
        last_height = new_height
    return data_tuples