import sqlite3 as sql

conn = sql.connect('jdp.db')
cur = conn.cursor()
cur.execute("""DROP table passwords;""")
# Création de la table de mots de passe
cur.execute("""
CREATE TABLE passwords(
password text,
screen_name text,
unlocked boolean);
""")
conn.commit()

# Insertion des mots de passe
cur.execute("""INSERT INTO passwords VALUES 
('http://fr.wikipedia.org/','wiki',0),
('http://www.unitaglive.com','unitag',0)
;""")
conn.commit()
conn.close()
