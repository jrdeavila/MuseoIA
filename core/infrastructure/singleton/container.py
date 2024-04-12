class SingletonContainer:
    _dependencies = {}

    @classmethod
    def register(cls, name, dependency):
        cls._dependencies[name] = dependency

    @classmethod
    def resolve(cls, name):
        if name not in cls._dependencies:
            raise ValueError(f"Dependency '{name}' not found in container")
        return cls._dependencies[name]

    @classmethod
    def close_all(cls):
        for key in cls._dependencies:
            del cls._dependencies[key]
        cls._dependencies.clear()

    @classmethod
    def close(cls, name):
        if name not in cls._dependencies:
            raise ValueError(f"Dependency '{name}' not found in container")
        del cls._dependencies[name]
        cls._dependencies.pop(name, None)
