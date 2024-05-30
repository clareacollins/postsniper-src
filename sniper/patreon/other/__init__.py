import time, re

from sniper import scope
import dir

dest = dir.root + "\\in"

def main(driver, targets, sysargv):
    # Begin Iteration
    for target in targets:
        print(f"{targets.index(target)+1}/{len(targets)}")
        # Open URL
        try:
            driver.get(target)
            time.sleep(5)
        except:
            print(f"Error: {target}")
            continue
    # Look at Webpage
        if sysargv == "check":
            wait = input("Press Enter to Continue")
        filename = re.sub('http(s)?://', '', target)
        filename = re.sub('/|\?', '_', filename)
        print(filename)
        scope.captureElement(driver, f"{dest}\\{filename}", cookies=300, banner=300)
