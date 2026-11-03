/* This Source Code Form is subject to the Mozilla Public License, v. 2.0. */
//! Legacy iAd API: the advertising network was discontinued in 2016.
//! Present its view class and original content-size constant without requesting
//! ads; the view remains hidden so the original game's playfield stays usable.
use crate::dyld::{HostConstant, HostDylib};
use crate::frameworks::core_graphics::{CGRect, CGSize};
use crate::objc::{id, msg, msg_super, nil, objc_classes, ClassExports};

const CLASSES: ClassExports = objc_classes! {
(env, this, _cmd);
@implementation ADBannerView: UIView

+ (CGSize)sizeFromBannerContentSizeIdentifier:(id)_id {
    CGSize { width: 480.0, height: 32.0 }
}


- (id)initWithFrame:(CGRect)frame {
    let this: id = msg_super![env; this initWithFrame:frame];
    () = msg![env; this setHidden:true];
    this
}

- (())setDelegate:(id)_delegate {}
- (id)delegate { nil }
- (bool)isBannerLoaded { false }
- (bool)isBannerViewActionInProgress { false }
- (())cancelBannerViewAction {}
- (())setRequiredContentSizeIdentifiers:(id)_ids {}
- (())setCurrentContentSizeIdentifier:(id)_id {}
- (())setHidden:(bool)_hidden { () = msg_super![env; this setHidden:true]; }

@end
};

pub const DYLIB: HostDylib = HostDylib {
    path: "/System/Library/Frameworks/iAd.framework/iAd",
    aliases: &[],
    class_exports: &[CLASSES],
    constant_exports: &[&[("_ADBannerContentSizeIdentifier480x32", HostConstant::NSString("ADBannerContentSizeIdentifier480x32"))]],
    function_exports: &[],
};
