#include "rgbcamera.h"


RGBCamera::RGBCamera()
{
    QCamera* camera = new QCamera;
    QCameraViewfinder *viewFinder = new  QCameraViewfinder();

    viewFinder->show();
    viewFinder->setWindowTitle("RGB Camera");
    camera->setViewfinder(viewFinder);


    mRGBCapture = new QCameraImageCapture(camera);

    camera->setCaptureMode(QCamera::CaptureStillImage);
    camera->start();
}
//save capture and save image
void RGBCamera::capture(QString path)
{
    if(mRGBCapture->mediaObject()->isAvailable());
        mRGBCapture->capture(path);
}
