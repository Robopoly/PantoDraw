#ifndef RGBCAMERA_H
#define RGBCAMERA_H

#include <QString>
#include <QCamera>
#include <QCameraViewfinder>
#include <QCameraImageCapture>
class RGBCamera
{
public:
    RGBCamera();
    void capture(QString path);
private:
    QCameraImageCapture* mRGBCapture;
};

#endif // RGBCAMERA_H
