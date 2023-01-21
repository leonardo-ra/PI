import math
from statistics import median
import numpy as np
import cv2
from numpy import linalg 

"""
Module to transform camera points (pixels) in to robot plane points (mm)
"""

def yolo_point_to_robot_plane(yolo_point, square_pixel_size, angle, origin_robot_plane, square_size_m):

    pixel_to_m = square_size_m/square_pixel_size        # pixel to m convertion ratio
    yolo_point_x_in_pixels = yolo_point[0]              # x yolo point in pixels
    yolo_point_y_in_pixels = yolo_point[1]              # y yolo point in pixels
    yolo_point_x_in_meters_robot_plane =  (yolo_point_x_in_pixels - origin_robot_plane[0]) * pixel_to_m
    yolo_point_y_in_meters_robot_plane =  (yolo_point_y_in_pixels - origin_robot_plane[1]) * pixel_to_m
    x_point_to_robot =  yolo_point_x_in_meters_robot_plane * math.cos(angle) - yolo_point_y_in_meters_robot_plane * math.sin(angle) + 0.004
    y_point_to_robot =  yolo_point_x_in_meters_robot_plane * math.sin(angle) + yolo_point_y_in_meters_robot_plane * math.cos(angle) + 0.0035

    return x_point_to_robot, y_point_to_robot

def undistor_image(img, camera_file):
    """
    img -> image we want to apply undistort on
    camera_file -> path to the file with the calibration parameters
    returns: image undistor
    """

    with np.load (camera_file) as data :
        mtx = data['cameraMatrix']
        dist = data['distortion']
        
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst
