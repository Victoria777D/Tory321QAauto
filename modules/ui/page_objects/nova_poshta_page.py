from modules.ui.page_objects.nova_poshta_base import NovaPoshtaBase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException



# клас для взаємодії зі сторінкою
class NovaPoshtaPage(NovaPoshtaBase):
    URL = "https://novaposhta.ua"

    def __init__(self) -> None:
        super().__init__()

    # відкриваємо головну сторінку NovaPoshta
    def go_to(self):
        self.driver.get(NovaPoshtaPage.URL)
        self.close_popup()
        
    # перевіряємо наявність спливаючого вікна
    def close_popup(self):
        # для закриття всіх вспливаючих вікон
        while True:
            # закриваємо перше вікно
            try:
                popup_close_button = self.driver.find_element(By.CSS_SELECTOR, "#main_page")
                popup_close_button.click()
            except NoSuchElementException:
                try:
                    # закриваємо друге вікно якщо є
                    modal_body = self.driver.find_element(By.TAG_NAME, "body") 
                    if "modal-open" in modal_body.get_attribute("class"):
                        # перевіряємо атрибут class
                        close_button = self.driver.find_element(By.CLASS_NAME, "modal-close")
                        close_button.click()
                    else:
                        break # виходить з циклу якщо нема модального вікна
                except NoSuchElementException:
                    break # виходить з циклу якщо більше немає спливаючих вікон


    # знаходимо центр підтримки клієнтів і клікаєм на нього
    def go_to_support_center(self):
        support_link = self.driver.find_element(By.CSS_SELECTOR, "#online_chat > a")
        support_link.click()

    # знаходимо "відстежити посилку" і клікаємо
    def click_tracking(self):
        trach_link = self.driver.find_element(By.CSS_SELECTOR, "#nav > div > div > div.navbar__menu > div.menu > ul > li:nth-child(1) > a")
        trach_link.click()

    # знаходимо поле для вводу номера посилки і вводимо номер
    def enter_parcel_number(self, parcel_number):
        parcel_input = self.driver.find_element(By.ID, "en")
        
        parcel_input.send_keys(parcel_number)

    # натискаємо кнопку "пошук"
    def click_search(self):
        search_button = self.driver.find_element(By.ID, "np-number-input-desktop-btn-search-en")
        search_button.click()

        # отримуємо текст повідомлення результату
        results_massage = self.driver.find_element(By.CLASS_NAME, "header__status-text")
        return results_massage.text



                                          










    

    