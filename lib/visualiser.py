from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageChops
from .logger import write_log
from .alerts import send_slack_message, send_email
import os
import time
import selenium as se


def detect_visual_changes(system_config, host, target_url):
    website_screenshot(system_config, host, target_url)

    if os.path.isfile("log/" + host + "/scans/prev_" + host +
                      ".png") and os.path.isfile("log/" + host +
                                                 "/scans/prev_" + host +
                                                 ".jpg"):
        check_filesize_changes(system_config, host, "log/" + host +
                               "/scans/new_" + host + ".jpg", "log/" + host +
                               "/scans/prev_" + host + ".jpg")
        image_diff(system_config, host, "log/" + host + "/scans/new_" +
                   host + ".png", "log/" + host + "/scans/prev_" + host +
                   ".png", "log/" + host + "/scans/diff_" + host + ".png")
    else:
        print("[-] Error: No previous image does not exist")

    # Move new to old
    if os.path.exists("log/" + host + "/scans/prev_" + host + ".png"):
        os.remove("log/" + host + "/scans/prev_" + host + ".png")
    if os.path.exists("log/" + host + "/scans/prev_" + host + ".jpg"):
        os.remove("log/" + host + "/scans/prev_" + host + ".jpg")
    if os.path.exists("log/" + host + "/scans/new_" + host + ".jpg"):
        os.rename("log/" + host + "/scans/new_" + host + ".jpg", "log/" +
                  host + "/scans/prev_" + host + ".jpg")
    if os.path.exists("log/" + host + "/scans/new_" + host + ".png"):
        os.rename("log/" + host + "/scans/new_" + host + ".png", "log/" +
                  host + "/scans/prev_" + host + ".png")


def website_screenshot(system_config, host, target_url):
    try:
        driver_type = system_config.systemconfig.get('Visual', 'driver_type')
        driver_location = system_config.systemconfig.get('Visual',
                                                         'driver_location')
        if driver_type == "chrome":
            driver_options = webdriver.ChromeOptions()
            driver_options.add_argument('headless')
            driver = webdriver.Chrome(executable_path=driver_location, options=driver_options)
        elif driver_type == "gecko":
            driver = webdriver.Firefox(executable_path=driver_location)
        driver.set_window_size(1024, 768)

        driver.set_page_load_timeout(10)
        try:
            driver.get(target_url)
            print("[+] URL successfully Accessed")
            screenshot = driver.save_screenshot("log/" + host +
                                                "/scans/new_" + host + ".png")
            png = driver.get_screenshot_as_png()
        except TimeoutException as e:
            print("[-] Error: Page load Timeout occured. Quiting!")
            driver.close()
            driver.quit()

    except TimeoutException as e:
        print("[-] Error: Page load Timeout Occured.")
        write_log(host, "Error", "Page load Timeout Occured")
        driver.close()
        driver.quit()

    image = Image.open(BytesIO(png))
    fill_color = '#fff'  # your background
    if image.mode in ('RGBA', 'LA'):
        background = Image.new(image.mode[:-1], image.size, fill_color)
        background.paste(image, image.split()[-1])
        image = background
    image.save("log/" + host + "/scans/new_" + host + ".jpg", "JPEG",
               optimize=True, quality=95)
    driver.close()
    driver.quit()


def check_filesize_changes(system_config, host, new_image, previous_image):
    latest = os.stat(new_image).st_size
    prev = os.stat(previous_image).st_size

    print(latest)
    print(prev)
    if latest != prev:
        error_message = "[-] Error: Visible website difference detected for " + host + "!"
        print(error_message)
        write_log(host, "Error", "Difference in JPEG Comparison")
        send_slack_message(system_config, error_message)
        send_email(system_config, error_message)
    else:
        print("[+] No visible changes, based on filesize of jpg for " +
              host + "!")


def image_diff(system_config, host, new_image, previous_image, diff_image):
    im1 = Image.open(new_image)
    im2 = Image.open(previous_image)

    # Difference calculated here
    diff = ImageChops.difference(im1, im2)

    # Method to check if there is no difference
    if diff.getbbox() is None:
        print("[+] Image Diff Completed for " + host +
              ". No visual difference in the images.")
        return
    else:
        error_message = "[-] Error: Visual difference detected in " + host
        print(error_message)
        write_log(host, "Error", "Visual difference in website detected!")
        send_slack_message(system_config, error_message)
        send_email(system_config, error_message)
        diff.save(diff_image)
