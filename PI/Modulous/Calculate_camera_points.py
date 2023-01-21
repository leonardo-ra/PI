import math
from statistics import median
import numpy as np
import cv2
from numpy import linalg 

"""
Module to transform camera points (pixels) in to robot plane points (mm)
"""



def  Find_Corner_Chessboard(img, board_h = 9, board_w = 6):
    """
    img -> image we want to use to calibrate and know the positions on the world plane
    board_h -> number of square edges in hight
    board_w -> number of square edges in widht
    returns:    square_pixel_size -> size of square of board in pixels
                angle  -> angle between the robot plane and the camera plane
                origin_robot_plane -> origin of robot plane in the camera plane and coordinates
    """

    # Find the chess board corners
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (board_w,board_h), None)

    # Set the needed parameters to find the refined corners
    winSize = (5, 5)
    zeroZone = (-1, -1)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_COUNT, 40, 0.001)
    # Calculate the refined corner locations
    corners = cv2.cornerSubPix(gray, corners, winSize, zeroZone, criteria)

    ## Calculate pixel to mm conversion
    corner = np.squeeze(corners) 
    corner_tuples = list(map(tuple, corner))
    
    norms2 = []
    for i in range(0, len(corner_tuples)):
        if i != 0:
            norms2.append(math.sqrt(math.pow(corner_tuples[i - 1][0] - corner_tuples[i][0], 2) + math.pow(corner_tuples[i - 1][1] - corner_tuples[i][1], 2)))

    square_pixel_size = median(norms2)                                                  # Median of distance between consecutive points found with findChessboardCorners
                                                                                        # Most of the points in adjacent positions of the list are points of the same square of the chessboard
    norm = []
    for tuples in corner_tuples:
        norm.append(math.sqrt(math.pow(tuples[0], 2) + math.pow(tuples[1], 2)))           # distance to point (0,0) of camera

    min_norm = min(norm)
    ind_min_norm = norm.index(min_norm)
    origin_robot_plane = corner_tuples[ind_min_norm]                                    # robot_plane origin is the closest point to the origin of camera

    norm3 = []
    for tuples in corner_tuples:
        if tuples != origin_robot_plane:
            norm3.append(math.sqrt(math.pow(tuples[0] - origin_robot_plane[0] , 2) + math.pow(tuples[1] - origin_robot_plane[1], 2)))     # distance to robot_plane origin
        else:
            norm3.append(100000)
    
    first_min = min(norm3)
    ind_first_min = norm3.index(first_min)
    closest_point_to_robot_plane_origin = corner_tuples[ind_first_min]

    y_diff = abs(closest_point_to_robot_plane_origin[1] - origin_robot_plane[1])
    x_diff = abs(closest_point_to_robot_plane_origin[0] - origin_robot_plane[0])

    if y_diff > x_diff:
        angle = math.pi/2 - math.atan(y_diff/x_diff)
    else:
        angle = math.atan(y_diff/x_diff)

    
    return square_pixel_size, angle, origin_robot_plane

def yolo_point_to_robot_plane(yolo_point, square_pixel_size, angle, origin_robot_plane, square_size_m):

    pixel_to_m = square_size_m/square_pixel_size        # pixel to m convertion ratio
    yolo_point_x_in_pixels = yolo_point[0]              # x yolo point in pixels
    yolo_point_y_in_pixels = yolo_point[1]              # y yolo point in pixels
    yolo_point_x_in_meters_robot_plane =  (yolo_point_x_in_pixels - origin_robot_plane[0]) * pixel_to_m
    yolo_point_y_in_meters_robot_plane =  (yolo_point_y_in_pixels - origin_robot_plane[1]) * pixel_to_m
    x_point_to_robot =  yolo_point_x_in_meters_robot_plane * math.cos(angle) - yolo_point_y_in_meters_robot_plane * math.sin(angle) + 0.052
    y_point_to_robot =  yolo_point_x_in_meters_robot_plane * math.sin(angle) + yolo_point_y_in_meters_robot_plane * math.cos(angle) + 0.067

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

