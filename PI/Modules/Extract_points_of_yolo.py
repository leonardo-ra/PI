### Code based on: https://github.com/niconielsen32/YOLOv5Live/blob/main/YOLOv5Live.py https://www.youtube.com/watch?v=Cof7CNjDppo

import math
import torch
import numpy as np
import cv2
from operator import itemgetter

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
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
        return frame
    
    def find_Center_and_angle(self, info):
        center_x = []
        center_y = []
        angle_rad = []
        info_2 = []
        for inf in info:
            frame_aux = self.frame[inf[2]:inf[4], inf[1]:inf[3]] # img [y:y+h, x:x+w]
            gray = cv2.cvtColor(frame_aux,cv2.COLOR_BGR2GRAY)
            # Apply binary thresholding
            _, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
            # Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
            contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE) 
            # Find max area and create a flag if area of object detected is bigger than the expected -> possible not a XFP.
            max_area = 0
            for cont in contours:        
                area = cv2.contourArea(cont) 
                if area > max_area:
                    max_area = area

            if max_area > 30000:  # Value found manually
                print("Area of object detected bigger than 30000 (expected max value of XFP)")
                continue   # Pass to the next object
            info_2.append(inf)
            # Find biggest contour
            if contours:
                c = max(contours, key = cv2.contourArea)
                # Find centroid
                M = cv2.moments(c)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])

                center_x.append(cx + inf[1])
                center_y.append(cy + inf[2])

                cv2.drawContours(frame_aux, c, -1, (0,255,0), 3)
                
                # get rotated rectangle from outer contour
                rotrect = cv2.minAreaRect(c)
                # get angle from rotated rectangle
                            
                points = cv2.boxPoints(rotrect)
                points = points.tolist()
                points_tuples = list(map(tuple, points))

                norms2 = []
                for i in range(0, len(points_tuples)):
                    if i != 0:
                        norms2.append(math.sqrt(math.pow(points_tuples[i - 1][0] - points_tuples[i][0], 2) + math.pow(points_tuples[i - 1][1] - points_tuples[i][1], 2)))

                max_norm = max(norms2)
                ind_max_norm = norms2.index(max_norm)
                y_diff = abs(points_tuples[ind_max_norm+1][1] - points_tuples[ind_max_norm][1] )
                x_diff = abs(points_tuples[ind_max_norm+1][0] - points_tuples[ind_max_norm][0] )
                
                if (points_tuples[ind_max_norm][1] > points_tuples[ind_max_norm+1][1] and points_tuples[ind_max_norm][0] > points_tuples[ind_max_norm+1][0]):
                    angle = math.atan2(y_diff, x_diff)
                elif (points_tuples[ind_max_norm][1] < points_tuples[ind_max_norm+1][1] and points_tuples[ind_max_norm][0] < points_tuples[ind_max_norm+1][0]):
                    angle = math.atan2(y_diff, x_diff)
                else:
                    angle = math.atan2(-y_diff, x_diff)

                angle_rad.append(angle)

        return center_x, center_y, angle_rad, info_2

    def validate_label(self, info):
        info_2 = []
        for inf in info:
            frame_aux = self.frame[inf[2]:inf[4], inf[1]:inf[3]] # img [y:y+h, x:x+w]
            if inf[0] == "XFP_back":
                hsv = cv2.cvtColor(frame_aux, cv2.COLOR_BGR2HSV)
                # Define range of green color in HSV
                lower_green = np.array([30, 50, 30])
                upper_green = np.array([100, 255, 100])
                # preparing the mask to overlay
                mask = cv2.inRange(hsv, lower_green, upper_green)
                
                # Split image into top half and bottom half
                height, width = frame_aux.shape[:2]
                top_half = mask[0:height//2, 0:width]
                bottom_half = mask[height//2:height, 0:width]

                # Count non-zero pixels in top half and bottom half
                top_half_non_zero = cv2.countNonZero(top_half)
                bottom_half_non_zero = cv2.countNonZero(bottom_half)

                # Check in which half the green part is located
                if top_half_non_zero > bottom_half_non_zero:
                    info_2.append([inf[0], "top_half"])
                else:
                    info_2.append([inf[0], "bottom_half"])

            elif inf[0] == "XFP_front":
                gray = cv2.cvtColor(frame_aux,cv2.COLOR_BGR2GRAY)
                # Apply binary thresholding
                _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
                # Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
                contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE) 
                copy_frame = frame_aux.copy()
                # Find areas of contours
                areaArray = []
                for i, c in enumerate(contours):
                    area = cv2.contourArea(c)
                    areaArray.append(area)
                #first sort the array by area
                sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
                #find the nth largest contour [n-1][1], in this case 2
                secondlargestcontour = sorteddata[1][1]
                cv2.drawContours(copy_frame, secondlargestcontour, -1, (255,0,0), 3)
                hsv = cv2.cvtColor(copy_frame, cv2.COLOR_BGR2HSV)

                # Define range of blue color in HSV
                lower_blue = np.array([110,50,50])
                upper_blue = np.array([130,255,255])

                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(hsv, lower_blue, upper_blue)

                # Split image into top half and bottom half
                height, width = copy_frame.shape[:2]
                top_half = mask[0:height//2, 0:width]
                bottom_half = mask[height//2:height, 0:width]

                # Count non-zero pixels in top half and bottom half
                top_half_non_zero = cv2.countNonZero(top_half)
                bottom_half_non_zero = cv2.countNonZero(bottom_half)

                # Check in which half the blue part is located
                if top_half_non_zero > bottom_half_non_zero:
                    info_2.append([inf[0], "top_half"])
                else:
                    info_2.append([inf[0], "bottom_half"])

        return info_2

    def __call__(self):
        """
        This function is called when class is executed. It processes the image passed, finds the XFP thanks to Yolo model and returns labels and coord of the XFPs found
        :return: Labels and coordinates of objects detected by the model in the frame.
        """
        frame = cv2.resize(self.frame, (1280, 720)) # Resize to the same dimentions of the images we trained the model on
        frame = self.frame.copy()
        results = self.score_frame(frame)
        labels, coord = results
        frame = self.plot_boxes(results, frame)
        info = []
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(len(labels)):
            row = coord[i]
            if row[4] > 0.7:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                info.append([self.class_to_label(labels[i]), x1, y1, x2, y2])
        
        center_x, center_y, angle_rad, info = self.find_Center_and_angle(info)
        if center_x:
            info = self.validate_label(info)
            for i in range(len(center_x)):
                cv2.circle(frame, (center_x[i], center_y[i]), 7, (0, 0, 255), -1)
                start_point = (center_x[i], center_y[i])
                end_point = (int(round(center_x[i] + 100 * math.cos(angle_rad[i]))), int(round(center_y[i] + 100 * math.sin(angle_rad[i]))))
                cv2.line(frame, start_point, end_point, (255, 0, 0), 2) 

            cv2.imshow("Yolo", frame)
            for count, list in enumerate(info):
                if (list[1] == "top_half" and list[0] == "XFP_front") or (list[1] == "bottom_half" and list[0] == "XFP_back"):
                    angle_rad[count] = angle_rad[count] - math.pi

            cv2.waitKey(3000)
            cv2.destroyAllWindows()
        return  center_x, center_y, angle_rad, info

# def load_model():
#     model = torch.hub.load(r'C:\Users\User\Desktop\PIC\PIC\Grupo Vasco\Final\yolov5', 'custom', path=r'C:\Users\User\Desktop\PIC\PIC\Grupo Vasco\Final\yolov5\models\best (1).pt', source='local')
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
# print('info:' +str(info))                                       # Use the call function of the object


