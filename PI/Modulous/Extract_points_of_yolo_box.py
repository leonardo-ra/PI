### Code based on: https://github.com/niconielsen32/YOLOv5Live/blob/main/YOLOv5Live.py https://www.youtube.com/watch?v=Cof7CNjDppo

import fnmatch
import torch
import numpy as np
import cv2
import os
import math

"""
This function implements Yolo_v5 model to detect XFP on image
Shows a image of detected XFP
:param: frame after imread
:param: model of Yolo
:return: Labels and coordinates
"""
    
class XFP:
    """
    Class that implements Yolo_v5 model to make detect XFP on video
    """

    def __init__(self, frame, model):
        """
        Initialize the class 
        """
        self.frame = frame                                          # Frame/ image we want to analize (after imread)
        self.model = model                                          # Trained pytorch model (after load)
        self.classes = self.model.names                             # Classes = different labels we want to identify/used on our model
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

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
        # print(results.pandas().xyxy[0])
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
            if row[4] > 0.7: # Threshold -> If our detection is not more certain than a threshold (confidence score level)
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (255, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
        return frame
    
    def box_size(self, info):
        diff = []
        result = []
        for inf in info:
            if inf[0] == 'Test-Box':
                frame_aux = self.frame[inf[2]:inf[4], inf[1]:inf[3]] # img [y:y+h, x:x+w]
                gray = cv2.cvtColor(frame_aux,cv2.COLOR_BGR2GRAY)
                bi = cv2.bilateralFilter(gray, 5, 75, 75)
                # Apply binary thresholding
                _, thresh = cv2.threshold(bi, 90, 255, cv2.THRESH_BINARY_INV)
                cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (5,5))
                # Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
                contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
                # Find biggest contour
                c = max(contours, key = cv2.contourArea)

                # Find the minimum area rectangle that encloses the contour
                rect = cv2.minAreaRect(c)

                # Find the corner points of the rectangle
                box = cv2.boxPoints(rect)

                # Convert the corner points to integers
                box = np.int0(box)

                # Draw the rectangle on the image
                cv2.drawContours(frame_aux, [box], 0, (0, 0, 255), 2)

                first_element = min([sublist[1] for sublist in box])
                result = list(filter(lambda x: x[1] == first_element, box))
                result = [tuple(x) for x in result]
                norm1 = math.sqrt(math.pow(result[0][0], 2) + math.pow(result[0][1], 2))
                norm2 = math.sqrt(math.pow(result[1][0], 2) + math.pow(result[1][1], 2))
                diff = abs(norm1 - norm2)
                # cv2.imshow("Frame", frame_aux)
                # cv2.waitKey(0)
        return  diff, result

    def __call__(self, flag = 0):
        """
        This function is called when class is executed. It processes the image passed, finds the XFP thanks to Yolo model and returns labels and coord of the XFPs found
        :return: Labels and coordinates of objects detected by the model in the frame.
        """
        frame = cv2.resize(self.frame, (1280, 720)) # Resize to the same dimentions of the images we trained the model on
        results = self.score_frame(frame)
        labels, coord = results
        frame = self.plot_boxes(results, frame)
        info = []
        info2 = []
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(len(labels)):
            row = coord[i]
            if row[4] > 0.7:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                if self.class_to_label(labels[i]) != 'Test-Box':
                    info2.append([self.class_to_label(labels[i]), int((x1+x2)/2), int((y1+y2)/2)])
                else:
                    info.append([self.class_to_label(labels[i]), x1, y1, x2, y2])

        size, aux = self.box_size(info)
        origin_robot_plane = (info[0][1] + aux[0][0], info[0][2] + aux[0][1])
        other_point = (info[0][1] + aux[1][0], info[0][2] + aux[1][1])

        y_diff = abs(other_point[1] - origin_robot_plane[1])
        x_diff = abs(other_point[0] - origin_robot_plane[0])

        if y_diff > x_diff:
            angle = math.pi/2 - math.atan(y_diff/x_diff)
        else:
            angle = math.atan(y_diff/x_diff)

        for i in info2:
            cv2.circle(frame, (i[1], i[2]), 7, (0, 255, 255), -1)    

        cv2.circle(frame, origin_robot_plane, 7, (0, 0, 255), -1)
        cv2.circle(frame, other_point, 7, (0, 255, 0), -1)

        cv2.imshow("Yolo", frame)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()

        if flag == 1:      # Calibration
            return size, origin_robot_plane, angle
        else:
            return info2



# def load_model():    
#     """
#     Loads Yolo_v5 model from pytorch hub.
#     :return: Trained pytorch model.
#     """
#     model = torch.hub.load(r'C:\Users\User\Desktop\PIC\PIC\Grupo Vasco\Final\yolov5', 'custom', path=r'C:\Users\User\Desktop\PIC\PIC\Grupo Vasco\Final\yolov5\models\best_box2.pt', source='local')
#     return model



# model = load_model()
# capture_index = 1   # Index of camera we want to acess
# cam = cv2.VideoCapture(capture_index, cv2.CAP_DSHOW)    #Create video stream
# cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)  #Turn the autofocus off
# cam.set(3, 1280)
# cam.set(4, 720)
# cam.set(cv2.CAP_PROP_FPS, 60)
# ret, frame = cam.read()
# assert ret # check if we got a frame
# detector = XFP(frame, model)                                    # Create a new object to identify XFPs
# center_x, center_y, angle_rad, info = detector()
# print('info:' + str(info))                                       # Use the call function of the object


# # frame = cv2.imread("frame0.jpg")
# cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)  
# cam.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
# cam.set(3, 1280)
# cam.set(4, 720)
# cam.set(cv2.CAP_PROP_FPS, 60)
# dir_path = os.getcwd()
# files = fnmatch.filter(os.listdir(dir_path), 'frame*.jpg')
# model = load_model()
# for file in files:
#     frame = cv2.imread(file)
#     detector = XFP(frame, model)
#     flag = 1
#     if flag == 0:
#         info = detector(flag)
#         print(info)
#     else: 
#         size, origin_robot_plane, angle = detector(flag)
#         print(f"Box size in pixels: {size}")
#         print(f"Origin point: {origin_robot_plane}")
#         print(f"Angle: {angle}")
    