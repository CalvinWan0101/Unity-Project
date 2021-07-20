import cv2
import mediapipe as mp
import json
import socket
import sys

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


def draw_key_points(image, key_points):
    height, width, channels = image.shape
    for p in key_points:
        cv2.circle(image, (int(p['x'] * width), int(p['y'] * height)), 3, (0, 255, 0), -1)


def get_key_points(face_landmarks):
    '''
        key_points :
        1: nose (center),
        4: top of nose,
        27: right eye,
        2: down of nose
        257: left eye
    '''
    key_points = []
    for i in [1, 4, 27, 2, 257]:
        data_point = face_landmarks.landmark[i]
        key_points.append({
            'x': data_point.x,
            'y': data_point.y,
            'z': data_point.z,
            'visibility': data_point.visibility,
        })
    return key_points


def get_center_point(key_points):
    '''
        get head center point (front of face is x=0, y=0)
        make -1<x<1, -1<y<1
        head turn right (x<0), left(x>0)
        head turn up(y>0), down(y<0)
    '''

    center_point = {
        'x': (2 * key_points[0]['x'] - (key_points[2]['x'] + key_points[4]['x'])) * 10,
        'y': (key_points[1]['y'] + key_points[3]['y'] - 2 * key_points[0]['y']) * 100,
    }

    return center_point


def get_face_landmarks(image):
    '''use mediapipe's face mesh get face landmarks'''
    results = face_mesh.process(image)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            return face_landmarks
    return None


def preprocess_img(image):
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image


def mark_img(filename):
    '''mark face key point from image'''
    image = cv2.imread(filename)

    image = preprocess_img(image)

    face_landmarks = get_face_landmarks(image)

    if face_landmarks:
        key_points = get_key_points(face_landmarks)
        draw_key_points(image, key_points)

    cv2.imshow('MediaPipe FaceMesh', image)

    cv2.waitKey(0)


def mark_cam():
    '''mark face key point from webcam video'''
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        image = preprocess_img(image)

        face_landmarks = get_face_landmarks(image)

        if face_landmarks:
            key_points = get_key_points(face_landmarks)

            center_point = get_center_point(key_points)

            json_data = json.dumps(center_point)

            print(json_data)

            draw_key_points(image, key_points)

        cv2.imshow('MediaPipe FaceMesh', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()


def post_data():
    ''' use socket post face key points from webcam video'''
    host = '127.0.0.1'
    port = 8787

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        image = preprocess_img(image)

        face_landmarks = get_face_landmarks(image)

        if face_landmarks:
            key_points = get_key_points(face_landmarks)

            center_point = get_center_point(key_points)

            json_data = json.dumps(center_point)

            # using \n mark data end
            packet_data = json_data + '\n'

            print(packet_data)

            draw_key_points(image, key_points)

            s.send(packet_data.encode())

        cv2.imshow('MediaPipe FaceMesh', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()


if __name__ == '__main__':
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        # mark_cam()
        post_data()
