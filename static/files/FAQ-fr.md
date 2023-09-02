# Bienvenue dans la FAQ WebDeck!
Vous pouvez utiliser `ctrl+f` pour cherchez ce que vous voulez

## C'est quoi le WebDeck ?

Le WebDeck est une application qui permet à l'utilisateur de controller son ordinateur depuis n'importe quel appareil doté d'un navigateur et d'un écran tactile. Contrairement au StreamDeck d'Elgato, qui nécessite un équipement physique, le WebDeck utilise une application web que l'utilisateur héberge sur son propre ordinateur et utilise sur son appareil avec écran tactile.
<div align="center">
  <img src="https://media.discordapp.net/attachments/939294227152662589/1144740939873669221/example.png" alt="WebDeck example image" width="375" height="257">
</div>


## Comment installer le WebDeck ?

1. Téléchargez la dernière version de WebDeck depuis la section [Releases](https://github.com/LeLenoch/WebDeck/releases) sur GitHub.

2. Extrayez le contenu de `WebDeck-win-amd64-portable.zip` dans l'emplacement de votre choix sur votre ordinateur.

3. Ouvrez l'emplacement choisi et lancez `WebDeck.exe`.

4. Vous n'avez rien à installer sur votre appareil mobile, il vous suffira simplement de scanner le qr code présent en cliquant sur l'icone minimisée.


## Comment changer la langue d'utilisation ?

Si vous préférez utiliser une autre langue que l'anglais, vous pouvez suivre ces étapes simples pour modifier la langue de l'application :

1. Accédez aux paramètres de l'application.
2. Dans la section "Language" (Langue), sélectionnez la langue de votre choix parmi les options disponibles. Actuellement, seules l'anglais et le français sont pris en charge. Veuillez noter que la traduction en français peut ne pas couvrir l'ensemble des paramètres à ce stade. Vous pouvez remédier à cela en faisant un clic droit sur la page des paramètres et en sélectionnant "Traduire en français".
3. Dans le futur, nous prévoyons de permettre à chaque utilisateur de contribuer facilement à la traduction de l'application dans leur langue préférée.

Ainsi, vous pourrez personnaliser la langue de l'application selon vos préférences linguistiques.


## Comment réinitialiser les paramètres de l'application ?

La réinitialisation des paramètres est un processus simple. Suivez ces étapes :

1. Accédez aux fichiers de l'application sur votre système.
2. Localisez le fichier nommé `config.json`.
3. Supprimez ce fichier ou renommez-le.
4. Redémarrez l'application.

Une fois ces étapes accomplies, les paramètres de l'application seront réinitialisés à leurs valeurs par défaut, vous permettant de recommencer avec une configuration fraîche si nécessaire.


## Le logiciel communique-t-il avec un serveur ?

Oui, mais non. En effet, le WebDeck établit une communication avec un serveur, mais ce serveur, c'est vous. Le WebDeck sur votre appareil mobile n'est rien de plus qu'une simple page web, et le "serveur" auquel il se connecte est en réalité votre ordinateur. La communication entre ces deux appareils s'effectue par le biais de votre réseau local. Autrement dit, votre ordinateur agit comme un serveur, mais l'accès à ce serveur est strictement réservé à vous seul.

Si votre question porte sur la communication du logiciel avec un **autre** serveur que celui de votre ordinateur, alors la réponse est non. Pour garantir un maximum de sécurité, aucune donnée ne sort de votre réseau. Les seules données envoyées à l'extérieur de votre domicile sont les requêtes API vers Spotify, mais ces données ne transitent pas par des serveurs dédiés au WebDeck, elles sont dirigées directement vers les serveurs de Spotify.


## Puis-je mettre un GIF sur un bouton ?

Bien sur ! Vous pouvez facilement ajouter un fichier `.gif` en tant qu'image de votre bouton lors de sa création ou de sa modification.

Formats de fichiers acceptés pour l'image du bouton:\
`.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, `.bmp`, `.ico`, `.tiff`, `.tif`, `.heif`, `.heic`, `.apng`, `.mng`


## Comment personnaliser le fond d'écran derrière les boutons ?

La personnalisation du fond d'écran est un jeu d'enfant. Suivez ces étapes simples :

1. Ouvrez les paramètres de l'application.
2. Cliquez sur le bouton "Open the backgrounds menu" (Ouvrir le menu des arrière-plans).
3. Ce menu vous permettra d'ajouter des couleurs ou des images de fond en toute simplicité. Vous pouvez en ajouter autant que vous le souhaitez.
4. Lors du chargement de la page, un fond aléatoire sera sélectionné parmi ceux que vous avez ajoutés.
5. Si vous souhaitez désactiver certains arrière-plans, cochez simplement la case à droite de l'arrière-plan en question.
6. Pour supprimer un arrière-plan, cliquez sur l'icône de suppression correspondante.

Ainsi, vous pourrez personnaliser l'arrière-plan des boutons selon vos préférences en quelques clics.



## Je suis développeur, comment puis-je personnaliser le CSS de la page ?

En tant que développeur, vous avez la possibilité de personnaliser le CSS de la page selon vos préférences. Voici comment procéder en quelques étapes simples :

1. Accédez au répertoire `static/themes/` de l'application.
2. Dupliquez le fichier `theme1.css`.
3. Redémarrez l'application sur votre ordinateur.

Une fois ces étapes accomplies, vous pourrez sélectionner votre propre thème dans les paramètres. Vous aurez ainsi la liberté de modifier le CSS selon vos besoins et de personnaliser l'apparence de la page à votre gré. Vous pourrez même partager votre fichier `.css` avec d'autres utilisateurs si vous le souhaitez.


## Peut-on ouvrir des fichiers autres que des logiciels via le bouton "Ouvrir ..." ?

Absolument ! Vous avez la possibilité de sélectionner n'importe quel fichier, et il sera ouvert avec l'application par défaut correspondante. Par exemple, si vous choisissez de ouvrir une image, elle s'ouvrira automatiquement avec votre visionneuse d'images habituelle.


## Pourquoi le WebDeck est détecté comme un malware/trojan sur virustotal.com ?
<div align="center">
  <img src="https://media.discordapp.net/attachments/963555711839789186/1147571325955739648/8PfwKlprM3SEYAAAAASUVORK5CYII.png" alt="CHOKBAR" width="300" height="200">
  <img src="https://media.discordapp.net/attachments/963555711839789186/1147571577790136452/wFPJuo8xUTmGQAAAABJRU5ErkJggg.png" alt="CHOKBAR DE BZ" width="300" height="200">
</div>

Ne vous inquiétez pas, le WebDeck n'est évidemment PAS une application malveillante. Il existe plusieurs raisons à cette détection par l'antivirus `Jiangmin` de virustotal.

Tout d'abord, il est essentiel de comprendre qu'avant d'être un fichier .exe, une application est initialement écrite en utilisant un langage de programmation compréhensible par un ordinateur. Dans le cas du WebDeck, ce langage est Python. Le processus de transformation d'un fichier .py en fichier .exe peut être réalisé à l'aide de trois logiciels principaux, mais ils présentent tous un problème : quel que soit l'objectif de l'application, elle peut être identifiée comme un possible malware par certains antivirus.

- `PyInstaller` : 18 / 69 antivirus ont détecté des virus.
- `py2exe` : 4 / 68 antivirus ont détecté des virus.
- `cx_Freeze` : 1 / 68 antivirus ont détecté des virus.

*Source : [Stack Overflow](https://stackoverflow.com/questions/67702280/why-are-executable-created-from-python-scripts-detected-as-viruses)*

WebDeck utilise `cx_Freeze`, qui est l'option la moins sujette à la détection (mais a été choisie par hasard). Cependant, tous ces outils fonctionnent de manière similaire : le fichier .exe final exécute une version modifiée du fichier .py, permettant de lancer le logiciel. Malheureusement, certains antivirus ne parviennent pas à faire le lien entre ces fichiers, ne voyant que le fait qu'un fichier .exe en ouvre un autre, ce qui peut potentiellement être interprété comme une activité malveillante par l'antivirus.

Tout cela pour dire que l'application n'est en aucun cas un virus. Mais il y a tout de même une autre raison. Même si `cx_Freeze` était parfait, virustotal.com pourrait toujours détecter le logiciel comme un possible malware, car le WebDeck offre une personnalisation totale. Vous pouvez créer des boutons qui effectuent diverses actions, comme éteindre votre ordinateur, supprimer des fichiers, ou exécuter des macros, par exemple. Bien que certains logiciels malveillants puissent ressembler à cela, en utilisant des combinaisons de touches clavier pour causer des dommages, ce n'est pas le but du WebDeck. Ici, l'utilisateur a le plein contrôle sur les actions que le logiciel effectue sur son ordinateur lorsque vous cliquez sur un bouton, alors que l'antivirus préfère penser que le logiciel a simplement tout droit sur votre ordinateur.

*Autres sources : [1](https://stackoverflow.com/questions/11860287/why-my-freezed-app-is-detected-as-possible-virus?rq=4) - [2](https://stackoverflow.com/questions/22693665/python-executables-alarms-antivirus?rq=4) - [3](https://stackoverflow.com/questions/23815222/py2exe-application-flagged-as-malware-by-windows-defender-what-to-do?rq=4) - [4](https://stackoverflow.com/questions/48464693/py2exe-detected-as-virus-alternatives?rq=4) - [5](https://github.com/marcelotduarte/cx_Freeze/issues/315)*