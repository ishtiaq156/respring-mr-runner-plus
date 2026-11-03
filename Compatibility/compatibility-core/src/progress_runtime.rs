// Mr. Runner Plus has its own save logic inside the guest application.
// Peggle's host-side progress snapshots and auto-import are inapplicable.
use crate::Environment;
use std::sync::atomic::{AtomicBool, Ordering};

static RELOAD_READY: AtomicBool = AtomicBool::new(false);
pub fn reload_ready() -> bool { RELOAD_READY.load(Ordering::SeqCst) }
pub fn take_reload() -> bool { RELOAD_READY.swap(false, Ordering::SeqCst) }
pub fn snapshot(_env: &mut Environment, _force: bool) {}
pub fn service(_env: &mut Environment) {}
pub fn prompt() -> bool { false }
pub fn finish_reload(env: &mut Environment) -> ! {
    RELOAD_READY.store(true, Ordering::SeqCst);
    env.yield_thread(crate::environment::ThreadBlock::NotBlocked);
    unreachable!("The old guest must not continue after a reload request")
}
