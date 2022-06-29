import time
from threading import Thread
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

browsers = [
    {
        "platform": "Windows 7 64-bit",
        # "browserName": "Internet Explorer",
        "browserName": "Firefox",
        "version": "10",
        "name": "Python Parallel"
    },
    {
        "platform": "Windows 8.1",
        "browserName": "Brave",
        "version": "50",
        "name": "Python Parallel"
    },
]


browsers_waiting = []


def get_browser(browser_data):
    firefox_driver_binary = "./drivers/geckodriver"
    ser_firefox = FirefoxService(firefox_driver_binary)

    brave_path = "/usr/bin/brave-browser"
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path

    if str.lower(browser_data["browserName"]) == "firefox-webdriver":
        driver = webdriver.Firefox(service=ser_firefox)
    elif str.lower(browser_data["browserName"]) == "firefox":
        dc = {
            "browserName": "firefox",
            "platformName": "LINUX"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc)

    elif str.lower(browser_data["browserName"]) == "brave":
        dc = {
            "browserName": "chrome",
            "platformName": "LINUX"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc, options=options)

    elif str.lower(browser_data["browserName"]) == "firefox-mobile":
        firefox_options = FireFoxOptions()
        firefox_options.add_argument("--width=375")
        firefox_options.add_argument("--height=812")
        firefox_options.set_preference("general.useragent.override", "userAgent=Mozilla/5.0 "
                                                                     "(iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like "
                                                                     "Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
        # firefox_options.set_preference("general.useragent.override", "Nexus 7")

        driver = webdriver.Firefox(service=ser_firefox, options=firefox_options)

    elif str.lower(browser_data["browserName"]) == "android":
        dc = {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "Android Emulator",
            # "platformVersion": "11.0.0",
            # "deviceName": "1aaa4ea80404",
            "automationName": "Appium",
            # "app": "com.android.chrome",
            "browserName": "Chrome"
        }

        driver = webdriver.Remote("http://localhost:4723/wd/hub", dc)
    else:
        raise Exception("driver doesn't exists")

    return driver


def get_browser_and_wait(browser_data):

    print ("starting %s\n" % browser_data["browserName"])

    browser = get_browser(browser_data)

    # browser.get("http://crossbrowsertesting.com")
    browser.get("http://www.google.com")


    browsers_waiting.append({"data": browser_data, "driver": browser})

    # browsers_waiting.append(browser)


    print ("%s ready" % browser_data["browserName"])

    while len(browsers_waiting) < len(browsers):

        print ("working on %s.... please wait" % browser_data["browserName"])

        # browser.get("http://crossbrowsertesting.com")
        browser.get("http://www.google.com")


    time.sleep(3)


threads = []
for i, browser in enumerate(browsers):

    thread = Thread(target=get_browser_and_wait, args=[browser])

    threads.append(thread)

    thread.start()

for thread in threads:

    thread.join()

    print("all browsers ready")

    for i, b in enumerate(browsers_waiting):
        print("browser %s's title: %s" % (b["data"]["name"], b["driver"].title))
        b["driver"].close()