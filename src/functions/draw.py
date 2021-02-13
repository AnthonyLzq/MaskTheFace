import face_recognition as fr
import math as m
import operator as o
from pathlib import Path
from PIL import Image, ImageDraw


def get_rotation_angle_from_Y_axis(array_of_two_points, inverse=False):
    p1, p2 = array_of_two_points
    vector = (p2[0] - p1[0], - p2[1] + p1[1])

    # Inclination across Y axis: vector . (0, 1) = vector[1]
    vector_module = (vector[0]**2 + vector[1]**2)**0.5
    scalar_product = vector[1]
    cos = scalar_product/vector_module

    if (p2[0] > p1[0]):
        angle = 180 - m.degrees(m.acos(cos))
    else:
        angle = m.degrees(m.acos(cos)) - 180

    if inverse:
        return -angle
    else:
        return angle


def get_distance(array_of_two_points):
    p1, p2 = array_of_two_points

    return int(((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5)


def get_middle_point(array):
    mid_len = int(len(array)/2)

    if len(array) % 2 == 0:
        return array[mid_len]
    else:
        tuple_mid_value = tuple(
            map(o.add, array[mid_len], array[mid_len - 1])
        )
        tuple_mid_value = tuple(
            [int(x/2) for x in tuple_mid_value]
        )

        return tuple_mid_value


def draw_masks(
    points,
    pil_image,
    left_chin_nose_connection,
    right_chin_nose_connection,
    bottom_chin_nose_connection,
    mask
):
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

    # Y - face tilt
    left_chin_node_distance = get_distance(left_chin_nose_connection)
    right_chin_node_distance = get_distance(right_chin_nose_connection)
    distance_difference = abs(
        left_chin_node_distance - right_chin_node_distance
    )

    # Z - face tilt validation
    inverse = False

    # Mask
    if distance_difference < 20:
        pil_mask = Image.open(f'{path}/../../images/masks/{mask}')
        pil_mask_resized = pil_mask.resize((width, height))
        mask_position = (left[0] + int(0.15*width), top[1])

    elif left_chin_node_distance > right_chin_node_distance:
        right = f'{mask.split(".")[0]}_right.{mask.split(".")[1]}'

        pil_mask = Image.open(f'{path}/../../images/masks/{right}')
        pil_mask_resized = pil_mask.resize((width, height))
        mask_position = (left[0] + int(0.175*width), top[1])
        inverse = True
    else:
        left_mask = f'{mask.split(".")[0]}_left.{mask.split(".")[1]}'

        pil_mask = Image.open(f'{path}/../../images/masks/{left_mask}')
        pil_mask_resized = pil_mask.resize((width, height))
        mask_position = (left[0] + int(0.15*width), top[1])

    # Z - face tilt
    angle = get_rotation_angle_from_Y_axis(bottom_chin_nose_connection, inverse)
    pil_mask_rotated = pil_mask_resized.rotate(angle)
    pil_image.paste(pil_mask_rotated, mask_position, pil_mask_rotated)


def draw_landmarks(image, mask):
    face_landmarks_list = fr.face_landmarks(image)
    pil_image = Image.fromarray(image)

    for _, face_landmarks in enumerate(face_landmarks_list):
        # Getting face critical points
        reduced_chin = face_landmarks['chin'][1:-1]
        reduced_nose = face_landmarks['nose_bridge'][1:]
        lowest_face_point = get_middle_point(reduced_chin)

        left_chin_nose_connection = [reduced_nose[0], reduced_chin[0]]
        right_chin_nose_connection = [reduced_nose[0], reduced_chin[-1]]
        bottom_chin_nose_connection = [reduced_nose[0], lowest_face_point]

        # d = ImageDraw.Draw(pil_image, 'RGBA')
        ImageDraw.Draw(pil_image, 'RGBA')

        # d.line(left_chin_nose_connection, fill=(0, 0, 0))
        # d.line(right_chin_nose_connection, fill=(0, 0, 0))
        # d.line(bottom_chin_nose_connection, fill=(0, 0, 0))

        draw_masks(
            [
                reduced_nose[0],
                reduced_chin[-1],
                lowest_face_point,
                reduced_chin[0]
            ],
            pil_image,
            left_chin_nose_connection,
            right_chin_nose_connection,
            bottom_chin_nose_connection,
            mask
        )

        # if _ == 0:
        #     break

    pil_image.show()
