import os
import requests
import asyncio

HETZNER_API_TOKEN = os.getenv("HETZNER_API_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")

HEADERS = {
    "Authorization": f"Bearer {HETZNER_API_TOKEN}",
    "Content-Type": "application/json"
}

async def handle_server():
    base_url = "https://api.hetzner.cloud/v1"

    servers_response = requests.get(f"{base_url}/servers", headers=HEADERS)
    servers_response.raise_for_status()
    servers = servers_response.json().get("servers", [])

    for server in servers:
        server_id = server["id"]
        labels = server.get("labels", {})
        updated_labels = labels.copy()
        modified = False

        if labels.get("locked") != "true":
            updated_labels["locked"] = "true"
            modified = True

        if labels.get("Autobackup") != "true":
            updated_labels["Autobackup"] = "true"
            modified = True

        if modified:
            payload = {"labels": updated_labels}
            print(f"Updating server {server_id}: {payload}")
            update_response = requests.put(f"{base_url}/servers/{server_id}", headers=HEADERS, json=payload)
            update_response.raise_for_status()
        else:
            print(f"Server {server_id} already up to date.")

if __name__ == "__main__":
    asyncio.run(handle_server())
