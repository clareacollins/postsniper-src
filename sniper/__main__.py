from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from sniper import login, scope, dir

from sniper import tumblr, patreon, twitter, other

import sys

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')

if __name__ == "__main__":
    print("Welcome to the main Sniper Shell!")
    print("Please wait while the driver is established...")
# Establish Driver
    driver = webdriver.Chrome(options=chrome_options)
    print("Driver Established")
    while True:
        platform = scope.handlePlatform(sys.argv)
        if platform == "exit":
            break
        elif platform == "tumblr":
            print("Logging into Tumblr...")
            login.tumblrLogin(driver)
            print("Welcome to the Tumblr Shell")
            print("Commands: ingest, cap, prev, pic, in, data, source, text, reblog, test, link, url, archive, feed")
            while True:
                command = input("tumblr> ")
                if command == "exit":
                    print("Exiting the Tumblr Shell")
                    break
                elif command == "help":
                    print("Commands:" + \
                        "\n\tingest - download images and capture post" + \
                        "\n\tcap - capture entire post" + \
                        "\n\tprev - capture top of post" + \
                        "\n\tpic - download images" + \
                        "\n\tin - assemble post with images zoomed in" + \
                        "\n\tdata - get post data" + \
                        "\n\tsource - get source data" + \
                        "\n\ttext - get all text" + \
                        "\n\treblog - get count of reblogs with content" + \
                        "\n\ttest - get Bool for if post url still works" + \
                        "\n\tlink - get links in post text" + \
                        "\n\turl - get blog-first url" + \
                        "\n\tarchive - get links from users in archive" + \
                        "\n\tfeed - get links from users with no archive page" + \
                        "\n\thelp - display this message" + \
                        "\n\texit - exit the tumblr shell")
                else:
                    tumblr.main(driver, command)
        elif platform == "patreon":
            print("Logging into Patreon...")
            login.patreonLogin(driver)
            print("Welcome to the Patreon Shell")
            while True:
                command = input("patreon> ")
                if command == "exit":
                    print("Exiting Patreon Shell")
                    break
                elif command == "help":
                    print("Commands:" + \
                        "\n\tingest - download images and capture post" + \
                        "\n\tcap - capture entire post" + \
                        "\n\tprev - capture top of post" + \
                        "\n\tpic - download images" + \
                        "\n\tdata - get post data" + \
                        "\n\ttext - get all text" + \
                        "\n\tfeed - get links from users in feed" + \
                        "\n\thelp - display this message" + \
                        "\n\texit - exit the patreon shell")
                else:
                    patreon.main(driver, command)
        elif platform == "twitter":
            print("Logging into twitter...")
            login.twitterLogin(driver)
            print("Welcome to the Twitter Shell")
            while True:
                command = input("twitter> ")
                if command == "exit":
                    print("Exiting Twitter Shell")
                    break
                elif command == "help":
                    print("Commands:" + \
                        "\n\tingest - download images and capture post" + \
                        "\n\tcap - capture entire post" + \
                        "\n\tprev - capture top of post" + \
                        "\n\tpic - download images" + \
                        "\n\tdata - get post data" + \
                        "\n\ttext - get post text" + \
                        "\n\tmedia - get links from user's media" + \
                        "\n\thelp - display this message" + \
                        "\n\texit - exit the twitter shell")
                else:
                    twitter.main(driver, command)
        elif platform == "other":
            print("Welcome to the Other Shell")
            while True:
                command = input("other> ")
                if command == "exit":
                    print("Exiting Generic Shell")
                    break
                elif command == "help":
                    print("Commands:" + \
                        "\n\thelp - display this message" + \
                        "\n\texit - exit the other shell")
                else:
                    other.main(driver, command)
        elif platform == "test":
            # driver.set_window_size(1024, 1940)
            print("Welcome to the Test Shell")
            login.loginType(driver, scope.handleTest(sys.argv))
            while True:
                command = input("test> ")
                if command == "exit":
                    print("Exiting Test Shell")
                    break
                elif command == "help":
                    print("Commands:" + \
                        "\n\telement --action --count" + \
                        "\n\thelp - display this message" + \
                        "\n\texit - exit the test shell")
                elif " --" in command:
                    command_list = command.split(" --")
                    element = command_list[0]
                    action = command_list[1]
                    if len(command_list) > 2:
                        count = command_list[2]
                    else:
                        count = 0
                    try:
                        if action == "len":
                            print(len(driver.find_elements(By.CSS_SELECTOR, element)))
                        elif action == "click":
                            driver.find_elements(By.CSS_SELECTOR, element)[int(count)].click()
                        elif action == "text":
                            print(driver.find_elements(By.CSS_SELECTOR, element)[int(count)].text)
                        elif action == "enter":
                            driver.find_elements(By.CSS_SELECTOR, element)[int(count)].send_keys(Keys.RETURN)
                        elif action == "esc":
                            driver.find_elements(By.CSS_SELECTOR, element)[int(count)].send_keys(Keys.ESCAPE)
                        elif action == "src":
                            print(driver.find_elements(By.CSS_SELECTOR, element)[int(count)].get_attribute("src"))
                        elif action == "href":
                            print(driver.find_elements(By.CSS_SELECTOR, element)[int(count)].get_attribute("href"))
                        elif action == "class":
                            print(driver.find_elements(By.CSS_SELECTOR, element)[int(count)].get_attribute("class"))
                        elif action == "html":
                            print(driver.find_elements(By.CSS_SELECTOR, element)[int(count)].get_attribute("innerHTML"))
                        elif action == "cap":
                            scope.captureElement(driver, f"{dir.root}\\in\\preview\\test - {element} {count}", element=driver.find_elements(By.CSS_SELECTOR, element)[int(count)])
                    except:
                        print("Error Processing Command")
        else:
            print("Invalid Platform. Please try again or type 'exit' to exit the Sniper Shell.")
    
    print("Exiting the Sniper Shell")
    driver.quit()
    print("Misson Complete")
    