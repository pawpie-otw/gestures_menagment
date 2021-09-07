from __future__ import annotations
from hand_tracking_min import HandTracking
import cv2
import mediapipe as mp
import numpy as np
from volume_set import set_audio_volume
from gestures import Gestures
from math import dist

###############
wCam, hCam = 1280, 720

###############


def main():
    hand_tracking = HandTracking(min_det_conf=.7)
    gestures = Gestures()
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

            point_a = hand_lms_pos[4, 1:]
            point_b = hand_lms_pos[8, 1:]
            center = (point_a + point_b) // 2
            cv2.circle(img, tuple(
                hand_lms_pos[4]), 4, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, tuple(
                hand_lms_pos[8]), 4, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (320, 0), (320, 480), (255, 0, 255), 2, cv2.FILLED)
            cv2.line(img, hand_lms_pos[0], hand_lms_pos[9],
                     (255, 0, 255), 2, cv2.FILLED)
            cv2.putText(img, "pos: " + str(gestures.hand_pos_angle(hand_lms_pos)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 0, 255), 2, cv2.LINE_AA)
            print(gestures.straightened_all_fingers(hand_lms_pos))

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
