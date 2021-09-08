from __future__ import annotations
from hand_tracking_min import HandTracking
import cv2
import mediapipe as mp
import numpy as np
from volume_set import set_audio_volume
from gestures import GesturesDetect
from math import dist
from triggers import *
# from enum_classes import HandVerticalGestures
###############
wCam, hCam = 1280, 720

###############


def main():
    list_used_functions = set()
    DEVIL_HORNS = np.array([False, True, False, False, True])
    hand_tracking = HandTracking(min_det_conf=.7)
    gestures = GesturesDetect()
    while True:

        # capturing the img
        img = hand_tracking.capture()

        # processing looking for hand
        ht_solution = hand_tracking.track_hands(
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # draw
        hand_tracking.draw_landmarks(img, ht_solution, connections=True)

        # compute position
        hand_lms_pos = hand_tracking.lms_position(img, ht_solution)

        if len(hand_lms_pos) != 0:
            # print(hand_lms_pos)

            # point_a = hand_lms_pos[4, 1:]
            # point_b = hand_lms_pos[8, 1:]
            # center = (point_a + point_b) // 2
            # cv2.circle(img, tuple(
            #     hand_lms_pos[4]), 4, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, tuple(
            #     hand_lms_pos[8]), 4, (255, 0, 255), cv2.FILLED)
            # cv2.line(img, (320, 0), (320, 480), (255, 0, 255), 2, cv2.FILLED)
            # cv2.line(img, hand_lms_pos[0], hand_lms_pos[9],
            #          (255, 0, 255), 2, cv2.FILLED)

            fingers = gestures.straightened_all_fingers(hand_lms_pos)
            angle = gestures.hand_pos_angle(hand_lms_pos, rad_to_deg=True)
            if abs(angle) < 15:
                cv2.putText(img, "fingers: " + str(fingers), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 255), 1, cv2.LINE_AA)

            cv2.putText(img, "ang: " + str(angle), (50, 150), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 255), 1, cv2.LINE_AA)

            if hand_angle_between(-15, 15, angle) and \
                    all(fingers == DEVIL_HORNS) and \
                    not 1 in list_used_functions:
                list_used_functions.add(1)
                print("devil horns")
            if not hand_angle_between(-15, 15, angle):
                list_used_functions.clear()

            # if gestures.like(hand_lms_pos):
            #     cv2.putText(img, 'You like it', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
            #                 2, (255, 0, 255), 2, cv2.LINE_AA)
            # set_audio_volume(dist(point_a, point_b, r=0))
            # hand_arrangment(hand_lms_pos)
        # draw result as  image
        cv2.imshow("Image", img)

        # exit program if conditions
        if cv2.waitKey(1) & 0xFF == ord('q'):
            hand_tracking.cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
