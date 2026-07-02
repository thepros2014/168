import os
import sys
import hashlib
import uuid
import zipfile
from datetime import datetime

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Exclude patterns
exclude = {'.git', '__pycache__', '.venv', 'venv', '.pytest_cache'}

guid = str(uuid.uuid4())
zip_name = f'submission-{guid}.zip'
zip_path = os.path.join(root, zip_name)
manifest_path = os.path.join(root, 'submission-manifest.txt')
guid_path = os.path.join(root, 'SUBMISSION_GUID.txt')

# Write GUID file
with open(guid_path, 'w') as f:
    f.write(guid + '\n')

# Create zip
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for dirpath, dirnames, filenames in os.walk(root):
        # remove excluded dirs in-place
        dirnames[:] = [d for d in dirnames if d not in exclude]
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == '.':
            rel_dir = ''
        for fname in filenames:
            if fname.endswith('.pyc') or fname.endswith('.patch'):
                continue
            full = os.path.join(dirpath, fname)
            arcname = os.path.join(rel_dir, fname) if rel_dir else fname
            zf.write(full, arcname)

# Compute SHA256
sha256 = hashlib.sha256()
with open(zip_path, 'rb') as f:
    for chunk in iter(lambda: f.read(8192), b''):
        sha256.update(chunk)
sha = sha256.hexdigest()

# Write manifest
with open(manifest_path, 'w') as f:
    f.write(f'GUID: {guid}\n')
    f.write(f'ZIP: {zip_name}\n')
    f.write(f'SHA256: {sha}\n')
    f.write(f'DATE: {datetime.utcnow().isoformat()}Z\n')

print(zip_path)
print(guid)
print(sha)
