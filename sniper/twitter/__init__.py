from sniper.twitter import twitter_funcs as funcs
from sniper.twitter import twitter_utils as utils

from sniper import scope, dir

def main(driver, command):
    targets = scope.readLines(dir.target)
    print(f"Sniper Engaged: {len(targets)} Targets Aquired")
    data_tuples = []
# Begin Iteration
    for target in targets:
        user = utils.extractUser(target)
        code = utils.extractCode(target)
        scope.printProgress(targets, target)
        # Open URL
        scope.driverGet(driver, target, sleep=5)
# Command Types
    # Capture Commands
        if command in ["ingest", "cap", "prev", "pic"]:
            post = utils.getPost(driver)
            driver.set_window_size(1024, 1940)
            if command == "ingest":
                scope.captureElement(driver, f"{dir.post}\\{user} - x{code}", element=post, bottom=utils.getPostEnd(post))
                images = utils.getPostImages(post)
                funcs.downloadImages(images, f"{dir.img}\\{user} - x{code}")
            elif command == "cap":
                scope.captureElement(driver, f"{dir.post}\\{user} - x{code}", element=post, bottom=utils.getPostEnd(post))
            elif command == "prev":
                scope.captureElement(driver, f"{dir.post}\\{user} - x{code}", element=post, bottom=min(utils.getPostEnd(post), 1939))
            elif command == "pic":
                images = utils.getPostImages(post)
                funcs.downloadImages(images, f"{dir.img}\\{user} - x{code}")
    # Archive Commands
        elif command in ['media']:
            scope.driverGet(driver, f"https://twitter.com/{user}/media", sleep=5)
            data_tuples = funcs.commandMedia(driver)
            scope.write(f"{dir.root}\\{command} {user}.txt", data_tuples)
    # Data Commands
        elif command in ["data", "text"]:
            post = utils.getPost(driver)
            if command == "data":
                username = utils.getUserName(post)
                text = utils.getPostText(post)
                date = utils.getPostDate(post)
                data_tuples.append((target, username, text, date))
            elif command == "text":
                text = utils.getPostText(post)
                data_tuples.append((target, text))
            scope.write(f"{dir.root}\\twitter {command}.txt", data_tuples)