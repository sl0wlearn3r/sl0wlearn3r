import random, time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



""" shit to add:
def search random shit and browse:
def select text (like double clicking on a word or tripe clicking on a line) when browsing:
def not randomly but deliberately open consecutive tabs, look through them and close them:
def low chance to close the browser entirely and then open it back up and find the page where you left off and continue browsing:
"""


class HumanSimulator:

    def __init__(self, driver):
        self.driver = driver

    def simulate_hooman(self):
        """Simulate human-like interactions with random actions"""
        try:
            # Random chance to perform these actions (30-50% probability)
            if random.random() < 0.4:
                self.random_delay(2, 5)
                self.random_mouse_movements()

                # 25% chance to open random links in new tabs
                if random.random() < 0.25:
                    self.open_random_tabs()

                # 40% chance to click wrong elements
                if random.random() < 0.4:
                    self.click_random_elements()

                # Random browsing pattern
                self.random_scroll_behavior()

                # 15% chance to linger on error pages
                if random.random() < 0.15:
                    self.random_delay(5, 8)

        except Exception as e:
            print(f"Human simulation error: {str(e)}")

    def random_mouse_movements(self):
        """Create human-like mouse movements"""
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a, button, img")
            if elements:
                for _ in range(random.randint(2, 5)):
                    element = random.choice(elements)
                    ActionChains(self.driver)\
                        .move_to_element(element)\
                        .pause(random.uniform(0.5, 1.5))\
                        .perform()
                    self.random_delay(0.2, 0.5)
        except:
            pass

    def click_random_elements(self):
        """Click random non-essential elements"""
        try:
            # Get safe-to-click elements (avoid forms/logout buttons)
            elements = self.driver.find_elements(By.CSS_SELECTOR,
                "a:not([href*='logout']), button:not([type='submit']), .pagination-link"
            )

            if elements:
                for _ in range(random.randint(1, 3)):
                    element = random.choice(elements)
                    try:
                        element.click()
                        self.random_delay(1, 3)
                        self.driver.back()
                        self.random_delay(1, 7)
                    except:
                        pass
        except:
            pass

    def open_random_tabs(self):
        """Open and close random links in new tabs"""
        try:
            links = self.driver.find_elements(By.CSS_SELECTOR, "a[href]")
            if links:
                main_window = self.driver.current_window_handle

                for _ in range(random.randint(1, 2)):
                    link = random.choice(links)

                    self.driver.execute_script(
                        "arguments[0].style.border='3px solid red'",
                        link
                    )

                    ActionChains(self.driver)\
                        .pause(1)\
                        .key_down(Keys.CONTROL)\
                        .click(link)\
                        .key_up(Keys.CONTROL)\
                        .pause(2)\
                        .perform()

                    self.random_delay(1, 2)

                    # Switch to new tab and simulate activity
                    new_window = [w for w in self.driver.window_handles if w != main_window][-1]
                    self.driver.switch_to.window(new_window)
                    self.driver.maximize_window()
                    self.random_delay(2, 4)
                    self.random_scroll_behavior()
                    self.driver.close()
                    # %25 chance to open the link back up and scroll through it and then close it back down
                    if random.random() < 0.25:

                        ActionChains(self.driver)\
                        .key_down(Keys.CONTROL)\
                        .key_down(Keys.SHIFT)\
                        .send_keys("t")\
                        .pause(1)\
                        .key_up(Keys.CONTROL)\
                        .key_up(Keys.SHIFT)\
                        .perform()
                        self.driver.maximize_window()
                        self.random_scroll_behavior()

                        ActionChains(self.driver)\
                        .key_down(Keys.CONTROL)\
                        .send_keys("w")\
                        .key_up(Keys.CONTROL)\
                        .perform()

                    self.driver.switch_to.window(main_window)

        except:
            pass

    def random_scroll_behavior(self):
        """Simulate human-like scrolling patterns"""
        try:
            scroll_actions = [
                (random.randint(300, 800), random.uniform(0.5, 1.5)),
                (random.randint(-400, -200), random.uniform(0.3, 0.7)),
                (random.randint(100, 300), random.uniform(0.2, 0.5))
            ]

            for distance, speed in scroll_actions:
                self.driver.execute_script(f"window.scrollBy(0, {distance})")
                time.sleep(speed)
                self.random_delay(2, 7)

            # Random chance to scroll to top
            if random.random() < 0.3:
                self.driver.execute_script("window.scrollTo(0, 0)")
                time.sleep(random.uniform(0.5, 1.5))

            # Random chance to scroll to bottom and then right back up
            if random.random() < 0.2:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                self.random_delay(2,7)
                self.driver.execute_script("window.scrollTo(0, 0)")

        except:
            pass

    def random_delay(self, min_sec, max_sec):
        """random wait time between le actionz"""
        time.sleep(random.uniform(min_sec, max_sec))
