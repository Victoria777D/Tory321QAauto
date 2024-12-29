from modules.ui.page_objects.rozetka_page import RozetkaPage
import pytest

@pytest.mark.ui                                                                  
def test_search_and_add_to_cart():
    rozetka_page = RozetkaPage()

    rozetka_page.go_to("https://rozetka.com.ua/") # відкриваємо сайт 

    rozetka_page.search_product("ноутбуки") # вводить запит в поле пошуку

    rozetka_page.verify_search_results() # чи знайдено товар за запитом

    rozetka_page.select_first_product() # вибір першого товару з результатів пошуку

    rozetka_page.add_product_to_cart() # додає товар до кошика

    message = rozetka_page.verify_add_to_cart_message() # чи з'явилось повідомлення про додавання товару
    
    # перевірка, чи містить повідомлення фразу "товар додано до кошика"
    assert "товар додано до кошика" in message.lower(), "Повідомлення про додавання товару не з'явилось"

    rozetka_page.close() # закриває браузер після завершення теста 