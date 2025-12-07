import sqlite3
conn=sqlite3.connect("inventory.db")
cur=conn.cursor()
cur.execute('''
  CREATE TABLE IF NOT EXISTS items(
  sn INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  price REAL NOT NULL,
  total REAL NOT NULL
  );
''')

cur.execute('''
 CREATE TABLE IF NOT EXISTS user(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 firstname TEXT NOT NULL,
 lastname TEXT NOT NULL,
 username TEXT NOT NULL,
 address TEXT NOT NULL,
 phone_no TEXT NOT NULL,
 email TEXT NOT NULL,
 new_password TEXT NOT NULL,
 confirm_password TEXT NOT NULL,
 gender TEXT
);
''')

conn.commit()
conn.close()