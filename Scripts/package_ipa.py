#!/usr/bin/env python3
"""Build an unsigned ARM64 device IPA and remove provisioning/account sidecars."""
import argparse
import hashlib
import plistlib
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('app', type=Path)
parser.add_argument('--output', type=Path, default=Path('release-output/MrRunnerPlus-Respring-unsigned.ipa'))
a = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='mrrunner-release-') as tmp:
    target = Path(tmp) / 'Payload' / 'MrRunnerPlus.app'
    shutil.copytree(a.app, target, symlinks=False)
    info = plistlib.loads((target / 'Info.plist').read_bytes())
    executable = target / info['CFBundleExecutable']
    assert executable.is_file(), f'Missing native executable: {executable}'
    if subprocess.run(['codesign', '-dv', str(target)], capture_output=True).returncode == 0:
        subprocess.run(['codesign', '--remove-signature', str(target)], check=True)
    for file in target.rglob('embedded.mobileprovision'):
        file.unlink()
    for directory in list(target.rglob('_CodeSignature')):
        if directory.is_dir():
            shutil.rmtree(directory)
    for file in target.rglob('iTunesMetadata.plist'):
        file.unlink()
    guest = target / 'MrRunnerPlus.ipa'
    assert guest.is_file(), 'Missing nested original game'
    with zipfile.ZipFile(guest) as archive:
        assert archive.testzip() is None, 'Corrupt guest IPA'
        assert all(n.startswith('Payload/') and not any(ex in n for ex in
                   ('_CodeSignature/', 'SC_Info/', 'embedded.mobileprovision', 'iTunesMetadata.plist'))
                   for n in archive.namelist()), 'Unsanitized guest'
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(a.output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(target.rglob('*')):
            if path.is_file() and not path.name.startswith('._') and path.name != '.DS_Store':
                archive.write(path, path.relative_to(Path(tmp)))
    with zipfile.ZipFile(a.output) as archive:
        assert archive.testzip() is None, 'Corrupt output IPA'
print(f'{hashlib.sha256(a.output.read_bytes()).hexdigest()}  {a.output}')
