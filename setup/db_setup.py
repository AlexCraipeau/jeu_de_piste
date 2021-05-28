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
('log_2','log_2','',0),
('cross_ciel','cross_ciel','show_cross(App.get_running_app().root, "cross_ciel")',0),
('cross_statue','cross_statue','show_cross(App.get_running_app().root, "cross_statue")',0),
('cross_marais','cross_marais','show_cross(App.get_running_app().root, "cross_marais")',0),
('log_3','log_3','clear_enigme_2_laby(App.get_running_app().root)',0),
('log_4','log_4','',0),
('log_5','log_5','clear_enigme_3_analyse(App.get_running_app().root)',0),
('log_6','log_6','',0),
('log_7','log_7','',0),
('log_8','log_8','clear_enigme_4_pigpen(App.get_running_app().root)',0),
('log_8b','log_8b','',0),
('log_9','log_9','clear_enigme_5_cryptex(App.get_running_app().root)',0),
('log_9b','log_9b','',0),
('log_10','log_10','init_enigme_6_lievre(App.get_running_app().root)',0),
('log_11','log_11','clear_enigme_6_lievre(App.get_running_app().root)',0),
('log_12','log_12','',0),
('log_13','log_13','clear_enigme_7_dessin(App.get_running_app().root)',0),
('arcenciel','arcenciel','clear_enigme_7_dessin(App.get_running_app().root)',0),
('log_14','log_14','',0)
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
('enigme_2', 'labyrinthe ouvert', 'clear_enigme_2_laby(screen_manager)', 0),
('enigme_3', 'analyse effectuée', 'clear_enigme_3_analyse(screen_manager)', 0),
('enigme_4', 'pigpen cracké', 'clear_enigme_4_pigpen(screen_manager)', 0),
('enigme_5', 'cryptex récupéré', 'clear_enigme_5_cryptex(screen_manager)', 0),
('init_enigme_6', 'début énigme 6', 'init_enigme_6_lievre(screen_manager)',0),
('enigme_6', 'lievre complété', 'clear_enigme_6_lievre(screen_manager)', 0),
('enigme_7', 'dessin complété', 'clear_enigme_7_dessin(screen_manager)', 0),
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
('init', "Jeune Moineau,
Voyant de son âge poindre le printemps
S’en alla par monts et par vaux 
Découvrir ce monde exaltant.
Quitta sa jungle natale,
But aux sources des grandes montagnes,
Survola les murailles colossales
Et les vastes campagnes,
Traversant champs et villes
Jusqu’à un jardin luxuriant.
S’abrita sous un toit, lui procurant asile
Puis monta jusqu’au firmament,
Royaume des dieux et des anges.
Tout cela était songe - prémonition étrange.
L’œuf n’avait pas encore éclot.
 
Toi aussi voyageur, garde l’esprit curieux,
Cherche les signes de cet étrange pays
Dont jeune Moineau a rêvé quelques lieux
Avant même de commencer sa vie.
", 0),

('enigme_map', "Aujourd’hui, j’ai fait preuve de [color=#ff0000]CURIOSITE[/color]. 
Ce grand saut dans l’inconnu ne fait que nourrir ma soif d’apprendre et de comprendre. 
Je sens que je suis prêt. Mon voyage commence.
", 1),
('log_2', "Il m’est venu une réflexion curieuse : De la mer jusqu’aux cieux, des plus grands hommes aux plus petits insectes, chaque chose à son rôle et sa leçon à apporter.
En me mettant à la croisée de ces mondes, m’approcherai-je d’une vérité nouvelle ?
", 2),
('log_3', "Enfin, ma [color=#ff7f00]DETERMINATION[/color] a payé ! 
Face à l’immensité et la complexité de ce monde, la persévérance est une vertu nécessaire.
", 3),
('log_4', "À chaque jour suffit sa peine. 
L’atmosphère des marais pèse sur mon esprit et mon corps aspire à un peu de fraîcheur. Un retour aux sources serait une délivrance. 
J'accueillerais avec joie une oreille attentive : ma quête de vérité ne saurait être solitaire - il me faut en faire part à mes pairs.
Découvrir leur pensée, récolter leur point de vue - Il n’y aura qu’ainsi que je progresserai.
", 4),
('log_5', "Lire entre les lignes n’est pas une évidence. Pour percer les secrets de ce monde, d’aucun doit faire preuve de [color=#ffff00]DISCERNEMENT[/color]. 
Mon ami le Moineau s’en est-il rendu compte ?
Mon apprentissage continuant, une question me taraude. 
A-t-il réussi à réaliser ses rêves ? Il me faut le savoir. En fut-il capable ? 
Et moi, le serai-je ?
", 5),
('log_6', "Aux abords d’une source, j’ai retrouvé sa trace. 
D’infimes marques de pattes, encore bien dessinées. 
A mon instar, Moineau semble bien suivre son propre chemin. 
Si je souhaite le revoir, je ne peux juste le suivre. 
Sa destination doit être celle de mes songes. Je l’y attendrai. 
", 6),
('log_7', "Funeste découverte : Le corps de Moineau, inerte. 
Mon cœur est lourd mais son visage, serein. Est-ce une coïncidence ? 
Ce ne peut être ici la fin de l’aventure. L’histoire est incomplète : c’est certain. 
Peut-être a-t-il laissé dans ce fécond jardin un indice, un moyen d’en découvrir la suite.
", 7),
('log_8', "De l’oeuf que j’ai trouvé, un oisillon est sorti. La descendance de Moineau, nul doute. Il semble au courant de ma quête. 
A-t-il rêvé de moi comme j’ai rêvé de son père ?
Cette [color=#00ff00]EMPATHIE[/color] que je ressens m’offre un regard nouveau sur la nature. 
A peine ai-je le temps de me faire cette réflexion que jeune Moineau voltige autour de moi. 
Lui reste-t-il des choses à dire ? 
", 8),
('log_8b', "Moineau est parti. 
Je l’ai suivi jusqu’à trois soeurs. 
Il s’est posé sur la cadette avant de me faire ses adieux. 
L’air solennel, la jeune femme semblait scruter en contrebas. 
A-t-elle perdu quelque chose ?", 9),
('log_9',"Prenant mon courage à deux mains, j’ai descendu la ravine. 
Sous un buisson, un éclat a attiré mon regard. 
Ce fut périlleux, mais ma [color=#0000ff]BRAVOURE[/color] fut récompensée par un étrange artefact. 
Un curieux cylindre recouvert de lettres, semblant abriter quelque secret.
Longtemps, j’ai essayé d’en percer les mystères, mais rien n’y fait. 
Impossible de l’ouvrir.
", 10),
('log_9b', "Rongé par la frustration, je remontais le chemin escarpé. La jeune femme ressentit mon trouble. 
    - <<Voyageur, tu as trouvé un trésor dont il te manque la clé. 
    Une telle énigme est excitante, pourquoi cette colère ?>>
Ces mots me plongèrent dans une profonde réflexion. 
Jadis, j’aurais chéri un tel jeu, cherchant jour et nuit à résoudre ce problème. 
Où donc est passée mon âme d’enfant ?
", 11),
('log_10',"J’errais au hasard, absorbé par ce problème, quand je me rendis compte que mes pas m’avaient mené près du lieu où, enfant, je vivais mes aventures. 
Une nouvelle génération semble avoir pris le relais.
Sur l’un des murs, des symboles étranges et familiers sont inscrits. 
Les décoder me permettrait-il d’enfin connaître le contenu du cylindre ?
", 12),
('log_11', "Quel imbécile ! Ces 'symboles' que je voyais n’étaient que gribouillages. 
J’aurais dû faire preuve de [color=#2e2b5f]PATIENCE[/color]. 
Il me faut voir les choses sous un autre angle. 
Tel ces enfants qui ont imaginé ce langage, je dois prendre de la hauteur et penser hors des sentiers battus. 
Je vais repartir m’imprégner à nouveau de ce que monde a à offrir.
", 13),
('log_12', "Voilà donc ce qu’il me manquait : l’[color=#8b00ff]IMAGINATION[/color].
Parcourir les chemins, découvrir ces paysages m’a fait voir les choses sous un autre angle : 
les sons, les couleurs, les symboles se mêlent et se répondent. 
Un message qui se révèle à qui sait le lire. 
", 14),
('log_13', "J’ai suivi un arc-en-ciel par delà les remparts. A son pied veillait un ange, protecteur et bienveillant, qui me tint ces propos :
    - <<Des lacs infinis aux montagnes de feu, de l’air que tu respires à la terre que tu foules, tout n’est qu’un.
    Fais tienne cette sagesse que je te confie, et mène ta quête à sa fin.>>
", 15),
('log_14', "Enfin ! J’ai découvert le contenu du cylindre. 
Nul trésor ni richesse, mais un parchemin vierge. 
Ironique découverte ! 
Moi qui cherchais la vérité, entière et nue, il semblerait que la tâche me revienne de la révéler. 
Et bien soit ! 
J’accepte mon destin. 
De par mes expériences, je tirerai des maximes, des leçons à transmettre aux miens. 
Ici-même je créerai la première, cachée pour qui comme moi a cherché des réponses.
Non loin de l'ange, au pied de l'arc-en-ciel, résident les filles d'Atlas. Elles y tiennent le ciel
duquel coulent les flots. Je leur confierai mon oeuvre.
", 16)
;""")
conn.commit()

conn.close()
