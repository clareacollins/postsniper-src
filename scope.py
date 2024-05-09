from selenium.webdriver import ActionChains

from PIL import Image
from io import BytesIO
import urllib.request
import time, re

# UTILITIES
def getHeight(driver, cookies=0, banner=0):
    return driver.execute_script("return window.innerHeight") - cookies - banner

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

def grabSrc(element, size):
    srcset = element.get_attribute("srcset").split(", ")
    src = srcset[-1]
    if size != "MAX":
        for src_text in srcset:
            if size in src_text:
                src = src_text
    src = re.sub(' [\d]+w', '', src)
    return src

# DOWNLOAD FUNCTIONS
def downloadContents(contents, filename, caption=None):
    num = 1
    for tuple in contents:
        for el in tuple[0]:
            if el == tuple[0][-1] and caption != None:
                new_filename = f"{filename} - {num} {caption}.{tuple[1]}"
            else:
                new_filename = f"{filename} - {num}.{tuple[1]}"
            src = grabSrc(el, "MAX")
            try:
                urllib.request.urlretrieve(src, new_filename)
            except:
                print(f"Failed to Download {src}")
            num += 1

# CAPTURE FUNCTIONS
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
    image.save(f"{dest}Temp0.png")
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
        # new_img.save(f"{dest}Temp1.png")
        new_img = new_img.crop((0, banner, image.width, new_img.height - cookies))
        # At end of page, crop out duplicate parts of screen
        if scroll_length != getHeight(driver, cookies, banner):
            new_img = new_img.crop((0, getHeight(driver, cookies, banner) - scroll_length, new_img.width, new_img.height))
        # new_img.save(f"{dest}Temp1crop.png")
        # wait = input("Press Enter to Continue")
        combine(f"{dest}Temp", new_img)
    image_final = Image.open(f"{dest}Temp.png")
    if element != None:
        image_final = image_final.crop((coords["left"], coords["top"], coords["right"], coords["bottom"]))
    image_final.save(f"{filename}.png")
    image_final.close()
