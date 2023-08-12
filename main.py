import tkinter as tk
import subprocess
from threading import Thread
import pystray
from PIL import Image
from pystray import MenuItem as item
import ctypes
import sys
import pywintypes
import win32gui, win32con
import win32com.client
import asyncio
import os
import time


wmi = win32com.client.GetObject("winmgmts:")
processes = wmi.InstancesOf("Win32_Process")

if_webdeck = False
wd_count = 0
for process in processes:
    if 'webdeck' in process.Properties_('Name').Value.lower().strip():
        wd_count += 1
if wd_count > 1:
    time.sleep(1)
    wmi = win32com.client.GetObject("winmgmts:")
    processes = wmi.InstancesOf("Win32_Process")

    if_webdeck = False
    wd_count = 0
    for process in processes:
        if 'webdeck' in process.Properties_('Name').Value.lower().strip():
            wd_count += 1
    if wd_count > 1:
        if_webdeck = True
    
if if_webdeck == False:
        
    

        icon = None

        # Créer une fenêtre principale
        window = tk.Tk()
        window.title("WebDeck Debug")
        window.withdraw()  # Masquer la fenêtre principale au démarrage

        # Créer un widget Text pour afficher la sortie du terminal
        output_text = tk.Text(window, bg="black", fg="white", width=80, height=24)
        output_text.pack()

        # Créer un widget Entry pour saisir les commandes
        input_entry = tk.Entry(window, bg="black", fg="white")
        input_entry.pack()

        # Fonction pour exécuter la commande saisie
        def run_command():
            command = input_entry.get()
            input_entry.delete(0, tk.END)  # Effacer l'entrée après avoir appuyé sur Entrée
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            update_output_text(output.decode("utf-8"))
            update_output_text(error.decode("utf-8"))

        # Associer la fonction `run_command` à l'événement "Return" (Entrée)
        input_entry.bind("<Return>", lambda event: run_command())

        # Fonction pour mettre à jour le widget Text
        def update_output_text(text):
            output_text.configure(state="normal")  # Activer l'édition du widget Text
            output_text.insert(tk.END, text)
            output_text.configure(state="disabled")  # Désactiver l'édition du widget Text
            output_text.see(tk.END)  # Défiler automatiquement vers la dernière ligne

        # Fonction pour afficher les résultats du code donné
        def display_results():

            async def read_subprocess_output(stream, name):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    line = line.decode().strip()
                    window.after(0, update_output_text, f"{line}\n")

            async def main():
                # Lancer main_server.py en arrière-plan avec l'option --reload
                main_server_process = await asyncio.create_subprocess_exec(
                    # sys.executable, 'main_server.py', '--reload',
                    sys.executable, 'WD_main.exe', '--reload',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT
                )

                # Lancer start_server.py en arrière-plan
                start_server_process = await asyncio.create_subprocess_exec(
                    # sys.executable, 'start_server.py', '--reload',
                    sys.executable, 'WD_start.exe', '--reload',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT
                )

                # Lire les sorties des deux programmes en parallèle
                await asyncio.gather(
                    read_subprocess_output(main_server_process.stdout, 'MAIN  :'),
                    read_subprocess_output(start_server_process.stdout, 'START :')
                )

            asyncio.run(main())

        # Lancer l'exécution du code dans un thread séparé
        execution_thread = Thread(target=display_results)
        execution_thread.start()

        def quit_program():
            global icon  # Utiliser la variable globale icon
            
            wmi = win32com.client.GetObject("winmgmts:")
            processes = wmi.InstancesOf("Win32_Process")
            
            for process in processes:
                if 'webdeck' in process.Properties_('Name').Value.lower().strip():
                    print(f"Stopping process: {process.Properties_('Name').Value.lower().strip()}")
                    result = process.Terminate()
                    if result == 0:
                        print("Process terminated successfully.")
                    else:
                        print("Failed to terminate process.")
            try: sys.exit()
            except: exit()

            
            icon.stop()  # Arrêter l'icône Tray
            window.quit()  # Fermer la fenêtre principale
            window.destroy()  # Fermer la fenêtre principale


        # Créer l'icône System Tray
        def create_tray_icon():
            global icon  # Utiliser la variable globale icon
            # Charger l'icône
            image = Image.open("static/files/icon.ico")

            # Créer le menu de l'icône Tray
            menu = (
                item('Réouvrir', lambda: window.deiconify()),
                item('Quitter', lambda: quit_program()),
            )

            # Créer l'icône Tray
            icon = pystray.Icon("name", image, "Titre", menu)
            return icon

        # Lancer l'icône System Tray
        def start_tray_icon(icon):
            icon.run()

        # Lancer l'icône System Tray dans un thread séparé
        tray_icon_thread = Thread(target=start_tray_icon, args=(create_tray_icon(),))
        tray_icon_thread.start()

        # Lancer la boucle principale de l'application
        window.protocol("WM_DELETE_WINDOW", quit_program)  # Définir la fonction de fermeture lors de la fermeture de la fenêtre principale
        window.mainloop()