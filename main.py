from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import zipfile
import time
import os
import random


PROXY_HOST = '52.87.222.91'  # rotating proxy or host
PROXY_PORT = '80' # port
PROXY_USER = 'geic' # username
PROXY_PASS = 'geic' # password

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)

    # Download and install the chromedriver binary
    service = Service(ChromeDriverManager().install())
    # Initiate the driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

website = 'https://www.minuteinbox.com/'
website2_url = 'https://www.upwork.com/nx/signup/?dest=home'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension("upwork.zip")
password = 'PICpic123!@#'


while True:
    chrome = get_chromedriver(use_proxy=True)
    chrome.maximize_window()

    chrome.get(website)

    xpath_expression = "//span[@id='email']"

    # Find the span element by XPath
    email_span = chrome.find_element(By.XPATH, xpath_expression)

    # Extract the text content of the span
    email_text = email_span.text

    print(email_text)

    name = email_text.split("@")

    full_name = name[0].split(".")
    first_name = full_name[0]
    last_name = full_name[1]

    print(first_name)
    print(last_name)

    chrome.execute_script("window.open('" + website2_url + "')")

    time.sleep(5)
    chrome.switch_to.window(chrome.window_handles[1])
    time.sleep(5)

    try:
        try:
            chrome.find_element(
                By.XPATH, "//button[@id='onetrust-accept-btn-handler']").click()
            time.sleep(1)
        except Exception as e:
            print(e)
        chrome.find_element(By.XPATH, "//div[@data-qa='work']").click()
        time.sleep(1)
        chrome.find_element(By.XPATH, "//button[@data-qa='btn-apply']").click()
        time.sleep(1)
        chrome.find_element(
            By.XPATH, "//input[@id='first-name-input']").send_keys(first_name)
        time.sleep(1)
        chrome.find_element(
            By.XPATH, "//input[@id='last-name-input']").send_keys(last_name)
        time.sleep(1)
        chrome.find_element(
            By.XPATH, "//input[@id='redesigned-input-email']").send_keys(email_text)
        time.sleep(1)
        chrome.find_element(
            By.XPATH, "//input[@id='password-input']").send_keys(password)
        time.sleep(1)
        chrome.find_element(
            By.XPATH, "//label[@id='checkbox-terms']").click()
        time.sleep(1)
        chrome.find_element(
            By.XPATH, "//button[@id='button-submit-form']").click()
        chrome.switch_to.window(chrome.window_handles[0])
        time.sleep(5)

        chrome.get("https://www.minuteinbox.com/email/id/2")

        href = chrome.find_element(
            By.XPATH, "//div[@class='button-holder']/a").get_property("href")

        print(href)
        chrome.switch_to.window(chrome.window_handles[1])
        time.sleep(5)

        chrome.get(href)

        time.sleep(5)

        elements = chrome.find_elements(
            By.XPATH, "//ul[@class='welcome-step1-list']/li")

        filename = "emails.txt"
        with open(filename, "a") as file_object:
            # Write content to the file here
            file_object.write(email_text + '\n')

        if (len(elements) == 3):
            filename = "emails-success.txt"
            with open(filename, "a") as file_object:
                # Write content to the file here
                file_object.write(email_text + '\n')

    except Exception as e:
        print(e)

    min_sleep_time = 1 * 60  # 3 minutes in seconds
    max_sleep_time = 2 * 60  # 5 minutes in seconds

    sleep_duration = random.uniform(min_sleep_time, max_sleep_time)    
    chrome.quit()
    time.sleep(sleep_duration)
