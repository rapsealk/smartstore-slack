import os

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

# TITLE = "젤다의 전설 시간의 오카리나 3D"
# URL = "https://smartstore.naver.com/gameswitch/products/4690559023"
# TITLE = "젤다의 전설 무쥬라의 가면 3D"
# URL = "https://smartstore.naver.com/gameswitch/products/4108361209"
TITLE = "케이던스 오브 하이랄: 크립트 오브 더 네크로댄서"
URL = "https://smartstore.naver.com/techline/products/5133701323"


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
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15")
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
        post_slack_message(f"The product({TITLE}) has been stocked! ({URL})", token=SLACK_BOT_TOKEN)


if __name__ == "__main__":
    main()
