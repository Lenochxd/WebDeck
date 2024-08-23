# Bienvenue dans la FAQ WebDeck!
Vous pouvez utiliser `ctrl+f` pour cherchez ce que vous voulez

## C'est quoi le WebDeck ?

Le WebDeck est une application qui permet à l'utilisateur de controller son ordinateur depuis n'importe quel appareil doté d'un navigateur et d'un écran tactile. Contrairement au StreamDeck d'Elgato, qui nécessite un équipement physique, le WebDeck utilise une application web que l'utilisateur héberge sur son propre ordinateur et utilise sur son appareil avec écran tactile.
<div align="center">
  <img src="https://i.imgur.com/OLE1oWk.png" alt="WebDeck example image" width="375" height="257">
</div>


## Comment installer le WebDeck ?

1. Téléchargez la dernière version de WebDeck depuis la section [Releases](https://github.com/Lenochxd/WebDeck/releases) sur GitHub.

2. Extrayez le contenu de `WebDeck-win-amd64-portable.zip` dans l'emplacement de votre choix sur votre ordinateur.

3. Ouvrez l'emplacement choisi et lancez `WebDeck.exe`.

4. Vous n'avez rien à installer sur votre appareil mobile, il vous suffira simplement de scanner le qr code présent en cliquant sur l'icone minimisée.


## Comment changer la langue d'utilisation ?

Si vous préférez utiliser une autre langue que l'anglais, vous pouvez suivre ces étapes simples pour modifier la langue de l'application :

1. Accédez aux paramètres de l'application.
2. Dans la section "Language" (Langue), sélectionnez la langue de votre choix parmi les options disponibles. Actuellement, seules l'anglais et le français sont pris en charge. Veuillez noter que la traduction en français peut ne pas couvrir l'ensemble des paramètres à ce stade. Vous pouvez remédier à cela en faisant un clic droit sur la page des paramètres et en sélectionnant "Traduire en français".
3. Dans le futur, nous prévoyons de permettre à chaque utilisateur de contribuer facilement à la traduction de l'application dans leur langue préférée.

Ainsi, vous pourrez personnaliser la langue de l'application selon vos préférences linguistiques.


## Comment configurer ma soundboard ?

Suivez ces étapes pour configurer la soundboard de l'application:

1. **Installer le pilote VB-CABLE:**
   - Téléchargez le pilote à partir de [ce lien](https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip).
   - Dézippez le fichier téléchargé.
   - Exécutez `VBCABLE_Setup_x64.exe`.
   - Cliquez sur "Install Driver".
   - Redémarrer l'ordinateur.

2. **Installer VLC media player:**
   - Si VLC media player n'est pas déjà installé sur votre ordinateur, téléchargez-le à partir de [ce lien](https://www.videolan.org/vlc/download-windows.html).
   - Procédez à l'installation en suivant les instructions.
   - VLC est essentiel pour la lecture des sons sur la soundboard. Cependant, il n'est pas nécessaire d'ouvrir le logiciel une seule fois pour que la soundboard fonctionne. L'installation suffit, et tout sera parfaitement fonctionnel.

3. **Configurer les paramètres du webdeck:**
   - Ouvrez les paramètres du webdeck.
   - Faites défiler jusqu'à la section "Soundboard".
   - Sélectionnez votre microphone d'entrée.
   - Choisissez "CABLE Input (VB-Audio Virtual Cable)" comme sortie.

4. **Configurer les paramètres du logiciel externe:**
   - Ouvrez les paramètres du logiciel où vous souhaitez utiliser la soundboard et sélectionnez "CABLE Output (VB-Audio Virtual Cable)" comme entrée microphone.

5. **Configuration pour Discord:**
   - Si vous utilisez la soundboard sur Discord, désactivez la fonction "Annulation d'écho" dans "Paramètres > Voix & Vidéo".
   - Notez que l'utilisation de la suppression du bruit peut entraîner une qualité altérée des sons.

6. **Ajouter des sons:**
   - Ajoutez un bouton avec la touche Q.
   - Allez dans la section "Soundboard" puis "Jouer un son".
   - Importez votre fichier audio **au format MP3**.

Vous avez maintenant configuré avec succès la soundboard de l'application. Appuyez sur le bouton associé pour jouer votre son.


## Comment configurer OBS Studio ?

Suivez ces étapes simples pour configurer OBS pour WebDeck:

1. Ouvrez OBS Studio puis allez dans `Outils > Paramètres du serveur WebSocket`

2. Vérifiez que la case "Activer le serveur WebSocket" est cocheé

3. Dans la section du dessous (Paramètres du serveur), cliquez en bas sur "Afficher les informations de connexion"

4. Copiez le port et le mot de passe généré aléatoirement par OBS pour les entrer dans les paramètres du webdeck.

6. Enregistrez la configuration et voilà, OBS est connecté au WebDeck !


## Comment connecter mon compte Spotify ?

Suivez ces étapes simples pour connecter votre compte Spotify à WebDeck :

1. Connectez-vous à votre compte Spotify sur le site [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

2. Cliquez sur le bouton bleu "Create app" pour créer une nouvelle application.

3. Remplissez le formulaire comme suit :
   - Nom et Description : Facultatif, écrivez ce que vous voulez.
   - Redirect URI : Entrez `http://localhost:8888/callback`.

4. Cochez la case pour accepter les conditions d'utilisation.

5. Cliquez sur "Save" pour enregistrer votre application.

6. Une fois sur la page d'accueil, cliquez sur "Settings" dans le menu de droite.

7. Copiez votre "Client ID" et cliquez sur "View client secret" en dessous pour copier également le secret client. Vous aurez besoin de ces informations pour configurer votre WebDeck.

8. Dans votre WebDeck, assurez-vous de fournir votre nom d'utilisateur Spotify dans le champ "Username" des paramètres, ainsi que le **Cliend ID** et **Client Secret**.

9. Enregistrez la configuration et voilà, votre compte Spotify est désormais connecté à l'application !

N'oubliez pas de garder votre "Client ID" et votre "Client Secret" en sécurité, car ils sont nécessaires pour l'authentification de votre application WebDeck auprès de Spotify.


## Comment réinitialiser les paramètres de l'application ?

La réinitialisation des paramètres est un processus simple. Suivez ces étapes :

1. Accédez aux fichiers de l'application sur votre système.
2. Localisez le fichier nommé `config.json`.
3. Supprimez ce fichier ou renommez-le.
4. Redémarrez l'application.

Une fois ces étapes accomplies, les paramètres de l'application seront réinitialisés à leurs valeurs par défaut, vous permettant de recommencer avec une configuration fraîche si nécessaire.


## Puis-je mettre un GIF sur un bouton ?

Bien sur ! Vous pouvez facilement ajouter un fichier `.gif` en tant qu'image de votre bouton lors de sa création ou de sa modification.

Formats de fichiers acceptés pour l'image du bouton:\
`.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, `.bmp`, `.ico`, `.tiff`, `.tif`, `.heif`, `.heic`, `.apng`, `.mng`


## Comment personnaliser le fond d'écran/arrière-plan derrière les boutons ?

La personnalisation de l'arrière est un jeu d'enfant. Suivez ces étapes simples :

1. Ouvrez les paramètres de l'application.
2. Cliquez sur le bouton "Ouvrir le menu des arrière-plans".
3. Ce menu vous permettra d'ajouter des couleurs ou des images de fond en toute simplicité. Vous pouvez en ajouter autant que vous le souhaitez.
4. Lors du chargement de la page, un fond aléatoire sera sélectionné parmi ceux qui sont sélectionnés.
5. Si vous souhaitez désactiver certains arrière-plans, cochez simplement la case à droite de l'arrière-plan en question.
6. Pour supprimer un arrière-plan, cliquez sur l'icône de suppression correspondante.

Ainsi, vous pourrez personnaliser l'arrière-plan des boutons selon vos préférences en quelques clics.


## Pourquoi VLC Media Player est nécessaire ?

WebDeck utilise la bibliothèque `python-vlc` pour la lecture des sons sur la soundboard. Par conséquent, il est indispensable d'avoir VLC media player installé sur votre ordinateur, même si vous n'utilisez pas l'interface du logiciel VLC. Malheureusement, à ce jour, aucune solution alternative n'a été identifiée pour contourner cette exigence.

**Remarque :** Cette dépendance est une limitation actuelle, et l'équipe de développement de Webdeck explore activement des alternatives potentielles pour simplifier l'expérience utilisateur dans les futures mises à jour.


## Le logiciel communique-t-il avec un serveur ?

Oui, mais non. En effet, le WebDeck établit une communication avec un serveur, mais ce serveur, c'est votre propre ordinateur. Le WebDeck sur votre appareil mobile n'est rien de plus qu'une simple page web, et le "serveur" auquel il se connecte est en réalité votre ordinateur. La communication entre ces deux appareils s'effectue par le biais de votre réseau local. Autrement dit, votre ordinateur agit comme un serveur, mais l'accès à ce serveur est strictement réservé à vous seul.

Si votre question porte sur la communication du logiciel avec un **autre** serveur que celui de votre ordinateur, alors la réponse est non. Pour garantir un maximum de sécurité, aucune donnée ne sort de votre réseau. Les seules données envoyées à l'extérieur de votre domicile sont les requêtes API vers Spotify, mais ces données ne transitent pas par des serveurs dédiés au WebDeck, elles sont dirigées directement vers les serveurs de Spotify.


## Peut-on ouvrir des fichiers autres que des logiciels via le bouton "Ouvrir ..." ?

Absolument ! Vous avez la possibilité de sélectionner n'importe quel fichier, et il sera ouvert avec l'application par défaut correspondante. Par exemple, si vous choisissez de ouvrir une image, elle s'ouvrira automatiquement avec votre visionneuse d'images habituelle.


## Je suis un développeur, comment puis-je personnaliser le CSS de la page ?

En tant que développeur, vous avez la possibilité de créer un thème en personnalisant le CSS de la page selon vos préférences. Voici comment le faire en quelques étapes simples :

1. Accédez aux paramètres > 'Ouvrir le menu des thèmes' > 'Ouvrir le dossier des thèmes' pour accéder au répertoire `.config/themes/` de l'application.
2. Créez un nouveau fichier CSS manuellement ou dupliquez-en un existant pour commencer votre personnalisation.
3. Modifiez les informations du thème selon vos besoins dans le fichier CSS que vous avez créé, en vous assurant qu'il commence par la structure suivante :

```css
/*
theme-name = MonTheme
theme-description = Ma description de thème :)
theme-icon = https://i.imgur.com/qhaL1EU.png
theme-author-github = VotreGithubIci
*/

/* ------------------------------------------------------ */
```

4. Rechargez la page de configuration de WebDeck.

Une fois ces étapes terminées, vous pourrez sélectionner votre propre thème dans les paramètres. Vous aurez la liberté de modifier le CSS selon vos besoins et de personnaliser l'apparence de la page à votre guise. Vous pouvez même partager votre fichier .css avec d'autres utilisateurs si vous le souhaitez.


## Pourquoi le WebDeck est détecté comme un malware par mon antivirus ?

Ne vous inquiétez pas, le WebDeck n'est évidemment PAS une application malveillante.\
Je n'ai aucune explication à ce sujet, cependant, le code source étant accessible, n'hésitez pas à le vérifier par vous-même pour dissiper toute inquiétude. Allez hop


## Comment compiler le fichier `WebDeck.exe` par vous-même ?

Si vous préférez compiler le fichier `WebDeck.exe` vous-même par mesure de sécurité, voici les étapes à suivre :

1. Téléchargez le code source et extrayez-le.
2. Ouvrez un terminal dans le dossier du code source.
3. Créez un environnement virtuel :\
`python -m venv webdeck`\
`webdeck\Scripts\activate.bat`
4. Installez les dépendances :\
`pip install -r requirements.txt`
5. Effectuez la compilation :\
`python setup.py build`
6. (Optionnel) Si vous souhaitez signer les exécutables avecsigntool, suivez les instructions fournies dans le lien pour l'installer: https://stackoverflow.com/a/52963704/17100464.
7. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com td SHA256 WebDeck.exe`
8. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com td SHA256 WD_main.exe`
9. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com td SHA256 WD_updater.exe`