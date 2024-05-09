from sniper import utils

from selenium import webdriver
from selenium.webdriver.common.by import By

import time, re
import scope, files, login, dir

dest = dir.root + "\\in"

def loadDriver(driver):
    driver = webdriver.Chrome()
    login.tumblrLogin(driver)
    driver.set_window_size(1024, 1940)

def main(driver, targets, sysargv):
    login.tumblrLogin(driver)
    data_tuples = []
# Begin Iteration
    iter = 0
    for target in targets:
        print(f"{targets.index(target)+1}/{len(targets)}")
        # Open URL
        driver.get(target)
        time.sleep(2)
    # Look at Webpage
        if sysargv == "check":
            wait = input("Press Enter to Continue")
        else:
        # Get User and Code from Target URL
            user, code = files.extractUserAndCode(target)
            # Detect Lost Posts
            if utils.detectLostPosts(driver) or driver.current_url == "https://www.tumblr.com/explore/trending":
                print(f"Lost Post: {code}")
                data_tuples.append((user, code, "False"))
                continue
            else:
                # Open Post Features
                post, notes = utils.openPost(driver)
                # Get Source
                source = post.find_elements(By.CSS_SELECTOR, "div.sqHC2")[0].text if len(post.find_elements(By.CSS_SELECTOR, "div.sqHC2")) != 0 else user
                # Get Type and Contents
                type, contents = utils.detectPostType(post)

        # Detect Post Type
            if sysargv == "ingest": # Perform all operations and return all data
                scope.downloadContents(contents, f"{dest}\\{type}\\{source} - {code}")
                scope.captureElement(driver, f"{dest}\\preview\\{source} - {code}", post, bottom=notes.location["y"])
                text = utils.grabPostText(post, allBool=False)
                source_code = utils.grabSourceCode(driver, post, source)
                # Write Data
                data_tuples.append((user, code, source, source_code, type, text))
                files.write(f"{dir}\\ingestion.txt", data_tuples)                
            elif sysargv == "cap":
                # Download Contents
                try:
                    caption = re.sub("<|>|@|\:|\n|\?|\/|\~|\*", "", utils.grabPostText(post)[:150]).strip()
                    # print(caption)
                    scope.downloadContents(contents, f"{dest}\\{type}\\{source} - {code}", caption)
                except:
                    caption = None
                    scope.downloadContents(contents, f"{dest}\\{type}\\{source} - {code}", caption)
                # scope.downloadContents(contents, f"{dest}\\{type}\\{source} [{user}]- {code}")
                # scope.captureElement(driver, f"{dest}\\preview\\{source} - {code}", post, bottom=notes.location["y"])
                if type == 'gif':
                    utils.assemblePost(driver, f"{dest}\\il\\{source} - {code}", post)
                else:
                    # Capture Post
                    scope.captureElement(driver, f"{dest}\\preview\\{source} - {code}", post, bottom=notes.location["y"])
            elif sysargv == "prev":
                #scope.captureElement(driver, f"{dest}\\preview\\{source} - {code}", post, bottom=min(notes.location["y"], 1939))
                scope.captureElement(driver, f"{dest}\\preview\\{source} - {code}", post, bottom=notes.location["y"])
            elif sysargv == "in":
                utils.assemblePost(driver, f"{dest}\\il\\{source} - {code}", post, fitBool=False)
            elif sysargv == "source":
                source_code = utils.grabSourceCode(driver, post, source)
                data_tuples.append((user, code, source, source_code))
                files.write(f"{dir}\\source.txt", data_tuples)
            elif sysargv == "text":
                data_tuples.append((user, code, utils.grabPostText(post)))
                # data_tuples.append((user, code, utils.grabPostText(post, delimiter="|", allBool=True)))
                files.write(f"{dir}\\postText.txt", data_tuples)
            elif sysargv == "reblog":
                comms = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.u2tXn")
                data_tuples.append((user, code, type, str(len(comms))))
                files.write(f"{dir}\\reblog.txt", data_tuples)
            elif sysargv == "test": # Tests if post is lost
                data_tuples.append((user, code, "True"))
                files.write(f"{dir}\\test.txt", data_tuples)
            elif sysargv == "link":
                # scope.captureElement(driver, f"{dest}\\link\\{source} - {code}.png", post, bottom=notes.location["y"])
                links = post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 div.k31gt a")
                links.extend(post.find_elements(By.CSS_SELECTOR, "div.VDRZ4 li.k31gt a"))
                int = 1
                working_links = []
                for el in links:
                    new_url = el.get_attribute('href')
                    print(new_url)
                    data_tuples.append((new_url, el.text))
                files.write(f"{dir}\\links.txt", data_tuples)
            elif sysargv == "url":
                post.find_element(By.CSS_SELECTOR, "div.KFWnx").click()
                time.sleep(.5)
                # wait = input("Press Enter to Continue")
                source_code = driver.find_elements(By.CSS_SELECTOR, "div.iaJAj a")[0].get_attribute("href")
                data_tuples.append((user, code, source_code))
                files.write(f"{dir}\\blog.txt", data_tuples)
                
        iter += 1
        if iter > 100:
            iter = 0
            print("Reloading Driver")
            driver.quit()
            time.sleep(5)
            loadDriver()
    