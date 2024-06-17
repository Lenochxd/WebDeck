[![Version française](https://img.shields.io/badge/Lire%20en-Fran%C3%A7ais-blue?style=for-the-badge&logo=appveyor)](https://github.com/Lenochxd/WebDeck/blob/master/docs/FAQ-fr.md)
[![Version Korean](https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4%EB%A1%9C-%EC%9D%BD%EA%B8%B0-blue?style=for-the-badge&logo=appveyor)](https://github.com/Lenochxd/WebDeck/blob/master/docs/FAQ-ko.md)

# Welcome to the WebDeck FAQ!
You can use `ctrl+f` to search for what you want.

## What is WebDeck?

The WebDeck is an application that allows the user to control their computer from any device with a browser and a touchscreen. Unlike Elgato's StreamDeck, which requires physical equipment, WebDeck uses a web application that the user hosts on their own computer and accesses from their device with a touchscreen.
<div align="center">
  <img src="https://i.imgur.com/OLE1oWk.png" alt="WebDeck example image" width="375" height="257">
</div>


## How do I install WebDeck?

1. Download the latest version of WebDeck from the [Releases](https://github.com/Lenochxd/WebDeck/releases) section on GitHub.

2. Extract the contents of `WebDeck-win-amd64-portable.zip` to the location of your choice on your computer.

3. Open the chosen location and run `WebDeck.exe`.

4. There is nothing to install on your mobile device, you simply need to scan the QR code by clicking on the tray icon.


## How do I change the language of use?

If you prefer to use a language other than English, you can follow these simple steps to change the language of the application:

1. Access the application settings.

2. In the "Language" section, select your preferred language from the available options. Currently, only English and French are supported. Please note that the French translation may not cover all settings at this stage. You can remedy this by right-clicking on the settings page and selecting "Translate to French."

3. In the future, we plan to allow each user to easily contribute to the translation of the application into their preferred language.

This way, you can customize the application's language according to your linguistic preferences.


## How to set up my soundboard?

Follow these steps to configure the application's soundboard:

1. **Install VB-CABLE Driver:**
   - Download the driver from [this link](https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip).
   - Unzip the downloaded file.
   - Run `VBCABLE_Setup_x64.exe`.
   - Click on "Install Driver".
   - Restart your computer.

2. **Install VLC media player:**
   - If VLC media player is not already installed on your computer, download it from [this link](https://www.videolan.org/vlc/download-windows.html).
   - Proceed with the installation by following the instructions.
   - VLC is essential for playing sounds on the soundboard. However, it is not necessary to open the software even once for the soundboard to work. Installation is sufficient, and everything will function perfectly.

3. **Configure Webdeck Settings:**
   - Open the webdeck settings.
   - Scroll down to the "Soundboard" section.
   - Select the appropriate input microphone.
   - Choose "CABLE Input (VB-Audio Virtual Cable)" as the output.

4. **Configure External Software Settings:**
   - Open the settings of the software where you want to use the soundboard and make sure to select "CABLE Output (VB-Audio Virtual Cable)" as the microphone input.

5. **Discord Configuration:**
   - If you are using the soundboard on Discord, disable the "Automatic Gain Control" feature in "Settings > Voice & Video".
   - Note that the use of noise suppression may result in distorted sound quality.

6. **Add Sounds:**
   - Add a button with the Q key.
   - Go to the "Soundboard" section, then "Play a sound".
   - Import your audio file **in MP3 format**.

You have now successfully configured the application's soundboard. Press the associated button to play your sound.


## How to set up OBS Studio?

Follow these steps to configure the OBS websocket:

1. Open OBS Studio and go on `Tools > WebSocket Server Settings`

2. Ensure that the "Enable WebSocket server" checkbox is checked.

3. In the section below (Server Settings), click on "Show Connection Information" at the bottom.

4. Copy the randomly generated port and password provided by OBS and enter them in the WebDeck settings.

5. Save the configuration, and there you have it! OBS is now connected to WebDeck!


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


## Can I put a GIF on a button?

Of course! You can easily add a `.gif` file as the image for your button when creating or editing it.

Accepted file formats for button images:
`.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, `.bmp`, `.ico`, `.tiff`, `.tif`, `.heif`, `.heic`, `.apng`, `.mng`


## How can I customize the background behind the buttons?

Customizing the background is a breeze. Follow these simple steps:

1. Open the application settings.
2. Click the "Open the backgrounds menu" button.
3. This menu allows you to add colors or background images with ease. You can add as many as you like.
4. When the page loads, a random background will be selected from those selected.
5. If you want to disable certain backgrounds, simply check the box to the right of the background in question.
6. To remove a background, click the corresponding delete icon.

This way, you can customize the button backgrounds to your preferences with just a few clicks.


## Why is VLC Media Player necessary?

WebDeck needs the `python-vlc` library for sound playback on the soundboard. Therefore, it is essential to have VLC media player installed on your computer, even if you do not use the VLC software interface. Unfortunately, to date, no alternative solution has been identified to bypass this requirement.

**Note:** This dependency is a current limitation, and the WebDeck development team is actively exploring potential alternatives to streamline the user experience in future updates.


## Does the software communicate with a server?

Yes, but no. Indeed, WebDeck establishes communication with a server, but that server is in fact your computer. The WebDeck on your mobile device is nothing more than a simple web page, and the "server" it connects to is actually your computer. The communication between these two devices takes place through your local network. In other words, your computer acts as a server, but access to this server is strictly reserved for you alone.

If your question concerns the software communicating with a **different** server than your computer's, then the answer is no. To ensure maximum security, no data leaves your network. The only data sent outside your home are API requests to Spotify, but these data do not pass through dedicated WebDeck servers, they are going straight to Spotify's servers.


## Can I open files other than software via the "Open ..." button?

Absolutely! You have the option to select any file, and it will be opened with the corresponding default application. For example, if you choose to open an image, it will automatically open with your usual image viewer.


## I'm a developer, how can I customize the page's CSS?

As a developer, you have the option to create a theme by customizing the CSS of the page according to your preferences. Here's how to do it in a few simple steps:

1. Go to settings > 'Open the themes menu' > 'Open themes folder' to access the `.config/themes/` directory of the application.
2. Create a new CSS file manually or duplicate an existing one to begin your customization.
3. Edit the theme information as needed in the CSS file you created, ensuring it starts with the following structure:

```css
/*
theme-name = MyTheme
theme-description = My custom theme description :)
theme-logo = https://i.imgur.com/qhaL1EU.png
theme-author-github = YourGithubHere
*/

/* ------------------------------------------------------ */
```

4. Reload the WebDeck configuration page.

Once these steps are completed, you can select your own theme in the settings. You will have the freedom to modify the CSS as needed and customize the appearance of the page to your liking. You can even share your .css file with other users if you wish.


## Why is WebDeck detected as malware by my antivirus?

I have no idea, but it's open source, so if you're concerned about malicious code, feel free to check it yourself.\
But don't worry, WebDeck is obviously NOT a malicious application.


## Can you compile the software yourself?

If you prefer to compile the executable files yourself for security reasons, here are the steps to follow:

1. Download the source code and extract it.
2. Open a terminal in the source code folder.
3. Create a virtual environment:\
`python -m venv webdeck`\
`webdeck\Scripts\activate.bat`
4. Install the dependencies:\
`pip install -r requirements.txt`
5. Start the compilation:\
`python setup.py build`
6. (Optional) If you want to sign the executables with signtool, follow the instructions provided in [this link](https://stackoverflow.com/a/52963704/17100464).
7. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WebDeck.exe`
8. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_main.exe`
9. `signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 WD_updater.exe`