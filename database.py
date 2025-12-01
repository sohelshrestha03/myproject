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

conn.commit()
conn.close()