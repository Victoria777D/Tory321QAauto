import sqlite3


class Database():

    def __init__(self):
        self.connection = sqlite3.connect(r'C:\Users\Admin\Downloads\become_qa_auto (3).db')
        self.cursor = self.connection.cursor()

    def test_connection(self):
        sqlite_select_Query = "SELECT sqlite_version();"
        self.cursor.execute(sqlite_select_Query)
        record = self.cursor.fetchall()
        print(f"Connected successfully. SQLite Database Version is: {record}")

    def get_all_users(self):
        query = "SELECT name, address, city FROM customers"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record 

    def get_user_address_by_name(self, name):
        query = f"SELECT address,city, postalCode, country FROM customers WHERE name = '{name}'"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record 
    

    def update_product_qnt_by_id(self, product_id, qnt):
        query = f"UPDATE products SET quantity = {qnt} WHERE id = {product_id}"
        self.cursor.execute(query)
        self.connection.commit()
    

    def select_product_qnt_by_id(self, product_id):
        query = f"SELECT quantity FROM products WHERE id = {product_id}"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record
    

    def insert_product(self, product_id, name, description, qnt):
        query = f"INSERT OR REPLACE INTO products (id, name, description, quantity) \
            VALUES ({product_id}, '{name}', '{description}', {qnt})"
        self.cursor.execute(query)
        self.connection.commit()


    def delete_product_by_id(self, product_id):
        query = f"DELETE FROM products WHERE id = {product_id}"
        self.cursor.execute(query)
        self.connection.commit()


    def get_detailed_orders(self):
        query = "SELECT orders.id, customers.name, products.name, \
                products.description, orders.order_date \
                FROM orders \
                JOIN customers ON orders.customer_id = customers.id \
                JOIN products ON orders.product_id = products.id"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record

    # individual.
    # додає значення неправильного типу у вказану таблицю і колонку 
    def insert_invalid_type(self, table, column, value):
        try:
            query = f"INSERT INTO {table} ({column}) VALUES (?);"
            self.cursor.execute(query, (value,))
            self.connection.commit()
            # щоб не спричиняло помилку TypeError
            return None # повертає None, якщо помилки немає
        except sqlite3.Error as e:
            return str(e) # повертає повідомлення про помилку як рядок
        

    # додає дані до вказаної таблиці та перевіряє їх коректне додавання
    def insert_and_validate_data(self, table, column, value):
        try:
            query = f"INSERT INTO {table} ({column}) VALUES (?);"
            self.cursor.execute(query, (value,))
            self.connection.commit()

            # перевірка даних, що додали
            select_query = f"SELECT {column} FROM {table} ORDER BY ROWID DESC LIMIT 1;"
            self.cursor.execute(select_query)
            inserted_value = self.cursor.fetchone()[0]
            return inserted_value
        except sqlite3.Error as e:
            return str(e)
        

    # вставляє нові значення якщо такий запис вже існує
    def insert_product(self, product_id, name, description, qnt):
        query = f"INSERT OR REPLACE INTO products (id, name, description, quantity) VALUES ({product_id}, '{name}', '{description}', {qnt})"
        self.cursor.execute(query) # взаємодіє з базою даних виконуючи SQL-запит через об'єкт cursor
        self.connection.commit() # підтверджує зміни в базі даних після виконання запиту; без цього виклику зміни не будуть збережені



    # отримує всі дані про продукт
    def get_product_by_id(self, product_id):
        query = f"SELECT * FROM products WHERE id = {product_id}"
        self.cursor.execute(query) # виконує запит
        return self.cursor.fetchall() # повертає всі рядки, що відповідають запиту у вигляді списку
    

    # отримує кількість товару 
    def validate_quantity_is_positive(self, product_id):
        query = f"SELECT quantity FROM products WHERE id = {product_id}"
        self.cursor.execute(query) # виконує запит
        quantity = self.cursor.fetchone()[0] # отримує перший результат запиту,а також доступ до кількості товару  
        return quantity > 0 # істина,якщо більше нуля і похибка - якщо менше
    

    # вставляє дані
    def insert_data(self, table, columns, data):
        try:
            query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['?'] * len(data))})"
            self.cursor.execute(query, data)
            self.connection.commit()
        except sqlite3.Error as e:
            return str(e)
        return None
    

    # отримуємо загальну к-сть рядків
    def get_total_rows(self, table):
        query = f"SELECT COUNT(*) FROM {table}"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    

    # отримує запис за id
    def get_data_by_id(self, table, record_id):
        query = f"SELECT * FROM {table} WHERE id = ?"
        self.cursor.execute(query, (record_id,))
        return self.cursor.fetchone()
        

    # формує запит щоб отримати всі продукти,де кількість товару більша або дорівнює min_gnt
    def get_all_products_with_minimum_quantity(self, min_qnt):
        query = f"SELECT * FROM products WHERE quantity >= {min_qnt}"
        self.cursor.execute(query) # виконує запит
        return self.cursor.fetchall() # повертає всі рядки, які відповідають запиту у вигляді списку
    

    # отримує список існуючих id з вказаної таблиці
    def get_existing_ids(self, table_name):
        query = f"SELECT id FROM {table_name}"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]
    

    # вставляє кілька замовлень(параметр ? для запобігання SQl-ін'єкціям)
    def insert_bulk_orders(self, orders):
        query = "INSERT INTO orders (customer_id, product_id, order_date) VALUES (?, ?, ?)"
        # використовуємо метод executemany щоб вставити одночасно кілька записів
        self.cursor.executemany(query, orders) # orders - список кортежів,що містить значення для одного замовлення
        self.connection.commit() # підтверджує зміни


    # отримує кількість всіх замовлень в orders
    def get_total_orders_count(self):
        query = "SELECT COUNT(*) FROM orders"
        self.cursor.execute(query) #виконує запит
        return self.cursor.fetchone()[0] # повертає перший результат запиту(кількість замовлень)
    

    # пошук всіх клієнтів чиє ім'я містить partial_name
    def get_customer_by_partial_name(self, partial_name):
        # LIKE % для пошуку за частковим збігом(за частиною імені) 
        query = f"SELECT * FROM customers WHERE name LIKE '%{partial_name}%'"
        self.cursor.execute(query) # виконує запит
        return self.cursor.fetchall() # повертає рядки, які відповідають запиту 


    # додає новий запис у таблицю orders
    def insert_order(self, order_id, customer_id, product_id, order_date):
        # SQL-запит щоб вставити нове замовлення
        query = f"INSERT INTO orders (id,customer_id, product_id, order_date) \
        VALUES ({order_id}, {customer_id}, {product_id}, '{order_date}');"
        try:
            self.cursor.execute(query)# виконує запит
            self.connection.commit() # фіксує зміни
        except sqlite3.Error as e:
            # виключення з детальним описом в разі помилки 
            raise sqlite3.Error(f"Failed to insert order {order_id}. Error: {e}")    
             

    
