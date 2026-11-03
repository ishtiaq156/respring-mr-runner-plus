# Changelog

## Rev 1 — 2026-11-03

- Restore **Mr. Runner Plus 1.0** as an ARM64 iOS app with a modified touchHLE interpreter and original 2011 game content.
- Add the original 480 × 320 landscape drawing pipeline, preserving the game's visuals and controls.
- Implement missing historical APIs for libc, Foundation, CoreGraphics, iAd, CoreAnimation, OpenGL ES 1.1 and audio file completion.
- Fix the inherited OpenGL ES buffer binding lookup so the original title screen renders correctly.
- Package a verified unsigned IPA for sideloading on modern iPhones (iOS 15+).
- Verify the animated title screen in an iOS 27.2 simulator and working operation on the owner's iPhone 15 Pro Max.
