# WebDeck

Le WebDeck est une application Flask qui permet à l'utilisateur de contrôler son ordinateur à distance depuis n'importe quel appareil doté d'un navigateur et d'un écran tactile. Contrairement au StreamDeck d'Elgato, qui nécessite un équipement physique, le WebDeck utilise une application Flask que l'utilisateur héberge sur son propre ordinateur.

## Installation
1. Clonez le dépôt git en utilisant `git clone https://github.com/LeLenoch/WebDeck-PRE-RELEASE.git` ou en téléchargant le [fichier ZIP](https://github.com/LeLenoch/WebDeck-PRE-RELEASE/archive/refs/heads/main.zip)

2. Accédez au dossier du projet : `cd webdeck`

3. Installez les dépendances nécessaires avec `pip install -r requirements.txt`

4. Exécutez le programme en utilisant `python main.py`

5. Ouvrez votre navigateur web préféré sur votre appareil et accédez à l'URL http://IP:PORT/, remplacez IP par l'ip locale de votre ordinateur (s'affiche lors du lancement du programme) et le PORT par le port inscrit tout en bas de config.json (par défaut 5000)


## Configuration

La configuration des boutons se fait dans un fichier JSON. Un exemple de fichier `config.json` est disponible en bas de cette page.


Les paramètres de configuration suivants sont disponibles:

- `ear-soundboard`: active ou désactive le retour son de la soundboard. Valeurs valides: `"true"` ou `"false"`.
- `mp3_method`: spécifie la méthode à utiliser pour lire les fichiers MP3. Valeurs valides: `"vlc"` ou `"pygame"`.
- `show-console`: active ou désactive l'affichage de la console sur la page. Valeurs valides: `"true"` ou `"false"`.
- `dev-mode`: active ou désactive le mode de développement. Valeurs valides: `"true"` ou `"false"`.
- `spotify-api`: spécifie les informations d'identification de l'API Spotify. Les champs `USERNAME`, `CLIENT_ID` et `CLIENT_SECRET` doivent être renseignés.

Les paramètres de configuration de l'interface utilisateur suivants sont disponibles:

- `theme`: spécifie le thème à utiliser pour l'interface utilisateur. Le nom du fichier CSS doit être spécifié.
- `background`: spécifie l'image ou la couleur (css) à utiliser comme arrière-plan de l'interface utilisateur.
- `show-names`: active ou désactive l'affichage des noms des boutons. Valeurs valides: `"true"` ou `"false"`.
- `names-color`: spécifie la couleur du texte pour les noms de boutons.
- `computer-usage-reload-time`: spécifie le temps en millisecondes entre chaque rafraîchissement des informations d'utilisation de l'ordinateur.
- `height`: spécifie la hauteur de la grille de boutons.
- `width`: spécifie la largeur de la grille de boutons.

Chaque bouton est défini par un objet dans le tableau `buttons`. Les champs suivants sont disponibles pour chaque bouton:

- `name`: le nom à afficher sur le bouton.
- `position`: la position du bouton sur la grille (par exemple, "a1", "b2", etc.).
- `image`: l'image à afficher sur le bouton.
- `image_size`: la taille de l'image en pourcentage.
- `background-color`: la couleur de fond du bouton.
- `color`: la couleur du texte sur le bouton.
- `message`: la commande à exécuter lorsque le bouton est pressé.

Pour configurer les boutons, modifiez simplement le fichier `config.json` en fonction de vos besoins.

## Commandes disponibles

Les commandes suivantes sont disponibles pour les boutons:

- `/folder <nom_du_dossier>` : ouvre le dossier spécifié du webdeck
- `/openfile <chemin_vers_le_fichier>` : ouvre le fichier ou logiciel spécifié
- `/start <chemin_vers_le_fichier>` : ouvre le fichier ou logiciel spécifié
- `/batch <code>` : exécute du batch
- `/exec <code>` : exécute du python
- `/volume +` : augmente de 1 le volume de windows
- `/volume -` : baisse de 1 le volume de windows
- `/volume set <nombre>` : change le volume de windows
- `/soundcontrol mute` : coupe le volume de windows
- `/mediacontrol playpause` : alterne entre play et pause sur windows
- `/mediacontrol previous` : joue le son précédent
- `/mediacontrol next` : joue le son suivant
- `/spotify likesong` : mettre le son actuellement joué sur spotify en favoris
- `/spotify likealbum` : mettre l'album actuellement joué sur spotify en favoris
- `/spotify add_or_remove <nom de la playlist>` : ajoute ou retire le son actuellement joué dans la playlist spécifiée
- `/spotify add_to_playlist <nom de la playlist>` : ajoute le son actuellement joué dans la playlist spécifiée
- `/spotify remove_from_playlist <nom de la playlist>` : retire le son actuellement joué dans la playlist spécifiée
- `/spotify follow_or_unfollow_artist` : s'abonne ou se désabonne de l'artiste actuellement joué
- `/spotify follow_artist` : s'abonner à l'artiste actuellement écouté
- `/spotify unfollow_artist` : se désabonner de l'artiste actuellement en écoute
- `/spotify volume +` : augmente de 1 le volume de SPOTIFY (pas de windows) (requiert spotify prenium)
- `/spotify volume -` : baisse de 1 le volume de SPOTIFY (pas de windows) (requiert spotify prenium)
- `/spotify volume set <nombre>` : change le volume de SPOTIFY (pas de windows) (requiert spotify prenium)
- `/fullscreen` : active/désactive le mode plein écran
- `/reload` : recharge la page
- `/screensaver` : éteint les écrans
- `/screensaver full` : éteint les écrans complètement
- `/screensaver off` : rallume les écrans
- `/superAltF4` : ferme de force la fenêtre au premier plan
- `/taskill <programme.exe>` : ferme de force le programme spécifié
- `/forceclose <programme.exe>` : ferme de force le programme spécifié
- `/restart <programme.exe>` : redémarre le programme spécifié
- `/restartexplorer` : redémarre l'explorateur Windows
- `/key <touche>` : presse une touche
- `/write <texte>` : écrit le texte
- `/writeandsend <texte>` : écrit le texte et appuie sur Entrée
- `/copy` : copie (Ctrl+C)
- `/copy <texte>` : copie le texte spécifié
- `/paste` : colle (Ctrl+V)
- `/paste <texte>` : colle le texte spécifié
- `/clipboard` : ouvre le presse-papiers de Windows
- `/clearclipboard` : efface le presse-papiers de Windows
- `/locksession` : verrouille la session Windows
- `/speechrecognition` : active la reconnaissance vocale de Windows pour écrire en parlant



Exemple du fichier json:
```json
{
    "settings": {
        "ear-soundboard": "true",
        "mp3_method": "vlc",
        "show-console": "false",
        "dev-mode": "false",
        "spotify-api": {
            "USERNAME": "",
            "CLIENT_ID": "",
            "CLIENT_SECRET": ""
        }
    },
    "front": {
        "theme": "theme1.css",
        "background": "",
        "show-names": "true",
        "names-color": "#b3b3b3",
        "computer-usage-reload-time": "3000",
        "height": "4",
        "width": "8",
        "buttons": {
            "index": [
                {
                    "name": "Folder 1",
                    "position": "a1",
                    "image": "folder.png",
                    "image_size": "70%",
                    "message": "/folder folder1"
                },
                {
                    "name": "Spotify",
                    "position": "a2",
                    "image": "spotify.png",
                    "image_size": "70%",
                    "message": "/folder spotify"
                },
                {
                    "name": "Fullscreen",
                    "position": "a3",
                    "image": "fullscreen2.png",
                    "image_size": "50%",
                    "message": "/fullscreen"
                },
                {
                    "name": "Refresh",
                    "position": "a4",
                    "image": "reload.png",
                    "image_size": "50%",
                    "message": "/reload"
                },
                {
                    "name": "ETEINDRE ECRANS",
                    "position": "a5",
                    "image": "screensaver.png",
                    "image_size": "100%",
                    "message": "/screensaver"
                },
                {
                    "name": "ETEINDRE ECRANS FULL",
                    "position": "a6",
                    "image": "screensaver-full.png",
                    "image_size": "50%",
                    "message": "/screensaver full"
                },
                {
                    "name": "RE ALLUMER ECRANS",
                    "position": "a7",
                    "image": "computer-screen.svg",
                    "image_size": "50%",
                    "message": "/screensaver off"
                },
                {
                    "name": "restart explorer",
                    "position": "b3",
                    "image": "https://www.sordum.org/wp-content/uploads/2020/01/restart_explorer.png",
                    "image_size": "80%",
                    "message": "/restartexplorer"
                },
                {
                    "VOID": "VOID"
                },
                {
                    "name": "button pious",
                    "position": "c7",
                    "image": "D:\\Images\\jop3.png",
                    "image_size": "100%",
                    "message": "/openfile D:\\Images\\jop3.png"
                },
                {
                    "name": "Config",
                    "position": "d1",
                    "image": "",
                    "image_size": "90%",
                    "background-color": "91a2ff",
                    "message": "/open-config"
                },
                {
                    "name": "Color picker",
                    "position": "d4",
                    "image": "eyedropper.svg",
                    "image_size": "50%",
                    "color": "#fff",
                    "background-color": "#2e2e2e",
                    "message": "/colorpicker lang:fr"
                },
                {
                    "name": "GPU usage",
                    "position": "d5",
                    "image": "",
                    "image_size": "100%",
                    "color": "#fff",
                    "background-color": "#2e2e2e",
                    "message": "/usage 'GPU USAGE' usage_dict['gpus']['GPU1']['utilization_percent']"
                },
                {
                    "name": "RAM USAGE",
                    "position": "d6",
                    "image": "",
                    "image_size": "100%",
                    "message": "/usage 'RAM%' usage_dict['memory']['usage_percent']"
                },
                {
                    "name": "disk E usage",
                    "position": "d7",
                    "image": "",
                    "image_size": "100%",
                    "message": "/usage 'disque E' usage_dict['disks']['E']['total_gb']"
                },
                {
                    "name": "Cpu usage",
                    "position": "d8",
                    "image": "",
                    "image_size": "100%",
                    "color": "#fff",
                    "background-color": "#2e2e2e",
                    "message": "/usage 'CPU USAGE' usage_dict['cpu']['usage_percent']"
                }
            ],
            "folder1": [
                {
                    "name": "back to index",
                    "image": "folder.png",
                    "image_size": "70%",
                    "message": "/folder index"
                }
            ],
            "spotify": [
                {
                    "name": "Retour",
                    "position": "a1",
                    "image": "back10.svg",
                    "image_size": "110%",
                    "message": "/folder index"
                },
                {
                    "name": "Previous",
                    "position": "a6",
                    "image": "skip-start-fill.svg",
                    "image_size": "100%",
                    "background-color": "#1ed664",
                    "message": "/soundcontrol previous"
                },
                {
                    "name": "Play/Pause",
                    "position": "a7",
                    "image": "playpause.png",
                    "image_size": "100%",
                    "background-color": "#1ed664",
                    "message": "/soundcontrol playpause"
                },
                {
                    "name": "Next",
                    "position": "a8",
                    "image": "skip-end-fill.svg",
                    "image_size": "100%",
                    "background-color": "#1ed664",
                    "message": "/soundcontrol next"
                },
                {
                    "name": "Mute",
                    "position": "d8",
                    "image": "volume-mute.png",
                    "image_size": "100%",
                    "background-color": "#1ed664",
                    "message": "/soundcontrol mute"
                }
            ]
        }
    },
    "url": {
        "ip": "0.0.0.0",
        "port": 5000
    }
}
```

## Commpatibilité

- https://bishokus.fr/webdeck/test-it
- [Google Sheets](https://docs.google.com/spreadsheets/d/1tyfyFJzIdrOl0-Y6wBXaq9EXqViVVCEJu4zQ2-VMGgM/edit#gid=0)

|Type         |Marque     |Appareil                |Date de sortie|Modèle       |Version de l'OS   |Navigateur           |Version du navigateur       |Note (%)|Testé par           |Date      |Comment                                                                                                                                                                                                                                                                                                                 |
|-------------|-----------|------------------------|--------------|-------------|------------------|---------------------|----------------------------|--------|--------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Phone        |Xiaomi     |Xiaomi 11 Lite 5G       |03/2021       |2109119DG    |Android 12        |Chrome               |112.0                       |100%    |anonymous      |19/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Xiaomi     |Redmi 9                 |06/2020       |M2004J19C    |Android 12        |Chrome               |105.0                       |100%    |anonymous        |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Xiaomi     |Redmi 9c NFC            |08/2020       |Not Specified|Android 10        |Chrome               |100.0(.4896.127)            |100%    |Vector#2215         |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Xiaomi     |Redmi 8                 |10/2019       |Not Specified|Android 10        |Opera Gx             |104.0(.5112.97)             |100%    |[TruiteJaaj](https://twitter.com/ExeLatruite)          |19/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Chrome               |111.0(.5563.57) (07/03/2023)|100%    |[Lenoch](https://github.com/LeLenoch)              |17/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Chrome Canary        |114.0                       |95%     |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Quand on passe en format paysage il faut refresh sinon les boutons restent en mode verticale, mais tout fonctionne                                                                                                                                                                                                      |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Edge                 |111.0                       |100%    |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Tout fonctionne (mais éléments html pas changés par du css comme les sliders et checkbox sont grises et moche)                                                                                                                                                                                                          |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Firefox              |112.0                       |100%    |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Tout fonctionne même en thème sombre de l'application. (mais éléments html pas changés par du css comme les sliders et checkbox sont grises et moche)                                                                                                                                                                   |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Firefox Focus        |112.0                       |100%    |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Tout fonctionne même en thème sombre de l'application. (mais éléments html pas changés par du css comme les sliders et checkbox sont grises et moche)                                                                                                                                                                   |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Opera                |110.0(5481.192)             |100%    |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Opera Beta           |112.0(.5615.48)             |100%    |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Opera Mini           |111.0(.5563.116)            |?       |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|CPU usage ne fonctionne pas, a voir si les boutons eux mêmes fonctionnent                                                                                                                                                                                                                                               |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Opera Gx             |111.0(.5563.116)            |?       |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|CPU usage ne fonctionne pas, a voir si les boutons eux mêmes fonctionnent                                                                                                                                                                                                                                               |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Tor                  |102.0                       |100%    |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Aloha Browser        |106.0(.5249.65)             |100%    |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Samsung Internet     |106.0(.5249.126)            |90%     |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Utilisable seulement si le thème du téléphone est sur le mode clair ou alors faire cette manipulation: "Affichage et défilement pages web > Mode Sombre > Utilisation du mode Sombre > Jamais" ou "3 barres en bas à droite > Sites en thème clair" si non les boutons sont noirs                                       |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Samsung Internet Beta|110.0(.5481.154)            |90%     |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Utilisable seulement si le thème du téléphone est sur le mode clair ou alors faire cette manipulation: "Affichage et défilement pages web > Mode Sombre > Utilisation du mode Sombre > Jamais" ou "3 barres en bas à droite > Sites en thème clair" si non les boutons sont noirs                                       |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Brave                |112.0                       |?       |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|CPU usage ne fonctionne pas, a voir si les boutons eux mêmes fonctionnent                                                                                                                                                                                                                                               |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Opera Touch          |111.0(5563.116)             |?       |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|Boutons blancs invisibles en mode sombre: a voir si c'est réparable en changeant un tout petit peu la couleur du blanc, impossible de tester le mode clair car aucune page ne veux charger maintenant (c'est pas la faute de ma co)                                                                                     |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |DuckDuckGo           |111.0(.5563.116)            |?       |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|CPU usage ne fonctionne pas, a voir si les boutons eux mêmes fonctionnent                                                                                                                                                                                                                                               |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Kiwi Browser         |112.0                       |?       |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|CPU usage ne fonctionne pas, a voir si les boutons eux mêmes fonctionnent                                                                                                                                                                                                                                               |
|Phone        |Samsung    |Samsung Galaxy S9       |02/2018       |SM-G960F     |Android 10        |Mi Browser           |100.0(.4896.127)            |?       |[Lenoch](https://github.com/LeLenoch)              |19/04/2023|CPU usage ne fonctionne pas, en http en tout cas, a voir si les boutons eux mêmes fonctionnent. + Utilisable seulement si le thème du téléphone est sur le mode clair ou alors faire cette manipulation: "cliquer en bas à droite sur Profil > Cliquez sur mode sombre pour le désactiver" si non les boutons sont noirs|
|Phone        |Samsung    |Samsung Galaxy S20 FE   |02/2020       |SM-G780G     |Android 13        |Chrome               |106.0(.5249.126)            |100%    |[Chalet](https://github.com/chadLet)          |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Samsung    |Samsung Galaxy S7 Edge  |03/2016       |SM-G935F     |Android 8         |Chrome               |112.0                       |100%    |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |Samsung    |Samsung Galaxy S7 Edge  |03/2016       |SM-G935F     |Android 8         |Opera                |110.0(.5481.192)            |99%     |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Plein écran parfait mais quand ça l'est pas les boutons sont décalés                                                                                                                                                                                                                                                    |
|Phone        |Samsung    |Samsung Galaxy S7 Edge  |03/2016       |SM-G935F     |Android 8         |Samsung explorer     |Not Specified               |99%     |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Plein écran parfait mais quand ça l'est pas les boutons sont décalés                                                                                                                                                                                                                                                    |
|Phone        |Samsung    |Samsung Galaxy s6 Edge  |04/2015       |Not Specified|Android 7         |Brave                |102.0(.5005.99)             |100%    |Kiwaxu#8745         |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Tablet       |Samsung    |Galaxy Tab A 2016       |05/2016       |Not Specified|Not Specified     |Chrome               |112.0                       |?       |anonymous      |19/04/2023|CPU usage ne fonctionne pas, a voir si les boutons eux mêmes fonctionnent, + Le formulaire ne s'envoie pas                                                                                                                                                                                                              |
|Phone        |Oppo       |Oppo A16e               |03/2022       |CPH2421      |Android 11        |Chrome               |111.0                       |100%    |anonymous    |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Phone        |ESSENTIEL B|HeYOU 70                |Not Specified |HEYOU70      |Android 11        |Chrome               |112.0                       |100%    |[etoiledefeu](https://github.com/etoiledefeu)|22/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Tablet       |Huawei     |Huawei Matepad          |04/2020       |BAH3-W09     |Android 10        |Chrome               |112.0                       |99%     |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Tout fonctionne mais quand on écrit du texte depuis l'appareil tout devient petit (screen: https://media.discordapp.net/attachments/891378858274746438/1097862617504161842/Screenshot_20230418_142237_com.opera.browser.jpg)                                                                                            |
|Tablet       |Huawei     |Huawei Matepad          |04/2020       |BAH3-W09     |Android 10        |Opera                |110.0(.5481.192)            |99%     |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Tout fonctionne mais quand on écrit du texte depuis l'appareil tout devient petit (screen: https://media.discordapp.net/attachments/891378858274746438/1097862617504161842/Screenshot_20230418_142237_com.opera.browser.jpg)                                                                                            |
|Tablet       |Huawei     |Huawei Matepad          |04/2020       |BAH3-W10     |Android 10        |Huawei browser       |99.0.4844.88                |95%     |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Recharger la page remets au format vertical                                                                                                                                                                                                                                                                             |
|Tablet       |Huawei     |Huawei Matepad          |04/2020       |BAH3-W09     |Android 10        |Opera Gx             |88.0(.4324.93)              |75%     |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Bordure orange quand clic sur un bouton + recharger la page remets au format vertical                                                                                                                                                                                                                                   |
|Phone        |Apple      |iPhone 5s               |09/2013       |ME432F/A     |iOS 12.5.5        |Safari               |604.1                       |90%     |[Lenoch](https://twitter.com/pepitus)v              |17/04/2023|Le plein écran ne peut pas s'enclencher grâce à un click sur le bouton fait pour, mais peut être activé en mettant le téléphone à l'horizontale. Point négatif: quand on clique trop sur le haut de l'écran, le plein écran se retire et l'écran est très petit. Peut être utilisé pour du 2x3 voir 3x5                 |
|Phone        |Apple      |iPhone 5s               |09/2013       |ME432F/A     |iOS 12.5.5        |Chrome               |92.0(.4515.90)              |15%     |[Lenoch](https://twitter.com/pepitus)              |17/04/2023|En tournant l'écran, les boutons deviennent très petits et c'est inutilisable. Le plein écran n'existe alors pas du tout sur Chrome. Utilisable seulement à la verticale et pour du 3x2 voir 5x3                                                                                                                        |
|Phone        |Apple      |iPhone 5s               |09/2013       |ME432F/A     |iOS 12.5.5        |Opera                |3.6.1 (1)                   |15%     |[Lenoch](https://twitter.com/pepitus)              |17/04/2023|En tournant l'écran, les boutons deviennent très petits et c'est inutilisable. Le plein écran n'existe alors pas du tout sur Opera. Utilisable seulement à la verticale et pour du 3x2 voir 5x3                                                                                                                         |
|Phone        |Apple      |iPhone 11               |09/2020       |Not Specified|iOS 16.?          |Safari               |604.1                       |20%     |anonymous     |18/04/2023|Pas du tout de plein écran, 5% de plus que l'iphone 5s avec Chrome ou Opera car là c'est toujours nul mais quand même plus grand                                                                                                                                                                                        |
|Phone        |Apple      |iPhone SE 2             |04/2020       |Not Specified|iOS 16.3          |Safari               |604.1                       |20%     |Leroox#8925         |18/04/2023|Pas du tout de plein écran, 5% de plus que l'iphone 5s avec Chrome ou Opera car là c'est toujours nul mais quand même plus grand                                                                                                                                                                                        |
|Tablet       |Apple      |iPad Mini               |11/2012       |MD786NF/B    |iOS 12.5.7 (16H81)|Opera                |3.5.5 (26)                  |90%     |[Lenoch](https://github.com/LeLenoch)              |17/04/2023|affichage fonctionnel contrairement à l'iPad originel avec iOS 10.3.3 mais plein écran toujours impossible, les deux navigateurs sont pareil. Conclusion: tout est parfait, mais pas possible en plein écran, et puis comme c'est grand (c'est un ipad quand même) c'est pas si gênant                                  |
|Tablet       |Apple      |iPad Mini               |11/2012       |MD786NF/B    |iOS 12.5.7 (16H81)|Safari               |Not Specified               |90%     |[Lenoch](https://github.com/LeLenoch)              |17/04/2023|affichage fonctionnel contrairement à l'iPad originel avec iOS 10.3.3 mais plein écran toujours impossible, les deux navigateurs sont pareil. Conclusion: tout est parfait, mais pas possible en plein écran, et puis comme c'est grand (c'est un ipad quand même) c'est pas si gênant                                  |
|Tablet       |Apple      |iPad                    |03/2012       |MD513NF/A    |iOS 10.3.3 (14G60)|Chrome               |111.0(.5563.101)            |25%     |[Lenoch](https://github.com/LeLenoch)              |17/04/2023|Affichage cassé, les images sont décalées, plein écran impossible. Très nul mais fonctionnel en soi                                                                                                                                                                                                                     |
|Tablet       |Apple      |iPad                    |03/2012       |MD513NF/A    |iOS 10.3.3 (14G60)|Safari               |602.1                       |25%     |[Lenoch](https://github.com/LeLenoch)              |17/04/2023|Affichage cassé, les images sont décalées, plein écran impossible. Très nul mais fonctionnel en soi                                                                                                                                                                                                                     |
|Console      |Nintendo   |Nintendo new 3ds        |02/2015       |New XL       |11.16.0-49        |Default browser      |Not Specified               |0,50%   |anonymous      |19/04/2023|versions de html css et js beaucoup trop vieux: AUCUN js mais y'a les images lul (screen: https://media.discordapp.net/attachments/437956710435389440/1098344081127637193/rn_image_picker_lib_temp_29964ccb-2e7b-4250-87b4-0fbc335e54a3.jpg)                                                                            |
|Console      |Nintendo   |Nintendo 3ds            |07/2012       |XL           |11.16.0-49        |Default browser      |Not Specified               |0%      |[Lenoch](https://github.com/LeLenoch)              |17/04/2023|versions de html css et js beaucoup trop vieux: pas d'images du tout + AUCUN js                                                                                                                                                                                                                                         |
|Console      |Nintendo   |Nintendo Switch         |03/2017       |V1           |16.0.1            |SwitchBru DNS        |Not Specified               |1%      |[Lenoch](https://github.com/LeLenoch)              |17/04/2023|Affichage mais aucun bouton n'envoie de donnée + pas de plein écran + lags                                                                                                                                                                                                                                              |
|PC           |Microsoft  |Microsoft Surface Laptop|06/2017       |first gen    |Windows 10 x64    |Opera Gx             |111.0                       |100%    |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|PC           |Microsoft  |Microsoft Surface Laptop|06/2017       |first gen    |Windows 10 x64    |Chrome               |112.0                       |100%    |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|PC           |Microsoft  |Microsoft Surface Laptop|06/2017       |first gen    |Windows 10 x64    |Firefox              |112.0                       |100%    |[pepijaaj](https://twitter.com/pepitus)  |18/04/2023|Tout fonctionne                                                                                                                                                                                                                                                                                                         |
|Smart display|Google     |Google Nest Hub         |11/2016       |first gen    |Not Specified     |Not Specified        |90.0(.4430.223)             |40%     |[Lenoch](https://github.com/LeLenoch)              |20/04/2023|Pas de plein écran + si tu n'appuies sur rien du tout pendant environ 5 minutes, le nest hub décide simplement d'afficher l'heure, c'est certainement plus utile (peut être réparable je sais pas)                                                                                                                      |

