#!/usr/bin/env python3
import sys
import subprocess
import requests

ZAMMAD_URL = "<Enter your Zammad URL here>"
ZAMMAD_TOKEN = "<Enter your Zammad API Token here>"

HEADERS = {
    "Authorization": f"Token token={ZAMMAD_TOKEN}",
    "Content-Type": "application/json"
}

def run_ansible_patch(hostname):
    cmd = [
        "ansible-playbook",
        "-i", "/opt/patchmgmt/patching/inventory",
        "/opt/patchmgmt/patching/patch.yml",
        "--vault-password-file", "/opt/patchmgmt/patching/.vault",
        "--limit", hostname
    ]
    print(f"[INFO] Running Ansible for host: {hostname}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr

def post_ticket_article(ticket_id, body):
    url = f"{ZAMMAD_URL}/api/v1/ticket_articles"
    data = {
        "ticket_id": ticket_id,
        "body": body,
        "internal": False
    }
    r = requests.post(url, headers=HEADERS, json=data)
    if not r.ok:
        print(f"[ERROR] Failed to post article to ticket {ticket_id}: {r.text}")
        return False
    return True

def close_ticket(ticket_id):
    url = f"{ZAMMAD_URL}/api/v1/tickets/{ticket_id}"
    data = {
        "state_id": 4  # state_id 4 = closed
    }
    r = requests.put(url, headers=HEADERS, json=data)
    if not r.ok:
        print(f"[ERROR] Failed to close ticket {ticket_id}: {r.text}")
        return False
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: run_patch.py <ticket_id> <hostname>")
        sys.exit(1)
    ticket_id = int(sys.argv[1])
    hostname = sys.argv[2]

    retcode, stdout, stderr = run_ansible_patch(hostname)
    output = f"Ansible Return Code: {retcode}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"

    posted = post_ticket_article(ticket_id, output)
    if not posted:
        print("[ERROR] Aborting: Could not post Ansible output to ticket.")
        sys.exit(2)

    closed = close_ticket(ticket_id)
    if closed:
        print(f"[INFO] Ticket {ticket_id} closed successfully.")
    else:
        print("[ERROR] Failed to close ticket.")

if __name__ == "__main__":
    main()
