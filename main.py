# 06.10.2025

# EYEINSIDE

# EyeInside project. 
# Created by Oguz Demirtas
# https://github.com/oguz81/EyeInsideV1

# 2025 

# MIT License

# Copyright (c) 2025 Oğuz DEMİRTAŞ

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.




import tkinter as tk
import os
#os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" 
import cv2

from ultralytics import YOLO
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import Canvas, Frame, Scrollbar

def clear_images():
    for widget in frame.winfo_children():
        widget.destroy()

def small_images(param_frame, param_path, param_filename):
    smallSizeImage = Image.open(param_path)
    smallSizeImage = smallSizeImage.resize((100, 100))
    smallSizeImage = ImageTk.PhotoImage(smallSizeImage)
                        
                            # new frame for image and its name
    imageAndName = tk.Frame(param_frame)
    imageAndName.pack(side=tk.TOP, padx=10, pady=5)

                            # Detected objects label
    #detectedObjectsLabel = tk.Label(imageAndName, text=", ".join(elem for elem in yoloDetectedObjects if elem in userQuery), font=("Arial", 8), bg='white') # check later if this line works well
    #detectedObjectsLabel.pack(side=tk.RIGHT, padx=45, pady=20)
                            # Image label
    imageLabel = tk.Label(imageAndName, image=smallSizeImage)
    imageLabel.image = smallSizeImage  # Prevent garbage collection
    imageLabel.pack()

                            # Text label (image filename)
    imageName = tk.Label(imageAndName, text=param_filename, font=("Arial", 10))
    imageName.pack()


def searchExecution():
    userQuery = query.get()
    directory = filePath.get()
    copiedDirectory = directory + "\\copiedImages"
    selectedYoloModel = "C:\\Program Files\\EyeInside\\YOLOmodels\\" + selectedModel.get()
    yoloModel = YOLO(selectedYoloModel)
   
    
    detectedImages = []
    searchResultText = []
    clear_images()  
    countedPerson = 0
    # YOLO section
    detectionCounter = 0
    try:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        else:
            yoloClassNames = list(yoloModel.names.values())
         
            for filename in os.listdir(directory):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    detections = yoloModel(directory + "\\" + filename)
                    if count.get() == True : # count person tick
                        numberOfPerson = numberBox.get()
                        print("The countbox is clicked", numberOfPerson)
                        results = detections[0]
                        class_names = results.names
                        class_ids = results.boxes.cls.int().tolist()
                        countedPerson = 0
                        for i in class_ids:
                            if i == 0:
                                countedPerson += 1
                        print("Number of person in the image:", countedPerson)
                        print("Type of numberOfPerson:", type(numberOfPerson))
                        print("Type of countedPerson:", type(countedPerson))
                        if countedPerson == int(numberOfPerson):
                            detectionCounter += 1
                            print("This image has", countedPerson, " person.")
                            ImagePath = os.path.join(directory, filename)
                            small_images(frame, ImagePath, filename)

                    else :
                    
                        class_names = [yoloModel.names[int(boxe.cls)] for boxe in detections[0].boxes] # gets  class names of the detected objects
                        yoloDetectedObjects = list(set([name.lower() for name in class_names]))

                        print("Here are YOLO objects:", yoloDetectedObjects)
                        print("Here are query words:", userQuery)



                        #compare the query words with the detected objects
                        #yoloDetectedObjects = ''.join(yoloDetectedObjects)
                        if (userQuery in yoloDetectedObjects):
                            print(type(userQuery))
                            print(type(yoloDetectedObjects))
                            #dtc = elem
                            #print the image name and the detected objects
                            print("These objects are detected in the image " + filename + ": " + str(yoloDetectedObjects))
                            detectionCounter += 1
                            #copy the image to the specific folder
                            ImagePath = os.path.join(directory, filename)
                            small_images(frame, ImagePath, filename)


            searchResultText = f"{detectionCounter} images found."
    except FileNotFoundError as e:
        print("Error: {e}")
        searchResultText = f"Error: {e}"
    searchResults.config(text=searchResultText)

def countPersonFunc():
    if count.get() == True:
        numberBox.place(x=180, y=180)
    else:
        numberBox.place_forget()

yoloModelFolderPath = "C:\\Program Files\\EyeInside\\YOLOmodels"
yoloModels = os.listdir(yoloModelFolderPath)
print("Available YOLO models:")
for model in yoloModels:
    print(model)


window = tk.Tk()
window.title('EYEINSIDE v1')
window.geometry('1000x600')
# color of the window
window.configure(bg='gray')

# File path input
filePathLabel = tk.Label(window, text='File Path:',font=("Helvetica", 15), bg='gray')
filePathLabel.place(x=20, y=20)
filePath = tk.Entry(window,width=60)
#filePath.pack(pady=10)
filePath.place(x=20, y=60)

# Query input
queryLabel = tk.Label(window, text='Objects to search:',font=("Helvetica", 15), bg='gray')
queryLabel.place(x=20, y=100)
query = tk.Entry(window,width=60)
#filePath.pack(pady=10)
query.place(x=20, y=140)

# Count person box
numberBox = tk.Entry(window,width=10)
count = tk.BooleanVar()
countPersonBox = tk.Checkbutton(window, command=countPersonFunc, onvalue=True,offvalue=False, variable=count)
countPersonBox.place(x=20, y=180)
countPersonBoxLabel = tk.Label(window, text='Count person', font=("Helvetica", 15), bg='gray')
countPersonBoxLabel.place(x=60, y=180)

# YOLO model select dropdown menu
yoloListBoxLabel = tk.Label(window, text='Select YOLO Model:', font=("Helvetica", 15), bg='gray')
yoloListBoxLabel.place(x=20, y=280)
selectedModel = tk.StringVar(value="Select model") 
yoloListBox = ttk.Combobox(window, values=yoloModels, state='readonly', width=20, textvariable=selectedModel)
yoloListBox.place(x=20, y=320)
def modelSelected(event):
    print(selectedModel.get())
yoloListBox.bind("<<ComboboxSelected>>", modelSelected)


canvas = Canvas(window, width=300, height=400, bg="#edeef0")
scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold images
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))  # Update scrolling

frame.bind("<Configure>", update_scroll_region)

# Place widgets using 'place()'
canvas.place(x=580, y=60, width=380, height=480)  # Place canvas on the right
scrollbar.place(x=960, y=60, height=480)  # Scrollbar next to canvas

# Search results label
searchResultsLabel = tk.Label(window, text='SEARCH RESULTS:',font=("Helvetica", 15), bg='gray')
searchResultsLabel.place(x=20, y=480)

searchResults = tk.Label(window, text="",font=("Helvetica", 10), bg='white')
searchResults.place(x=20, y=520)


searchButton = tk.Button(window, text='Search',font=("Helvetica", 15), bg='gray', command=searchExecution)
searchButton.place(x=280, y=303)

# Image Results label
imageResultsLabel = tk.Label(window, text='IMAGES:',font=("Helvetica", 15), bg='gray')
imageResultsLabel.place(x=700, y=20)


window.mainloop()
