import random
from kmk.keys import AX, make_key
from kmk.modules import Module
from kmk.scheduler import cancel_task, create_task

class MouseJiggler(Module):
    def __init__(self, interval=100, distance=10):
        self.distance = distance
        self.interval = interval
        self._jiggle = False
        make_key(
            names=("TG_JIGGLER",),
            on_press=self.toggle,
        )

    def during_bootup(self, keyboard):
        self._task = create_task(
            lambda: self._move(keyboard),
            period_ms=self.interval,
        )
        cancel_task(self._task)
        self._jiggle = False

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def toggle(self, *args, **kwargs):
        if self._jiggle:
            cancel_task(self._task)
            print("jiggle cancelled")
            self._jiggle = False
        else:
            self._task.restart()
            print("jiggle started")
            self._jiggle = True

    def _move(self, keyboard):
        AX.X.move(keyboard, random.choice([-1, 1]) * self.distance)
        AX.Y.move(keyboard, random.choice([-1, 1]) * self.distance)
