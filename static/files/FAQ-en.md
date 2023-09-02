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


## How do I reset the application settings?

Resetting the settings is a simple process. Follow these steps:

1. Access the application files on your system.
2. Locate the file named `config.json`.
3. Delete this file or rename it.
4. Restart the application.

Once these steps are completed, the application settings will be reset to their default values, allowing you to start fresh with a clean configuration if necessary.


## Does the software communicate with a server?

Yes, but no. Indeed, WebDeck establishes communication with a server, but that server is you. The WebDeck on your mobile device is nothing more than a simple web page, and the "server" it connects to is actually your computer. The communication between these two devices takes place through your local network. In other words, your computer acts as a server, but access to this server is strictly reserved for you alone.

If your question concerns the software communicating with a **different** server than your computer's, then the answer is no. To ensure maximum security, no data leaves your network. The only data sent outside your home are API requests to Spotify, but these data do not pass through dedicated WebDeck servers; they are directed straight to Spotify's servers.


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


## I'm a developer; how can I customize the page's CSS?

As a developer, you have the option to customize the CSS of the page according to your preferences. Here's how to do it in a few simple steps:

1. Access the `static/themes/` directory of the application.
2. Duplicate the `theme1.css` file.
3. Restart the application on your computer.

Once these steps are completed, you can select your own theme in the settings. You will have the freedom to modify the CSS as needed and customize the appearance of the page to your liking. You can even share your `.css` file with other users if you wish.


## Can I open files other than software via the "Open ..." button?

Absolutely! You have the option to select any file, and it will be opened with the corresponding default application. For example, if you choose to open an image, it will automatically open with your usual image viewer.


## Why is WebDeck detected as malware/trojan on virustotal.com?

Don't worry; WebDeck is obviously NOT a malicious application. There are several reasons for its detection as malware by the `Jiangmin` antivirus on virustotal.com.

Firstly, it's essential to understand that before being an .exe file, an application is initially written using a programming language understandable by a computer. In the case of WebDeck, this language is Python. The process of transforming a .py file into a .exe file can be done using three main software, but they all have one problem: regardless of the application's purpose, it can be identified as a potential malware by some antivirus programs.

- `PyInstaller`: 18 / 69 antivirus detected viruses.
- `py2exe`: 4 / 68 antivirus detected viruses.
- `cx_Freeze`: 1 / 68 antivirus detected viruses.

*Source: [Stack Overflow](https://stackoverflow.com/questions/67702280/why-are-executable-created-from-python-scripts-detected-as-viruses)*

WebDeck uses `cx_Freeze`, which is the least prone to detection (but was chosen by chance). However, all these tools work similarly: the final .exe file runs a modified version of the .py file, allowing the software to run. Unfortunately, some antivirus programs fail to make the connection between these files, seeing only that one .exe file opens another, which can potentially be interpreted as malicious activity by the antivirus.

All of this to say that the application is by no means a virus. But there is still another reason. Even if `cx_Freeze` were perfect, virustotal.com could still detect the software as potential malware because WebDeck offers complete customization. You can create buttons that perform various actions, such as shutting down your computer, deleting files, or running macros, for example. While some malicious software may look like this, using keyboard shortcuts to cause harm, that is not the purpose of WebDeck. Here, the user has full control over the actions the software takes on their computer when clicking a button, while the antivirus prefers to think that the software simply has full control over your computer.

*Other sources: [1](https://stackoverflow.com/questions/11860287/why-my-freezed-app-is-detected-as-possible-virus?rq=4) - [2](https://stackoverflow.com/questions/22693665/python-executables-alarms-antivirus?rq=4) - [3](https://stackoverflow.com/questions/23815222/py2exe-detected-as-virus-alternatives?rq=4) - [4](https://stackoverflow.com/questions/48464693/py2exe-detected-as-virus-alternatives?rq=4) - [5](https://github.com/marcelotduarte/cx_Freeze/issues/315)*
