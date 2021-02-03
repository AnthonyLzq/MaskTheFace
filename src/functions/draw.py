import face_recognition as fr
import operator
from pathlib import Path
from PIL import Image, ImageDraw


def get_middle_point(array):
    mid_len = int(len(array)/2)

    if len(array) % 2 == 0:
        return array[mid_len]
    else:
        tuple_mid_value = tuple(
            map(operator.add, array[mid_len], array[mid_len - 1])
        )
        tuple_mid_value = tuple(
            [int(x/2) for x in tuple_mid_value]
        )
        return tuple_mid_value


def draw_masks(points, pil_image, mask):
    """
    It receives 4 key points of the mask in the following format:
    points: [top, right, bottom, left]
    """
    top, right, bottom, left = points
    # Vertical distance
    height = int(((top[0] - bottom[0])**2 + (top[1] - bottom[1])**2)**0.5)
    # Horizontal distance
    width = int(0.8*((right[0] - left[0])**2 + (right[1] - left[1])**2)**0.5)

    # Getting the current path
    path = Path(__file__).parent

    # Mask
    pil_mask = Image.open(f'{path}/../../images/masks/{mask}')
    pil_mask_resized = pil_mask.resize((width, height))
    mask_position = (left[0] + int(0.15*width), top[1])

    pil_image.paste(pil_mask_resized, mask_position, pil_mask_resized)


def draw_landmarks(image, mask):
    face_landmarks_list = fr.face_landmarks(image)
    pil_image = Image.fromarray(image)

    for _, face_landmarks in enumerate(face_landmarks_list):
        reduced_chin = face_landmarks['chin'][1:-1]
        reduced_nose = face_landmarks['nose_bridge'][1:]

        ImageDraw.Draw(pil_image, 'RGBA')

        draw_masks(
            [
                reduced_nose[0],
                reduced_chin[-1],
                get_middle_point(reduced_chin),
                reduced_chin[0]
            ],
            pil_image,
            mask
        )

        # if _ == 1:
        #     break

    pil_image.show()
