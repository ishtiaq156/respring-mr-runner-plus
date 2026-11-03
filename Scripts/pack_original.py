#!/usr/bin/env python3
"""Rebuild the original, signature-free guest IPA from pinned local inputs."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
payload = root / 'Original' / 'Payload'
pins = json.loads((root / 'Original' / 'payload-sha256.json').read_text())
assert pins, 'Missing original game manifest'
with zipfile.ZipFile(sys.argv[1], 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for relative, expected in sorted(pins.items()):
        path = root / 'Original' / relative
        assert path.is_file() and not path.is_symlink(), f'Missing or linked guest file: {relative}'
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise SystemExit(f'Guest input checksum mismatch: {relative}')
        entry = zipfile.ZipInfo(relative, (2026, 1, 1, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = 0o100644 << 16
        z.writestr(entry, data)
