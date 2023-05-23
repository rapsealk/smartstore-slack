import logging
import os
import time
from datetime import datetime
from pathlib import Path

import selenium
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

TITLE = "젤다의 전설 시간의 오카리나 3D"
URL = "https://smartstore.naver.com/gameswitch/products/4690559023"
# TITLE = "젤다의 전설 무쥬라의 가면 3D"
# URL = "https://smartstore.naver.com/gameswitch/products/4108361209"


def post_slack_message(message: str) -> None:
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        response = client.chat_postMessage(
            channel="#notification",
            text=message,
        )
    except SlackApiError as e:
        print(e)
    return


def check_purchase_button_enabled(url: str) -> bool:
    result = False

    driver = webdriver.Edge()
    driver.get(URL)
    try:
        element = driver.find_element(By.CLASS_NAME, "sys_chk_buy")
        result = element.is_displayed() and element.is_enabled()
    except selenium.common.exceptions.NoSuchElementException:
        result = False
    finally:
        driver.close()

    return result


def main():
    has_button_enabled = False
    while True:
        is_button_enabled = check_purchase_button_enabled(URL)
        if is_button_enabled and not has_button_enabled:
            post_slack_message(f"The product({TITLE}) has been stocked! ({URL})")
            log.info(f"[{datetime.now()}] {TITLE} has been stocked! ({URL})")
        has_button_enabled = is_button_enabled
        time.sleep(60)


if __name__ == "__main__":
    main()
