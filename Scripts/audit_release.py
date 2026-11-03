#!/usr/bin/env python3
"""Verify the exact original guest and unsigned ARM64 iOS host in a release IPA."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import plistlib
import struct
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('ipa', type=Path)
args = parser.parse_args()

root = Path(__file__).resolve().parents[1]
expected = json.loads((root / 'Original' / 'payload-sha256.json').read_text())
sha256 = lambda data: hashlib.sha256(data).hexdigest()

def content_only_names(archive):
    return {name for name in archive.namelist() if not name.endswith('/')}

with zipfile.ZipFile(args.ipa) as host:
    assert host.testzip() is None, 'Damaged IPA member'
    names = content_only_names(host)
    assert len(names) == len([i for i in host.infolist() if not i.is_dir()]), 'Duplicate member'
    assert all(n.startswith('Payload/MrRunnerPlus.app/') and '..' not in n.split('/') for n in names), 'Outside app payload'
    assert not any(m in n for n in names for m in ('_CodeSignature/', 'SC_Info/', 'embedded.mobileprovision', 'iTunesMetadata.plist')), 'Signed or sensitive metadata'
    prefix = 'Payload/MrRunnerPlus.app/'
    info = plistlib.loads(host.read(prefix + 'Info.plist'))
    assert info['CFBundleIdentifier'] == 'com.respring.mrrunnerplus', 'Wrong bundle identity'
    assert info['CFBundleSupportedPlatforms'] == ['iPhoneOS'], 'Not an iPhone device build'
    assert info['CFBundleShortVersionString'] == '1.0', 'Unexpected host version'
    native = host.read(prefix + info['CFBundleExecutable'])
    magic, cpu, subtype, filetype = struct.unpack_from('<4I', native, 0)
    assert magic == 0xFEEDFACF and cpu == 0x0100000C and filetype == 2, 'Not ARM64 Mach-O executable'
    assert 'armv7' not in info['CFBundleExecutable'].lower(), 'Wrong executable'
    assert prefix + 'touchHLE_dylibs/libstdc++.6.0.9.dylib' in names, 'Missing guest C++ library'
    assert prefix + 'touchHLE_dylibs/libgcc_s.1.dylib' in names, 'Missing guest libgcc'
    guest_data = host.read(prefix + 'MrRunnerPlus.ipa')
    with zipfile.ZipFile(io.BytesIO(guest_data)) as guest:
        assert guest.testzip() is None, 'Guest IPA damaged'
        guest_names = content_only_names(guest)
        assert guest_names == set(expected), 'Guest files differ from pinned inventory'
        for n, value in expected.items():
            assert sha256(guest.read(n)) == value, f'Game source altered: {n}'
        guest_plist = plistlib.loads(guest.read('Payload/Mr.Runner Plus.app/Info.plist'))
        assert guest_plist['CFBundleIdentifier'] == 'com.gamevision.mrrunnerplus', 'Wrong guest game'
    with tempfile.TemporaryDirectory() as folder:
        executable = Path(folder) / 'MrRunnerPlusCompatibility'
        executable.write_bytes(native)
        result = subprocess.run(['otool', '-l', str(executable)], text=True, stdout=subprocess.PIPE, check=True)
        assert 'platform 2\n' in result.stdout, 'Expected iOS device Mach-O platform (2)'

print('PASS: unsigned ARM64 iPhone host, iOS platform, original guest, no profile/metadata')
print(f'PASS: {len(expected)} exact original guest input files verified by SHA-256')
print(f'IPA SHA-256: {sha256(args.ipa.read_bytes())}')
