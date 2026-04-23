#!/usr/bin/env python3
import os
import subprocess
import time
import random
import datetime
import json
import hashlib
import sqlite3
import sys

user = "shell"
hostname = "featherplayzz"

if user == "root":
    exit()

def makeh(pasw):
    return hashlib.sha256(pasw.encode()).hexdigest()

if not os.path.exists(".sys.db"):
    connect = sqlite3.connect(".sys.db")
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (user, password) VALUES (?, ?)", ("root", makeh("root")))
    cursor.execute("INSERT INTO users (user, password) VALUES (?, ?)", (user, makeh("shell")))
    connect.commit()
    connect.close()

connect = sqlite3.connect(".sys.db")
cursor = connect.cursor()

cursor.execute("SELECT password FROM users WHERE user = 'root'")
passdbsqlroot = cursor.fetchone()[0]
cursor.execute(f"SELECT password FROM users WHERE user = '{user}'")
passdbsqluser = cursor.fetchone()[0]

r, g, y, b, m, c, w, gr = "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m", "\033[90m"
lr, lg, ly, lb, lm, lc, lw = "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m"
br, bg, by, bb, bm, bc = "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m", "\033[1;35m", "\033[1;36m"
rs, it, un = "\033[0m", "\033[3m", "\033[4m"

path = os.path.join(os.getcwd(), "shelldata")
aliasp = os.path.join(path, "root/shellsys/alias.json")
ll = os.path.join(path, "root/shellsys/login.log")
root_log = False
user_path = os.path.join(path, user)
root_path = os.path.join(path, "root")

os.makedirs(os.path.join(path, "root/shellsys"), exist_ok=True)
os.makedirs(user_path, exist_ok=True)
if not os.path.exists(ll): open(ll, 'a').close()
if not os.path.exists(aliasp):
    with open(aliasp, 'w') as f: json.dump({}, f)

with open(aliasp, 'r') as f:
    alias = json.load(f)

def login_system():
    global root_log
    count = 0
    while True:
        print("[Security]: System is locked!")
        u_in = input("Username: ")
        p_in = input("Password: ")
        h_in = makeh(p_in)
        if h_in == passdbsqluser and u_in == user:
            print(f"[{by}Security{rs}]: System Unlocked √")
            break
        elif h_in == passdbsqlroot and u_in == "root":
            print(f"[{by}Security{rs}]: System Unlocked as root √")
            root_log = True
            break
        else:
            count += 1
            print(f"{by}[{br}ERROR{by}]{rs} Access Denied! ({count}X)")
            with open(os.path.join(path, ".login.log"), 'a') as f:
                f.write(f"\n[WRONG LOGIN] User: {u_in} | Date: {datetime.datetime.now()}\n")
            if count >= 3:
                print("Locked for 60s...")
                time.sleep(60)
                count = 0

def main():
    ban = ["cd", "ls", "cat", "rm"]
    global alias, root_log, passdbsqluser, passdbsqlroot
    active_path = root_path if root_log else user_path
    os.chdir(active_path)
    
    print(f"=============================\nShell v3.0.0-beta\nLogged in as: {'root' if root_log else user}\n=============================")

    while True:
        curr = os.getcwd()
        prompt = f"root@{hostname}:{curr}/:$ " if root_log else f"{user}@{hostname}:{curr}/:$ "
        cmd = input(prompt).strip()
        if not cmd: continue
        parts = cmd.split()
        
        if parts[0] in alias:
            subprocess.run(alias[parts[0]], shell=True)
            continue

        if cmd == "shell --info":
            print("SoftOS v3.0.0-beta | Developed by FeatherPlayz")
        elif cmd == "shell --help":
            print("Commands: --info, --alias, --edit, --delete, --list, --shutdown, --reload, --reboot")
        elif cmd == "shell --shutdown":
            connect.close()
            exit()
        elif cmd == "shell --reload":
            connect.commit()
            print("System Reloaded.")
        elif cmd == "shell --edit":
            fn = input("Path: ")
            if not root_log and any(b in fn for b in ban): print("Denied"); continue
            os.system(f"nano {fn}")
        elif parts[0] == "cd":
            if not root_log: print("Root required"); continue
            try:
                os.chdir(os.path.expanduser(parts[1]))
            except: print("Path not found")
        else:
            if not root_log and parts[0] in ban:
                print("Permission Denied")
            else:
                os.system(cmd)

login_system()
main()
  
