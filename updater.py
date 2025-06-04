import requests

class Updater:
    def __init__(self, version, update_url):
        self.version = version
        self.update_url = update_url

    def check_for_update(self):
        try:
            response = requests.get(self.update_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('version')
                if latest_version and latest_version != self.version:
                    return True, latest_version, data.get('changelog', '')
                return False, self.version, ''
            else:
                return False, self.version, 'Update server error.'
        except Exception as e:
            return False, self.version, f'Error: {e}'

    def download_update(self, download_url, dest_path):
        try:
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return True
        except Exception as e:
            print(f"[Updater] Download failed: {e}")
            return False

    def get_current_version(self):
        """Return the current version of the application."""
        return self.version

    def get_latest_version_info(self):
        """Fetch and return the latest version info from the update server."""
        try:
            response = requests.get(self.update_url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"[Updater] Error fetching latest version info: {e}")
            return None

    def verify_update_integrity(self, file_path, expected_hash):
        """Verify the integrity of the downloaded update file using SHA256."""
        import hashlib
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            file_hash = sha256.hexdigest()
            return file_hash == expected_hash, file_hash
        except Exception as e:
            print(f"[Updater] Integrity check failed: {e}")
            return False, None

    def apply_update(self, file_path):
        """Stub for applying the update (e.g., extracting and replacing files)."""
        # In a real app, implement extraction and replacement logic here
        print(f"[Updater] Applying update from {file_path} (stub)")
        return True

    def rollback_update(self, backup_path):
        """Stub for rolling back to a previous version using a backup."""
        # In a real app, implement rollback logic here
        print(f"[Updater] Rolling back using backup at {backup_path} (stub)")
        return True

if __name__ == "__main__":
    updater = Updater(version="1.0.0", update_url="https://example.com/sackbot_update.json")
    has_update, latest, changelog = updater.check_for_update()
    print(f"Update available: {has_update}, Latest: {latest}, Changelog: {changelog}")
    # Example: get current and latest version info
    print("Current version:", updater.get_current_version())
    print("Latest version info:", updater.get_latest_version_info())
    # Example: verify integrity (stub hash)
    # ok, file_hash = updater.verify_update_integrity('sackbot-latest.zip', 'expectedsha256hash')
    # print('Integrity OK:', ok, 'Hash:', file_hash)
    # Example: apply and rollback update (stubs)
    # updater.apply_update('sackbot-latest.zip')
    # updater.rollback_update('backup.zip')
