import numpy as np
import math
from typing import List


class GesturesDetect:
    @staticmethod
    def like(hand_lms: np.array) -> bool:
        """work on this feature is ongoing...

        It will check if hand is in "like" or thumb up position.

        Args:
            hand_lms (np.array): Landmarks

        Returns:
            bool
        """
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
    def hand_pos_angle(hand_lms: np.array, rad_to_deg: bool = False) -> float:
        """Calculate the angle between vertical axe and hand direction.
        Negative value means that hand is directed to left, positive - right.


        Args:
            hand_lms (np.array): hand landmarks in format such 
            as generated by mediapipe lib.

        Returns:
            float: angle in radians.
        """
        point_a = hand_lms[0]
        point_b = hand_lms[9]
        point_c = np.array([point_a[0], point_b[1]])

        dist_a_b = math.dist(point_a, point_b)
        dist_a_c = math.dist(point_a, point_c)

        result = dist_a_c / dist_a_b

        quarter = GesturesDetect.angle_quarter(point_a, point_b)

        if quarter == 1:
            result = (1+result)/2
        if quarter == 2:
            result = (1+result)/-2
        if quarter == 3:
            result = (1-result)/-2
        if quarter == 4:
            result = (1-result)/2
        if rad_to_deg:
            result = round(result*180, 0)
        return result

    @staticmethod
    def straightened_all_fingers(hand_lms_pos: np.array) -> List[bool]:
        """Check all fingers in hand if these are straightened or not
        and return List[bool] in order: 
        [thumb, index, middle, ring, little/pinky] * -finger
        Where True mins straightened and False bent.
        Args:
            hand_lms_pos (np.array): Hand landmarks points like generated by mediapipe

        Returns:
            List[bool]: list of fingers
        """
        default_fingers = np.array([GesturesDetect.straightened_finger(
            hand_lms_pos[5+i*4:i*4+9]) for i in range(4)])
        thumb_finger = GesturesDetect.straightened_thumb(hand_lms_pos[1:5])
        return np.r_[thumb_finger, default_fingers]

    @staticmethod
    def straightened_finger(finger_lms_pos: np.array) -> bool:
        """Check, if finger (except for the thumb) is bent or straightened

        Args:
            finger_lms_pos (np.array): 4 finger landmarks like generated by mediapipe

        Returns:
            bool: True - straightened, False - bent
        """
        if finger_lms_pos[-1, 1] < finger_lms_pos[-3, 1]:
            return True
        return False

    @staticmethod
    def straightened_thumb(finger_lms: np.array) -> bool:
        """special method for straightened thumb verification,
        because the thumb bends slightly differently

        Args:
            hand_lms (np.array): 4 finger landmarks like generated by mediapipe

        Returns:
            bool: True - straightened, False - bent
        """
        if finger_lms[-1, 0] < finger_lms[-2, 0] < finger_lms[-3, 0]:
            return True
        return False

    @staticmethod
    def angle_quarter(points_a: np.array, points_b: np.array) -> int:
        """
        Args:
            points_a (np.array[]): center point *np.array<=> (x,y)
            points_b (np.array[]): second point *np.array<=> (x,y)

        Returns:
            int: number of quarter (1,2,3 or 4)
        """
        # if point b is at right to a point (center)
        if points_a[0] < points_b[0]:
            # if b is above a
            if points_a[1] < points_b[1]:
                return 1
            # if b is below a
            return 4
        else:
            # if b is above a
            if points_a[1] < points_b[1]:
                return 2
            # if b is below a
            return 3


if __name__ == '__main__':
    Gestures.hand_pos_ang_by_vec(pa=(2, 4), pb=(3, 4))
