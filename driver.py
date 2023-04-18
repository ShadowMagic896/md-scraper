import asyncio
import io
from typing import Any, Coroutine
from selenium.webdriver import Firefox as SeleniumFirefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import WebDriverException

from bs4 import BeautifulSoup


pass_prompts: bool = True

class _AsyncFirefox(SeleniumFirefox):

    def __init__(self, headless: bool = False):
        super().__init__()
        options = FirefoxOptions()
        options.headless = headless
        options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

        driver = SeleniumFirefox(
            options=options,
            executable_path="C:\\Program Files\\Mozilla Firefox\\geckodriver.exe",
            firefox_profile=FirefoxProfile(),
        )
        profile: FirefoxProfile = driver.firefox_profile # type: ignore
        # profile.add_extension("services/modify_headers_extension.xpi")

        self._driver = driver
    
    async def get(self, url: str, /, wait: float = 0) -> str:
        """Get the HTML of a page"""
        thread_get = asyncio.to_thread(self._driver.get, url)
        await thread_get
        thread_get.close()
        await asyncio.sleep(wait)
        thread_return: Coroutine[Any, Any, str] = asyncio.to_thread(
            self._driver.execute_script, "return document.documentElement.outerHTML"
        )
        return await thread_return

    async def load(self, url: str):
        thread_get = asyncio.to_thread(self._driver.get, url)
        await thread_get
        thread_get.close()

    async def screenshot(self, url: str, /, wait: float = 0) -> io.BytesIO:
        thread_get = asyncio.to_thread(self._driver.get, url)
        await thread_get
        thread_get.close()
        await asyncio.sleep(wait)
        thread_return: Coroutine[Any, Any, bytes] = asyncio.to_thread(
            self._driver.get_screenshot_as_png
        )
        b = await thread_return
        buf = io.BytesIO(b)
        buf.seek(0)
        return buf

    def close(self) -> None:
        self._driver.close()


class MemedroidFirefox(_AsyncFirefox):
    def __init__(self):
        super().__init__()
        self.base = "https://www.memedroid.com"
    
    async def login(self, username_or_email: str, password: str) -> None:
        await self.load(self.base)
        login_button: WebElement = self._driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/div[2]/a/span")
        login_button.click()

        await asyncio.sleep(0.5)

        username_input: WebElement = self._driver.find_element(By.ID, "login-form-modal-identifier")
        username_input.send_keys(username_or_email)

        password_input: WebElement = self._driver.find_element(By.ID, "login-form-modal-password")
        password_input.send_keys(password)

        del username_or_email, password

        submit_button: WebElement = self._driver.find_element(By.ID, "login-button-modal")
        submit_button.click()
    
    async def get_latest_id(self) -> int:

        soup = BeautifulSoup(await self.get(f"{self.base}/memes/latest", wait=1), "html.parser")
        meme_article = soup.select_one("html > body > div > div > div > section > div.gallery-memes-container > article")
        if meme_article is None:
            raise Exception("No memes found")
        meme_id = int(str(meme_article["data-item-id"]))
        return meme_id

    async def goto_meme(self, meme_id: int) -> None:
        await self.load(f"{self.base}/memes/detail/{meme_id}")
        
    async def upvote(self) -> None:
        upvote_button: WebElement = self._driver.find_element(By.ID, "detailed-item-like-button")
        try:
            upvote_button.click()
        except:
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            upvote_button.click()

    
    async def next(self) -> None:
        next_arrow: WebElement = self._driver.find_element(By.ID, "item-detail-icon-next")
        try:
            next_arrow.click()
        except:
            self._driver.execute_script("window.scrollTo(0, 0);")
            next_arrow.click()
    
    async def cycle(self) -> None:
        await self.login(
            input("Username / Email: "),
            input("Password: ")
        )
        if input("Do you want to preload a meme? (y/n): ") == "y":
            load = int(input("Meme ID: "))
        else:
            load = await self.get_latest_id()
        await self.goto_meme(load)
        cinput("When ready, press enter...")
        while True:
            try:
                await self._cycle()
            except:
                print("An error occurred. Press enter to try to fix it, or ! to end.")
                if cinput() == "!": break
                try:
                    ad_close_button = self._driver.find_element(By.XPATH, "/html/body/div[12]/div/button")
                    ad_close_button.click()
                except:
                    pass

                self.refresh()
                await asyncio.sleep(1)
                self.execute_script("window.scrollTo(0, 0);")
                await asyncio.sleep(1)
                print("Problem solving attempted. Press enter to continue.")
                cinput()
                continue
    
    async def _cycle(self):
        while True:
            await self.upvote()
            await asyncio.sleep(0.25)
            await self.next()
            await asyncio.sleep(0.75)


def cinput(prompt: str = "") -> str:
    if not pass_prompts:
        return input(prompt)
    return "\n"



