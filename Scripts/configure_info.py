#!/usr/bin/env python3
"""Set the build destination identity, preserving other host metadata."""
from pathlib import Path
import os
import plistlib
import sys

path = Path(sys.argv[1])
sdk = sys.argv[2]
assert sdk in ('iphoneos', 'iphonesimulator')
info = plistlib.loads(path.read_bytes())
info['CFBundleSupportedPlatforms'] = ['iPhoneOS' if sdk == 'iphoneos' else 'iPhoneSimulator']
if os.environ.get('PRODUCT_BUNDLE_IDENTIFIER'):
    info['CFBundleIdentifier'] = os.environ['PRODUCT_BUNDLE_IDENTIFIER']
path.write_bytes(plistlib.dumps(info))
