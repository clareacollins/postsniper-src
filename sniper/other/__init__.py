import time, re

from sniper import scope, dir

def main(driver, targets, command):
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
        filename = re.sub('http(s)?://', '', target)
        filename = re.sub('/|\?', '_', filename)
        print(filename)
        scope.captureElement(driver, f"{dir.post}\\{filename}", cookies=300, banner=300)