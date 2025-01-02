import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# налаштування для маскування браузера під справжнього користувача
options = Options()
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, як Gecko) Chrome/131.0.0.0 Safari/537.36")
# вимкнення (реклами)
options.add_argument("--disable-notifications") # вимикає спливаючі вікна
options.add_argument("--disable-extensions")# вимкнути можливі розширення реклами
options.add_argument("--start-maximized") # запускає браузер в максимізованому вікні
# для діагностики скрипта
logging.basicConfig(level=logging.INFO)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# відкриття сайту розетка
driver.get("https://rozetka.com.ua/ua/")
logging.info("Сайт відкрито")

try:
    # поле пошуку: метод, щоб переконатись що елемент видимий для взаємодії
    search_box = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > rz-app-root > div > div > rz-main-header > header > div > div > div.header-search > rz-search-suggest > form > div.search-form > div > div > input'))
    )
    search_box.send_keys("ноутбуки")
    logging.info("Введено запит в поле пошуку")

    # кнопка "знайти"
    search_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > rz-app-root > div > div > rz-main-header > header > div > div > div.header-search > rz-search-suggest > form > div.search-form > button')) 
    )

    search_button.click()
    logging.info("Кнопка пошуку натиснута")

    #перший товар в результатах пошуку
    first_product = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > rz-app-root > div > div > rz-category > div > main > rz-catalog > div > div > section > rz-grid > ul > li:nth-child(1) > rz-catalog-tile > app-goods-tile-default > div > div.goods-tile__inner > div.goods-tile__content > rz-button-product-page:nth-child(5) > rz-indexed-link > a > span'))
    )
    logging.info("Перший товар знайдено")

    # кнопка "додати до кошика"
    add_to_cart_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > rz-app-root > div > div > rz-category > div > main > rz-catalog > div > div > section > rz-grid > ul > li:nth-child(1) > rz-catalog-tile > app-goods-tile-default > div > div.goods-tile__inner > div.goods-tile__content > div.goods-tile__prices > div.goods-tile__price.price--red.ng-star-inserted > rz-buy-button > button > svg > use'))
    )

    add_to_cart_button.click()
    logging.info("Товар додано до кошика")

    # кошик
    cart_badge = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > rz-app-root > rz-modal > rz-modal-layout > div.header.border.empty-none > h2'))
    )

    cart_badge.click()
    logging.info("Перейшли до кошика")

    # муню: три крапки 
    cart_actions = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#cartProductActions0'))
    )

    cart_actions.click()
    logging.info("Меню відкрито")

    # кнопка "видалити"
    delete_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#cartProductActions0 > ul > li:nth-child(1) > rz-trash-icon > button'))
    )

    delete_button.click()
    logging.info("Товар видалено з кошика")

    # повідомлення "кошик порожній"
    empty_cart_message = WebDriverWait(driver,30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > rz-app-root > rz-modal > rz-modal-layout > div.content.padding > rz-shopping-cart > div > div.cart-dummy.ng-star-inserted > h4'))
    )

    assert "Кошик порожній" in empty_cart_message.text,  "Кошик не порожній"
    logging.info("Повідомлення про порожній кошик підтверджено")

    #Обробка виключень на випадок помилок
except TimeoutException as e:
     logging.error(f"Помилка очікування елемента: {e}") 
except NoSuchElementException as e:
     logging.error(f"Елемент не знайдено") 
finally:
     driver.quit()
     logging.info("Браузер закрито")