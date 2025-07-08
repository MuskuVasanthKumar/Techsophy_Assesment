

import os
import requests
from dotenv import load_dotenv


load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

def get_commit_details(repo_owner, repo_name, commit_sha):
    """
    Fetch commit details from GitHub using the API.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        files = data.get('files', [])

        return {
            "commit_sha": commit_sha,
            "total_files_changed": len(files),
            "total_lines_added": sum(f.get('additions', 0) for f in files),
            "total_lines_deleted": sum(f.get('deletions', 0) for f in files),
            "services_affected": list(set(f["filename"].split("/")[0] for f in files if "/" in f["filename"]))
        }
    else:
        raise Exception(f"GitHub API Error {response.status_code}: {response.text}")


def compute_change_impact_score(commit_data):
    """
    Compute a simple impact score based on changed files and lines of code.
    Scale to 0–1 range.
    """
    score = (
        0.4 * commit_data["total_files_changed"] +
        0.3 * commit_data["total_lines_added"] +
        0.3 * commit_data["total_lines_deleted"]
    ) / 100.0

    return min(round(score, 2), 1.0)
