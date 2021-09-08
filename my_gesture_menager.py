from typing import List, Callable, Any
from dataclasses import dataclass


@dataclass
class OneTimeAction:
    """Dataclasses to storage informaction about functions like run a program
    that you want to use single time
    """
    action: Callable[[], Any]
    trigger: Callable[[], bool]
    refresh_trigger: Callable[[], bool]
    ready_to_use: bool = True


@dataclass
class ContinuousAction:
    """Dataclass with information about continuous actions like change volume
    """
    action: Callable[[], Any]
    trigger: Callable[[], bool]


class GestureMenager:
    """work on this feature is ongoing...

    my class to simple gestures menagment that allow you to add
    You gesture and linking an action to it
    """

    def __init__(self, break_key: str[1]) -> None:
        self.break_key = break_key
        self.actions: List[OneTimeAction] = []
        self.continuous_actions: List[ContinuousAction] = []

    def add_one_time_action(self, action: Callable[[], Any], trigger: Callable[[], bool], refresh_trigger: Callable[[], bool]) -> None:
        """Append new action with trigger and refresher to trigger
        This type of action required refresh after use

        Args:
            action (Callable[[],Any]): action to do if trigger and ready to use
            trigger (Callable[[],bool]): trigger to run action
            refresh_trigger (Callable[[],bool]): refresh the action, call this function allow to use the action again
        """
        self.actions.append(
            OneTimeAction(action, trigger, refresh_trigger))

    def add_continuos_action(self, action: Callable[[], Any], trigger: Callable[[], bool]) -> None:
        """Append new action with trigger

        Args:
            action (Callable[[],Any])): task to do
            trigger (Callable[[],bool]): trigger (if True then do)
        """
        self.continuous_actions.append(
            ContinuousAction(action, trigger))

    def run(self) -> None:
        while True:
            for action in self.actions:
                if action.trigger:
                    action.action()
            for action in self.continuous_actions:
                if action.trigger and action.ready_to_use:
                    action.action()
                    action.ready_to_use = False
                else:
                    if action.refresh_trigger:
                        action.ready_to_use = True
            if 0xFF == ord(self.break_key):
                break
