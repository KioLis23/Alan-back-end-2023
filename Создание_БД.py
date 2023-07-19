import sqlite3
import random
import string
import os

conn = sqlite3.connect('BD_New.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Warehouse (
    id INTEGER PRIMARY KEY,
    name TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Company (
    id INTEGER PRIMARY KEY,
    name TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
    id INTEGER PRIMARY KEY,
    name TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Sales (
    date DATE,
    sales_sum REAL,
    amount INTEGER,
    product_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES Product(id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ProductSegmentation (
    product_id INTEGER,
    segment_name TEXT,
    FOREIGN KEY (product_id) REFERENCES Product(id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Stock (
    date DATE,
    product_id INTEGER,
    value INTEGER,
    warehouse_id INTEGER,
    company_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES Product(id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(id),
    FOREIGN KEY (company_id) REFERENCES Company(id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ProductMovement (
    date DATE,
    product_id INTEGER,
    in_value INTEGER,
    out_value INTEGER,
    type BOOLEAN,
    FOREIGN KEY (product_id) REFERENCES Product(id)
)''')

for i in range(2):
    name = ''.join(random.choices(string.ascii_uppercase, k=5))
    cursor.execute("INSERT INTO Warehouse (name) VALUES (?)", (name,))

for i in range(2):
    name = ''.join(random.choices(string.ascii_uppercase, k=5))
    cursor.execute("INSERT INTO Company (name) VALUES (?)", (name,))

for i in range(21):
    name = ''.join(random.choices(string.ascii_uppercase, k=5))
    cursor.execute("INSERT INTO Product (name) VALUES (?)", (name,))

for i in range(100):
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    year = random.randrange(2018,2022,1)
    date = f"{year:02d}-{month:02d}-{day:02d}"
    product_id = random.randint(1, 21)
    sales_sum = round(random.uniform(1000, 5000), 2)
    amount = random.randint(1, 100)
    in_value = random.randint(1, 100)
    out_value = random.randint(1, in_value - 1)  # Генерация случайного значения out_value меньше in_value
    
    if in_value <= out_value:
        in_value = out_value + 1

    cursor.execute("INSERT INTO Sales (date, sales_sum, amount, product_id) VALUES (?, ?, ?, ?)", (date, sales_sum, amount, product_id))
    cursor.execute("INSERT INTO Stock (date, product_id, value, warehouse_id, company_id) VALUES (?, ?, ?, ?, ?)", (date, product_id, amount, random.randint(1, 2), random.randint(1, 2)))
    cursor.execute("INSERT INTO ProductMovement (date, product_id, in_value, out_value, type) VALUES (?, ?, ?, ?, ?)", (date, product_id, in_value, out_value, random.choice([True, False])))

segment_names = random.sample(set(string.ascii_uppercase), 3)
for product_id in range(1, 22):
    segment_name = random.choice(segment_names)
    cursor.execute("INSERT INTO ProductSegmentation (product_id, segment_name) VALUES (?, ?)", (product_id, segment_name))

conn.commit()
conn.close()

os.rename('BD_New.db', 'BD_New.sqlite3')
