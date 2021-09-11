from dataclasses import dataclass, field
from typing import Optional
import numpy as np


@dataclass
class Point:
    """simple point dataclass which allow to
    get data as np.array and as dataclass (if u want use .x/.y)
    """
    x: float
    y: float

    def __iter__(self) -> np.array:
        """Return just a np array [x,y]
        """
        return np.array([self.x, self.y])

    def __getitem__(self, index) -> 'np.array[4,2]':
        """ Something like iter but you can use slice
        """
        return self.__iter__()[index]


@dataclass
class Finger:
    """Dataclass that represent 4 landmarks of finger
    It was build to help in menage a landmarks generated from mediapipe in comparison etc.
    """
    lms: np.array
    __current: int = field(default=-1, init=False)

    def __iter__(self) -> np.array:
        return self

    def __next__(self):
        self.__current += 1
        if self.__current < len(self.lms):
            return self.lms[self.__current]
        self.__current = -1
        raise StopIteration

    def __getitem__(self, index_x: slice, index_y: Optional[slice] = None
                    ) -> np.array:
        if index_y:
            self.lms[index_x, index_y]
        return self.lms[index_x]


@dataclass
class HandLms:
    """Dataclass that contains 21 landmarks (5 fingers and wrist)
    It was build to help in menage a landmarks generated from mediapipe in comparison etc.
    """
    wrist: Point
    thumb_fin: np.array
    index_fin: np.array
    middle_fin: np.array
    ring_fin: np.array
    little_fin: np.array
    __current: int = field(default=-1, init=False)

    def __iter__(self) -> np.array:
        return self

    def __next__(self):
        self.__current += 1
        if self.__current < len(self.__to_chain()):
            return self.__to_chain()[self.current]
        self.__current = -1
        raise StopIteration

    def __getitem__(self, index_x: slice, index_y: Optional[slice] = None):
        if index_y:
            return self.__to_chain()[index_x, index_y]
        return self.__to_chain()[index_x]

    def __to_chain(self):
        return np.array([self.wrist, *self.thumb_fin, *self.index_fin,
                        *self.middle_fin, *self.ring_fin, *self.little_fin])
