import face_recognition as fr
from PIL import Image, ImageDraw


def draw_landmarks(image):
    face_landmarks_list = fr.face_landmarks(image)
    pil_image = Image.fromarray(image)

    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')
        d.line(face_landmarks['chin'], fill=(255, 255, 255), width=1)
        d.polygon(face_landmarks['nose_bridge'], fill=(255, 255, 255))

    pil_image.show()
