from sniper.patreon import patreon_utils as utils

from sniper import scope

import time, requests

def downloadImages(driver, images, filename):
    num = 1
    for image in images:
        try:
            image.click()
            time.sleep(2)
            src = utils.grabLightboxImage(driver).get_attribute("src")
        except:
            src = image.get_attribute("src")
        if src != "https://":
            r = requests.get(src)
            print(f"{filename} - {num}.png")
            with open(f"{filename} - {num}.png", "wb") as f:
                f.write(r.content)
            num += 1

def commandFeed(driver):
    post_list = []
    data_tuples = []
    # Process Posts while scrolling
    last_height = scope.getScroll(driver)
    while True:
        new_height = scope.scrollScreen(driver)
        if new_height == last_height:
            time.sleep(2)
            # Expand
            expand = utils.grabExpandButtons(driver)
            if len(expand) > 0:
                expand[0].click()
                time.sleep(10)
                # Grab Posts
                new_posts = []
                posts = utils.grabFeedPosts(driver)
                for post in posts:
                    if post not in post_list:
                        post_list.append(post)
                        new_posts.append(post)
                for post in new_posts:
                    data_tuples.append((post.get_attribute("href"), post.text))
                last_height = scope.getScroll(driver)
                continue                
            else:
                break
        last_height = new_height
    return data_tuples