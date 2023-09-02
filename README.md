[![GitHub release (latest by date)](https://img.shields.io/github/v/release/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/releases)
[![GitHub downloads](https://img.shields.io/github/downloads/LeLenoch/WebDeck/total.svg)](https://github.com/LeLenoch/WebDeck/releases)
[![GitHub stars](https://img.shields.io/github/stars/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/watchers)
[![CodeFactor](https://www.codefactor.io/repository/github/LeLenoch/WebDeck/badge)](https://www.codefactor.io/repository/github/LeLenoch/WebDeck)
[![GitHub issues](https://img.shields.io/github/issues/LeLenoch/WebDeck.svg)](https://github.com/LeLenoch/WebDeck/issues)

[![Version française](https://img.shields.io/badge/Lire%20en-Fran%C3%A7ais-blue?style=for-the-badge&logo=appveyor)](https://github.com/LeLenoch/WebDeck/blob/master/README-fr.md)

# WebDeck

The WebDeck is a Flask application that allows users to control their computer remotely from any device with a browser and a touchscreen. Unlike Elgato's StreamDeck, which requires physical equipment, WebDeck uses a Flask application that the user hosts on their own computer.

<div align="center">
  <img src="https://media.discordapp.net/attachments/939294227152662589/1144740939873669221/example.png" alt="WebDeck example image" width="375" height="257">
</div>

## 🖥️🚀 Installation

1. Download the latest version of WebDeck from the [Releases](https://github.com/LeLenoch/WebDeck/releases) section on GitHub.

2. Extract the contents of `WebDeck-win-amd64-portable.zip` to the location of your choice on your computer.

3. Open the chosen location and run  `WebDeck.exe`.

4. There is nothing to install on your mobile device, you simply need to scan the QR code by clicking on the tray icon.

## 📱❔ Compatibility

To check the compatibility of your device and browser with WebDeck, you can refer to the  [test table](https://docs.google.com/spreadsheets/d/1tyfyFJzIdrOl0-Y6wBXaq9EXqViVVCEJu4zQ2-VMGgM/edit#gid=0). This table details the results of various experiments on different devices and browsers. You can also contribute to the table using https://bishokus.fr/webdeck/test-it

## Compilation (Nerds only)

<details>
  <summary>If you wish to compile the software into .exe yourself, follow these steps:</summary>

1. Download the source code and extract it.
2. Open a terminal in the source code folder.
3. Create a virtual environment:\
`python -m venv webdeck`\
`webdeck\Scripts\activate.bat`
4. Install the dependencies:\
`pip install -r requirements.txt`
5. Start the compilation:\
`python setup.py build`
6. (Optional) If you want to sign the executables with signtool, follow the instructions provided in this link: https://stackoverflow.com/a/52963704/17100464.
7. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WebDeck.exe`
8. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_main.exe`
9. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_updater.exe`

</details>

## ⭐ Contributors


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
      👨‍💻 Made the algorithm for modifying the grid size
    </td>
    <td align="center">
      🎨 Logo and color design
    </td>
    <td align="center">
      📈 Math, beta testing, and <a href="https://bishokus.fr/wdt">bishokus.fr/wdt</a> enjoyer
    </td>
    <td align="center">
      ➗ Math (volume modification function)
    </td>
    <td align="center">
      🤓 Everything else
    </td>
  </tr>
</table>
<br>


## 🙏 Donate
https://buymeacoffee.com/bishokus

---

WebDeck is an ever-evolving project, and we appreciate your contributions to further improve it. If you encounter any issues, feel free to open an issue on GitHub, submit a pull request with your upgrades, or if you're not a nerd, contact me elsewhere:

Discord: Lenoch\
Discord Server: https://discord.gg/CK2mu4P \
Twitter: https://twitter.com/LenochJ \
Email (?): contact.lenoch@gmail.com

<br>

---

[![wakatime](https://wakatime.com/badge/user/0929cfd2-6330-4ccd-b5d6-859515b66a10/project/4bcf5971-919c-48a5-9f8c-2f1a06046591.svg)](https://wakatime.com/badge/user/0929cfd2-6330-4ccd-b5d6-859515b66a10/project/4bcf5971-919c-48a5-9f8c-2f1a06046591) : (only since July 3rd 2023, started on December 16th, 2022)
