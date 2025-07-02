import random
from kmk.keys import AX, make_key
from kmk.modules import Module
from kmk.scheduler import cancel_task, create_task
from kmk.extensions.display import TextEntry


class MouseJiggler(Module):
    def __init__(self, interval=100, distance=10):
        self.distance = distance
        self.interval = interval
        self._jiggle = False
        self._prev_jiggle = False
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
        if self._jiggle != self._prev_jiggle:
            self._prev_jiggle = self._jiggle
            if self._jiggle:
                keyboard.extensions[0].entries.append(
                    TextEntry(text="*", x=0, y=32, y_anchor="B")
                )
            else:
                keyboard.extensions[0].entries.pop()
            keyboard.extensions[0].render()

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
