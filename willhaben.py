import warnings

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v133.fetch import continue_request
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import requests, logging
from human_sim import HumanSimulator

""" shit to add:
def type() where anything you want to send_keys for is typed letter by letter via a function that sends keys
for each letter specifically. It also holds down shift for capitalization, sends space for spacing between
words and so on...

"""


options = ChromeOptions()
# options.add_argument("--headless")
#options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

def main():
    hs = HumanSimulator(driver)

    def fcookies():
        try:
            reject_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='didomi-notice-disagree-button']")
                )
            )
            reject_button.click()
            print("successfully avoided the mf cookies")
        except TimeoutException:
            print("could not avoid the mf cookies OR the cookies popup did not show up")

    def paginate():
        try:
            current_page_element = WebDriverWait(driver,10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[aria-current='page']")
                    # there are other tags I can try as well as CSS methods
                    #so fucking weird, XPATH cant find the same shit but CSS can!?
                )
            )

            print("Now, at the page:", current_page_element.text)
        except Exception as e:
            #print("Couldnt determine the current page ")
            print("\n\n\n", e, "Couldnt determine the current page")


        try:
            next_button = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable(

                    (By.XPATH, '//a[@aria-label = "Weiter zur nächsten Seite"]')
                )
            )
            next_button.click()
            print("successfully went on to the next mfing page")
            hs.simulate_hooman()
        except TimeoutException:
            print("next button isnt clickable")
            return False

        except NoSuchElementException:
            print("next button is not present")
            return False

    def get_search_results():
        results = []

        # Wait for at least one result to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@data-testid, 'search-result-entry')]"))
        )

        # Get all result containers - multiple possible selectors
        result_containers = driver.find_elements(
            By.XPATH, "//*[@data-testid[contains(., 'search-result-entry')]]"
        )

        for item in result_containers:
            try:
                # Title - try multiple selectors
                title = (
                        item.find_element(By.XPATH, ".//h3").text or  # Any h3
                        item.find_element(By.XPATH, ".//*[@aria-label[contains(., 'title')]]").text or
                        item.find_element(By.XPATH, ".//*[contains(@class, 'title')]").text
                )

                # Price - prioritize data-testid, then aria-label, then class
                price = (
                        item.find_element(By.XPATH, ".//*[contains(@data-testid, 'price')]").text or
                        item.find_element(By.XPATH, ".//*[@aria-label[contains(., '€')]]").text or
                        item.find_element(By.XPATH, ".//*[contains(@class, 'price')]").text
                ).replace("€", "").strip()

                # Description - look for longest text span
                #description = dunno how to get it yet because all it has is a cryptic class name, solve this problem last

                results.append({
                    'title': title,
                    'price': price,
                    #'description': description
                })

            except NoSuchElementException:
                continue

        return results


    # driver.execute_cdp_cmd("Network.enable", {})
    # driver.execute_cdp_cmd("Network.setExtraHTTPHeaders",
    #                        {'content-security-policy': "frame-ancestors 'self' http://app.storyblok.com",
    #                         'strict-transport-security': 'max-age=31536000; includeSubDomains',
    #                         'x-content-type-options': 'nosniff', 'x-dns-prefetch-control': 'off',
    #                         'x-download-options': 'noopen', 'x-frame-options': 'SAMEORIGIN', 'x-xss-protection': '0',
    #                         'set-cookie': 'IADVISITOR=d4b0cc68-664b-49ba-b7ed-3a7234aa0b59; Max-Age=5184000; Path=/; Expires=Tue, 17 Jun 2025 08:03:59 GMT, context=prod; Path=/, TRACKINGID=08b2a1c1-3630-4296-8a83-dc4cedf699ce; Max-Age=315360000; Path=/; Expires=Mon, 16 Apr 2035 08:03:59 GMT; HttpOnly, x-bbx-csrf-token=dce3f130-700c-4513-bd2e-9a8df3e061ba; Path=/; Secure',
    #                         'permissions-policy': 'ch-ua-model=*,ch-ua-platform-version=*,interest-cohort=()',
    #                         'accept-ch': 'sec-ch-ua-model,sec-ch-ua-platform-version', 'gip': '47',
    #                         'cache-control': 'private, no-cache, no-store, max-age=0, must-revalidate',
    #                         'etag': '"w7l3x6wyei56yy"', 'content-type': 'text/html; charset=utf-8',
    #                         'vary': 'Accept-Encoding', 'content-encoding': 'gzip',
    #                         'date': 'Fri, 18 Apr 2025 08:03:59 GMT', 'keep-alive': 'timeout=5',
    #                         'transfer-encoding': 'chunked', 'alt-svc': 'h3=":443";ma=864000;persist=1'})
    # #got it with headers = requests.get(willhaben).headers

    willhaben = "https://www.willhaben.at"
    driver.get(willhaben)
    fcookies()
    try:
        driver.save_screenshot("screenshot_ofmainpage.png")
    except Exception as e:
        print("A problem occured when taking the screenshot of main page",e)
    hs.simulate_hooman()

    main_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@href = '/iad/kaufen-und-verkaufen/']")
        )
    )
    main_page.click()
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='keyword']"))
    )
    search.send_keys("Balenciaga sneaker")
    search.send_keys(Keys.ENTER)
    WebDriverWait(driver,2)
    try:
        adsperpage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "select[data-testid*='adsperpage']")
            )
        )
        select = Select(adsperpage)
        select.select_by_visible_text("90")
        print("successfully selected 90 ads per page")
    except Exception as e:
        print(e ,"The adsperpage button could not be found OR ALl listings are only one page long.")
        pass
    paginate()

    shoes = {}



    # Usage:
    items = get_search_results()
    for item in items:
        print(f"Title: {item['title']}")
        print(f"Price: {item['price']}")
        print(f"Desc: {item['description'][:50]}...")  # First 50 chars
        print("-" * 50)



if __name__ == "__main__":
    main()
