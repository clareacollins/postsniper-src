from selenium.webdriver.common.by import By

import files, login, dir

import time

def getScroll(driver):
    return driver.execute_script("return document.body.scrollHeight;")

def main(driver):
    login.tumblrLogin(driver)
    url_tags = []
    tuples = [
    # ('user', 'tag'),
    ]
    for user, tag in tuples:
        code_list = []
        # Grab Dates
        if tag == None:
            driver.get(f"https://{user}.tumblr.com/archive")
        else:
            driver.get(f"https://{user}.tumblr.com/archive/tagged/{tag}")
        time.sleep(2)
        # Scroll down until you can't anymore
        last_height = getScroll(driver)
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = getScroll(driver)
            if new_height == last_height:
                break
            last_height = new_height
        # print("Scrolled to Bottom")

        for month in driver.find_elements(By.CSS_SELECTOR, "div.hSoZ1"):
            for post in month.find_elements(By.CSS_SELECTOR, "div.NGc5k"):
                code = post.get_attribute("data-login-wall-post-id")
                if code not in code_list:
                    code_list.append(code)
                link = post.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                tags = post.find_elements(By.CSS_SELECTOR, "div.d1luu")
                tags_text = "" if len(tags) == 0 else tags[0].get_attribute("innerHTML")
                type = post.find_elements(By.CSS_SELECTOR, "div.valeh figure img")
                text = post.find_elements(By.CSS_SELECTOR, "div.valeh div.k31gt")
                if len(type) > 0:
                    type = "img"
                else:
                    type = "text"
                if len(text) > 0:
                    text = text[0].text
                else:
                    text = ""
                url_tags.append((link, user, code, tags_text, type, text))
        print(len(code_list))
    files.write(f"{dir.root}\\Archive {user} {tag}.txt", url_tags)