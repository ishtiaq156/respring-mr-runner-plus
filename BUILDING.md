# Building Mr. Runner Plus

Respring Mr. Runner Plus includes the ARM64 iOS host, a modified touchHLE ARM/Thumb interpreter, vendored Cargo dependencies and SDL2, original game files and a hash manifest. It is reproducible on Apple silicon macOS using the checked-in sources.

## Requirements

- Full Xcode with an iPhoneOS SDK and the corresponding iPhone Simulator SDK, selected using `xcode-select`
- Python 3.11 or later
- Rust installed with rustup (`1.99.0` pinned in `rust-toolchain.toml`)
- CMake and Ninja on PATH
- An Apple silicon Mac for ARM64 simulator testing

Install the pinned Rust toolchain and targets:

```sh
rustup toolchain install 1.99.0 --profile minimal
rustup target add --toolchain 1.99.0 aarch64-apple-ios aarch64-apple-ios-sim
```

Compilation uses `--offline --locked` and vendored dependencies. Build outputs should be placed outside File Provider/iCloud-managed directories, such as `/tmp`.

## Build for a physical iPhone

From the repository root:

```sh
MRRUNNER_NATIVE_BUILD=/tmp/mrrunner-build bash Compatibility/ios/build.sh iphoneos
python3 Scripts/package_ipa.py /tmp/mrrunner-build/iphoneos/MrRunnerPlus.app \
  --output release-output/MrRunnerPlus.ipa
python3 Scripts/audit_release.py release-output/MrRunnerPlus.ipa
```

The final IPA is deliberately **unsigned**, contains no provisioning profile, and is ready to sign using an external sideloading tool. Its bundle ID defaults to `com.respring.mrrunnerplus`; `PRODUCT_BUNDLE_IDENTIFIER` can override the build-time identifier when your signing workflow requires it. The metadata audit currently expects the default identifier, so adjust that check for a custom build.

## Build for iOS Simulator

```sh
MRRUNNER_NATIVE_BUILD=/tmp/mrrunner-build bash Compatibility/ios/build.sh iphonesimulator
xcrun simctl boot <SIMULATOR_UDID>
xcrun simctl install <SIMULATOR_UDID> /tmp/mrrunner-build/iphonesimulator/MrRunnerPlus.app
xcrun simctl launch <SIMULATOR_UDID> com.respring.mrrunnerplus
```

Use `xcrun simctl list devices available` to find the destination. The legacy game launches in the modern ARM64 simulator via its interpreter and is not a native ARMv7 application installation.

## Original game verification

The original 2011 game files are in `Original/Payload/Mr.Runner Plus.app`. `Original/payload-sha256.json` records the expected hash of every file. The build regenerates `MrRunnerPlus.ipa` inside the host, verifying hashes and not altering the game's executable or resources. `Scripts/audit_release.py` validates both nested and outer IPAs, the original bundle identity, ARM64 Mach-O host, the iPhoneOS build platform, and absence of signing/provisioning metadata.

## Build layout

| Path | Purpose |
| --- | --- |
| `Compatibility/compatibility-core` | Modified touchHLE core, interpreter, old iOS frameworks and OpenGL ES bridges |
| `Compatibility/ios` | Native iOS UIKit/SDL scene host and Rust entry point |
| `Original` | Original game payload and checksums |
| `Vendor` | Vendored Rust dependencies and adapted SDL2 |
| `Notices` | License texts and third-party attributions included in the host app |
| `Scripts` | Guest rebuilding, Info.plist configuration, IPA packaging, and audit |
| `evidence` | Simulator screenshot validating startup and the title screen |
| `release-output` | Local unsigned IPA (ignored by git; release asset is uploaded to GitHub Releases) |

Some upstream Peggle-related filenames and diagnostic symbols remain in the derived compatibility core; those game-specific acceleration paths are guarded and do not apply to Mr. Runner Plus. The main game execution uses the original interpreted ARM code.

## Releasing

After building and auditing, publish the unsigned `MrRunnerPlus.ipa` along with a GitHub source snapshot of the same tagged revision and SHA-256 checksums. The release files are intentionally excluded from the tracked git tree. Matching legacy GNU runtime sources are linked from the upstream [Respring Peggle release archive](https://github.com/DylanMcD8/respring-peggle/releases/tag/revision-2), which documents those bundled compatibility libraries.
