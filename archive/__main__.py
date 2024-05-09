from selenium import webdriver
import sys
import tumblr, patreon

if __name__ == "__main__":
    driver = webdriver.Chrome()
    if sys.argv[1] == "tumblr":
        tumblr.main(driver)
    elif sys.argv[1] == "patreon":
        patreon.main(driver)
    driver.quit()
    print("Archive Complete")