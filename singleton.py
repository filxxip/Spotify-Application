class Singleton(type):
    instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self.instances:
            instance = type.__call__(self, *args, **kwargs)
            self.instances[self] = instance
        return self.instances[self]
