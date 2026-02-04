#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
import platform
import threading
import time
from wcwidth import wcswidth
import yaml

#Config yaml file
CONFIG_FILE = "config.yml"

#CONFIG Machine MAP
CONFIG_MACHINE_MAP = {
    "install_root_ad": [
        "MAD-VECNA-DC01",
        "MAD-ARCADE-PC01",
        "MAD-DND-SERVER"
    ],
    "install_child_ad": [
        "MAD-BRENNER-DC02",
        "MAD-LAB-SYSTEM01",
        "MAD-BYERS-PC01"
    ],
    "install_adcs": [
        "MAD-STARCOURT-DC"
    ]
}

#Windows Machine
WINDOWS_MACHINES = [
    "MAD-VECNA-DC01",
    "MAD-BRENNER-DC02",
    "MAD-ARCADE-PC01",
    "MAD-BYERS-PC01",
    "MAD-LAB-SYSTEM01",
    "MAD-STARCOURT-DC"
]


#CONFIG FILE FUNCTIONS
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f) or {}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False)


# ==================================================
# MAD METADATA
# ==================================================
LAB_NAME = "[MAD – MindFlayer's Active Directory]"
VERSION = "1.0"

OVERVIEW = """
Hands-on Active Directory security lab focused on:
• Real-world AD misconfigurations
• Multiple attack paths
• Domain trust abuse
• Cross-platform exploitation
"""

# REQUIREMENTS
# Here you specify the minimum requirement for the MAD LAB

MIN_CPU = 4
MIN_RAM = 16
MIN_DISK = 120

REQUIRED_PLUGINS = ["vagrant-reload", "vagrant-vbguest", "winrm", "winrm-fs", "winrm-elevated",]

# ==================================================
# COLORS & ICONS
# ==================================================
RESET="\033[0m"
TITLE="\033[38;5;81m"
MENU="\033[38;5;117m"
INFO="\033[38;5;250m"
SUCCESS="\033[38;5;82m"
WARN="\033[38;5;214m"
ERROR="\033[38;5;196m"
ACCENT="\033[38;5;141m"

ICON_SYS="🧠"
ICON_LAB="🧪"
ICON_VM="💻"
ICON_NET="🌐"
ICON_OK="✔"
ICON_WARN="⚠"
ICON_FAIL="✖"

def show_machine_states():
    states = get_vm_states()

    print(ACCENT + "\nLive Machine Status\n" + "-" * 40 + RESET)

    for phase, vms in PHASES.items():
        print(MENU + f"\nChapter {phase}" + RESET)
        for vm in vms:
            state = states.get(vm, "not_created")
            print(f"  {ICON_VM} {vm:<25} {format_state(state)}")


def format_state(state):
    if state == "running":
        return SUCCESS + "● RUNNING" + RESET
    elif state == "poweroff":
        return WARN + "● OFF" + RESET
    elif state == "not_created":
        return ERROR + "● NOT CREATED" + RESET
    elif state == "aborted":
        return ERROR + "● ABORTED" + RESET
    else:
        return INFO + "● UNKNOWN" + RESET


# ==================================================
# UTILITIES
# ==================================================
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def run(cmd):
    os.system(cmd)

def exists(cmd):
    return shutil.which(cmd) is not None

def pause():
    input(INFO + "Press Enter to continue..." + RESET)

def confirm(msg):
    return input(WARN + msg + " (y/N): " + RESET).strip().lower() == "y"

# ANSI stripping
ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(text):
    return ANSI_RE.sub('', text)

# UI BOX
BOX_WIDTH = 70

def display_width(text):
    return wcswidth(strip_ansi(text))

def pad(text, width):
    return text + " " * max(0, width - display_width(text))

def box(text=""):
    print("│" + pad(text, BOX_WIDTH) + "│")

def box_top():
    print("┌" + "─" * BOX_WIDTH + "┐")

def box_mid():
    print("├" + "─" * BOX_WIDTH + "┤")

def box_bot():
    print("└" + "─" * BOX_WIDTH + "┘")

# MACHINE STATUS
def get_vm_states():
    """
    Returns dict:
    {
        "MAD-BRENNER-DC02": "running",
        "MAD-BYERS-PC01": "poweroff",
        ...
    }
    """
    states = {}

    try:
        out = subprocess.run(
            "vagrant status --machine-readable",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        ).stdout
    except:
        return states

    for line in out.splitlines():
        parts = line.split(",")
        if len(parts) >= 4 and parts[2] == "state":
            states[parts[1]] = parts[3]

    return states

# SYSTEM CHECK
def system_check():
    print(MENU + f"{ICON_SYS} System Requirement Check" + RESET)

    cpu = os.cpu_count()
    disk = shutil.disk_usage("/").free / (1024**3)

    try:
        ram = round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024**3),1)
    except:
        ram = None

    print(f"CPU Cores : {cpu}")
    print(f"RAM       : {ram} GB" if ram else "RAM       : Unknown")
    print(f"Disk Free : {int(disk)} GB")

    ok = True
    if cpu < MIN_CPU:
        print(ERROR + f"{ICON_FAIL} CPU below {MIN_CPU} cores" + RESET); ok=False
    if ram and ram < MIN_RAM:
        print(ERROR + f"{ICON_FAIL} RAM below {MIN_RAM} GB" + RESET); ok=False
    if disk < MIN_DISK:
        print(ERROR + f"{ICON_FAIL} Disk below {MIN_DISK} GB" + RESET); ok=False
    if not exists("vagrant"):
        print(ERROR + f"{ICON_FAIL} Vagrant not installed" + RESET); ok=False
    if not exists("VBoxManage"):
        print(ERROR + f"{ICON_FAIL} VirtualBox not installed" + RESET); ok=False

    if ok:
        print(SUCCESS + f"{ICON_OK} System meets MAD requirements" + RESET)
    else:
        print(WARN + f"{ICON_WARN} System may not run MAD optimally" + RESET)

# PLUGIN CHECK
def plugin_check():
    print(MENU + "🔌 Vagrant Plugin Check" + RESET)
    out = subprocess.run("vagrant plugin list", shell=True, stdout=subprocess.PIPE, text=True).stdout
    for p in REQUIRED_PLUGINS:
        if p in out:
            print(SUCCESS + f"{ICON_OK} {p}" + RESET)
        else:
            print(WARN + f"{ICON_WARN} {p} missing" + RESET)
            if confirm(f"Install {p}?"):
                run(f"vagrant plugin install {p}")

# NETWORK
def network_isolate():
    print(WARN + ICON_NET + " Simulating network outage..." + RESET)
    run("vagrant ssh dc01 -c 'sudo systemctl stop named'")

def network_restore():
    print(SUCCESS + ICON_NET + " Restoring network..." + RESET)
    run("vagrant ssh dc01 -c 'sudo systemctl start named'")


# ROE (Rules Of Engagement Powershell Script)
def run_roe():
    if not os.path.exists("roe.ps1"):
        return

    print(INFO + "\nLaunching Rules of Engagement...\n" + RESET)

    if os.name == "nt":
        run("powershell -ExecutionPolicy Bypass -File roe.ps1")
    else:
        run("pwsh -ExecutionPolicy Bypass -File roe.ps1")

# Configure the LAB based on config file

def configure_lab():
    cfg = load_config()

    print(MENU + "\nLab Component Configuration\n" + RESET)

    def ask(key, label):
        current = cfg.get(key, False)
        val = input(
            f"{label} [{ 'ON' if current else 'OFF' }] (y/N): "
        ).strip().lower()
        if val == "y":
            cfg[key] = True
        elif val == "n":
            cfg[key] = False
        # else: keep existing value

    ask("install_root_ad",  "Install ROOT AD (HAWKINS.MAD)")
    ask("install_child_ad", "Install CHILD AD (LAB.HAWKINS.MAD)")
    ask("install_adcs",     "Install STARCOURT ADCS")

    save_config(cfg)

    print(SUCCESS + "\nConfiguration saved to config.yaml\n" + RESET)

#Enable FULL MAD LAB Function
def enable_full_lab():
    cfg = {
        "install_root_ad": True,
        "install_child_ad": True,
        "install_adcs": True
    }
    save_config(cfg)
    print(SUCCESS + "✔ Full MAD lab enabled (all components ON)\n" + RESET)

# LAB Health check function
def health_check():
    print(MENU + "\nMAD Lab Health Check\n" + RESET)

    checks = [
        ("Vagrant status", "vagrant status"),
        ("STARCOURT CA", "vagrant winrm MAD-STARCOURT-DC -c \"certutil -ping\""),
        ("Web Enrollment", "vagrant winrm MAD-STARCOURT-DC -c \"Invoke-WebRequest http://localhost/certsrv -UseDefaultCredentials\"")
    ]

    for name, cmd in checks:
        print(INFO + f"[*] {name}" + RESET)
        rc = os.system(cmd + " > nul 2>&1")
        if rc == 0:
            print(SUCCESS + "  ✔ OK" + RESET)
        else:
            print(ERROR + "  ✖ FAILED" + RESET)

#Windows Defender Toggle
def defender_toggle(enable: bool):
    mode = "Enable" if enable else "Disable"
    print(WARN + f"{mode} Windows Defender across lab\n" + RESET)

    ps_cmd = (
        "Set-MpPreference -DisableRealtimeMonitoring $false"
        if enable else
        "Set-MpPreference -DisableRealtimeMonitoring $true"
    )

    for vm in WINDOWS_MACHINES:
        print(INFO + f"→ {vm}" + RESET)
        run(f'vagrant winrm {vm} -c "{ps_cmd}"')


# LAB STATUS (CACHED)
_last_status = {}
_last_status_time = 0

def get_vm_states_cached(ttl=5):
    global _last_status, _last_status_time
    now = time.time()

    if now - _last_status_time < ttl:
        return _last_status

    out = subprocess.run(
        "vagrant status --machine-readable",
        shell=True,
        stdout=subprocess.PIPE,
        text=True
    ).stdout

    states = {}
    for line in out.splitlines():
        parts = line.split(",")
        if len(parts) >= 4 and parts[2] == "state":
            states[parts[1]] = parts[3]

    _last_status = states
    _last_status_time = now
    return states

def lab_status_badge():
    states = get_vm_states_cached()
    if not states:
        return WARN + "[NO VMS]" + RESET

    running = sum(1 for s in states.values() if s == "running")
    total = len(states)

    if running == 0:
        return ERROR + "[OFFLINE]" + RESET
    elif running == total:
        return SUCCESS + f"[ONLINE {running}/{total}]" + RESET
    else:
        return WARN + f"[PARTIAL {running}/{total}]" + RESET


#Show Lab Summary
def show_lab_summary():
    cfg = load_config()

    enabled = []
    disabled = []

    for key, machines in CONFIG_MACHINE_MAP.items():
        if cfg.get(key, False):
            enabled.extend(machines)
        else:
            disabled.extend(machines)

    attack_surface = cfg.get("attack_surface", "lab").upper()
    defender = "DISABLED" if attack_surface == "LAB" else "ENABLED"

    print(MENU + "\nMAD Deployment Summary\n" + RESET)
    print(ACCENT + "-" * 50 + RESET)

    print(INFO + "Configuration:" + RESET)
    for k in ["install_root_ad", "install_child_ad", "install_adcs"]:
        state = "ON" if cfg.get(k, False) else "OFF"
        print(f"  {k:<20}: {state}")

    print("\n" + INFO + "Attack Surface:" + RESET)
    print(f"  Mode              : {attack_surface}")
    print(f"  Windows Defender  : {defender}")

    print("\n" + INFO + "Machines to be DEPLOYED:" + RESET)
    if enabled:
        for m in sorted(set(enabled)):
            print(SUCCESS + f"  ✔ {m}" + RESET)
    else:
        print(WARN + "  (none)" + RESET)

    print("\n" + INFO + "Machines SKIPPED:" + RESET)
    if disabled:
        for m in sorted(set(disabled)):
            print(ERROR + f"  ✖ {m}" + RESET)
    else:
        print(INFO + "  (none)" + RESET)

    print(ACCENT + "-" * 50 + RESET)

    if not confirm("Proceed with this deployment?"):
        print(WARN + "Deployment cancelled." + RESET)
        return False

    return True


# BANNER
# Make it little nice
def banner():
    clear()
    print(TITLE)
    print("███╗   ███╗  █████╗  ██████╗ ")
    print("████╗ ████║ ██╔══██╗ ██╔══██╗")
    print("██╔████╔██║ ███████║ ██║  ██║")
    print("██║╚██╔╝██║ ██╔══██║ ██║  ██║")
    print("██║ ╚═╝ ██║ ██║  ██║ ██████╔╝")
    print("╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚═════╝ ")
    print(RESET)
    print(TITLE + LAB_NAME + " " + lab_status_badge() + RESET)
    print(INFO + f"Version {VERSION}  |  MADness of Active Directory Security" + RESET)
    print(ACCENT + "-"*70 + RESET)
    print(INFO + OVERVIEW.strip() + RESET)
    print(ACCENT + "-"*70 + RESET)

# Script MENU 
def menu():
    box_top()
    box(TITLE + LAB_NAME + " " + lab_status_badge() + RESET)
    box(INFO + f"Version {VERSION}  |  MADness of Active Directory Security" + RESET)
    box_mid()
    box(MENU + f"{ICON_SYS} SYSTEM" + RESET)
    box(" [1] Check system requirements")
    box(" [2] Validate / install plugins")
    box("")
    box(MENU + f"{ICON_LAB} LAB CONTROL" + RESET)
    box(" [3] Start full lab")
    box(" [4] Start lab phase")
    box(" [5] Show lab status")
    box(" [6] Shutdown lab")
    box(" [7] Destroy lab")
    box("")
    box(MENU + f"{ICON_VM} MACHINE CONTROL" + RESET)
    box(" [8] Enable Windows Defender")
    box(" [9] Disable Windows Defender")
    box("")
    box(MENU + f"{ICON_NET} NETWORK" + RESET)
    box("")
    box(" [11] Read the ROE")
    box(" [0] Exit")
    box_bot()

# MAIN Function
def main():
    while True:
        banner()
        menu()
        c = input(ACCENT + "mad> " + RESET)
        print(ACCENT + "-"*70 + RESET)

        if c=="1": system_check()
        elif c=="2": plugin_check()
        elif c=="3":
            enable_full_lab()
            if show_lab_summary():
                rc = run("vagrant up")
                if rc == 0:
                    run_roe()

        elif c=="4":
            configure_lab()
            if show_lab_summary():
                rc = run("vagrant up")
                if rc == 0:
                    run_roe()
        elif c=="5": show_machine_states()
        elif c=="6": run("vagrant halt")
        elif c=="7":
            if confirm("Destroy the entire lab?"):
                run("vagrant destroy -f")
        elif c=="8": defender_toggle(enable=True)
        elif c=="9": defender_toggle(enable=False)
        elif c=="10": network_restore()
        elif c=="11": run_roe()
        elif c=="0":
            print(INFO + "Exiting MAD Controller." + RESET)
            break
        else:
            print(ERROR + "Invalid option." + RESET)

        print(ACCENT + "-"*70 + RESET)
        pause()

if __name__ == "__main__":
    main()
