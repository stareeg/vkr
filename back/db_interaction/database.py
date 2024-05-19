import random
from datetime import datetime, timedelta
import psycopg2

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Функция для генерации данных
def generate_data():
    # Генерация данных для таблицы StorageZones
    zone_types = ['Холодное хранение', 'Сухое хранение', 'Охлаждаемое хранение']
    for _ in range(350):
        zone_type = random.choice(zone_types)
        zone_size = round(random.uniform(50.0, 300.0), 1)
        cursor.execute('INSERT INTO StorageZones (zone_type, zone_size) VALUES (%s, %s)', (zone_type, zone_size))
    
    # Генерация данных для таблицы StorageStages
    stages = ['Принят', 'В обработке', 'Хранится', 'Отправлен']
    for stage in stages:
        cursor.execute('INSERT INTO StorageStages (description) VALUES (%s)', (stage,))
    
    # Генерация данных для таблицы Clients
    company_names = ['ООО "Техносфера"', 'ЗАО "Металлокомплект"', 'ОАО "ЭнергоСервис"', 'ИП Иванов И.И.', 'АО "КабельЭлектро"']
    for _ in range(300):
        name = random.choice(company_names)
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        delivery_address = f"ул. {random.choice(['Ленина', 'Советская', 'Пушкина', 'Кирова'])}, д. {random.randint(1, 100)}, г. {random.choice(['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань'])}"
        cursor.execute('INSERT INTO Clients (name, phone, delivery_address) VALUES (%s, %s, %s)', (name, phone, delivery_address))
    
    # Генерация данных для таблицы Products
    for _ in range(500):
        production_date = datetime.now() - timedelta(days=random.randint(1, 365*10))
        report_date = production_date + timedelta(days=random.randint(1, 10))
        storage_change_date = report_date + timedelta(days=random.randint(1, 5))
        storage_zone = random.randint(1, 3)
        storage_stage = random.randint(1, 4)
        initial_cable_material = random.choice(['Медь', 'Алюминий'])
        initial_cable_length = round(random.uniform(50, 200), 1)
        initial_cable_diameter = round(random.uniform(1, 20), 1)
        product_size = round(random.uniform(10, 500), 1)
        cursor.execute('''INSERT INTO Products 
                          (name, brand_id, manufacturer, is_written_off, production_date, report_date, storage_change_date, 
                           storage_zone, storage_stage, initial_cable_material, initial_cable_length, initial_cable_diameter, product_size) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                       ("Кабель", random.randint(100, 200), "ЗАО \"МеталлоПрофиль\"", False, production_date, report_date, storage_change_date, 
                        storage_zone, storage_stage, initial_cable_material, initial_cable_length, initial_cable_diameter, product_size))
    
    # Генерация данных для таблицы DisposedProducts
    for _ in range(150):
        production_date = datetime.now() - timedelta(days=random.randint(1, 365*10))
        report_date = production_date + timedelta(days=random.randint(1, 10))
        storage_change_date = report_date + timedelta(days=random.randint(1, 5))
        cable_material = random.choice(['Медь', 'Алюминий'])
        cable_length = round(random.uniform(50, 200), 1)
        cable_diameter = round(random.uniform(1, 20), 1)
        disposal_reason = random.choice(['Поврежден', 'Просрочен'])
        cursor.execute('''INSERT INTO DisposedProducts 
                          (name, brand_id, manufacturer, production_date, report_date, storage_change_date, 
                           cable_material, cable_length, cable_diameter, disposal_reason) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                       ("Старый кабель", random.randint(100, 200), "ОАО \"ЭнергоСервис\"", production_date, report_date, storage_change_date, 
                        cable_material, cable_length, cable_diameter, disposal_reason))
    
    # Генерация данных для таблицы Orders
    for _ in range(200):
        start_date = datetime.now() - timedelta(days=random.randint(1, 365))
        end_date = start_date + timedelta(days=random.randint(1, 10))
        order_cable_material = random.choice(['Медь', 'Алюминий'])
        order_cable_length = round(random.uniform(50, 200), 1)
        order_cable_diameter = round(random.uniform(1, 20), 1)
        cursor.execute('''INSERT INTO Orders 
                          (name, client_id, product_id, start_date, end_date, order_cable_material, order_cable_length, order_cable_diameter) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                       ("Заказ на кабель", random.randint(1, 300), random.randint(1, 500), start_date, end_date, order_cable_material, order_cable_length, order_cable_diameter))
    
    # Генерация данных для таблицы Sensors с использованием нормального распределения Гаусса
    for _ in range(100):
        model = f"Сенсор-{random.randint(1000, 9999)}"
        manufacturer = random.choice(["ООО \"ТехноСенсор\"", "АО \"Сенсорные Системы\"", "ЗАО \"ПромСенсор\""])
        zone_id = random.randint(1, 350)
        min_value = round(random.normalvariate(20, 5), 2)   # Генерация случайных данных с нормальным распределением
        max_value = min_value + round(random.normalvariate(10, 2), 2)   # Генерация случайных данных с нормальным распределением
        cursor.execute('INSERT INTO Sensors (model, manufacturer, zone_id, min_value, max_value) VALUES (%s, %s, %s, %s, %s)', 
                       (model, manufacturer, zone_id, min_value, max_value))
    
    # Закоммитить изменения в базе данных
    conn.commit()

# Запуск функции для генерации данных
generate_data()

# Закрытие соединения с базой данных
cursor.close()
conn.close()

### Описание:
# 1. **Импорт библиотек:** Подключаем библиотеки для работы с PostgreSQL (`psycopg2`) и для генерации данных (`faker`).
# 2. **Настройка подключения к базе данных PostgreSQL:** Заполняем данные для подключения (имя базы данных, пользователь, пароль, хост, порт). Замените `your_database`, `your_username`, `your_password`, `your_host`, `your_port` на фактические значения вашей базы данных.
# 3. **Функция `generate_data`:** 
#     - Используем цикл для вставки данных в каждую таблицу.
#     - Генерируем случайные данные с использованием библиотеки Faker.
#     - Вставляем данные в базу с помощью SQL-запросов.
# 4. **Вызов функции `generate_data` и коммит изменений:** Генерируем данные и сохраняем их в базу данных.
# 5. **Закрытие соединения:** Закрываем соединение с базой данных.

# Перед выполнением скрипта, убедитесь, что у вас настроена база данных PostgreSQL и есть все необходимые таблицы. Скрипт примерочный, его можно адаптировать под свои нужды.