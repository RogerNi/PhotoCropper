# PhotoCropper
## Overview
This is an application for cropping image. You can process many images easily with this application. You can specify the size of cropped images. Also, you can make your origin photo larger and smaller without changing the size of cropped image.
## Functions
- Cropping a folder of images easily
- Zoom in and out without changing crop size
- Gaussian blur to smoothen the zoom in photos
## Usage
|Function|Operation|
|---|---|
|Zoom in|Mouse wheel up|
|Zoom out|Mouse wheel down|
|Drag photo|Mouse right press and drag|
|Capture current image|Mouse left click|
|Next image|Space|
|Previous image|Z|
|Open Output folder|X|
|Open Input folder|S|
|Show current image number|D|
|Change to another image|F|
|Turn on/off Gaussian Blur|G|
|Reduce blur radius|,|
|Increase blur radius|.|
|Reset blur radius to 1|/|
|Reset zoom ratio|R|
|Change Output path|C|
## Some perameters need to specify (examples)
~~~~
INPUT_DIR = '/home/mars/Documents/Input'
OUTPUT_DIR = '/home/mars/Documents/Test_Output'    # Directory will be created if not found
ZOOM_RATIO = 1.08
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
CROP_SIZE = (122, 122)
~~~~
## Snapshots
|   |   |
|---|---|
|![Snapshot 1](/snapshots/Screenshot_1.png)|![Snapshot 2](/snapshots/Screenshot_2.png)|
|![Snapshot 3](/snapshots/Screenshot_3.png)|![Snapshot 4](/snapshots/Screenshot_4.png)|
