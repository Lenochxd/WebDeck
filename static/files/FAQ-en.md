# Welcome to the WebDeck FAQ!
You can use `ctrl+f` to search for what you want.

## What is WebDeck?

The WebDeck is an application that allows the user to control their computer from any device with a browser and a touchscreen. Unlike Elgato's StreamDeck, which requires physical equipment, WebDeck uses a web application that the user hosts on their own computer and accesses from their device with a touchscreen.
<div align="center">
  <img src="https://media.discordapp.net/attachments/939294227152662589/1144740939873669221/example.png" alt="WebDeck example image" width="375" height="257">
</div>


## How do I install WebDeck?

1. Download the latest version of WebDeck from the [Releases](https://github.com/LeLenoch/WebDeck/releases) section on GitHub.

2. Extract the contents of `WebDeck-win-amd64-portable.zip` to the location of your choice on your computer.

3. Open the chosen location and run `WebDeck.exe`.

4. There is nothing to install on your mobile device, you simply need to scan the QR code by clicking on the tray icon.


## How do I change the language of use?

If you prefer to use a language other than English, you can follow these simple steps to change the language of the application:

1. Access the application settings.

2. In the "Language" section, select your preferred language from the available options. Currently, only English and French are supported. Please note that the French translation may not cover all settings at this stage. You can remedy this by right-clicking on the settings page and selecting "Translate to French."

3. In the future, we plan to allow each user to easily contribute to the translation of the application into their preferred language.

This way, you can customize the application's language according to your linguistic preferences.

## How to Set Up My Soundboard?

Follow these steps to configure the application's soundboard:

1. **Install VB-CABLE Driver:**
   - Download the driver from [this link](https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip).
   - Unzip the downloaded file.
   - Run `VBCABLE_Setup_x64.exe`.
   - Click on "Install Driver".
   - Restart your computer.

2. **Configure Webdeck Settings:**
   - Open the webdeck settings.
   - Scroll down to the "Soundboard" section.
   - Select the appropriate input microphone.
   - Choose "CABLE Input (VB-Audio Virtual Cable)" as the output.

3. **Configure External Software Settings:**
   - Open the settings of the software where you want to use the soundboard and make sure to select "CABLE Output (VB-Audio Virtual Cable)" as the microphone input.

4. **Discord Configuration:**
   - If you are using the soundboard on Discord, disable the "Automatic Gain Control" feature in "Settings > Voice & Video".
   - Note that the use of noise suppression may result in distorted sound quality.

5. **Add Sounds:**
   - Add a button with the Q key.
   - Go to the "Soundboard" section, then "Play a sound".
   - Import your audio file **in MP3 format**.

You have now successfully configured the application's soundboard. Press the associated button to play your sound.


## How to connect your Spotify account

Follow these simple steps to connect your Spotify account to WebDeck:

1. Log in to your Spotify account on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

2. Click the blue "Create app" button to create a new application.

3. Fill out the form as follows:
   - Name and Description: Optional, write whatever you want.
   - Redirect URI: Enter `http://localhost:8888/callback`.

4. Check the box to accept the terms of use.

5. Click "Save" to save your application.

6. Once on the homepage, click "Settings" in the right-hand menu.

7. Copy your "Client ID" and click "View client secret" below to also copy the client secret. You will need this information to configure your WebDeck.

8. In your WebDeck, make sure to provide your Spotify username in the "Username" field in the settings, as well as the **Client ID** and **Client Secret**.

9. Save the configuration, and there you go! Your Spotify account is now connected to the application!

Remember to keep your "Client ID" and "Client Secret" secure, as they are required for authenticating your WebDeck application with Spotify.


## How do I reset the application settings?

Resetting the settings is a simple process. Follow these steps:

1. Access the application files on your system.
2. Locate the file named `config.json`.
3. Delete this file or rename it.
4. Restart the application.

Once these steps are completed, the application settings will be reset to their default values, allowing you to start fresh with a clean configuration if necessary.


## Does the software communicate with a server?

Yes, but no. Indeed, WebDeck establishes communication with a server, but that server is you. The WebDeck on your mobile device is nothing more than a simple web page, and the "server" it connects to is actually your computer. The communication between these two devices takes place through your local network. In other words, your computer acts as a server, but access to this server is strictly reserved for you alone.

If your question concerns the software communicating with a **different** server than your computer's, then the answer is no. To ensure maximum security, no data leaves your network. The only data sent outside your home are API requests to Spotify, but these data do not pass through dedicated WebDeck servers, they are going straight to Spotify's servers.


## Can I put a GIF on a button?

Of course! You can easily add a `.gif` file as the image for your button when creating or editing it.

Accepted file formats for button images:
`.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, `.bmp`, `.ico`, `.tiff`, `.tif`, `.heif`, `.heic`, `.apng`, `.mng`


## How can I customize the background behind the buttons?

Customizing the background is a breeze. Follow these simple steps:

1. Open the application settings.
2. Click the "Open the backgrounds menu" button.
3. This menu allows you to add colors or background images with ease. You can add as many as you like.
4. When the page loads, a random background will be selected from those you've added.
5. If you want to disable certain backgrounds, simply check the box to the right of the background in question.
6. To remove a background, click the corresponding delete icon.

This way, you can customize the button backgrounds to your preferences with just a few clicks.


## Can I open files other than software via the "Open ..." button?

Absolutely! You have the option to select any file, and it will be opened with the corresponding default application. For example, if you choose to open an image, it will automatically open with your usual image viewer.


## I'm a developer, how can I customize the page's CSS?

As a developer, you have the option to customize the CSS of the page according to your preferences. Here's how to do it in a few simple steps:

1. Access the `static/themes/` directory of the application.
2. Duplicate the `theme1.css` file.
3. Restart the application on your computer.

Once these steps are completed, you can select your own theme in the settings. You will have the freedom to modify the CSS as needed and customize the appearance of the page to your liking. You can even share your `.css` file with other users if you wish.


## Why is WebDeck detected as malware by my antivirus?

I have no idea, but it's open source, so if you're concerned about malicious code, feel free to check it yourself.\
But don't worry, WebDeck is obviously NOT a malicious application.


## Can I compile the `WebDeck.exe` file yourself?

If you prefer to compile the WebDeck.exe file yourself for security reasons, even though WebDeck is open source, here are the steps to follow:

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