import pytest
from modules.ui.page_objects.nova_poshta_page import NovaPoshtaPage
from selenium.webdriver.common.by import By


@pytest.mark.ui 
def test_track_parcel():
    # створюємо об'єкт головної сторінки
    nv_poshta = NovaPoshtaPage()
    
    # відкриваємо головну сторінку 
    nv_poshta.go_to()

    # переходимо до центру підтримки клієнтів
    nv_poshta.go_to_support_center()

    # клікаємо на "відстежити посилку"
    nv_poshta.click_tracking()

    # вводимо номер посилки
    nv_poshta.enter_parcel_number(20451**2181***)
    
    # натискаємо кнопку пошук
    result_message = nv_poshta.click_search()

    # перевіряємо чи є потрібне повідомлення
    assert result_message == "Відправлення отримано. Грошовий переказ видано одержувачу"

    # закриваємо браузер
    nv_poshta.close()





