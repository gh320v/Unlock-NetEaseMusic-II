# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "006794A64646DE23B4A6AE78A2EC3055C5B4D37AA5E6E3A2D10CBC104CE66E14D66D75BD153E9BB7500BB0F0009F3F9EF17735A760CE2954BA73D6A29A404136F6500128F1A4A5B3DE0BA0D5FFC594CC239141B8FED6CFECB997CBBBA89C053E4981CFD771370B97B20A449DA9B8DADB6E7C83695C52E38DBE9641CA4F4B1183C47BE3EE1794207FF0803C0A3B9D713BB8348DE5CEC11745863EA6E4BBDA4B9A7D983B293DF9D4564E50C27EF7964B2E37ADB0A131503A1B7F115BA3994CA9F4C89AE73C92DABBD3C9171711B9E87E90DE537D66BE4025F2B18FC5A09A9E4AF35B37730C9220C8E83B37B84025BC90E53C53B4DD482DBC9CA49DCB1E731C0C68E5A75BBEB265EDF84EF5C53AF507E88F5858B790CEACE78159FE99C24B80E0E92F15A5CF8A423916AF037324F6EFD98C526360DE45E738E232D1557E1B0F203A475CEC3F9E184AFCDDA04B662BE5BEEC4CA04D4D85B56D79A480839C9B92A23A45"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
