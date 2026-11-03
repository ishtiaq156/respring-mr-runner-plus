//! iOS ARM64 host entry for the original Mr. Runner Plus 1.0 ARMv7 game.
//! The original executable and Lua/texture packages remain guest input data.
use std::ffi::{c_char, CStr};
use std::io::Write;
use std::path::Path;

#[no_mangle]
pub unsafe extern "C" fn mrrunner_ios_run(
    ipa: *const c_char,
    resources: *const c_char,
    documents: *const c_char,
) -> i32 {
    if ipa.is_null() || resources.is_null() || documents.is_null() {
        return 1;
    }
    let outcome = std::panic::catch_unwind(|| -> Result<(), String> {
        let ipa = CStr::from_ptr(ipa).to_str().map_err(|e| e.to_string())?;
        let resources = CStr::from_ptr(resources).to_str().map_err(|e| e.to_string())?;
        let documents = CStr::from_ptr(documents).to_str().map_err(|e| e.to_string())?;
        std::fs::create_dir_all(documents).map_err(|e| e.to_string())?;
        let log = Path::new(documents).join("MrRunnerPlus-diagnostics.jsonl");
        touchHLE::diagnostics::initialize(&log, true)
            .map_err(|e| format!("diagnostics: {e}"))?;
        let previous_hook = std::panic::take_hook();
        std::panic::set_hook(Box::new(move |info| {
            touchHLE::diagnostics::panic_message(&info.to_string());
            previous_hook(info);
        }));
        std::env::set_var("TOUCHHLE_RESOURCE_DIR", resources);
        std::env::set_var("TOUCHHLE_USER_DATA_DIR", documents);
        std::env::set_current_dir(documents).map_err(|e| e.to_string())?;
        // Game-authored logic runs in touchHLE's ARM interpreter; input is mapped
        // to the original 480x320 landscape canvas.
        let args = vec![
            "MrRunnerPlus Compatibility".to_owned(),
            ipa.to_owned(),
            "--fullscreen".to_owned(),
            "--wrapper-resolution=original".to_owned(),
            "--device-family=iphone".to_owned(),
            "--iphone-screen=3.5".to_owned(),
            "--landscape-right".to_owned(),
            "--scale-hack=1".to_owned(),
            "--screen-scale=2".to_owned(),
            "--compositor-scale=2".to_owned(),
            "--display-link-fps=60".to_owned(),
            "--fps-limit=60".to_owned(),
            "--pause-on-background".to_owned(),
            "--fullscreen-host-blit".to_owned(),
            "--no-error-popup".to_owned(),
        ];
        touchHLE::main(args.into_iter())
    });
    match outcome {
        Ok(Ok(())) => 0,
        Ok(Err(error)) => {
            let _ = writeln!(std::io::stderr().lock(), "MrRunnerPlus: {error}");
            1
        }
        Err(_) => {
            let _ = writeln!(std::io::stderr().lock(), "MrRunnerPlus: guest runtime panicked; see Documents diagnostics");
            2
        }
    }
}

// Optional diagnostic callbacks retained by the upstream compatibility host.
#[no_mangle]
pub extern "C" fn peggle_ios_fps_diagnostic(
    _kind: i32, _fps: f64, _count: u64, _warming: i32, _overflow: i32,
    _x: f64, _y: f64, _width: f64, _height: f64, _interactive: i32, _contained: i32,
) { }
#[no_mangle]
pub extern "C" fn peggle_ios_keyboard_native_diagnostic(
    _stage: i32, _current_units: u32, _replacement_units: u32,
) { }
