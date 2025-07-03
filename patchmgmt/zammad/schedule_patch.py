#!/usr/bin/env python3
import os
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
    url = f"{ZAMMAD_URL}/api/v1/tickets/search"
    params = {
        "query": "state_id:4"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def extract_hostname_from_article(ticket):
    for article_id in ticket.get("article_ids", []):
        article_url = f"{ZAMMAD_URL}/api/v1/ticket_articles/{article_id}"
        r = requests.get(article_url, headers=HEADERS)
        if r.ok:
            content = r.json().get("body", "")
            print(content)
            print(f"Ticket {ticket['id']} Artikel {article_id} Inhalt:\n{content}\n---")
            for line in content:
                #print(type(line))
                #hostname = line['Host']
                if "Host: " in line:
                    hostname = line.split("Host:")[1].strip()
                    print(hostname)

           # .splitlines():
           #     if line.startswith("Host: "):
           #         line_split = line.split(":",1)
           #         print(line_split)
           #         return line_split[1].strip()
                return hostname
    return None

def schedule_ansible_patch(hostname, at_time):
    # Ansible-Befehl mit Passwort-Variablen und -kK-Flags
    ansible_cmd = (
        f"ansible-playbook -i /opt/patchmgmt/ansible/inventory /opt/patchmgmt/patching/patch.yml --vault-password-file /opt/patchmgmt/patching/.vault --limit {hostname}"
    )

    print(f"Scheduling command at {at_time}: {ansible_cmd}")

    proc = subprocess.run(
        ['at', at_time],
        input=ansible_cmd + "\n",
        text=True,
        capture_output=True
    )
    print("stdout:", proc.stdout)
    print("stderr:", proc.stderr)
    print("returncode:", proc.returncode)

    if proc.returncode != 0:
        raise RuntimeError(f"at command failed: {proc.stderr}")

def schedule_patches():
    print("Fetching approved tickets...")
    tickets = get_approved_tickets()
    print(f"Found {len(tickets)} approved tickets")

    for ticket in tickets:
        hostname = extract_hostname_from_article(ticket)
        if not hostname:
            print(f"No hostname found in ticket {ticket['id']}")
            continue

        pending_till = ticket.get("pending_till")
        if pending_till:
            try:
                dt = datetime.strptime(pending_till, "%Y-%m-%dT%H:%M:%SZ")
                at_time = dt.strftime("%H:%M %m/%d/%Y")
            except Exception as e:
                print(f"Error parsing pending_till '{pending_till}' for ticket {ticket['id']}: {e}")
                at_time = "now + 2 minutes"
        else:
            at_time = "now + 2 minutes"

        print(f"Scheduling patch for host: {hostname}")
        schedule_ansible_patch(hostname, at_time)

if __name__ == "__main__":
    schedule_patches()

                                              