#08.01.2025
# This is the first version of the EyeInside project. 
# EyeInside takes your query and returns the photos you are looking for.
# You just have to describe the photo you are looking for. Then a YOLO model searches photos in the folder.
# Finally the most relevant photos are displayed.
#from msilib.schema import File

import tkinter as tk
import spacy
import os
#os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" 
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
from PIL import Image, ImageTk
from tkinter import Canvas, Frame, Scrollbar

def clear_images():
    for widget in frame.winfo_children():
        widget.destroy()


def searchExecution():
    userQuery = query.get()
    directory = filePath.get()
    copiedDirectory = directory + "\\copiedImages"
    
    #SpaCy section
    doc=nlp(userQuery)
    printSpaCyAnalysis = []
    queryWords = []
    detectedImages = []
    searchResultText = []
    clear_images()  
    if doc.ents:
        for ent in doc.ents:
            word, label = ent.text.lower(), ent.label_.lower()
            printSpaCyAnalysis.append("Word: " + word + " - Label: " + label + "\n")
            
            if label == "dress" or label == "accessory":
                queryWords.append(word)
                
    else:
        printSpaCyAnalysis = "No entity found"
    #print(result)    
    spaCyAnalysisResult.config(text=printSpaCyAnalysis)
    print(printSpaCyAnalysis)    
    # YOLO section
    detectionCounter = 0
    try:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        else:
            for filename in os.listdir(directory):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    detections = yolo(directory + "\\" + filename)
                    class_names = [yolo.names[int(boxe.cls)] for boxe in detections[0].boxes]
                    yoloDetectedObjects = list(set([name.lower() for name in class_names]))

                    print("Here are YOLO objects:", yoloDetectedObjects)
                    print("Here are query words:", queryWords)
                    #compare the query words with the detected objects
                    if any(elem in yoloDetectedObjects for elem in queryWords):
                        #print the image name and the detected objects
                        print("These objects are detected in the image " + filename + ": " + str(yoloDetectedObjects))
                        detectionCounter += 1
                        #copy the image to the specific folder
                        ImagePath = os.path.join(directory, filename)
                        smallSizeImage = Image.open(ImagePath)
                        smallSizeImage = smallSizeImage.resize((100, 100))
                        smallSizeImage = ImageTk.PhotoImage(smallSizeImage)
                        
                        # new frame for image and its name
                        imageAndName = tk.Frame(frame)
                        imageAndName.pack(side=tk.TOP, padx=10, pady=5)

                        # Detected objects label
                        detectedObjectsLabel = tk.Label(imageAndName, text=", ".join(yoloDetectedObjects), font=("Arial", 8), bg='white')
                        detectedObjectsLabel.pack(side=tk.RIGHT, padx=45, pady=20)
                        # Image label
                        imageLabel = tk.Label(imageAndName, image=smallSizeImage)
                        imageLabel.image = smallSizeImage  # Prevent garbage collection
                        imageLabel.pack()

                        # Text label (image filename)
                        imageName = tk.Label(imageAndName, text=filename, font=("Arial", 10))
                        imageName.pack()


            searchResultText = f"{detectionCounter} images found."
    except FileNotFoundError as e:
        print("Error: {e}")
        searchResultText = f"Error: {e}"
    searchResults.config(text=searchResultText)
# SpaCy model loading


window = tk.Tk()
window.title('EYEINSIDE v1')
window.geometry('1000x600')
# color of the window
window.configure(bg='gray')

# File path input
filePathLabel = tk.Label(window, text='File Path:',font=("Helvetica", 15), bg='gray')
filePathLabel.place(x=20, y=20)
filePath = tk.Entry(window,width=80)
#filePath.pack(pady=10)
filePath.place(x=20, y=60)

# Query input
queryLabel = tk.Label(window, text='Query:',font=("Helvetica", 15), bg='gray')
queryLabel.place(x=20, y=100)
query = tk.Entry(window,width=80)
#filePath.pack(pady=10)
query.place(x=20, y=140)

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
searchResultsLabel.place(x=20, y=400)

searchResults = tk.Label(window, text="",font=("Helvetica", 10), bg='white')
searchResults.place(x=20, y=440)

# Model paths
spaCyDirectory = "C:\\Users\\HP\\spacy_eyeinside_v1"
YOLO_MODEL = "C:\\Users\\HP\\Downloads\\eyeinside_v1_alldataset.pt"

# Check if the SpaCy model and YOLO model exist
try:
    if not os.path.exists(spaCyDirectory):
        raise FileNotFoundError(f"SpaCy not found on this directory: {spaCyDirectory}")
    elif not os.path.exists(YOLO_MODEL):
        raise FileNotFoundError(f"YOLO model not found on this directory: {YOLO_MODEL}")
    else:
        # if models exists, then they are loaded and the search button becomes active        
        nlp = spacy.load(spaCyDirectory)

        # YOLO model loading
        
        yolo = YOLO(YOLO_MODEL)
        searchButton = tk.Button(window, text='Search',font=("Helvetica", 15), bg='gray', command=searchExecution)
except FileNotFoundError as e:
    searchResults.config(text=f"Error: {e}")
    searchButton = tk.Button(window, text='Search',font=("Helvetica", 15), bg='gray', state='disabled') # if models do not exist, the search button is disabled

searchButton.place(x=20, y=180)

# SpaCy analysis label
spacyAnalysisLabel = tk.Label(window, text='SpaCy ANALYSIS:',font=("Helvetica", 15), bg='gray')
spacyAnalysisLabel.place(x=20, y=250)

spaCyAnalysisResult = tk.Label(window, text="",font=("Helvetica", 10), bg='white')
spaCyAnalysisResult.place(x=20, y=290)

# Image Results label
imageResultsLabel = tk.Label(window, text='IMAGES:',font=("Helvetica", 15), bg='gray')
imageResultsLabel.place(x=700, y=20)


window.mainloop()