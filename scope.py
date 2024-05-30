from selenium.webdriver import ActionChains

from PIL import Image
from io import BytesIO
import urllib.request
import time, re

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

### DRIVER FUNCTIONS ###
# Handle Errors and Invalid URLs
def driverGet(driver, target, sleep=2):
    if driver.current_url != target and not '\t' in target:
        try:
            driver.get(target)
        except:
            print(f"Error: Unable to get {target}")
    time.sleep(sleep)

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
# Get Image Source Link
def getSrc(element, MaxBool=False):
    srcset = [img.split(" ") for img in element.get_attribute("srcset").split(", ")]
    if MaxBool:
        src = srcset[-1][0]
    else:
        for tup in srcset:
            if tup[1] == "540w"  or tup[1] == "500w":
                src = tup[0]
    return src

### DOWNLOAD FUNCTIONS ###
def downloadFile(src, filename):
    try:
        urllib.request.urlretrieve(src, filename)
    except:
        print(f"Failed to Download {src}")

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
    dest = REDACTED
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
