import numpy as np
import math
from typing import List


class Gestures:
    @staticmethod
    def like(hand_lms: np.array) -> bool:
        thumb = hand_lms[:5]

        # ---------   THUMB   ---------
        # if thumb is not  upright
        if all(thumb[1:, 1] < thumb[:-1, 1]):
            return False
        for i in range(4):
            # check if all landmarks vertical points are correct
            lms_y = np.array([5, 9, 13]) + i
            if all(hand_lms[lms_y, 1] < hand_lms[lms_y+4, 1]):
                return False

            # check for horizontal arrangement
            lms_x = np.array([6, 7]) + i*4
            if hand_lms[6 + i*4, 0] > hand_lms[5 + i*4, 0] and \
               all(hand_lms[lms_x, 0] > hand_lms[lms_x+1, 0]):
                return False
        return True

    @staticmethod
    def hand_pos_angle(hand_lms: np.array) -> float:

        point_a = hand_lms[0]
        point_b = hand_lms[9]
        point_c = np.array([point_a[0], point_b[1]])

        dist_a_c = math.dist(point_a, point_c)
        dist_a_b = math.dist(point_a, point_b)

        result = dist_a_c / dist_a_b

        if point_a[1] > point_b[1]:
            result += 1

        if point_b[0] < point_b[0]:
            return round(result*-1, 2)

        return round(result, 2)

    @staticmethod
    def straightened_all_fingers(hand_lms_pos: np.array) -> List[bool]:

        return np.array([Gestures.straightened_finger(
            hand_lms_pos[1+i*4:i*4+5]) for i in range(5)])

    @staticmethod
    def straightened_finger(finger_lms_pos: np.array) -> bool:
        if finger_lms_pos[-1, 1] < finger_lms_pos[-3, 1]:
            return True
        return False


if __name__ == '__main__':
    Gestures.hand_pos_ang_by_vec(pa=(2, 4), pb=(3, 4))
