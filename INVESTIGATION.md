# Mr. Runner Plus — intake and compatibility record

## Original input

- Input: user-supplied 4.2 MB IPA for **Mr. Runner Plus 1.0**, `com.gamevision.mrrunnerplus`.
- Source IPA SHA-256: `7c9716e125ecb3278df2f5dc1fd28b94e7bf7f62204233f624595073fc07fa21`.
- Guest universal executable SHA-256: `7e85b9d9804612edd2ba5934401d3e89106a092226a56be24caa8c42cb8cada2`.
- Executable architectures: `armv6`, `armv7`; inspected ARMv7 `LC_ENCRYPTION_INFO` with `cryptid = 0`.
- Original minimum OS: 3.0; original SDK: 4.1; landscape-right iPhone app.
- Engine evidence: C++ symbols from `chaos3d`, Lua 5.1 runtime strings, Lua filename inventory in `script.pkg`; game assets inside `texture.pkg`; original OpenGLES and OpenAL dependencies.
- Remote/optional SDK references: Game Center, Facebook, Twitter, Flurry, AdMob, iAd, StoreKit. Whether these affect startup needs direct runtime evidence.

## Restoration choice

Preserve original gameplay via ARM/Thumb interpretation in modified touchHLE, with a native ARM64 UIKit/SDL host. This choice avoids guessing game physics or reimplementing proprietary `chaos3d` engine bindings. Start at original 480×320 landscape logical size and 60 FPS; enhance only after evidence from actual gameplay.

## Reference inheritance

Base: `DylanMcD8/respring-peggle`, shallow clone observed at `f689052`. Its native ARM64 host, Rust interpreter, dyld shims, modified SDL display plumbing and bundled old runtime libraries were adapted. Mr. Runner Plus does not use Peggle's progress import, nights theme, cloud save manager or game-specific acceleration. Any retained Peggle-specific native helper is guarded by the exact original Peggle identity/executable, so will not activate for this game. The inherited non-game-specific diagnostic functions keep their original names.

## Live simulator outcome (November 3, 2026)

**Verified:** The ARM64 host launched the original guest executable and rendered its animated **Mr. Run** title screen with **TAP ME TO START**, native OpenGL ES 1.1 drawing and the original 480 × 320 landscape canvas. It continued in its frame loop for over 65 seconds without a new panic. See `evidence/simulator-title-screen.png`. The simulator reported about 20–24 interpreted guest frames per second; physical iPhone performance may differ substantially.

**Compatibility changes discovered through successive simulator runs:**

- Added guest libc `asctime` with the 26-byte static buffer contract and a format unit test.
- Implemented `NSDirectoryEnumerator.skipDescendents` respecting the last enumerated directory.
- Added legacy CoreGraphics stroke-color-space and array-style fill/stroke setters, preserving color-space state across graphics save/restore.
- Added an inactive/hidden compatibility class for Apple's retired iAd `ADBannerView` and original size identifier.
- Added missing `CADisplayLink` timestamp/duration/targetTimestamp APIs.
- Implemented `glPointSizePointerOES` for the native GLES1 renderer.
- Corrected the inherited GL buffer lookup's `ARRAY_BUFFER_BINDING` enum and the incorrect temporary pointer that always returned buffer ID 0. This was the root cause of the white screen and repeated `GL_INVALID_OPERATION` errors. The original title image appeared once corrected.
- Allowed valid zero-packet success at the end of an audio stream in `AVAudioPlayer`.

**Still unverified:** tapping the start prompt, game input and jumping, progression through levels, correct music/sound, saves, background/foreground behavior and iPhone 15 Pro Max performance. The first signed physical-device sideload test will answer these questions. The original ARMv7 engine and assets are preserved in the nested guest IPA.
