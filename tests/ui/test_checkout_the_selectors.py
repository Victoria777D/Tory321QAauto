from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# ініціалізація вебдрайвера Chrome
driver = webdriver.Chrome()

# URL сайту який перевіряється
url = "https://novaposhta.ua"
driver.get(url)

selectors = [
    {"method": By.CSS_SELECTOR, "value":"#top_menu > li:nth-child(5) > ul > li:nth-child(3) > a"},
    {"method": By.CSS_SELECTOR, "value":"#top_menu > li:nth-child(5) > a"},
    {"method": By.TAG_NAME, "value":"body"},
    {"method": By.CSS_SELECTOR, "value":"#np-chat-magic-button-btn-open-main-menu > span > svg > path:nth-child(1)"}
]

# список селекторів які перевіряються
def check_selector(selector):
    try:
        elevent = driver.find_element(selector["method"], selector["value"])
        print(f"Selector found: {selector['value']}")
        return True
    
    except NoSuchElementException:
        print(f"Selector not found: {selector['value']}")
        return False
    
for selector in selectors:
    check_selector(selector)

    
driver.quit()
