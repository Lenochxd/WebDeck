# WebDeck

Le WebDeck est une application Flask qui permet à l'utilisateur de contrôler son ordinateur à distance depuis n'importe quel appareil doté d'un navigateur et d'un écran tactile. Contrairement au StreamDeck d'Elgato, qui nécessite un équipement physique, le WebDeck utilise une application Flask que l'utilisateur héberge sur son propre ordinateur.

<div align="center">
  <img src="https://github.com/LeLenoch/WebDeck/assets/101269524/c9c02a34-1f98-4a12-9cc0-621e06cfe2e5" alt="Bannière WebDeck" height="75%" width="75%">
  <img src="https://github.com/LeLenoch/WebDeck/assets/101269524/c601d4f6-cbb3-460b-874d-b74ec5e71696" alt="Exemple d'image WebDeck" width="45%" height="45%">
  
  [![GitHub release (latest by date)](https://img.shields.io/github/v/release/LeLenoch/WebDeck.svg?style=flat)](https://github.com/LeLenoch/WebDeck/releases)
  [![GitHub downloads](https://img.shields.io/github/downloads/LeLenoch/WebDeck/total.svg?style=flat)](https://github.com/LeLenoch/WebDeck/releases)
  [![GitHub stars](https://img.shields.io/github/stars/LeLenoch/WebDeck.svg?style=flat)](https://github.com/LeLenoch/WebDeck/stargazers)
  [![GitHub watchers](https://img.shields.io/github/watchers/LeLenoch/WebDeck.svg?style=flat)](https://github.com/LeLenoch/WebDeck/watchers)
  [![CodeFactor](https://www.codefactor.io/repository/github/LeLenoch/WebDeck/badge?style=flat)](https://www.codefactor.io/repository/github/LeLenoch/WebDeck)
  [![GitHub issues](https://img.shields.io/github/issues/LeLenoch/WebDeck.svg?style=flat)](https://github.com/LeLenoch/WebDeck/issues)
  [![Discord](https://discordapp.com/api/guilds/391919052563546112/widget.png?style=shield)](https://discord.gg/tUPsYHAGfm)
</div>


## 🖥️🚀 Installation

1. Téléchargez la dernière version de WebDeck depuis la section [Releases](https://github.com/LeLenoch/WebDeck/releases) sur GitHub.

2. Extrayez le contenu de `WebDeck-win-amd64-portable.zip` à l'emplacement de votre choix sur votre ordinateur.

3. Ouvrez l'emplacement choisi et exécutez `WebDeck.exe`.

4. Vous n'avez rien à installer sur votre appareil mobile, il vous suffira simplement de scanner le QR code présent en cliquant sur l'icone minimisée.


## 📋 Foire aux questions (FAQ)

Avant de poser des questions, veuillez consulter notre [FAQ](https://github.com/LeLenoch/WebDeck/blob/master/static/files/FAQ-fr.md) pour voir si votre question a déjà été répondue. Nous avons rassemblé les questions fréquemment posées pour vous fournir des réponses rapides.

Si votre question n'est pas abordée dans la FAQ, n'hésitez pas à nous la poser sur notre [serveur Discord](https://discord.gg/tUPsYHAGfm).


## 📱❔ Compatibilité

Pour vérifier la compatibilité de votre appareil et navigateur avec WebDeck, vous pouvez consulter le [tableau des tests](https://docs.google.com/spreadsheets/d/1tyfyFJzIdrOl0-Y6wBXaq9EXqViVVCEJu4zQ2-VMGgM/edit#gid=0). Celui-ci détaille les résultats de différentes expériences sur divers appareils et navigateurs. Vous pouvez vous aussi contribuer au tableau avec https://bishokus.fr/webdeck/test-it

### 💻 Systèmes d'Exploitation

Le WebDeck prend actuellement en charge Windows. Il est prévu de développer des versions pour Linux et macOS à l'avenir. Malheureusement, l'émulation Wine n'est pas une solution viable pour la compatibilité Linux. Nous vous remercions de votre patience pendant que nous travaillons à étendre nos plates-formes prises en charge.


## Compilation (Pour les nerds)

<details>
  <summary>Si vous souhaitez compiler le logiciel en .exe vous-même, suivez ces étapes :</summary>

1. Téléchargez le code source et extrayez-le.
2. Ouvrez un terminal dans le dossier du code source.
3. Créez un environnement virtuel :\
`python -m venv webdeck`\
`webdeck\Scripts\activate.bat`
4. Installez les dépendances :\
`pip install -r requirements.txt`
5. Lancez la compilation :\
`python setup.py build`
6. (Optionnel) Si vous souhaitez signer les exécutables avecsigntool, suivez les instructions fournies dans le lien pour l'installer: https://stackoverflow.com/a/52963704/17100464.
7. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com td SHA256 WebDeck.exe`
8. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com td SHA256 WD_main.exe`
9. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com td SHA256 WD_updater.exe`

</details>


## ⭐ Contributeurs

<table align="center">
  <tr>
    <td align="center">
      <a href="https://twitter.com/Nico_Sinban">
        <img src="https://cdn.discordapp.com/avatars/260325467406598144/a_13aa90e91c3dd999c74c02a2bbbf1922.png" alt="Nico Sinban" width="80px" height="80px" style="border-radius: 50%;">
        <br>
        Nico Sinban
      </a>
    </td>
    <td align="center">
      <a href="https://twitter.com/ZeyaTsu">
        <img src="https://pbs.twimg.com/profile_images/1571127084449136641/NKWj3-CK_400x400.jpg" alt="ZeyaTsu" width="80px" height="80px" style="border-radius: 50%;">
        <br>
        ZeyaTsu
      </a>
    </td>
    <td align="center">
      <a href="https://twitter.com/pepijaaj">
        <img src="https://pbs.twimg.com/profile_images/1623676018136342530/A3-lR6fP_400x400.jpg" alt="pepijaaj" width="80px" height="80px" style="border-radius: 50%;">
        <br>
        Pepijaaj
      </a>
    </td>
    <td align="center">
      <a href="https://twitter.com/HLeheurteur">
        <img src="https://images-ext-2.discordapp.net/external/Zpj31ZXa_MQ_UQzJleHXayFMXljDQzGknDVE63-4Ow4/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/513036764286550039/135b087469229643d6f409885824c033.png" alt="CONTRIBUTEUR2" width="80px" height="80px" style="border-radius: 50%;">
        <br>
        Horizuwu
      </a>
    </td>
    <td align="center">
      <a href="https://twitter.com/LenochJ">
        <img src="https://cdn.discordapp.com/avatars/390265556357611521/205d253b7e742b8f70174fdac8ca701d.png" alt="CONTRIBUTEUR2" width="80px" height="80px" style="border-radius: 50%;">
        <br>
        Lenoch
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      👨‍💻 Algorithme pour modifier la taille de la grille
    </td>
    <td align="center">
      🎨 Conception du logo et des couleurs
    </td>
    <td align="center">
      📈 Maths, beta tester et <a href="https://bishokus.fr/wdt">bishokus.fr/wdt</a> enjoyer
    </td>
    <td align="center">
      ➗ Mathématiques (fonction de modification de volume)
    </td>
    <td align="center">
      🤓 Tout le reste.
    </td>
  </tr>
</table>
<br>

## 🙏 Faire un don

Si vous appréciez le projet, envisagez de [m'offrir un café](https://buymeacoffee.com/bishokus).

---

WebDeck est un projet en constante évolution, et nous apprécions vos contributions pour l'améliorer davantage. Si vous rencontrez des problèmes, n'hésitez pas à ouvrir un problème sur GitHub, soumettre une demande d'extraction avec vos améliorations, ou si vous n'êtes pas un nerd, contactez-moi ailleurs:

- Discord: Lenoch
- Serveur Discord: [https://discord.gg/tUPsYHAGfm](https://discord.gg/tUPsYHAGfm)
- Twitter: [https://twitter.com/LenochJ](https://twitter.com/LenochJ)
- Email (?): contact.lenoch@gmail.com

<br>

---

[![wakatime](https://wakatime.com/badge/github/LeLenoch/WebDeck.svg)](https://wakatime.com/badge/github/LeLenoch/WebDeck) : (uniquement depuis le 3 juillet 2023, commencé le 16 décembre 2022)
