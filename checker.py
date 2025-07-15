import os
import requests
import asyncio

HETZNER_API_TOKEN = os.getenv("HETZNER_API_TOKEN")
if not HETZNER_API_TOKEN:
    raise Exception("HETZNER_API_TOKEN is missing")

HEADERS = {
    "Authorization": f"Bearer {HETZNER_API_TOKEN}",
    "Content-Type": "application/json"
}

async def handle_server():
    base_url = "https://api.hetzner.cloud/v1"
    servers_response = requests.get(f"{base_url}/servers", headers=HEADERS)
    if servers_response.status_code == 401:
        raise Exception("Unauthorized: Check if HETZNER_API_TOKEN is correct and has permissions!")
    servers_response.raise_for_status()
    servers = servers_response.json().get("servers", [])

    for server in servers:
        server_id = server["id"]
        labels = server.get("labels", {})
        updated_labels = labels.copy()
        modified = False

        # Check if delete and rebuild protections are enabled
        protection = server.get("protection", {})
        delete_protection = protection.get("delete", False)
        rebuild_protection = protection.get("rebuild", False)

        if not delete_protection or not rebuild_protection:
            payload = {"delete": True, "rebuild": True}
            print(f"Enabling protection for server {server_id}: {payload}")
            protection_resp = requests.post(
                f"{base_url}/servers/{server_id}/actions/change_protection",
                headers=HEADERS,
                json=payload,
            )
            protection_resp.raise_for_status()

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
