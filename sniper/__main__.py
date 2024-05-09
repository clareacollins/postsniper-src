from selenium import webdriver

import sys
import files, dir
import tumblr, patreon, other

dest = dir.root + "\\in"
target_file = dir.root + "\\target1.txt"

if __name__ == "__main__":
# Establish Driver
    driver = webdriver.Chrome()
    driver.set_window_size(1024, 1940)
# Grab Targets from File
    targets = files.readLines(target_file)
    print(f"Sniper Engaged: {len(targets)} Targets Aquired")
    if sys.argv[1] == "tumblr":
        tumblr.main(driver, targets, sys.argv[2])
    elif sys.argv[1] == "patreon":
        patreon.main(driver, targets)
    elif sys.argv[1] == "other":
        other.main(driver, targets, sys.argv[2])
    driver.quit()
    print("Misson Complete")
    