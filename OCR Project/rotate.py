import cv2
import dlib
import numpy as np
import base64
import matplotlib.pyplot as plt
from PIL import Image
detector = dlib.get_frontal_face_detector()
def base64_to_image(base64_str):
    img_data = base64.b64decode(base64_str)
    img_array = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def image_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64

def process_image(img, cnt=0):
    try:
        faces = detector(img, 1)
    except Exception as e:
        print("----------------------------===========================----------------------------")
        print(f"Face detection error: {e}")
        return None
    if faces:
        face = faces[0]
        print("----------------------------===========================----------------------------")
        print(f"Face found at position: top={face.top()}, left={face.left()}, bottom={face.bottom()}, right={face.right()}")
        try:
            face_height = face.bottom() - face.top()
            top = max(0, face.top() - int(face_height * 1.5))
            bottom = min(img.shape[0], face.bottom() + int(face_height * 2))
            left = max(0, face.left() - int(face_height * 4.7))
            right = min(img.shape[1], face.right() + int(face_height * 1.7))
            id_card_cropped = img[top:bottom, left:right]
            card_base64 = image_to_base64(id_card_cropped)
            return card_base64
        except Exception as e:
            print("----------------------------===========================----------------------------")
            print(f"Error processing ID card area: {e}")
            return None
    else:
        if cnt < 3:
            transpose_image = cv2.transpose(img)
            flipped_image = cv2.flip(transpose_image, 0)
            return process_image(flipped_image, cnt + 1)
        else:
            print("----------------------------===========================----------------------------")
            print("Face detection failed after 3 rotations.")
            return None

def process_single_image_base64(base64_str):
    # print(f"Processing base64 encoded image")
    img = base64_to_image(base64_str)
    if img is None:
        print("----------------------------===========================----------------------------")
        print(f"Error reading image from base64 string.")
        return None
    
    return process_image(img)


