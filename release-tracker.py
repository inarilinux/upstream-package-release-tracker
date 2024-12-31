import requests
import json
import os

def get_latest_release_or_tag(repo):
    release_url = f"https://api.github.com/repos/{repo}/releases/latest"
    tag_url = f"https://api.github.com/repos/{repo}/tags"
    
    try:
        release_response = requests.get(release_url)
        if release_response.status_code == 200:
            release_data = release_response.json()
            return release_data.get('tag_name')
        
        tag_response = requests.get(tag_url)
        if tag_response.status_code == 200:
            tag_data = tag_response.json()
            if tag_data:
                return tag_data[0].get('name')
            else:
                return "No tags"
        
        print(f"Tidak dapat mengambil rilis atau tag untuk {repo}.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {repo}: {e}")
        return None

def save_version(file_path, version):
    with open(file_path, 'w') as file:
        json.dump(version, file, indent=4)

def load_version(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def load_repos_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            # Baca setiap baris, strip spasi atau newline, dan abaikan baris kosong
            repos = [line.strip() for line in file if line.strip()]
        return repos
    else:
        print(f"File {file_path} tidak ditemukan.")
        return []


def track_multiple_versions_from_file(repo_file, version_file):
    repos = load_repos_from_file(repo_file)
    if not repos:
        print("Daftar repository kosong atau tidak ditemukan.")
        return

    saved_versions = load_version(version_file)
    updated_versions = {}

    for repo in repos:
        print(f"Memeriksa repository: {repo}")
        latest_version = get_latest_release_or_tag(repo)
        if not latest_version:
            print(f"Tidak dapat mengambil versi terbaru untuk {repo}.")
            continue

        saved_version = saved_versions.get(repo)
        if saved_version != latest_version:
            print(f"Versi baru untuk {repo}: {latest_version} (sebelumnya: {saved_version})")
        else:
            print(f"Versi terbaru untuk {repo} ({latest_version}) tidak ada versi terbaru.")

        print("")

        updated_versions[repo] = latest_version

    save_version(version_file, updated_versions)


repo_list_file = "upstream-list.txt"
version_file = "versions.json"

track_multiple_versions_from_file(repo_list_file, version_file)