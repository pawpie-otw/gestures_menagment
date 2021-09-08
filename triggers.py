from typing import List


def hand_angle_less_then(cond_angle: float, cur_angle: float) -> bool:
    if cur_angle < cond_angle:
        return True
    return False


def hand_angle_higher_then(cond_angle: float, cur_angle: float) -> bool:
    if cur_angle > cond_angle:
        return True
    return False


def hand_angle_between(left_cond_angle: float, right_cond_angle: float, cur_angle: float) -> bool:
    if left_cond_angle < cur_angle and cur_angle < right_cond_angle:
        return True
    return False


def straightened_fingers(cond_fingers: List[bool], curr_fingers: List[bool]) -> bool:
    if cond_fingers == curr_fingers:
        return True
    return False
