import os
import zipfile

EXCLUDE = {'__pycache__', 'output_test.avi', 'input.mp4', 'users.json', 'sackbot-latest.zip', 'backup.zip'}

PACKAGE_NAME = 'sackbot-latest.zip'


def should_include(filename):
    for ex in EXCLUDE:
        if filename.startswith(ex) or filename.endswith(ex):
            return False
    return True

def package_app():
    with zipfile.ZipFile(PACKAGE_NAME, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk('.'):
            # Skip excluded dirs
            dirs[:] = [d for d in dirs if d not in EXCLUDE]
            for file in files:
                if file == PACKAGE_NAME or not should_include(file):
                    continue
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, '.')
                zf.write(filepath, arcname)
    print(f"Packaged app as {PACKAGE_NAME}")

if __name__ == "__main__":
    package_app()
