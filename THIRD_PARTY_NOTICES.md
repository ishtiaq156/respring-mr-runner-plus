# Third-party components and provenance

- **Respring project and examples** — https://respring.dev/ — the overall approach, host integration, and release workflow follow the public Respring restoration skill. This port was adapted from https://github.com/DylanMcD8/respring-peggle, checkout `f689052`.
- **touchHLE** — https://github.com/touchHLE/touchHLE — MPL-2.0. Its derived, locally modified code includes ARM/Thumb emulation, old framework stubs, OpenGL ES bridges and host/runtime plumbing under `Compatibility/compatibility-core`.
- **ARM interpreter** — original notices in `Compatibility/compatibility-core/src/cpu/interpreter/LICENSE`.
- **SDL2** — https://github.com/libsdl-org/SDL — zlib license; modified iOS UIKit presentation sources under `Vendor/SDL2`.
- **Rust crates** — locked dependency versions and checksums in `Compatibility/ios/rust-entry/Cargo.lock`; sources/licenses in `Vendor/Rust` and summary in `Notices/rust-dependencies.txt`.
- **zlib 1.1.3**, **stb_image**, and **PVRTDecompress** — notices beside native/vendor source files in the compatibility core.
- **Fonts** — licensed fonts and notices under `Compatibility/compatibility-core/touchHLE_fonts`.
- **Legacy iOS runtime libraries** — original shared library binaries and respective COPYING notices under `Compatibility/compatibility-core/touchHLE_dylibs`. Upstream source archives/build scripts for Apple gcc-5664 and libstdcxx-39 are available as `Peggle-runtime-sources.zip` attached to the [Respring Peggle Rev 2 release](https://github.com/DylanMcD8/respring-peggle/releases/tag/revision-2). These old binaries were not rebuilt by this port with modern Xcode.

The iOS host ships the corresponding `ThirdPartyNotices` folder. The tagged repository snapshot supplies modified MPL-covered source and included dependency source. Mr. Runner Plus executable and original game assets are owned by the original rights holders and are outside the above open-source licenses.
