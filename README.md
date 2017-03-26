# UnParpaing
Useless Twitter bot for personnal server

Basé sur le travail d'Angristan & Shevabam

check https://github.com/Angristan/AngristanRPiBot

check https://github.com/shevabam/TweetBoxBot/

Le fichier kaamelott.txt a été créé à partir du fichier de citations généré par F.Tessier (http://www.francoistessier.info/blog/2010/07/22/fortune-et-kaamelott/)

# Projet
Les fonctions suivantes ont été ajoutées au projet de base :
- twitter()
- digital()
- kaamelott()
- fakeYourTwitterName()
- bullshit()

# Twitter()
La fonction twitter() permet de générer un objet Twitter afin d'exécuter les commandes spécifiques à Twython et l'API Twitter. Cela permet de faire des recherches, récupérer des tweets, etc. Cette fonctionnalité n'était pas utilisée dans les versions précédentes du projet. En effet, aucune de celles-ci ne jouaient avec la twittosphère. Le bot parlait dans son coin.

# Digital()
La fonction digital() permet de troller une personne aléatoirement choisie, en quotant son tweet et en se moquant du terme "digital" pour "numérique". La fonction prend le terme précédent digital et ajoutant "avec les doigts" à sa suite.

# Kaamelott()
Le bot lance une citation de Kaamelott au hasard parmis + de 500.

# FakeYourTwitterName()
Le bot prend deux tweets d'un compte Twitter pré-sélectionné, et les mélange entre eux en ajoutant un # associé.

# Bullshit()
Le bot génère aléatoirement une phrase de bullshit-language au sujet des nouvelles technologies, sauce webmarketing.

# Pour croner la bête
Personnellement, j'ai simplement créé un script bash exécutant la commande python unparpaing.py dans /etc/cron.hourly. Si vous voulez vous amuser un peu plus, Shevabam (lien git en haut du fichier README.md) avait prévu un fonctionnement aléatoire entre 1h30 et 11h30.
