import sqlite3 as sql

conn = sql.connect('../jdp.db')
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

# Insertion des mots de passe
cur.execute("""INSERT INTO passwords VALUES 
('http://fr.wikipedia.org/','wiki',0),
('http://www.unitaglive.com','unitag',0),
('test','test',0),
('bite','tralala',0)
;""")
conn.commit()

# Création d'une table d'avancement des enigmes
cur.execute("""
CREATE TABLE enigmes(
name text,
desc text,
command text,
cleared boolean);
""")
conn.commit()

#Insertion des enigmes
cur.execute("""INSERT INTO enigmes VALUES 
('enigme_map', 'carte complétée', 'clear_enigme_map()', 0),
('test', 'test pour unlock au lancement app', 'print("ca fonctionne")', 1)
;""")
conn.commit()

# Création d'une table des textes
cur.execute("""
CREATE TABLE textes(
password text,
texte text,
position numeric);
""")
conn.commit()

#Insertion des textes
cur.execute("""INSERT INTO textes VALUES 
('init', 'Il était une fois...', 0),
('enigme_map', 'La carte est complétée', 1)
;""")
conn.commit()


conn.close()
