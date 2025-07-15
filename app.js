import fetch from 'node-fetch';

const HETZNER_TOKEN = process.env.HETZNER_TOKEN;
const HETZNER_API_URL = 'https://api.hetzner.cloud/v1';

async function getServers() {
    const res = await fetch(`${HETZNER_API_URL}/servers`, {
        headers: { Authorization: `Bearer ${HETZNER_TOKEN}` }
    });
    const data = await res.json();
    return data.servers;
}

async function lockServer(serverId) {
    await fetch(`${HETZNER_API_URL}/servers/${serverId}/actions/lock`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${HETZNER_TOKEN}` }
    });
}

async function updateLabels(server) {
    const labels = { ...server.labels };
    if (labels.Autobackup !== 'true') {
        labels.Autobackup = 'true';
        await fetch(`${HETZNER_API_URL}/servers/${server.id}`, {
            method: 'PUT',
            headers: {
                Authorization: `Bearer ${HETZNER_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: server.name,
                labels
            })
        });
    }
}

async function checkAndUpdateServers() {
    const servers = await getServers();
    for (const server of servers) {
        if (!server.locked) await lockServer(server.id);
        await updateLabels(server);
    }
}

await checkAndUpdateServers();
process.exit(0);
