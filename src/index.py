from pathlib import Path
import face_recognition as fr

from functions.draw import draw_landmarks


def main():
    path = Path(__file__).parent

    image = fr.load_image_file(f'{path}/../images/groups/team-of-people-2.jpg')

    draw_landmarks(image, 'N95.png')


if __name__ == '__main__':
    main()
