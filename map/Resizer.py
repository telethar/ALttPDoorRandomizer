import os
import cv2


def resize():
    main_dir = "../test-output/room_images/"
    for file in os.listdir(main_dir):
        img = cv2.imread(main_dir+file, cv2.IMREAD_UNCHANGED)

        resized = cv2.resize(img, (64, 64), interpolation=cv2.INTER_AREA)
        help_me = cv2.imwrite("../data/room_images64/"+file, resized)
        if help_me:
            pass

if __name__ == '__main__':
    resize()


