import asyncio
import sys
from colorama import Fore, Style

async def read_subprocess_output(stream, name):
    while True:
        line = await stream.readline()
        if not line:
            break
        line = line.decode().strip()
        print(f"{Fore.GREEN}{name}{Style.RESET_ALL} {line}")

async def main():
    # Lancer main_server.py en arrière-plan avec l'option --reload
    main_server_process = await asyncio.create_subprocess_exec(
        sys.executable, 'main_server.py', '--reload',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    # Lancer start_server.py en arrière-plan
    start_server_process = await asyncio.create_subprocess_exec(
        sys.executable, 'start_server.py', '--reload',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    # Lire les sorties des deux programmes en parallèle
    await asyncio.gather(
        read_subprocess_output(main_server_process.stdout, 'MAIN  :'),
        read_subprocess_output(start_server_process.stdout, 'START :')
    )

if __name__ == '__main__':
    asyncio.run(main())
