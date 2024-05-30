from . import tumblr_funcs as funcs
from . import tumblr_utils as utils

from sniper import login, scope

import files, dir

dest = dir.root + "\\in"
target_file = f"{dir.root}\\target.txt"

def main(driver, command):
    targets = files.readLines(target_file)
    print(f"Sniper Engaged: {len(targets)} Targets Aquired")
    data_tuples = []
# Begin Iteration
    iter = 0
    for target in targets:
        scope.printProgress(targets, target)
        scope.driverGet(driver, target)
# Command Type
    # Look at Webpage
        if command == "check":
            wait = input("Press Enter to Continue")
            continue
# Archive and Feed
        if command in ["archive", "feed"]:
            user, tag = utils.extractUserAndTag(target)
            driver.set_window_size(1024, 1940)
            if command == "archive": # Grab Post Data from User and Tag in Archive
                data_tuples = funcs.commandArchive(driver, user, tag)
            elif command == "feed": # Grab Links from User and Tag in Feed
                data_tuples = funcs.commandFeed(driver, user, tag)
            files.write(f"{dir.root}\\{command} {user} {tag}.txt", data_tuples)
    # Get Post Data
        else:
            user, code = utils.extractUserAndCode(target)
            if not utils.detectLostPosts(driver):
                # Assign Post Features
                post = funcs.openPost(driver)
                source = utils.getSourceUser(post, user)
                type, contents = funcs.getPostContents(post)
            # Detect Lost Posts
            else:
                print(f"Lost Post: {code}")
                data_tuples.append((user, code, "False"))
                continue
# Capture Commands
        if command in ["ingest", "cap", "prev", "pic", "in"]:
            driver.set_window_size(1024, 1940)
            if command == "ingest": # Capture Post and Download Files
                caption = utils.getCaption(post)
                funcs.downloadContents(contents, f"{dest}\\{type}\\{source} - {code}", caption)
                scope.captureElement(driver, f"{dest}\\preview\\{source} - {code}", post, bottom=utils.getPostEnd(post))
            elif command == "cap": # Capture Post Image
                scope.captureElement(driver, f"{dest}\\preview\\{source} - {code}", post, bottom=utils.getPostEnd(post))
                # If gif, assemble
                if type == "gif":
                    funcs.assemblePost(driver, f"{dest}\\il\\{source} - {code}", post, contents, fitBool=True)
            elif command == "prev": # Capture Post Preview (No Scrolling)
                scope.captureElement(driver, f"{dest}\\preview\\{source} - {code}", post, bottom=min(utils.getPostEnd(post), 1939))
            elif command == "pic": # Download Post Images
                caption = utils.getCaption(post)
                funcs.downloadContents(contents, f"{dest}\\{type}\\{source} - {code}", caption)
            elif command == "in": # Assemble Post Image From Components
                funcs.assemblePost(driver, f"{dest}\\il\\{source} - {code}", post, contents, fitBool=False)
# Data Commands
        elif command in ["data", "source", "text", "reblog", "test", "link", "url"]:
            driver.set_window_size(1024, 1024)
            if command == "data":
                tags = utils.getTags(post)
                text = utils.getText(post, allBool=False)
                source_url = funcs.getSourceURL(driver, post, source)
                source_code = utils.extractSourceCode(source_url)
                data_tuples.append((user, code, type, source, source_code, source_url, tags, text))
            elif command == "source": # Grab Post Source Code
                source_url = funcs.getSourceURL(driver, post, source)
                source_code = utils.extractSourceCode(source_url)
                data_tuples.append((user, code, source, source_code, source_url))
            elif command == "text": # Grab Post Text
                text = utils.getText(post, allBool=True)
                data_tuples.append((user, code, text))
            elif command == "reblog": # Count Reblogs
                comms = utils.grabReblogs(post)
                data_tuples.append((user, code, type, str(len(comms))))
            elif command == "test": # Detect Lost Posts
                data_tuples.append((user, code, "True"))
            elif command == "link": # Grab Links from Post Text
                data_tuples = funcs.commandLink(post)
            elif command == "url": # Grab Blog-First URL
                url = funcs.commandURL(driver, post)
                data_tuples.append((user, code, url))
        # Write Data
            files.write(f"{dir.root}\\{command}.txt", data_tuples)

    # Reload Driver
        iter += 1
        if iter > 100:
            iter = 0
            driver.quit()
            driver = login.reload()
