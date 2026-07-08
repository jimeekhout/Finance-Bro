#!/usr/bin/env python3
"""
Finance Bro — Deploy script
Gebruik: python deploy.py
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

# ── Instellingen ──────────────────────────────────────────────────────────────
BRONBESTAND = "Finance Bro.html"   # naam van het bestand dat je downloadt
DOEL        = "index.html"         # naam die Netlify verwacht
REPO_PAD    = "."                  # pad naar je lokale GitHub-repo (zelfde map = .)

# ── Kleurtjes voor terminal ───────────────────────────────────────────────────
GROEN  = "\033[92m"
GEEL   = "\033[93m"
ROOD   = "\033[91m"
RESET  = "\033[0m"
VET    = "\033[1m"

def stap(nr, tekst):
    print(f"\n{VET}[{nr}]{RESET} {tekst}")

def ok(tekst):
    print(f"  {GROEN}✓{RESET} {tekst}")

def fout(tekst):
    print(f"  {ROOD}✗ {tekst}{RESET}")
    sys.exit(1)

def run(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        fout(f"Commando mislukt: {cmd}\n    {r.stderr.strip()}")
    return r.stdout.strip()

# ── Welkomstscherm ────────────────────────────────────────────────────────────
print(f"\n{VET}╔══════════════════════════════════╗")
print(f"║     Finance Bro Deploy Script     ║")
print(f"╚══════════════════════════════════╝{RESET}")
print(f"Tijdstip: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

# ── Stap 1: Controleer of bronbestand bestaat ─────────────────────────────────
stap(1, f"Zoek '{BRONBESTAND}'...")
if not os.path.exists(BRONBESTAND):
    fout(f"'{BRONBESTAND}' niet gevonden.\n    Zet het bestand in dezelfde map als dit script.")
ok(f"Gevonden ({round(os.path.getsize(BRONBESTAND)/1024)} KB)")

# ── Stap 2: Vraag versienaam ──────────────────────────────────────────────────
stap(2, "Versienaam invoeren")
print(f"  {GEEL}Geef een korte beschrijving van deze versie:{RESET}")
print(f"  Voorbeelden: 'uitlogfunctie verbeterd', 'account tab toegevoegd'")
versie = input("  → ").strip()
if not versie:
    versie = f"update {datetime.now().strftime('%d-%m-%Y %H:%M')}"
commit_msg = versie
ok(f"Commit-bericht: '{commit_msg}'")

# ── Stap 3: Kopieer naar index.html ──────────────────────────────────────────
stap(3, f"Hernoem naar '{DOEL}'...")
doel_pad = os.path.join(REPO_PAD, DOEL)
shutil.copy2(BRONBESTAND, doel_pad)
ok(f"Gekopieerd naar {doel_pad}")

# ── Stap 4: Controleer Git ───────────────────────────────────────────────────
stap(4, "Controleer Git-repository...")
try:
    branch = run("git rev-parse --abbrev-ref HEAD", cwd=REPO_PAD)
    ok(f"Git gevonden, branch: {branch}")
except:
    fout("Git niet gevonden of dit is geen Git-repository.\n    Zet dit script in je 'finance-bro' map.")

# ── Stap 5: Git add + commit + push ──────────────────────────────────────────
stap(5, "Bestanden toevoegen aan Git...")
run(f"git add -A", cwd=REPO_PAD)
ok("Alle bestanden toegevoegd")

stap(6, "Commit aanmaken...")
run(f'git commit -m "{commit_msg}"', cwd=REPO_PAD)
ok(f"Commit aangemaakt")

stap(7, "Pushen naar GitHub...")
run("git push", cwd=REPO_PAD)
ok("Gepusht naar GitHub!")

# ── Klaar ─────────────────────────────────────────────────────────────────────
print(f"\n{GROEN}{VET}✅ Klaar!{RESET}")
print(f"   Netlify deployt automatisch binnen ~30 seconden.")
print(f"   Bekijk versies op GitHub via: index.html → History\n")
