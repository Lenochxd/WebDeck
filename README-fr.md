[![GitHub release (latest by date)](https://img.shields.io/github/v/release/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/releases) [![GitHub stars](https://img.shields.io/github/stars/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/stargazers) [![GitHub downloads](https://img.shields.io/github/downloads/LeLenoch/WebDeck/total.svg)](https://github.com/LeLenoch/WebDeck/releases) [![GitHub watchers](https://img.shields.io/github/watchers/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/watchers)
 [![License](https://img.shields.io/github/license/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/blob/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/issues)

# WebDeck

Le WebDeck est une application Flask qui permet à l'utilisateur de contrôler son ordinateur à distance depuis n'importe quel appareil doté d'un navigateur et d'un écran tactile. Contrairement au StreamDeck d'Elgato, qui nécessite un équipement physique, le WebDeck utilise une application Flask que l'utilisateur héberge sur son propre ordinateur.

<div align="center">
  <img src="https://media.discordapp.net/attachments/939294227152662589/1144740939873669221/example.png" alt="WebDeck example image" width="375" height="257">
</div>

## 🖥️🚀 Installation

1. Téléchargez la dernière version de WebDeck depuis la section [Releases](https://github.com/LeLenoch/WebDeck/releases) sur GitHub.

2. Extrayez le contenu de `WebDeck-win-amd64-portable.zip` dans l'emplacement de votre choix sur votre ordinateur.

3. Ouvrez l'emplacement choisi et lancez `WebDeck.exe`.

4. Vous n'avez rien à installer sur votre appareil mobile, il vous suffira simplement de scanner le qr code présent en cliquant sur l'icone minimisée.

## 📱❔ Compatibilité

Pour vérifier la compatibilité de votre appareil et navigateur avec WebDeck, vous pouvez consulter le [tableau des tests](https://docs.google.com/spreadsheets/d/1tyfyFJzIdrOl0-Y6wBXaq9EXqViVVCEJu4zQ2-VMGgM/edit#gid=0). Celui-ci détaille les résultats de différentes expériences sur divers appareils et navigateurs. Vous pouvez vous aussi contribuer au tableau avec https://bishokus.fr/webdeck/test-it

## Compilation (Pour les nerds)

<details>
  <summary>Si vous souhaitez compiler vous-même le logiciel en `.exe`, suivez ces étapes :</summary>

1. Téléchargez le code source et extrayez-le.
2. Ouvrez un terminal dans le dossier du code source.
3. Créez un environnement virtuel :\
`python -m venv webdeck`\
`webdeck\Scripts\activate.bat`
4. Installez les dépendances :\
`pip install -r requirements.txt`
5. Effectuez la compilation :\
`python setup.py build`
6. (Optionnel) Si vous souhaitez signer les exécutables avecsigntool, suivez les instructions fournies dans le lien pourl'installer: https://stackoverflow.com/a/52963704/17100464.
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
    <!-- Ajoutez plus de contributeurs de la même manière -->
  </tr>
  <tr>
    <td align="center">
      👨‍💻 Algorithme pour modifier la taille de la grille
    </td>
    <td align="center">
      🎨 Création et conception du logo et des couleurs
    </td>
    <td align="center">
      📈 Maths, beta tester et <a href="https://bishokus.fr/wdt">bishokus.fr/wdt</a> enjoyer
    </td>
    <td align="center">
      ➗ Maths (fonction modifier le volume)
    </td>
    <td align="center">
      🤓 Tout le reste.
    </td>
  </tr>
</table>
<br>


## 🙏 Faire un don
https://buymeacoffee.com/bishokus

---

WebDeck est un projet en constante évolution, et nous apprécions vos contributions pour l'améliorer davantage. Si vous rencontrez des problèmes, n'hésitez pas à ouvrir un problème sur GitHub, à soumettre une demande de pull avec vos améliorations, ou si vous n'êtes pas un nerd, me contacter autre part:

Discord: Lenoch\
Serveur discord: https://discord.gg/CK2mu4P \
Twitter: https://twitter.com/LenochJ \
Email (?): contact.lenoch@gmail.com

<br>

---

[![wakatime](https://wakatime.com/badge/user/0929cfd2-6330-4ccd-b5d6-859515b66a10/project/4bcf5971-919c-48a5-9f8c-2f1a06046591.svg)](https://wakatime.com/badge/user/0929cfd2-6330-4ccd-b5d6-859515b66a10/project/4bcf5971-919c-48a5-9f8c-2f1a06046591) : (seulement depuis le 3 Juillet 2023, j'ai commencé le 16 décembre 2022)
