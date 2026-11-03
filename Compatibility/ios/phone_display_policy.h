#pragma once
#include <math.h>
// Inputs are drawable pixels. Match the renderer's rounded fit rectangle so
// even a fractional last pixel cannot become a black strip after cropping.
static inline double peggle_phone_crop_zoom(double width,double height,unsigned phoneHeight,int cropped){
 if(!cropped||width<=0||height<=0)return 1.0;
 double w,h;
 if(phoneHeight==568){
  if(width*40<=height*71){w=width;h=floor(width*40/71);}else{w=floor(height*71/40);h=height;}
 }else{double k=floor(fmin(width/3,height/2));w=k*3;h=k*2;}
 return w>0&&h>0?fmax(width/w,height/h):1.0;
}
