from PyQt5.QtCore import QTimer


def blocked_button(value, time):
    def blocked_button2(func):
        def decor(*args, **kwargs):
            self = args[0]
            s = self
            name = value.split(".")
            self = getattr(self, name.pop(0))
            while name:
                self = getattr(self, name.pop(0))

            self.disconnect()
            result = func(*args, **kwargs)
            QTimer.singleShot(
                1000 * time,
                lambda: self.clicked.connect(
                    lambda: getattr(s, func.__name__)(*args[1:], **kwargs)
                ),
            )
            return result

        return decor

    return blocked_button2
