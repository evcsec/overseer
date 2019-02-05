import os,time
import selenium as se
from selenium import webdriver
# import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageChops
from .logger import write_log

def detect_visual_changes(host, target_url):
    website_screenshot(host, target_url)

    if os.path.isfile("log/scan/prev_" + host + ".png"):
        check_filesize_changes(host, "log/scan/new_" + host + ".JPEG", "log/scan/prev_" + host + ".JPEG")
        image_diff("log/scan/new_" + host + ".png", "log/scan/prev_" + host + ".png", "log/scan/diff_" + host + ".png")

    # Move new to old
    os.remove("log/scan/prev_" + host + ".png")
    os.remove("log/scan/new_" + host + ".JPEG")
    os.remove("log/scan/prev_" + host + ".JPEG")
    os.rename("log/scan/new_" + host + ".png", "log/scan/prev_" + host + ".png")


def website_screenshot(host, target_url):
    # Super unreliable at the moment
    try:
        driver = webdriver.Firefox(executable_path='geckodriver')
        time.sleep(9)
        print("get: " + target_url)
        driver.get(target_url)
        time.sleep(10)
        driver.save_screenshot()
        driver.get_screenshot_as_png()
        driver.quit()
    except TimeoutException as e:
        print("[-] Error: Page load Timeout Occured.")
        write_log(host, "Error", "Page load Timeout Occured")
        driver.quit()

    image = Image.open(BytesIO(png))
    image.save("log/scan/new_" + host + ".png", "JPEG", optimize=True, quality=95)

    
def check_filesize_changes(host, new_image, previous_image):
    new = os.stat(new_image).st_size()
    old = os.stat(previous_image).st_size()

    if new != old:
        print("[-] Error: Visible website difference detected for " + host + "!")
        write_log(host, "Error", "Difference in JPEG Comparison")
    else:
        print('[-] Error: No visible changes, based on filesize of JPEG for ' + host + "!")
        

def image_diff(new_image, previous_image, diff_image):
    im1 = Image.open(new_image)
    im2 = Image.open(previous_image)

    # Difference calculated here
    diff = ImageChops.difference(im1, im2)

    #Method to check if there is no difference
    if diff.getbbox() is None:
        print("[+] Image Diff Completed for " + host + ". No visual difference in the images.")
        return
    else:
        print("[-] Error: Visual difference detected in " + host)
        write_log(host, "Error", "Visual difference in website detected!")
        diff.save(diff_image) 
