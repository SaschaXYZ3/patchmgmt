#!/usr/bin/env python3

import requests
from datetime import datetime
import subprocess

ZAMMAD_URL = "<Enter your Zammad URL here>"
ZAMMAD_TOKEN = "<Enter your Zammad API Token here>"

HEADERS = {
    "Authorization": f"Token token={ZAMMAD_TOKEN}",
    "Content-Type": "application/json"
}

def get_approved_tickets():
    url = f"{ZAMMAD_URL}/api/v1/tickets"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    all_tickets = response.json()

    approved_tickets = []
    for t in all_tickets:
        if t.get("state_id") == 4:  # closed überspringen
            continue
        ticket_id = t["id"]
        detail_url = f"{ZAMMAD_URL}/api/v1/tickets/{ticket_id}"
        detail_response = requests.get(detail_url, headers=HEADERS)
        if detail_response.ok:
            full_ticket = detail_response.json()
            approved_tickets.append(full_ticket)
        else:
            print(f"Failed to fetch full ticket {ticket_id}: {detail_response.text}")
    print(f"[INFO] Collected {len(approved_tickets)} tickets")
    return approved_tickets

def extract_hostname_from_article(ticket):
    ticket_id = ticket["id"]
    article_url = f"{ZAMMAD_URL}/api/v1/ticket_articles/by_ticket/{ticket_id}"
    r = requests.get(article_url, headers=HEADERS)
    if not r.ok:
        print(f"[ERROR] Failed to fetch articles for ticket {ticket_id}: {r.text}")
        return None
    articles = r.json()
    if not articles:
        print(f"[WARN] Ticket {ticket_id} has no articles")
        return None
    for article in articles:
        content = article.get("body", "")
        for line in content.splitlines():
            if "Host:" in line:
                return line.split("Host:")[1].strip()
    return None

def schedule_run_patch(ticket_id, hostname, at_time):
    if is_job_already_scheduled(ticket_id, hostname):
        print(f"[INFO] Skip scheduling, job already exists for ticket {ticket_id}, host {hostname}")
        return
    cmd = f"python3 /opt/patchmgmt/zammad/run_patch.py {ticket_id} {hostname}"
    print(f"[INFO] Scheduling run_patch.py for ticket {ticket_id} at {at_time}: {cmd}")
    proc = subprocess.run(
        ['at', at_time],
        input=cmd + "\n",
        text=True,
        capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"[ERROR] 'at' command failed: {proc.stderr}")
    print(f"[at stdout]: {proc.stdout.strip()}")

def schedule_patches():
    tickets = get_approved_tickets()
    for ticket in tickets:
        hostname = extract_hostname_from_article(ticket)
        if not hostname:
            print(f"[WARN] No hostname found in ticket {ticket['id']}")
            continue
        pending_time = ticket.get("pending_time")
        if pending_time:
            try:
                dt = datetime.strptime(pending_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                at_time = dt.strftime("%H:%M %Y-%m-%d")
            except Exception as e:
                print(f"[ERROR] Ungültiges pending_time Format in Ticket {ticket['id']}: {pending_time} - {e}")
                at_time = "now + 2 minutes"
        else:
            print(f"[WARN] Kein pending_time in Ticket {ticket['id']}, setze Standardzeit")
            at_time = "now + 2 minutes"
        schedule_run_patch(ticket['id'], hostname, at_time)

def is_job_already_scheduled(ticket_id, hostname):
    # Alle at-Jobs holen (nur die IDs)
    proc = subprocess.run(["atq"], capture_output=True, text=True)
    if proc.returncode != 0:
        print("[WARN] atq konnte nicht ausgeführt werden")
        return False

    jobs = proc.stdout.strip().splitlines()
    for line in jobs:
        # Job ID ist das erste Wort in der Zeile
        job_id = line.split()[0]
        # Job-Skript auslesen
        proc2 = subprocess.run(["at", "-c", job_id], capture_output=True, text=True)
        if proc2.returncode != 0:
            continue
        script = proc2.stdout
        # Prüfen, ob unser Befehl darin vorkommt
        if f"run_patch.py {ticket_id} {hostname}" in script:
            print(f"[INFO] Job für Ticket {ticket_id} und Host {hostname} bereits geplant (JobID {job_id})")
            return True
    return False

if __name__ == "__main__":
    schedule_patches()
