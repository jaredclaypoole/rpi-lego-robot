from typing import Optional, Callable

import brickpi3


def sgn(x) -> int:
    return +1 if x >= 0 else -1


class LegoMotors:
    def __init__(self, speed: int = 16):
        self._speed = speed
        self.print = print

        self.BP = brickpi3.BrickPi3()

        self.LEFT = self.BP.PORT_B
        self.RIGHT = self.BP.PORT_C

        self.action = self.stop
        self.default_redo_action_on_speed_change = False
        self._max_speed = 100

    @property
    def speed(self) -> int:
        return self._speed
    
    @speed.setter
    def speed(self, value: int) -> None:
        self._speed = max(min(value, self.max_speed), 1)
    
    @property
    def max_speed(self) -> int:
        return self._max_speed
    
    @max_speed.setter
    def max_speed(self, value: int) -> None:
        self._max_speed = int(min(value, 100))
    
    def double_speed(self, *args, redo_action: Optional[bool] = None) -> None:
        speed = self.speed
        speed *= 2
        if speed > self.max_speed:
            speed = self.max_speed
        self.speed = speed
        self.print(f"Increased speed to {speed}")

        if redo_action is None:
            redo_action = self.default_redo_action_on_speed_change
        if redo_action:
            print("Redoing action")
            self.action()

    def halve_speed(self, *args, redo_action: Optional[bool] = None) -> None:
        speed = self.speed
        speed //= 2
        if speed == 50:
            speed = 64
        self.speed = speed
        self.print(f"Decreased speed to {speed}")

        if redo_action is None:
            redo_action = self.default_redo_action_on_speed_change
        if redo_action:
            print("Redoing action")
            self.action()

    def set_dual_motor_power(self, left_fraction: Optional[float] = None, right_fraction: Optional[float] = None) -> None:
        self.action = self.make_dual_action(left_fraction, right_fraction)
        self.action()
    
    def stop(self, *args) -> None:
        self.set_dual_motor_power(0)

    def forward(self, *args) -> None:
        self.set_dual_motor_power()

    def backward(self, *args) -> None:
        self.set_dual_motor_power(-1)
    
    def left(self, *args) -> None:
        self.set_dual_motor_power(1, -1)

    def right(self, *args) -> None:
        self.set_dual_motor_power(-1, 1)
    
    def make_dual_action(self, left_fraction: Optional[float] = None, right_fraction: Optional[float] = None) -> Callable[[], None]:
        if left_fraction is None:
            left_fraction = 1
        if right_fraction is None:
            right_fraction = left_fraction

        def inner(*args):
            left_speed = int(left_fraction * self.speed)
            right_speed = int(right_fraction * self.speed)

            if left_speed == right_speed:
                self.BP.set_motor_power(self.LEFT + self.RIGHT, left_speed)
            else:
                self.BP.set_motor_power(self.LEFT, left_speed)
                self.BP.set_motor_power(self.RIGHT, right_speed)
        return inner
    
    def __del__(self):
        self.print("Resetting BrickPi controller")
        self.BP.reset_all()
        self.print("Done")
