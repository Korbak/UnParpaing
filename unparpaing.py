#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Basé sur le travail d'Angristan & Shevabam
# check https://github.com/shevabam/TweetBoxBot/
# check https://github.com/Angristan/AngristanRPiBot

import urllib, urlparse, json, random, os, time, sys, string
from twython import Twython

# CONFIGURATION TWITTER

CONSUMER_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CONSUMER_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ACCESS_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ACCESS_TOKEN_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Catégories des gifs (giphy.com)
GIF_CATEGORIES = ["computer", "network", "hacker", "fail", "code", "unicorn", "cat"]

# Fichier temporaire où seront stockés les URL des gifs
TMP_FILE = "/tmp/unprpg_tmp"

# Hashtags
TWITTER_SUFFIX = ""

# Fichier de log / débug
DEBUG = False
DEBUG_FILE = "UnParpaing.log"

# Return taille humaine
def sizeToHuman(num, suffix='B'):
	for unit in ['','K','M','G','T','P','E','Z']:
		if abs(num) < 1024.0:
			return "%3.2f %s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.2f %s%s" % (num, 'Y', suffix)

# Twitter initiator
def twitter():
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return twitter;

# Uptime
def uptime():
	try:
		f = open("/proc/uptime")
		contents = f.read().split()
		f.close()
	except:
		return

	total_seconds = float(contents[0])

	# Helper vars
	MINUTE = 60
	HOUR = MINUTE * 60
	DAY = HOUR * 24

	# Transformation de l'uptime en jours, heures, etc
	days = int(total_seconds / DAY)
	hours = int((total_seconds % DAY) / HOUR)
	minutes = int((total_seconds % HOUR) / MINUTE)
	seconds = int(total_seconds % MINUTE)

	# Création de la chaîne
	uptime = ""
	if days > 0:
		uptime += str(days) + " jour" + (days > 1 and "s" or "") + ", "
	if len(uptime) > 0 or hours > 0:
		uptime += str(hours) + " heure" + (hours > 1 and "s" or "") + ", "
	if len(uptime) > 0 or minutes > 0:
		uptime += str(minutes) + " minute" + (minutes > 1 and "s" or "") + ", "
	uptime += str(seconds) + " seconde" + (seconds > 1 and "s" or "")

	content = "Je tiens le coup depuis " + uptime + " ! #uptime"
	media = ""

	return content, media;

# CPU Load
def cpu_load():
	nb_cores = int(os.popen('cat /proc/cpuinfo | grep "^processor" | wc -l').read().strip())
	load = os.getloadavg()

	load1 = (load[0] * 100) / nb_cores
	if load1 > 100:
		load1 = 100

	load5 = (load[1] * 100) / nb_cores
	if load5 > 100:
		load5 = 100

	load15 = (load[2] * 100) / nb_cores
	if load15 > 100:
		load15 = 100

	content = "Charge du CPU : \nDepuis 1 minute: " + str(int(load1)) + "%\nDepuis 5 minutes: " + str(int(load5)) + "%\nDepuis 15 minutes : " + str(int(load15)) + "%"
	media = ""

	return content, media;

# CPU Temp
def cpu_temp():
	cpu_temp = ""

	#oLimex
	if os.path.isfile("/sys/class/thermal/thermal_zone0/temp"):
		cpu_temp = os.popen('cat /sys/class/thermal/thermal_zone0/temp').read().strip()
		cpu_temp = round(float(cpu_temp) / 1000, 2)

	# Si lm-sensors est installé
	elif os.path.isfile("/usr/bin/sensors"):
		cpu_temp = os.popen('/usr/bin/sensors | grep -E "^(CPU Temp|Core 0)" | cut -d \'+\' -f2 | cut -d \'.\' -f1').read().strip()

	if not cpu_temp:
		cpu_temp = "non-connue, disons 42"

	content = "Température actuelle du CPU : " + str(cpu_temp) + " °C"
	media = ""

	return content, media;

# Charge RAM
def mem_load():
	# total
	total = os.popen('grep MemTotal /proc/meminfo | awk \'{print $2}\'').readline().strip()
	total = long(total) * 1024

	# free = free + buffers + cached
	free = os.popen('grep MemFree /proc/meminfo | awk \'{print $2}\'').readline().strip()
	buffers = os.popen('grep Buffers /proc/meminfo | awk \'{print $2}\'').readline().strip()
	cached = os.popen('grep Cached /proc/meminfo | awk \'{print $2}\'').readline().strip()

	free = long(free) + long(buffers) + long(cached)
	free = free * 1024

	content = "J'ai " + str(sizeToHuman(free)) + " de RAM libre sur " + str(sizeToHuman(total))
	media = ""

	return content, media;

# Kernel version
def kernel():
	kernel = os.popen("uname -r").read().strip()

	content = "La version de mon #kernel est " + kernel
	media = ""

	return content, media;

# Quelques gifs random
def gif():
	category = random.choice(GIF_CATEGORIES)

	datas = json.loads(urllib.urlopen("http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=" + category).read())
	random_gif = datas['data']['image_original_url']

	urllib.urlretrieve(random_gif, TMP_FILE + '.gif')

	content = "Mood"
	media = TMP_FILE + '.gif'

	return content, media;

# RT si c digital
def digital():
    tw = twitter()
    search_results = tw.search(q='digital OR digitale -filter:retweets', count=200, lang='fr', result_type='mixed')
    mot_precedent = ""
    liste_tweets = []
    i = 0
    try:
        # On crée une liste contenant les résultats
        for tweet in search_results["statuses"]:
            liste_tweets.insert(i, tweet)
            i += 1
        # On tire un tweet au hasard
        tweet = liste_tweets[random.randint(0,len(liste_tweets))-1]
        # On crée le RT
        texte = tweet["text"]
        quote_id = tweet["id_str"]
        user_id = tweet["user"]["id_str"]
        texte = texte.lower()
        splitexte = [x.strip(string.punctuation) for x in texte.split()]
        digitale = "digitale"
        digital = "digital"
        if digitale in texte:
            mot_precedent = splitexte[splitexte.index("digitale") -1]
            if mot_precedent == 'la':
                mot_precedent = "Digitale, mais"
        elif digital in texte:
            mot_precedent = splitexte[splitexte.index("digital") - 1]
            if mot_precedent == 'le' or mot_precedent == 'du' or mot_precedent == 'au':
                mot_precedent = "Le digital"
        else:
            mot_precedent = "Digital"
    except :
        return
    content = (mot_precedent + " avec les doigts !" + " http://twitter.com/" + user_id + "/status/" + quote_id).capitalize()
    media = ""
    return content, media;

# Quote Kaamelott
def kaamelott():
    citations_kaamelott = open('kaamelott.txt', 'r').read().split('%')
    quote = ""
    while quote == "" or len(quote) > 129:
        quote = (random.choice(citations_kaamelott))
    content = quote + "#Kaamelott"
    media = ""
    return content, media

# Tweete comme @Your_Twitter_Name
def fakeYourTwitterName():
    # Pour des raisons techniques liées à l'API Twitter, la limite par recherche est de 200 tweets
    # On fait donc une boucle de 16x200 tweets, soient 3.200 tweets comme base de travail
    # qu'on insère dans une liste
    tw = twitter()
    liste_tweets = []
    for i in range(0, 16):
        j = len(liste_tweets)
        user_timeline = tw.get_user_timeline(screen_name="Your_Twitter_Name",count=200,include_retweets=False)
        for tweet in user_timeline:
            liste_tweets.insert(j, tweet['text'])
            j += 1
    # On a donc une liste 3.200 tweets, dont on extrait 2 tweets aléatoirement
    first_tweet = liste_tweets[random.randint(0,len(liste_tweets))-1]
    second_tweet = liste_tweets[random.randint(0,len(liste_tweets))-1]
    # On supprime tous les RT (l'option plus haut semble insuffisante ou inefficace)
    while "RT " in first_tweet:
        first_tweet = liste_tweets[random.randint(0,len(liste_tweets))-1]
    while "RT " in second_tweet:
        second_tweet = liste_tweets[random.randint(0,len(liste_tweets))-1]
   # On s'évite les deux tweets identiques
    while first_tweet == second_tweet:
        second_tweet = liste_tweets[random.randint(0,len(liste_tweets))-1]
    # On transforme chaque tweet en liste de mots
    first_tweet = first_tweet.split()
    second_tweet = second_tweet.split()
    # On compose les deux moitiés de contenu et on les rassemble en un tweet final (sans @ ni lien)
    compteur_car = False
    j = 0
    i = len(second_tweet) - 1
    part1 = ""
    while compteur_car == False:
        while "@" in first_tweet[j] or "http" in first_tweet[j]:
            j += 1
        if (len(part1) + len(first_tweet[j])) <= 62:
            if j < (len(first_tweet) - 1):
                part1 = part1 + " " + first_tweet[j]
                j += 1
            else:
                compteur_car = True
        else:
            compteur_car = True
    compteur_car = False
    part2 = ""
    while compteur_car == False and i > 0:
        while "@" in second_tweet[i] or "http" in second_tweet[i]:
            i -= 1
        if (len(part1) + len(part2) + len(second_tweet[i])) >= 124:
            compteur_car = True
        elif i >= 0:
            part2 = second_tweet[i] + " " + part2
        i -= 1
    content = part1 + " " + part2 + " #TweeteCommeMoi"
    media = ""
    return content, media

# Debug log
if DEBUG is True:
	log_file = open(DEBUG_FILE, 'ab+')
	log_gile.write("--- START " + time.strftime("%Y-%m-%d %H:%M:%S") + " ---\n")

# Liste des fonctions
options = [
    "uptime",
    "cpu_load",
    "cpu_temp",
    "mem_load",
    "gif",
    "digital",
    "kaamelott",
    "fakeYourTwitterName",
    "kernel"
]

# Si argument passé
if len(sys.argv) > 1:
	for key, item in enumerate(options):
		if item == sys.argv[1]:
			choice = key

# Sinon, générer un choix aléatoire
if not 'choice' in locals():
	choice = random.randint(0, int(len(options))-1)

# Récupérer le nécessaire en conséquence
content, media = locals()[options[choice]]()

# Debug
if DEBUG is True:
	log_file.write("Choice : " + str(choice) + "\n")
	log_file.write("Function : " + options[choice] + "\n")
	log_file.write("Content : " + content + "\n")
	log_file.write("--- END " + time.strftime("%Y-%m%d %H:%M:%S") + " --- \n\n")
	log_file_close()

# Publication sur Twitter
if content and content.strip() != "":
	twitter = twitter()

	if media:
		photo = open(media, 'rb')
		response = twitter.upload_media(media = photo)
		twitter.update_status(status=content+TWITTER_SUFFIX, media_ids=[response['media_id']])
		os.remove(media)
	else:
		twitter.update_status(status=content+TWITTER_SUFFIX)
