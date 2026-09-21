import json
import requests
import streamlit as st

def sync_to_github(filepath: str, data: list):
    token = st.secrets.get("GITHUB_TOKEN")
    repo = st.secrets.get("GITHUB_REPO")
    branch = st.secrets.get("GITHUB_BRANCH", "main")

    if not token or not repo:
        return False, "GitHub credentials not found in secrets. Saved locally."

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}/contents/{filepath}"

    res = requests.get(url, headers=headers, params={"ref": branch})
    sha = res.json().get("sha") if res.status_code == 200 else None

    import base64
    content_bytes = json.dumps(data, indent=2).encode('utf-8')
    content_b64 = base64.b64encode(content_bytes).decode('utf-8')

    payload = {
        "message": f"Update {filepath} via Streamlit Admin",
        "content": content_b64,
        "branch": branch
    }
    if sha:
        payload["sha"] = sha

    put_res = requests.put(url, headers=headers, json=payload)
    if put_res.status_code in [200, 201]:
        return True, "Synced directly to GitHub."
    return False, f"GitHub sync failed: {put_res.status_code}"
