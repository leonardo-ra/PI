### Code based on: https://github.com/niconielsen32/YOLOv5Live/blob/main/YOLOv5Live.py https://www.youtube.com/watch?v=Cof7CNjDppo

import torch
import numpy as np
import cv2
from time import time

class XFP:
    """
    Class that implements Yolo_v5 model to make detect XFP on video
    """

    def __init__(self, capture_index, model_name):
        """
        Initialize the class 
        """

        self.capture_index = capture_index          # index of webcam from where we want to get our image from
        self.model = self.load_model(model_name)    # model_name = weights file after we trained our model (path to our model)
        self.classes = self.model.names             # classes = different labels we want to identify/used on our model
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

    def get_video_capture(self):
        """
        Cretes a new video streaming object to extract video frame by frame to make prediction on.
        :return: Opencv2 video capture object.
        """

        return cv2.VideoCapture(self.capture_index)

    def load_model(self, model_name):    
        """
        Loads Yolo_v5 model from pytorch hub.
        :return: Trained pytorch model.
        """

        # If we specify a model we use that custom model, else we used the default model from yolo_v5
        if model_name:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path = model_name, force_reload=True)   # load a model from a github repo or a local directory (custom model)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5', pretrained=True)                        # load a model from a github repo or a local directory (yolov5 deafult model)


    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolov5 model.
        :param frame: Input frame in numpy/list/tuple format.
        :return: Labels and coordinates of objects detected by the model in the frame.
        """

        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)     # Pass frame trough our model
        labels, coord = results.xyxyn[0][:,-1], results.xyxyn[0][:, :-1]
        return labels, coord

    def class_to_label(self, x):
        """
        For a given label value, return correposding string label
        :param x: Numeric label
        :return: Corresponding string label
        """

        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: Contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels plotted on it.
        """

        labels, coord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = coord[i]
            if row[4] > 0.2: # Threshold -> If our detection is not more certain than a threshold (confidence score level)
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame

    def __call__(self):
        """
        This function is called when class is executed. It runs the loop to read the video frame by frame, and write the output into a new file
        :return: void
        """

        cam = self.get_video_capture()

        while cam.isOpened():
            ret, frame = cam.read()
            assert ret

            frame = cv2.resize(frame, (416, 416)) # Resize to the same dimentions of the images we trained the model on

            start_time = time()
           
            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)

            end_time = time()
            fps = 1/np.round(end_time-start_time, 2)
            print(f"Frames per second: {fps}")
            
            cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            cv2.imshow('Yolo_v5 detection', frame)

            if cv2.waitKey(5) & 0xFF == 27: # Press ESQ to exit the programm
                break
        
        cam.realease()

# Create a new object and execute
detector = XFP(capture_index=1, model_name='best.pt')
detector()