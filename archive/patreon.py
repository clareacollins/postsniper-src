from selenium.webdriver.common.by import By

import files, login, dir

import time

def getScroll(driver):
    return driver.execute_script("return document.body.scrollHeight;")

def main(driver):
    login.patreonLogin(driver)
    post_list = []
    # Grab Dates
    user = ''
    driver.get(f"https://www.patreon.com/{user}/posts")
    time.sleep(5)
    wait = input("Press Enter to Continue")
    # Filter in Web Browser
    add_text = ""
    # Scroll down until you can't anymore
    last_height = getScroll(driver)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = getScroll(driver)
        if new_height == last_height:
            time.sleep(2)
            expand = driver.find_elements(By.CSS_SELECTOR, "button.fofpnM")
            if len(expand) > 0:
                print([x.text for x in expand])
                expand[0].click()
                time.sleep(10)
                # Grab Posts
                new_posts = []
                posts = driver.find_elements(By.CSS_SELECTOR, "ul li p a.doifNG")
                for post in posts:
                    if post not in post_list:
                        post_list.append(post)
                        new_posts.append(post)
                for post in new_posts:
                    add_text += post.get_attribute("href") + "@" + post.text + "\n"
                files.write(f"{dir.root}\\in\\Patreon.txt", add_text)
                print(len(post_list))
                last_height = getScroll(driver)
                continue
            else:
                break
        last_height = new_height