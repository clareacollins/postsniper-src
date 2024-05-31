from sniper.twitter import twitter_utils as utils

from sniper import scope

import time


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