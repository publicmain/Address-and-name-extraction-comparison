# import cv2
# import numpy as np
# import math
# from PIL import Image
# from config import POINTS_NUM_LANDMARK,detector,predictor
# def rotate_img(image, angle):
#     (h, w) = image.shape[:2]
#     (cX, cY) = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
#     cos = np.abs(M[0, 0])
#     sin = np.abs(M[0, 1])
#     nW = int((h * sin) + (w * cos))
#     nH = int((h * cos) + (w * sin))
#     M[0, 2] += (nW / 2) - cX
#     M[1, 2] += (nH / 2) - cY
#     return cv2.warpAffine(image, M, (nW, nH))

# def _largest_face(dets): 
#     if len(dets) == 1:
#         return 0
#     face_areas = [(det.right() - det.left()) * (det.bottom() - det.top()) for det in dets]
#     largest_area = face_areas[0]
#     largest_index = 0
#     for index in range(1, len(dets)):
#         if face_areas[index] > largest_area:
#             largest_index = index
#             largest_area = face_areas[index]
#     return largest_index

# def get_image_points_from_landmark_shape(landmark_shape):
#     if landmark_shape.num_parts != POINTS_NUM_LANDMARK:
#         print("ERROR:landmark_shape.num_parts-{}".format(landmark_shape.num_parts))
#         return -1, None
#     image_points = np.array([
#         (landmark_shape.part(30).x, landmark_shape.part(30).y),
#         (landmark_shape.part(8).x, landmark_shape.part(8).y),
#         (landmark_shape.part(36).x, landmark_shape.part(36).y),
#         (landmark_shape.part(45).x, landmark_shape.part(45).y),
#         (landmark_shape.part(48).x, landmark_shape.part(48).y),
#         (landmark_shape.part(54).x, landmark_shape.part(54).y)
#     ], dtype="double")
#     return 0, image_points

# def computerAngle2(x1, y1, x2, y2):
#     angle = math.atan2((y1 - y2), (x2 - x1))
#     angle = angle * 180 / math.pi
#     return angle

# def detectImage(img, dets, angle):
#     largest_index = _largest_face(dets)
#     face_rectangle = dets[largest_index]
#     landmark_shape = predictor(img, face_rectangle)
#     return get_image_points_from_landmark_shape(landmark_shape)

# def findRotate(image):
#     img = np.array(image)
#     finallyImg = None
#     finallyAngle = 0
#     for angle in range(0, 360, 60):
#         rotateImg = rotate_img(img, angle)
#         dets = detector(rotateImg, 0)
#         if len(dets) > 0:
#             finallyImg = rotateImg
#             ret, image_points = detectImage(rotateImg, dets, angle)
#             if ret != 0:
#                 print('get_image_points failed')
#                 break
#             Nose_x, Nose_y = image_points[0]
#             Chin_x, Chin_y = image_points[1]
#             Left_Eye_x, Left_Eye_y = image_points[2]
#             Right_Eye_x, Right_Eye_y = image_points[3]
#             Left_Mouth_x, Left_Mouth_y = image_points[4]
#             Right_Mouth_x, Right_Mouth_y = image_points[5]
#             eyeAngle = computerAngle2(Left_Eye_x, Left_Eye_y, Right_Eye_x, Right_Eye_y)
#             mouthAngle = computerAngle2(Left_Mouth_x, Left_Mouth_y, Right_Mouth_x, Right_Mouth_y)
#             nose2chinAngle = computerAngle2(Nose_x, Nose_y, Chin_x, Chin_y)
#             nose2chinAngle += 90
#             avgAngle = (eyeAngle + mouthAngle + nose2chinAngle) / 3
#             finallyAngle = angle + avgAngle
#             if finallyAngle > 360:
#                 finallyAngle -= 360
#             if finallyAngle < -360:
#                 finallyAngle += 360
#             break
#     if finallyImg is not None:
#         finallyImg = rotate_img(img, finallyAngle)
#         return Image.fromarray(finallyImg)
# # def findRotate(image):
# #     return image