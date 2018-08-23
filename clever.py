from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import asyncio

class Cleverbot:
    def __init__(self, chromedriver=r"chromedriver.exe", headless=True):
        options = Options()
        if headless: options.add_argument('headless')
        options.add_argument('window-size=1280x720')
        options.add_argument('--disable-browser-side-navigation')
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs",prefs)

        self.driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
        self.driver.get("https://www.cleverbot.com/")

        self.delay = 0.25
        self.done = True

    @asyncio.coroutine
    async def send_message(self, txt):
        if self.done is False:
            return False

        self.done = False
        resp = False

        try:
            await asyncio.sleep(self.delay)

            while True:
                input = self.driver.find_element_by_css_selector("input.stimulus")

                if input.get_attribute("readonly"):
                    await asyncio.sleep(self.delay)
                    continue
                else:
                    try:
                        input.send_keys(txt)
                        input.send_keys(Keys.ENTER)
                    except Exception as e:
                        print(str(e))
                    break

            await asyncio.sleep(self.delay)

            done = False
            old = ""
            while not done:
                resp = self.driver.find_elements_by_css_selector("span.bot")[4].get_attribute("innerHTML")
                if resp == old and "&nbsp;" not in resp and resp[-1] != ",":
                    break
                old = resp
                await asyncio.sleep(self.delay)

        except:
            try:
                alert = self.driver.switch_to_alert()
                alert.dismiss()
                alert.accept()
            except:
                pass

        if txt == "qwertyuiop":
            resp = "lol"
        self.done = True
        return resp