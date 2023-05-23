import argparse

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

parser = argparse.ArgumentParser()
parser.add_argument("--token", type=str)
args = parser.parse_args()

# TITLE = "젤다의 전설 시간의 오카리나 3D"
# URL = "https://smartstore.naver.com/gameswitch/products/4690559023"
TITLE = "젤다의 전설 무쥬라의 가면 3D"
URL = "https://smartstore.naver.com/gameswitch/products/4108361209"


def post_slack_message(message: str, *, token: str) -> None:
    client = WebClient(token=token)
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

    options = webdriver.EdgeOptions()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50")
    options.add_argument("--headless")

    driver = webdriver.Edge(options=options)
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
    if check_purchase_button_enabled(URL):
        post_slack_message(f"The product({TITLE}) has been stocked! ({URL})", token=args.token)


if __name__ == "__main__":
    main()
