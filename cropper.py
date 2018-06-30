#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30
# @Author  : NI
# @Site    : https://github.com/RogerNi
# @File    : cropper.py

import os
import platform
import tkinter as tk

from PIL import ImageTk, Image

# This part of parameters can be changed
INPUT_DIR = '/home/mars/Documents/data/negative'
OUTPUT_DIR = '/home/mars/Documents/Test_Output'    # Directory will be created if not found
ZOOM_RATIO = 1.08
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
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
curr = Image.open(INPUT_DIR + '/' + imgs[currImage])
cropped = curr.crop((0, 0, CROP_SIZE[0], CROP_SIZE[1]))
maxImage = len(imgs)


def chgImg(event):
    if event.char == ' ':
        global currImage
        currImage += 1 if currImage + 1 < maxImage else 0
        global curr
        curr = Image.open(INPUT_DIR + '/' + imgs[currImage])
        global ratio
        ratio = 1
        loadImg()
        drawBox(None)
    elif event.char == 'z':
        currImage
        currImage -= 1 if currImage > 0 else 0
        curr = Image.open(INPUT_DIR + '/' + imgs[currImage])
        ratio = 1
        loadImg()
        drawBox(None)


def loadImg():
    img = ImageTk.PhotoImage(curr)
    panel.configure(image=img)
    panel.image = img


def zoom(r):
    global ratio
    ratio *= r
    global curr
    curr = Image.open(INPUT_DIR + '/' + imgs[currImage])
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
    canvas.create_image((0, 0), image=temp_crop, anchor=tk.NW)
    canvas.image = temp_crop
    canvas.create_rectangle(0, 0, CROP_SIZE[0], CROP_SIZE[1], width=5)
    canvas.place(x=x, y=y, anchor=tk.CENTER)


def capture(event):
    file = imgs[currImage] + "_" + "r_" + str(ratio) + "(" + str(master.winfo_pointerx()) + ", " + str(
        master.winfo_pointery()) + ").jpg"
    cropped.save(OUTPUT_DIR + "/" + file)
    print("File saved: " + file)


panel = tk.Label(master)
panel.pack(side="bottom", fill="both", expand="yes")
panel.place(x=x_position, y=y_position, anchor=tk.CENTER)
loadImg()
#zoom(1)

canvas = tk.Canvas(master, width=CROP_SIZE[0], height=CROP_SIZE[1])
canvas.create_rectangle(0, 0, CROP_SIZE[0], CROP_SIZE[1], width=5)
temp_crop = ImageTk.PhotoImage(cropped)
canimg = canvas.create_image((0, 0), image=temp_crop, anchor=tk.NW)
canvas.image = temp_crop

master.bind('<Key>', chgImg)
master.bind("<B3-Motion>", drag)
master.bind("<Button-1>", capture)
master.bind('<Button-3>', b3)
master.bind('<Motion>', drawBox)
print("OS: " + platform.system())
if platform.system() != "Linux":
    master.bind('<MouseWheel>', winZoom)
else:
    master.bind('<Button-4>', zoomIn)
    master.bind('<Button-5>', zoomOut)
master.mainloop()

# EOF.
