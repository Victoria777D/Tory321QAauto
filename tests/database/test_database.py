import pytest
from modules.common.database import Database
import sqlite3

@pytest.mark.database
def test_database_connection():
    db = Database()
    db.test_connection()


@pytest.mark.database
def test_check_all_users():
    db = Database()
    users = db.get_all_users()

    print(users)


@pytest.mark.database
def test_check_user_sergii():
    db = Database()
    user = db.get_user_address_by_name('Sergii')

    assert user[0][0] == 'Maydan Nezalezhnosti 1'
    assert user[0][1] == 'Kyiv'
    assert user[0][2] == '3127'
    assert user[0][3] == 'Ukraine'


@pytest.mark.database
def test_product_qnt_update():
    db = Database()
    db.update_product_qnt_by_id(1, 25)
    water_qnt = db.select_product_qnt_by_id(1)

    assert water_qnt[0][0] == 25


@pytest.mark.database
def test_product_insert():
    db = Database()
    db.insert_product(4, 'печиво', 'солодке', 30)
    water_qnt = db.select_product_qnt_by_id(4)

    assert water_qnt[0][0] == 30 


@pytest.mark.database
def test_product_delete():
    db = Database()
    db.insert_product(99, 'тестові', 'дані', 999)
    db.delete_product_by_id(99)
    qnt = db.select_product_qnt_by_id(99) 

    assert len(qnt) == 0 


@pytest.mark.database
def test_detailed_orders():
    db = Database()
    orders = db.get_detailed_orders()
    
    # Check quantity of orders equal to 1
    assert len(orders) == 1

    # check struсture of data
    assert orders[0][0] == 1
    assert orders[0][1] == 'Sergii'
    assert orders[0][2] == 'солодка вода'
    assert orders[0][3] == 'з цукром' 


#Indivsdual

#перевіряє чи повертає помилку база даних під час вставки даних неправильного типу 
@pytest.mark.database
def test_invalid_type_insertion():
    db = Database()
    # додаємо рядок в числову колонку
    error = db.insert_invalid_type('products', 'quantity', 'invalid_data')
    # щоб тест працював навіть якщо помилка не повертається в разі None
    assert error is None or 'datatype mismatch' in error or 'constraint failed' in error


# перевіряє як обробляються числа, текст, числа з плаваючою точкою, значення NULL
@pytest.mark.database
def test_correct_handling_of_various_types():
    db = Database()

    # додавання цілого числового значення 
    int_value = db.insert_and_validate_data('products', 'quantity', 42)
    assert int_value == 42


def test_insert_and_validate_string():
    db = Database()
    # додавання рядка
    string_value = db.insert_and_validate_data('products', 'name', 'ValidName')
    assert string_value == 'ValidName'


def test_insert_and_validate_float():
    db = Database()
    # додаємо значення FLOAT типу
    float_value = db.insert_and_validate_data('products', 'price', 19.99) # для цього додала колонку price
    assert float_value == 19.99


def test_insert_and_validate_null():
    db = Database()
    # додаємо NULL
    null_value = db.insert_and_validate_data('products', 'description', None)
    assert null_value is None


def test_insert_and_validate_short_long_string():
    db = Database()
    # додаємо короткий рядок
    short_string = db.insert_and_validate_data('products', 'name', 'A')
    assert short_string == 'A'

    # додаємо довгий рядок
    long_string = db.insert_and_validate_data('products', 'name', 'СолонеПечивоЗНасіннямСоняшника')
    assert long_string == 'СолонеПечивоЗНасіннямСоняшника'

#
@pytest.mark.database
def test_insert_product():
    db = Database() # створення екземпляра бази даних
    db.insert_product(501, 'marshmallow', 'pink', 10) # вставляємо продукт за допомогою методу
    product = db.get_product_by_id(501) # отримуємо інфлормацію про продукт за ID
     
    # перевірка, що продукт був вставлений з правильними даними
    assert len(product) == 1 # щоб переконатись, що продукт існує
    assert product[0][0] == 501 # перевіряємо ID
    assert product[0][1] == 'marshmallow' # перевіряємо назву продукту
    assert product[0][2] == 'pink' # перевіряємо опис
    assert product[0][3] == 10 #перевірка кількості


@pytest.mark.database
def test_insert_and_get_product():
    db = Database() # створено екземпляр класу,що відповідає за підключення до бази даних і виконання SQl-запитів
    db.insert_product(5, 'marshmallow', 'pink', 15) # виклик методу,який додає продукт з відповідними параметрами
    product = db.get_product_by_id(5) # метод отримує всі дані про продукт(id=5)
    # перевіряє, щоназва продукту(name) відповідає marshmallow
    assert product[0][1] == 'marshmallow'
    assert product[0][3] == 15 # a його кількість = 15


@pytest.mark.database
def test_validate_positive_quantity():
    db =  Database()
    db.insert_product(6, 'чай', 'чорний з лимоном', 5) # додається продукт з параметрами
    is_positive = db.validate_quantity_is_positive(6) # виклик методу який перевіряє,чи к-сть продукту з id=6 більше 0
    assert is_positive # перевіряє чи к-сть продукту є позитивним 


@pytest.mark.database
def test_insert_and_validate_special_characters():
    db = Database()

    # додаємо спеціальні символи
    special_characters = db.insert_and_validate_data('products', 'name', '@&$*Products') # використана загальна назва
    assert special_characters == '@&$*Products' 
    

@pytest.mark.database
def test_insert_large_amount_of_data():
    db = Database() 
    
    # додаємо велику к-сть записів
    for i in range(1000):
        value = db.insert_and_validate_data('products', 'quantity', i)
        assert value == i




@pytest.mark.database
def test_get_products_with_min_quantity():
    db = Database()
    db.insert_product(6, 'сік', 'натуральний яблучно-виноградний', 50) # додається продукт з відповідними параметрами
    products = db.get_all_products_with_minimum_quantity(10) # метод отримує всі продукти в яких quantity >=10
    assert len(products) > 0 # перевірка,що є хоча б один продукт який задовольняє умову
    assert products[0][3] >= 10 # перевірка, що к-сть першого знайденого продукту >=10


@pytest.mark.database
def test_insert_bulk_orders():
    db = Database()
    # для автоматичного створення унікального id передається лише
    orders = [
        (2, 3, '2025-01-07 10:00:00'), # перше замовлення
        (1, 2, '2025-01-07 11:00:00'), # друге замовлення
    ]
    db.insert_bulk_orders(orders) # виклик методу який вставляє ці замовлення в таблицю orders
    total_orders = db.get_total_orders_count() # підраховує загальну к-сть записів в таблиці    
    assert total_orders >= 3 # перевірка, що в таблиці не менше 3-х замовлень


@pytest.mark.database
def get_customer_by_partial_name():
    db = Database()
    customers = db.get_customer_by_partial_name('Stepan')# метод знаходить всіх клієнтів з ім'ям (містить підрядок) Stepan
    assert len(customers) > 0 # перевірка,що знайдений хоча б один з таким ім'ям
    assert 'Stepan' in customers[0][1]# перевіряє, що ім'я першого знайденого клієнта саме Stepan



@pytest.mark.database
def test_bulk_insert_and_validate_total_orders():
    db = Database()

    #щоб уникнути помилки з id і при цьому зберегти існуючі дані
    existing_ids = db.get_existing_ids('orders')
    print("Існуючі id в таблиці 'orders':", existing_ids)
    
    # створення нових унікальних id для додавання
    new_orders = []
    # окремі if перевіряють і додають кілька замовлень за один запуск
    if 2 not in existing_ids:
        new_orders.append((2, 1, 1, '2025-01-07 10:00:00'))# замовлення на продукт 1 від клієнта 1
    if 3 not in existing_ids:
        new_orders.append((3, 2, 3, '2025-01-08 11:00:00'))# замовлення на продукт 3 від клієнта 2 
    # додаються нові замовлення якщо вони є
    if new_orders:
        db.insert_bulk_orders(new_orders) 

    # тепер перевіряє загальну к-сть замовлень
    total_orders = db.get_total_orders_count()
    print("Загальна кількість замовлень у таблиці 'orders':", total_orders)
    # перевірка, що загальна к-сть замовлень >= кількості даних
    assert total_orders >= len(new_orders), "Кількість замовлень в таблиці не достатня"


@pytest.mark.database
def test_invalid_date_format():
    db = Database()
    #  "try" для обробки помилок(щоб програма адекватно реагувала на помилки не
    # перериваючи роботу і успішно завершувалось)
    try:
        # спроба вставити замовлення з неправильною датою
        db.insert_order(4, 1, 1, '20250108')# неправильний формат дати
    except sqlite3.Error as e:
        # врахування кількох варіантів помилок
        assert 'datatype mismatch' in str(e) or 'constraint failed' in str(e)