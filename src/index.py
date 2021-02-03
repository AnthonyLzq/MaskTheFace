from pathlib import Path
import face_recognition as fr
# import json

from functions.draw import draw_landmarks


def main():
    path = Path(__file__).parent

    image = fr.load_image_file(f'{path}/../images/groups/team-of-people-3.jpg')

    draw_landmarks(image, 'N95.png')


if __name__ == '__main__':
    main()

# face_locations = fr.face_locations(image)

# Array of coords of each face
# print(face_locations)

# Number of people in the image
# print(f'There are {len(face_locations)} people in this image')

# Locations of face parts
# face_parts = fr.face_landmarks(image, face_locations)
# print(json.dumps(face_parts[0], indent=2))
