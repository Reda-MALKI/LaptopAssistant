import sqlite3

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

# ---------------------------
# 1️ Drop old tables (clean start)
# ---------------------------
c.execute("DROP TABLE IF EXISTS orders")
c.execute("DROP TABLE IF EXISTS clients")
c.execute("DROP TABLE IF EXISTS laptops")

# ---------------------------
# 2️ Create laptops table
# ---------------------------
c.execute('''
CREATE TABLE laptops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    model TEXT,
    ram TEXT,
    storage TEXT,
    cpu TEXT,
    price INTEGER,
    release_year INTEGER
)
''')

# ---------------------------
# 3️ Insert laptops data
# ---------------------------
laptops_data = [
    ('Dell', 'XPS 13', '16GB', '512GB SSD', 'Intel i7', 1100, 2022),
    ('HP', 'Envy', '16GB', '512GB SSD', 'Intel i7', 900, 2022),
    ('Asus', 'VivoBook', '8GB', '256GB SSD', 'Intel i3', 700, 2021),
    ('Apple', 'MacBook Pro', '16GB', '512GB SSD', 'M1 Pro', 1800, 2022),
]

c.executemany('''
INSERT INTO laptops (brand, model, ram, storage, cpu, price, release_year)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', laptops_data)

# ---------------------------
# 4️ Create clients table
# ---------------------------
c.execute('''
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    city TEXT
)
''')

# ---------------------------
# 5️ Insert Moroccan clients
# ---------------------------
clients_data = [
    ('Reda', 'Malki', 'reda.malki@gmail.com', 'Fès'),
    ('Yassine', 'El Amrani', 'yassine.elamrani@gmail.com', 'Rabat'),
    ('Sara', 'Bennani', 'sara.bennani@gmail.com', 'Casablanca'),
    ('Omar', 'Zerouali', 'omar.zerouali@gmail.com', 'Tanger'),
    ('Khadija', 'Alaoui', 'khadija.alaoui@gmail.com', 'Marrakech'),
]

c.executemany('''
INSERT INTO clients (first_name, last_name, email, city)
VALUES (?, ?, ?, ?)
''', clients_data)

# ---------------------------
# 6️ Create orders table (linked to clients & laptops)
# ---------------------------
c.execute('''
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    laptop_id INTEGER,
    quantity INTEGER,
    status TEXT,
    order_date TEXT,
    delivery_date TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (laptop_id) REFERENCES laptops(id)
)
''')

# ---------------------------
# 7 Insert coherent orders
# ---------------------------
orders_data = [
    # Reda Malki (2 commandes)
    (1, 1, 1, 'delivered', '2025-11-20', '2025-11-25'),
    (1, 4, 1, 'shipped', '2025-12-02', None),

    # Yassine El Amrani (1 commande)
    (2, 2, 2, 'delivered', '2025-10-15', '2025-10-20'),

    # Sara Bennani (1 commande)
    (3, 3, 1, 'pending', '2025-12-01', None),

    # Omar Zerouali (0 commande) 

    # Khadija Alaoui (1 commande)
    (5, 1, 1, 'delivered', '2025-11-10', '2025-11-14'),
]

c.executemany('''
INSERT INTO orders (client_id, laptop_id, quantity, status, order_date, delivery_date)
VALUES (?, ?, ?, ?, ?, ?)
''', orders_data)

# ---------------------------
# 8️ Commit & close
# ---------------------------
conn.commit()
conn.close()

print(" Database created successfully with laptops, clients, and orders!")
