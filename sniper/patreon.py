from selenium.webdriver.common.by import By
import time, re
import files, scope, dir
import requests

def main(driver, targets):
    user = ''
    data_tuples = []
# Begin Iteration
    for target in targets:
        print(f"{targets.index(target)+1}/{len(targets)}")
        code = target.split("/")[-1].split("-")[-1]
        post_dir = f"{dir.root}\\in\\preview\\"
        img_dir = f"{dir.root}\\in\\img\\"
        # Open URL
        driver.get(target)
        time.sleep(5)
        # Capture Post
        post = driver.find_element(By.CSS_SELECTOR, "div.hVDa-Dc")
        end = post.find_element(By.CSS_SELECTOR, "div.julawU")
        scope.captureElement(driver, f"{post_dir}{user} - {code}", element=post, bottom=end.location["y"])
        # Data
        # wait = input("Press Enter to Continue")
        title = post.find_element(By.CSS_SELECTOR, "span.eGFfXM").text
        # title = post.find_element(By.CSS_SELECTOR, "span.hxhWXn").text
        text = post.find_element(By.CSS_SELECTOR, "div.kJujbw").text
        tags = post.find_elements(By.CSS_SELECTOR, "p.lbLzWd")
        tags = [x.text for x in tags]
        data_tuples.append((target, title, re.sub("\n|@", "|", text), ", ".join(tags)))
        files.write(f"{dir.root}\\patreon.txt", data_tuples) 
        # Download Contents
        srcs = []
        count = 1
        for el in post.find_elements(By.CSS_SELECTOR, "img"):
            try:
                el.click()
                time.sleep(2)
                lightbox = driver.find_element(By.CSS_SELECTOR, "div.hFYGny img")
                src = lightbox.get_attribute("src")
            except:
                src = el.get_attribute("src")
            srcs.append(src)
            if src != "https://":
                r = requests.get(src)
                with open(f"{img_dir}{user} - {code} - {count}.png", "wb") as f:
                    f.write(r.content)
                count += 1