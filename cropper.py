#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30
# @Author  : NI
# @Site    : https://github.com/RogerNi
# @File    : cropper.py

import os
import platform
import tkinter as tk
import subprocess

from PIL import ImageTk, Image, ImageFilter

# This part of parameters can be changed
INPUT_DIR = '/home/mars/Documents/GoogleImagesDownloader-master/data/arms'
OUTPUT_DIR = '/home/mars/Documents/Test_Output'    # Directory will be created if not found
ZOOM_RATIO = 1.08
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
BLUR = True
BLUR_RADIUS = 2
CROP_SIZE = (122, 122)


# Main part
master = tk.Tk()
master.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))

if os.path.isdir(OUTPUT_DIR) is False:
    os.mkdir(OUTPUT_DIR)

imgs = os.listdir(INPUT_DIR)
currImage = 0
ratio = 1
x_distance = 0
y_distance = 0

x_position = WINDOW_WIDTH / 2
y_position = WINDOW_HEIGHT / 2
# print(x_position)
# print(y_position)

global curr, cropped
currOrigin = Image.open(INPUT_DIR + '/' + imgs[currImage])
curr = Image.open(INPUT_DIR + '/' + imgs[currImage])
cropped = curr.crop((0, 0, CROP_SIZE[0], CROP_SIZE[1]))
maxImage = len(imgs)


def key(event):
    if event.char == ' ':
        global currImage
        currImage += 1 if currImage + 1 < maxImage else 0
        global curr, currOrigin
        currOrigin = Image.open(INPUT_DIR + '/' + imgs[currImage])
        curr = Image.open(INPUT_DIR + '/' + imgs[currImage])
        global ratio
        ratio = 1
        loadImg()
        drawBox(None)
    elif event.char == 'z':
        currImage
        currImage -= 1 if currImage > 0 else 0
        currOrigin = Image.open(INPUT_DIR + '/' + imgs[currImage])
        curr = Image.open(INPUT_DIR + '/' + imgs[currImage])
        ratio = 1
        loadImg()
        drawBox(None)
    elif event.char == 'g':
        global BLUR
        BLUR = not BLUR
        if BLUR:
            print("Gaussian Blur ON")
        else:
            print("Gaussian Blur OFF")
    elif event.char == ',':
        global BLUR_RADIUS
        if BLUR_RADIUS > 1:
            BLUR_RADIUS -= 1
            drawBox(None)
            print("Blur radius set to "+str(BLUR_RADIUS))
        else:
            print("Blur radius is 1. Cannot reduce.")
    elif event.char == '.':
        BLUR_RADIUS += 1
        drawBox(None)
        print("Blur radius set to "+str(BLUR_RADIUS))
    elif event.char == '/':
        BLUR_RADIUS = 1
        drawBox(None)
        print("Blur radius reset to 1")
    elif event.char == 'd':
        print("Current image is #"+str(currImage))
    elif event.char == 'f':
        currImage = int(input("Which image you want?\n"))
        currOrigin = Image.open(INPUT_DIR + '/' + imgs[currImage])
        curr = Image.open(INPUT_DIR + '/' + imgs[currImage])
        ratio = 1
        loadImg()
        drawBox(None)
        print("Image change to #"+str(currImage))
    elif event.char == 'r':
        ratio = 1
        curr = currOrigin
        loadImg()
        drawBox(None)
        print("Ratio reset")
    elif event.char == 'x':
        global OUTPUT_DIR
        openDir(OUTPUT_DIR)
    elif event.char == 's':
        openDir(INPUT_DIR)
    elif event.char == 'c':
        OUTPUT_DIR = input("Input new input dir:\n")
        if not os.path.isdir(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        print("Output dir changed to "+OUTPUT_DIR)

def openDir(path):
    if OS == "Linux":
        subprocess.Popen("gio open "+path, shell=True)
    elif OS == "Windows":
        subprocess.Popen("start "+path, shell=True)
    else:
        subprocess.Popen("open "+path, shell=True)

def loadImg():
    img = ImageTk.PhotoImage(curr)
    panel.configure(image=img)
    panel.image = img


def zoom(r):
    global ratio
    ratio *= r
    global curr
    curr = currOrigin
    w, h = curr.size
    new_w = round(ratio * w)
    new_h = round(ratio * h)
    curr = curr.resize((new_w, new_h))
    loadImg()
    drawBox(None)


def winZoom(event):
    zoom(ratio * (event.delta / 120))


def zoomIn(event):
    zoom(ZOOM_RATIO)
    # print(event.num)


def zoomOut(event):
    zoom(1 / ZOOM_RATIO)
    # print(event.num)


def drag(event):
    # print(event.x)
    # print(event.y)
    # print("Drag")
    global x_position, y_position
    x_position = master.winfo_pointerx() - master.winfo_rootx() + x_distance
    y_position = master.winfo_pointery() - master.winfo_rooty() + y_distance
    # print("x: "+str(x_position))
    # print("y: "+str(y_position))
    panel.place(x=x_position, y=y_position, anchor=tk.CENTER)


def b3(event):
    # print("Press")
    global x_distance, y_distance
    x_distance = x_position - master.winfo_pointerx() + master.winfo_rootx()
    y_distance = y_position - master.winfo_pointery() + master.winfo_rooty()
    # x_distance = master.winfo_pointerx()
    # y_distance = master.winfo_pointery()


def drawBox(event):
    x = master.winfo_pointerx() - master.winfo_rootx()
    y = master.winfo_pointery() - master.winfo_rooty()
    w, h = curr.size
    x1 = w / 2 + x - x_position
    y1 = h / 2 + y - y_position
    # print("x: "+str(x1))
    # print("y: "+str(y1))
    global cropped, canvas
    cropped = curr.crop((x1 - CROP_SIZE[0] / 2, y1 - CROP_SIZE[1] / 2, x1 + CROP_SIZE[0] / 2, y1 + CROP_SIZE[1] / 2))
    temp_crop = ImageTk.PhotoImage(cropped)
    if BLUR:
        temp_crop = ImageTk.PhotoImage(cropped.filter(ImageFilter.GaussianBlur(BLUR_RADIUS)))
    canvas.create_image((0, 0), image=temp_crop, anchor=tk.NW)
    canvas.image = temp_crop
    canvas.create_rectangle(0, 0, CROP_SIZE[0], CROP_SIZE[1], width=5)
    canvas.place(x=x, y=y, anchor=tk.CENTER)


def capture(event):
    file = imgs[currImage] + "_" + "r_" + str(ratio) + "(" + str(master.winfo_pointerx()) + ", " + str(
        master.winfo_pointery()) + ").jpg"
    if BLUR:
        cropped.filter(ImageFilter.GaussianBlur(BLUR_RADIUS)).save(OUTPUT_DIR + "/" + file)
    else:
        cropped.save(OUTPUT_DIR + "/" + file)
    print("File saved: " + file)


panel = tk.Label(master)
panel.pack(side="bottom", fill="both", expand="yes")
panel.place(x=x_position, y=y_position, anchor=tk.CENTER)
loadImg()
# zoom(1)

canvas = tk.Canvas(master, width=CROP_SIZE[0], height=CROP_SIZE[1])
canvas.create_rectangle(0, 0, CROP_SIZE[0], CROP_SIZE[1], width=5)
temp_crop = ImageTk.PhotoImage(cropped)
canimg = canvas.create_image((0, 0), image=temp_crop, anchor=tk.NW)
canvas.image = temp_crop

master.bind('<Key>', key)
master.bind("<B3-Motion>", drag)
master.bind("<Button-1>", capture)
master.bind('<Button-3>', b3)
master.bind('<Motion>', drawBox)
OS = platform.system()
print("OS: " + OS)
if OS != "Linux":
    master.bind('<MouseWheel>', winZoom)
else:
    master.bind('<Button-4>', zoomIn)
    master.bind('<Button-5>', zoomOut)
master.mainloop()

# EOF.
