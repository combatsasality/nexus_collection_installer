import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import json
import time


class SeleniumWrapper:
    accepted: bool = False
    skipped_urls: list[str] = []

    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(version_main=143, options=options)

    def _read_cookies(self):
        with open("cookies.json", "r") as f:
            cookies: list[dict[str, str]] = json.load(f)

            for cookie in cookies:
                cookie.update(
                    {
                        "domain": ".nexusmods.com",
                        "path": "/",
                        "secure": True,
                        "httpOnly": True,
                        "expiry": 9999999999,
                    }
                )

            self.cookies = cookies

    def set_cookies(self):
        self._read_cookies()
        self.driver.get("https://nexusmods.com")

        for cookie in self.cookies:
            self.driver.add_cookie(cookie)

        try:
            dialog_element = WebDriverWait(self.driver, 3).until(
                lambda d: d.find_element(By.CSS_SELECTOR, ".fc-dialog.fc-choice-dialog")
            )
        finally:
            if dialog_element:
                button = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button.fc-button.fc-cta-do-not-consent.fc-secondary-button",
                )
                button.click()

    def open_new_tab_and_start_downloading(self, url: str):
        self.driver.switch_to.new_window("tab")
        self.driver.get(url)

        self.start_downloading(url)

        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    def start_downloading(self, link: str):
        self.driver.get(link)

        custom_component = self.driver.find_element(
            By.CSS_SELECTOR, "mod-file-download"
        )

        shadow_root = self.driver.execute_script(
            "return arguments[0].shadowRoot", custom_component
        )

        slow_button = shadow_root.find_element(
            By.CSS_SELECTOR, "button.nxm-button.nxm-button-secondary-filled-weak"
        )
        slow_button.click()

        wait = WebDriverWait(self.driver, 7)

        wait.until(
            EC.text_to_be_present_in_element(
                (
                    By.CSS_SELECTOR,
                    "div.donation-wrapper p",
                ),
                "Your download has started",
            )
        )

        if not self.accepted:
            time.sleep(5)
            self.accepted = True
