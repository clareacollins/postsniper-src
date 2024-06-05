from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from sniper import login, scope, dir

from sniper import tumblr, patreon, twitter, other

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')

if __name__ == "__main__":
    print("Welcome to the main Sniper Shell!")
    print("Please wait while the driver is established...")
# Establish Driver
    driver = webdriver.Chrome(options=chrome_options)
    print("Driver Established")
    print("Enter a Platform:\n-> tumblr\n-> patreon\n-> twitter\n-> other")
    while True:
        platform = input("> ")
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
            # login.tumblrLogin(driver)
            # login.patreonLogin(driver)
            # login.twitterLogin(driver)
            while True:
                command = input("test> ")
                if command == "exit":
                    print("Exiting Test Shell")
                    break
                elif command == "help":
                    print("Commands:" + \
                        "\n\thelp - display this message" + \
                        "\n\texit - exit the test shell")
                elif " --" in command:
                    element, action, count = command.split(" --")
                    if action == "click":
                        try:
                            driver.find_elements(By.CSS_SELECTOR, element)[int(count)].click()
                        except:
                            print("Error Clicking Element")
                    elif action == "text":
                        try:
                            print(driver.find_elements(By.CSS_SELECTOR, element)[int(count)].text)
                        except:
                            print("Error Extracting Text")
                    elif action == "src":
                        try:
                            print(driver.find_elements(By.CSS_SELECTOR, element)[int(count)].get_attribute("src"))
                        except:
                            print("Error Grabbing Element SRC")
                else:
                    els = driver.find_elements(By.CSS_SELECTOR, command)
                    print(len(els))
                    for el in els:
                        print(el.get_attribute("class"))
                        try:
                            scope.captureElement(driver, f"{dir.root}\\in\\preview\\test - {command} {els.index(el)}", element=el)
                        except:
                            print("Error Capturing Element")
                            break
        else:
            print("Invalid Platform. Please try again or type 'exit' to exit the Sniper Shell.")
    
    print("Exiting the Sniper Shell")
    driver.quit()
    print("Misson Complete")
    