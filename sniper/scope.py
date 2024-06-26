from selenium.webdriver import ActionChains

from PIL import Image
from io import BytesIO
import urllib.request
import requests
import time, re, os

from sniper import dir

### ARGUMENT HANDLING ###
def handlePlatform(args):
    if len(args) == 1:
        print("Enter a Platform:\n-> tumblr\n-> patreon\n-> twitter\n-> other")
        return input("> ")
    elif len(args) > 1:
        return args[1]

def handleTest(args):
    if len(args) == 2:
        print("Enter a Platform:\n-> tumblr\n-> patreon\n-> twitter")
        return input("> ")
    elif len(args) == 3:
        return args[2]

### STRING PROCESSING ###
# Cleans text for entry into csv
def cleanText(text):
    new_text = re.sub(r"\n|@", " ", text)
    if new_text == None:
        new_text = ""
    return new_text
# Cleans text to be used as a filename
def cleanFilename(text):
    new_text = re.sub(r"\\|\/|\:|\*|\?|\"|\<|\>|\||\@|\n|\~", "", text)
    if new_text == None:
        new_text = ""
    return new_text

def userSelectMssg(options, keyword):
    user_mssg = f"Select {keyword}:\n"
    for count, option in options:
        user_mssg += f"[{count}] {option}\n"
    return user_mssg + "> "

### FILE FUNCTIONS ###
# Passed file title and data, writes data to file at location
def write(title, data):
    csvText = ""
    if isinstance(data, str):
        csvText = data
    else:
        for tuple in data:
            if isinstance(tuple, str):
                csvText += tuple + "\n"
            else:
                csvText += "@".join(tuple) + "\n"
    os.chdir(dir.root)
    FileObject = open(title, "w", encoding="utf-8")
    FileObject.write(csvText)
    FileObject.close()

def readLines(file_dir):
    if not os.path.exists(file_dir):
        return []
    else:
        FileObject = open(file_dir, "r")
        FileLines = FileObject.readlines()
        FileObject.close()
        return [line.strip() for line in FileLines if line.strip() != ""]

### DRIVER FUNCTIONS ###
# Handle Errors and Invalid URLs
def driverGet(driver, target, sleep=2):
    if driver.current_url != target and not '\t' in target and '/' in target:
        try:
            driver.get(target)
        except:
            print(f"Error: Unable to get {target}")
    time.sleep(sleep)

def grabElementByText(text, elements):
    for el in elements:
        if text == el.text:
            return el
    return None

### LOG ###
def printProgress(list, index):
    print(f"{list.index(index)+1}/{len(list)}")

### UTILITIES ###
# Get Scroll Height
def getScroll(driver):
    return driver.execute_script("return document.body.scrollHeight;")
# Scroll Down One Screen Length
def scrollScreen(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = getScroll(driver)
    return new_height
# Scroll to CSS Element
def scrollToElement(driver, element):
    driver.execute_script(f"window.scrollTo(0, 0);")
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(.5)
# Scroll down until you can't anymore
def scrollToBottom(driver):
    last_height = getScroll(driver)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = getScroll(driver)
        if new_height == last_height:
            break
        last_height = new_height

def whileScrolling(driver, action, sleep=2, expand=None):
    post_list = []
    returnValues = []
    last_height = getScroll(driver)
    while True:
        new_height = scrollScreen(driver)
        time.sleep(sleep)
        expandBool = False
        if expand != None and len(expand(driver)) > 0:
            expand(driver)[0].click()
            expandBool = True
            time.sleep(10)
        returnValues = newPosts(action(driver), returnValues, post_list)
        if new_height == last_height and expandBool == False:
            break
        last_height = new_height
    return returnValues

def newPosts(currentPosts, data_tuples, post_list):
    for post in currentPosts:
        if post not in post_list:
            post_list.append(post)
            data_tuples.append((post.get_attribute("href"), post.text))
    return data_tuples

# Get Window Height
def getHeight(driver, cookies=0, banner=0):
    return driver.execute_script("return window.innerHeight") - cookies - banner
# Get Element Boundaries
def getBoundaries(driver, element=None, bottom=None, top=None):
    # Coordinates of Page Element
    if element != None:
        coords = {
            'left': element.location['x'],
            'top': element.location['y'],
            'right': element.location['x'] + element.size['width'],
            'bottom': element.location['y'] + element.size['height']
        }
    # Else Coordinates of Whole Page
    else:
        coords = {
            'left': 0,
            'top': 0,
            'right': driver.execute_script("return document.body.scrollWidth"),
            'bottom': driver.execute_script("return document.body.scrollHeight")
        }
    # Override Coordinates with Passed Values
    if bottom != None:
        coords["bottom"] = bottom
    if top != None:
        coords["top"] = top
    return coords

### DOWNLOAD FUNCTIONS ###
def downloadUrllib(src, filename):
    try:
        urllib.request.urlretrieve(src, filename)
    except:
        print(f"Failed to Download {src}")

def downloadRequests(src, filename):
    try:
        r = requests.get(src)
        with open(f"{filename}.png", "wb") as f:
            f.write(r.content)
    except:
        print(f"Failed to Download {src}")

def downloadImages(images, filename, getSRC, dlType, driver=None):
    num = 1
    for image in images:
        src = getSRC(image, driver)
        if src != "https://":
            dlType(src, f"{filename} - {num}")
            num += 1

### CAPTURE FUNCTIONS ###
# Combine Screenshots
def combine(old_filename, new_filename_or_img, crop_coords=None, fitBool=False):
    # Grab Files
    old = Image.open(f"{old_filename}.png")
    # Remove Section from Old Screenshot
    old = old.crop((0, 0, old.width, old.height))# - 300))
    # If Passed the new filename, open it
    if type(new_filename_or_img) == str:
        new = Image.open(new_filename_or_img)
    # Else assign the new image
    else:
        new = new_filename_or_img
    # Crop New Screenshot
    if crop_coords != None:
        new = new.crop(crop_coords)
    if fitBool:
        new = new.resize((540, int(new.height * (540 / new.width))))
    # Concatenate Screenshots (width is largest of old and new, or standard 540)
    image = Image.new('RGB', (max(old.width, new.width, 540), old.height + new.height),color=(255,255,255))
    image.paste(old, (0, 0))
    image.paste(new, (0, old.height))
    # Save Screenshot
    image.save(f"{old_filename}.png")
    # Close Files
    old.close()
    new.close()
    image.close()

# Capture Element
def captureElement(driver, filename, element=None, bottom=None, top=None, cookies=0, banner=0):
    dest = 'C:\\TumblrSniper\\extract\\temp\\'
    # If Element is too small, add border
    coords = getBoundaries(driver, element, bottom, top)
    capture_bottom = coords["bottom"]
    screen_bottom = getHeight(driver)
    if element != None:
        screen_bottom = element.location["y"]
    # Grab Screenshot
    image = Image.open(BytesIO(driver.get_screenshot_as_png()))
    image = image.crop((0, 0, image.width, image.height - cookies))
    image.save(f"{dest}Temp.png")
# If Window isn't tall enough to capture element
    while capture_bottom > screen_bottom:# and screen_bottom < 25000:
        scroll_length = min(getHeight(driver, cookies, banner), capture_bottom - screen_bottom)
        time.sleep(1)
        # Scroll one screen length (or to the bottom of the element if it's shorter than a screen length)
        ActionChains(driver).scroll_by_amount(0, scroll_length).perform()
        time.sleep(1)
        screen_bottom = screen_bottom + getHeight(driver, cookies, banner)
        new_img = Image.open(BytesIO(driver.get_screenshot_as_png()))
        new_img = new_img.crop((0, banner, image.width, new_img.height - cookies))
        # At end of page, crop out duplicate parts of screen
        if scroll_length != getHeight(driver, cookies, banner):
            new_img = new_img.crop((0, getHeight(driver, cookies, banner) - scroll_length, new_img.width, new_img.height))
        combine(f"{dest}Temp", new_img)
    image_final = Image.open(f"{dest}Temp.png")
    if element != None:
        image_final = image_final.crop((coords["left"], coords["top"], coords["right"], coords["bottom"]))
    image_final.save(f"{filename}.png")
    image_final.close()