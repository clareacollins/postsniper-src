from sniper.patreon import patreon_funcs as funcs
from sniper.patreon import patreon_utils as utils

from sniper import scope, dir

def main(driver, command):
    targets = scope.readLines(dir.target)
    print(f"Sniper Engaged: {len(targets)} Targets Aquired")
    data_tuples = []
# Begin Iteration
    for target in targets:
        scope.printProgress(targets, target)
        # Open URL
        scope.driverGet(driver, target, sleep=5)
        user = utils.extractUser(target, driver)
        code = utils.extractCode(target)
# Command Types
    # Capture Commands
        if command in ["ingest", "cap", "prev", "pic"]:
            post = utils.grabPost(driver)
            driver.set_window_size(1024, 1940)
            if command == "ingest":
                scope.captureElement(driver, f"{dir.post}\\{user} - {code}", element=post, bottom=utils.getPostEnd(post))
                scope.downloadImages(utils.grabImages(post), f"{dir.img}\\{user} - {code}", utils.getSrc, scope.downloadRequests, driver)
            elif command == "cap":
                scope.captureElement(driver, f"{dir.post}\\{user} - {code}", element=post, bottom=utils.getPostEnd(post))
            elif command == "prev":
                scope.captureElement(driver, f"{dir.post}\\{user} - {code}", element=post, bottom=min(utils.getPostEnd(post), 1939))
            elif command == "pic":
                scope.downloadImages(utils.grabImages(post), f"{dir.img}\\{user} - {code}", utils.getSrc, scope.downloadRequests, driver)
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
        elif "feed" in command:
            scope.driverGet(driver, f"https://www.patreon.com/{user}/posts", sleep=5)
            driver.set_window_size(1024, 1940)
            defaults = utils.extractDefault(command)
            data_tuples, filter_str = funcs.commandFeed(driver, defaults)
            scope.write(f"{dir.root}\\feed {user} {filter_str}.txt", data_tuples)