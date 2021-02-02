import face_recognition as fr
from PIL import Image, ImageDraw


def draw_landmarks(image):
    face_landmarks_list = fr.face_landmarks(image)
    pil_image = Image.fromarray(image)

    for _, face_landmarks in enumerate(face_landmarks_list):
        reduced_chin = face_landmarks['chin'][1:-1]
        reduced_nose = face_landmarks['nose_bridge'][1:]
        left_chin_nose_connection = [reduced_nose[0], reduced_chin[0]]
        right_chin_nose_connection = [reduced_nose[0], reduced_chin[-1]]

        d = ImageDraw.Draw(pil_image, 'RGBA')
        d.line(reduced_chin, fill=(0, 0, 0), width=1)
        # d.line(reduced_nose, fill=(0, 0, 0))
        d.line(left_chin_nose_connection, fill=(0, 0, 0))
        d.line(right_chin_nose_connection, fill=(0, 0, 0))

        # if (_ == 0):
        #     break

    pil_image.show()
