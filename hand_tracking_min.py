from __future__ import annotations
import cv2
from numpy.core.records import array
import mediapipe as mp
import numpy as np
from typing import Literal


class HandTracking:

    def __init__(self, cam_num: int = 0, static_im_mode: bool = False,
                 max_hand_to_detect: int = 2, min_det_conf: float = .5,
                 min_track_conf: float = .5):

        # preparing tools to tracking
        self.cap = cv2.VideoCapture(cam_num)
        self.hand_tracking = mp.solutions.hands.Hands(
            static_im_mode, max_hand_to_detect, min_det_conf, min_track_conf)
        self.draw = mp.solutions.drawing_utils

    def capture(self) -> np.ndarray[int] | Literal[0]:
        """capture frame from camera and return 0 if error 
        but usually the frame as np.ndarray

        Args:
            to_rgb (bool): if you want video frame in rgb mode

        Returns:
            np.ndarray|0: img as np.ndarray or 0 if there was a capture error
        """
        success, img = self.cap.read()
        if not success:
            return 0
        # checking for quit the program
        return img

    def track_hands(self, img: np.array) -> np.array:
        return self.hand_tracking.process(img)

    def draw_landmarks(self, img, landmarks, connections: bool = False):

        if not landmarks.multi_hand_landmarks:
            return
        for hand_lms in landmarks.multi_hand_landmarks:

            if connections:
                self.draw.draw_landmarks(
                    img, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)
            else:
                self.draw.draw_landmarks(img, hand_lms)

    def lms_position(self, img, lm_solution, hand_no=0) -> np.array:

        height, width = img.shape[:2]
        if not lm_solution.multi_hand_landmarks:
            return np.array([])

        lm_solution = lm_solution.multi_hand_landmarks[hand_no]

        # return landmarks position on img
        return np.array([np.array([int(lm.x * width), int(lm.y * height)])
                         for id, lm in enumerate(lm_solution.landmark)])


def main():
    hand_tracking = HandTracking(min_det_conf=.6)
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

        # draw result as  image
        cv2.imshow("Image", img)

        # exit program if conditions
        if cv2.waitKey(1) & 0xFF == ord('q'):
            hand_tracking.cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
