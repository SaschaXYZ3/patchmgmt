#!/usr/bin/env python3
import requests

ZAMMAD_URL = "<Enter your Zammad URL here>"
ZAMMAD_TOKEN = "<Enter your Zammad API Token here>"

HEADERS = {
    "Authorization": f"Token token={ZAMMAD_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_tickets():
    response = requests.get(ZAMMAD_URL, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Fehler: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Antwort enthält kein gültiges JSON: {e}")
    return []

def print_ticket_info(tickets):
    for ticket in tickets:
        print(f"Ticket ID: {ticket.get('id')}")
        print(f"Title: {ticket.get('title')}")
        pending_time = ticket.get('pending_time')
        if pending_time is not None:
            pending_till = pending_time.get('until')
        else:
            pending_till = None
        print(f"Pending till: {pending_till}")
        print(f"Created at: {ticket.get('created_at')}")
        print("-" * 40)

def main():
    tickets = fetch_tickets()
    print_ticket_info(tickets)

if __name__ == "__main__":
    main()
