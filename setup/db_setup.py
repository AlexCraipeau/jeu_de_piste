import sqlite3 as sql

conn = sql.connect('jdp.db')
cur = conn.cursor()
# Création de la table de mots de passe
cur.execute("""
CREATE TABLE passwords(
password text,
screen_name text,
unlocked boolean);
""")
conn.commit()

# Création d'une table de temps
cur.execute("""
CREATE TABLE time(
start_time text);
""")
conn.commit()

# Insertion des mots de passe
cur.execute("""INSERT INTO passwords VALUES 
('http://fr.wikipedia.org/','wiki',0),
('http://www.unitaglive.com','unitag',0)
;""")
conn.commit()
conn.close()
