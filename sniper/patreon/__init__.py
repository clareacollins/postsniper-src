from sniper.patreon import patreon_funcs as funcs
from sniper.patreon import patreon_utils as utils

from sniper import scope, dir

def main(driver, command):
    targets = scope.readLines(dir.target)
    print(f"Sniper Engaged: {len(targets)} Targets Aquired")
    # Extract User from Target URL
    if "/posts" in targets[0]:
        user = utils.extractUser(targets[0])
    else:
        user = input("Enter User: ")
    print(f"User: {user}")
    data_tuples = []
# Begin Iteration
    for target in targets:
        scope.printProgress(targets, target)
        code = utils.extractCode(target)
        # Open URL
        scope.driverGet(driver, target, sleep=5)
# Command Types
    # Capture Commands
        if command in ["ingest", "cap", "prev", "pic"]:
            post = utils.grabPost(driver)
            driver.set_window_size(1024, 1940)
            if command == "ingest":
                scope.captureElement(driver, f"{dir.post}\\{user} - {code}", element=post, bottom=utils.getPostEnd(post))
                images = utils.grabImages(post)
                funcs.downloadImages(driver, images, f"{dir.img}\\{user} - {code}")
            elif command == "cap":
                scope.captureElement(driver, f"{dir.post}\\{user} - {code}", element=post, bottom=utils.getPostEnd(post))
            elif command == "prev":
                scope.captureElement(driver, f"{dir.post}\\{user} - {code}", element=post, bottom=min(utils.getPostEnd(post), 1939))
            elif command == "pic":
                images = utils.grabImages(post)
                funcs.downloadImages(driver, images, f"{dir.img}\\{user} - {code}")
    # Data Commands
        elif command in ["data", "text"]:
            post = utils.grabPost(driver)
            if command == "data":
                title = utils.getPostTitle(post)
                text = utils.getPostText(post)
                tags = utils.getPostTags(post)
                data_tuples.append((target, title, text, tags))
            elif command == "text":
                text = utils.getPostText(post)
                data_tuples.append((target, text))
            scope.write(f"{dir.root}\\patreon {command}.txt", data_tuples)
    # Archive Commands
        elif command == "feed":
            driver.set_window_size(1024, 1940)
            
            wait = input("Choose your Feed Settings in the driver and Press Enter to Continue")
            print("Processing Feed...")
            data_tuples = funcs.commandFeed(driver)
            scope.write(f"{dir.root}\\{command} {user}.txt", data_tuples)