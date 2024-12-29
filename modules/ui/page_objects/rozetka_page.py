from modules.ui.page_objects.rozetka_base import RozetkaBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



class RozetkaPage(RozetkaBase):
    URL = "https://rozetka.com.ua/"

    def __init__(self) -> None:
        super().__init__()

    def go_to(self, url):
        self.driver.get(url)

     # знаходимо поле для введення пошуку
    def search_product(self, product_name):
        search_box = self.driver.find_element(By.NAME, "search")
        search_box.send_keys(product_name)# вводимо запит
        search_box.send_keys(Keys.RETURN) # натискаємо enter для пошуку

    # результати пошуку
    def verify_search_results(self):
        results = self.driver.find_elements(By.CSS_SELECTOR, "catalog-heading.ng-star-inserted")

        assert len(results) > 0, "Результати пошуку не знайдено"
        return results
    

    # Вибираємо перший товар зі списку результатів
    def select_first_product(self):
        results = self.driver.find_elements(By.CLASS_NAME, "goods-tile__title")
        results[0].click() # клікаємо по товару

    # додаємо товар до кошика
    def add_product_to_cart(self):
        
         add_to_cart_button = self.driver.find_element(By.CSS_SELECTOR, ".buy-button.button.button--with-icon.button--green.button--medium.buy-button--tile.ng-star-inserted")
         add_to_cart_button.click()

    # перевіряємо, чи з'явилось повідомлення про додавання товару в кошик
    def verify_add_to_cart_message(self):
        try:
            cart_message = self.driver.find_element(By.CSS_SELECTOR, "h2.border.padding.ng-star-inserted")
            return cart_message.text
        # виключення, якщо повідомлення не буде знайдено
        except Exception as e:
            raise AssertionError("Повідомлення про додавання товару не з'явилось") from e 
    
