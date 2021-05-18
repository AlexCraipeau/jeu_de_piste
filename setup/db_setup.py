import sqlite3 as sql

conn = sql.connect('../jdp.db')
cur = conn.cursor()
# Création de la table de mots de passe
cur.execute("""
CREATE TABLE passwords(
password text,
screen_name text,
command text,
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
('http://fr.wikipedia.org/','wiki','',0),
('http://www.unitaglive.com','unitag','',0),
('test','test','',0),
('init','init','',1),
('enigme_map','enigme_map','clear_enigme_map(App.get_running_app().root)',0),
('log_2','log_2','add_log(App.get_running_app().root, search_log("log_2"))',0),
('log_3','log_3','clear_enigme_2(App.get_running_app().root)',0),
('log_4','log_4','',0),
('log_5','log_5','',0),
('log_6','log_6','',0),
('log_7','log_7','',0),
('log_8','log_8','',0),
('log_9','log_9','',0),
('log_19','log_10','',0),
('log_11','log_11','',0),
('log_12','log_12','',0),
('log_13','log_13','',0),
('log_14','log_14','',0),
('log_15','log_15','',0),
('log_16','log_16','',0),
('log_17','log_17','',0)
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
('enigme_map', 'carte complétée', 'clear_enigme_map(screen_manager)', 0),
('enigme_2', 'labyrinthe ouvert', 'clear_enigme_2(screen_manager)', 0),
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
('enigme_map', 'Vous avez fait preuve de [color=#ff0000]CURIOSITE[/color].
Au contact de l’inconnu, vous souhaitez apprendre et comprendre.
Vous êtes prêts. Votre voyage commence…', 1),
('log_2', 'De la mer jusqu’aux cieux, des plus grands hommes aux plus petits insectes, chaque chose à son rôle et sa leçon à apporter.
A la croisée des mondes, vous découvrirez une nouvelle vérité.', 2),
('log_3', 'log 3 - [color=#ff7f00]DETERMINATION[/color]', 3),
('log_4', 'log 4 - début énigme 2 (analyse de fable)', 4),
('log_5', 'La carte est complétée', 5),
('log_6', 'La carte est complétée', 6),
('log_7', 'La carte est complétée', 7),
('log_8', 'La carte est complétée', 8),
('log_9', 'La carte est complétée', 9),
('log_10', 'La carte est complétée', 10),
('log_11', 'La carte est complétée', 11),
('log_12', 'La carte est complétée', 12),
('log_13', 'La carte est complétée', 13),
('log_14', 'La carte est complétée', 14),
('log_15', 'La carte est complétée', 15),
('log_16', 'La carte est complétée', 16)
;""")
conn.commit()


conn.close()
