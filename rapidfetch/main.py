#!/usr/bin/env python3

import datetime
import getpass
import psutil
import socket
import platform
import time
import argparse
import os
from colorama import Fore, Style, init

init(autoreset=True)

FLAG = os.path.expanduser("~/.rapidfetch_welcome")

def welcome():
    if not os.path.exists(FLAG):
        print(Fore.CYAN + """
👋 Hola, espero estés bien!

🚀 Bienvenido a RapidFetch
💻 Usa:
              
              Uso Simple:
   rapidfetch
   rapidfetch --gradient
   rapidfetch --dark
   rapidfetch --minimal

              Uso Personalizado:
   rapidhomefetch
   rapidhomefetch --gradient
   rapidhomefetch --dark
   rapidhomefetch --minimal

✨ Éxitos — Elias Cobos ⚡
""")
        open(FLAG, "w").close()

def obtener_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "No disponible"

def barra(valor, total, length=20):
    filled = int(length * (valor / total))
    return "█" * filled + "░" * (length - filled)

def barra_color(valor, total, length=20):
    filled = int(length * (valor / total))
    bar = ""
    for i in range(length):
        if i < filled:
            color = 46 - int(i * 20 / length)
            bar += f"\033[38;5;{color}m█"
        else:
            bar += "\033[90m░"
    return bar + "\033[0m"

def gradient_text(text):
    colors = list(range(51, 27, -2))
    result = ""
    i = 0
    skip = False

    for char in text:
        if char == "\033":
            skip = True

        if not skip:
            color = colors[i % len(colors)]
            result += f"\033[38;5;{color}m{char}"
            i += 1
        else:
            result += char

        if char == "m":
            skip = False

    return result + "\033[0m"

def main():
    welcome()

    parser = argparse.ArgumentParser()
    parser.add_argument("--gradient", action="store_true")
    parser.add_argument("--dark", action="store_true")
    parser.add_argument("--minimal", action="store_true")
    args = parser.parse_args()

    now = datetime.datetime.now()

    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    cpu = psutil.cpu_percent(interval=0.5)

    use_color = args.gradient or args.dark

    ram_bar = barra_color(ram.used, ram.total) if use_color else barra(ram.used, ram.total)
    disk_bar = barra_color(disk.used, disk.total) if use_color else barra(disk.used, disk.total)
    cpu_bar = barra_color(cpu, 100) if use_color else barra(cpu, 100)

    logo = """
██████╗  █████╗ ██████╗ ██╗██████╗
██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗
██████╔╝███████║██████╔╝██║██║  ██║
██╔══██╗██╔══██║██╔═══╝ ██║██║  ██║
██║  ██║██║  ██║██║     ██║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝
"""

    output = ""

    if not args.minimal:
        output += logo + "\n"
        output += f"⚡ RapidFetch\n"
        output += "─" * 40 + "\n"
        output += f"Usuario : {getpass.getuser()}\n"
        output += f"IP      : {obtener_ip()}\n"
        output += f"Kernel  : {platform.release()}\n"
        output += f"Uptime  : {int((time.time()-psutil.boot_time())//3600)}h\n\n"

    output += f"RAM     : {ram_bar} {ram.used//(1024**3)}GB/{ram.total//(1024**3)}GB\n"
    output += f"Disco   : {disk_bar} {disk.used//(1024**3)}GB/{disk.total//(1024**3)}GB\n"
    output += f"CPU     : {cpu_bar} {cpu}%\n"

    if args.gradient:
        print(gradient_text(output))
    elif args.dark:
        dark = ""
        for line in output.split("\n"):
            if "RAM" in line:
                dark += Fore.GREEN + line + "\n"
            elif "CPU" in line:
                dark += Fore.YELLOW + line + "\n"
            elif "Disco" in line:
                dark += Fore.MAGENTA + line + "\n"
            else:
                dark += Fore.WHITE + line + "\n"
        print(dark)
    else:
        print(output)