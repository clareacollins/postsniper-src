from sniper import scope, dir
from sniper.tumblr import tumblr_utils as utils

import urllib.request

# Open Post
def openPost(driver):
    # Grab Post
    post = utils.grabPost(driver)
    utils.clickReadMore(post)
    utils.clickSeeAll(post)
    # Scroll to Top
    driver.execute_script(f"window.scrollTo(0, 0);")
    return post

# Grab Post Content Files
def getPostContents(post):
    images, gifs = utils.getImages(post)
    videos = utils.grabVideos(post)
    audio = utils.grabAudio(post)
    contents = [(images, "png"), (gifs, "gif"), (videos, "mp4"), (audio, "mp3")]
    # Determine Type
    if len(audio) > 0:
        return "audio", contents
    elif len(videos) > 0:
        return "video", contents
    elif len(gifs) > 0:
        return "gif", contents
    elif len(images) > 0:
        return "img", contents
    else:
        return "text", contents

def getSourceURL(driver, post, source):
    try:
        utils.clickOptions(post)
        source_link = utils.getURL(driver)
        if source not in source_link:
            source_link = "Error"
        return source_link
    except:
        return "None"

def downloadContents(contents, filename, caption=None):
    num = 1
    for tuple in contents:
        for el in tuple[0]:
            if el == tuple[0][-1] and caption != None:
                new_filename = f"{filename} - {num} {caption}.{tuple[1]}"
            else:
                new_filename = f"{filename} - {num}.{tuple[1]}"
            src = utils.getSrc(el, MaxBool=True)
            scope.downloadUrllib(src, new_filename)
            num += 1


# Assemble Post
def assemblePost(driver, filename, post, contents, fitBool=False):
    dest = f'{dir.root}\\extract\\temp\\'
    images = contents[0][0]
# Handle No Images
    if len(images) == 0:
        scope.captureElement(driver, filename, post, bottom=utils.getPostEnd(post))
        return TypeError
# Generate Image Element Location Tuples
    img_tuples = []
    for image in images:
        src = scope.getSrc(image, fitBool)
        # [0] element, [1] link, [2] top coord, [3] bottom coord
        img_tuples.append((image, src, image.location["y"], image.location["y"] + image.size["height"]))
# Screenshot from Top of Post to Top of First Image
    capture = scope.captureElement(driver, filename, post, bottom=img_tuples[0][2])
# Add Image
    for image_tup in img_tuples:
        # Download Image, add to Capture
        urllib.request.urlretrieve(image_tup[1], f"{dest}Temp - 1.png")
        scope.combine(filename, f"{dest}Temp - 1.png", fitBool=fitBool)
    # Between Images (and not after the last image)
        if image_tup != img_tuples[-1] and img_tuples[img_tuples.index(image_tup) + 1][2] - image_tup[3] > 20:
            driver.execute_script(f"window.scrollTo(0, 0);")
            scope.captureElement(driver, f"{dest}Temp - 1", post,
                                             top=image_tup[3], 
                                             bottom=img_tuples[img_tuples.index(image_tup) + 1][2])
            scope.combine(filename, f"{dest}Temp - 1.png")
            # Screenshot from Bottom of Last Image to Top of Notes (Post Footer)
    driver.execute_script(f"window.scrollTo(0, 0);")
    scope.captureElement(driver, f"{dest}Temp - 1", post, 
                                               top=img_tuples[-1][3],
                                               bottom=utils.getPostEnd(post))
    scope.combine(filename, f"{dest}Temp - 1.png")

def commandLink(post):
    tuples = []
    links = utils.grabLinks(post)
    for el in links:
        new_url = el.get_attribute('href')
        tuples.append((new_url, scope.cleanText(el.text)))
    return tuples

def commandURL(driver, post):
    utils.clickURL(post)
    source_code = utils.getURL(driver)
    return source_code

def commandArchive(driver, user, tag=None):
    #  Pass Users and tags from File
    url_tags = []
    code_list = []
    # Grab Dates
    utils.driverGetArchive(driver, user, tag)
    # Scroll down until you can't anymore
    scope.scrollToBottom(driver)
    # Process Posts
    for month in utils.grabArchiveMonths(driver):
        for post in utils.grabArchivePosts(month):
            code = post.get_attribute("data-login-wall-post-id")
            if code not in code_list:
                code_list.append(code)
            link = utils.getArchiveLink(post)
            tags = utils.getArchiveTags(post)
            type = getPostContents(post)[0]
            text = utils.getText(post, allBool=True)
            url_tags.append((link, user, code, tags, type, text))
    # Return Data
    print(f"{user} has {len(code_list)} posts in {tag}")
    return url_tags

def commandFeed(driver, user, tag=None):
    #  Pass Users and tags from File
    url_tags = []
    code_list = []
    utils.driverGetFeed(driver, user, tag)
    # Scroll down until you can't anymore
    scope.scrollToBottom(driver)
    # Process Posts
    for post in utils.grabFeedPosts(driver):
        code = utils.getFeedCode(post)
        if code not in code_list and code != "None":
            code_list.append(code)
            url_tags.append((user, code))
    # Return Data
    print(f"{user} has {len(code_list)} posts in {tag}")
    return url_tags