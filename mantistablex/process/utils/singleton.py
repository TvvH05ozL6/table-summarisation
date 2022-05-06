class Singleton(type):
    """
    Utility class that implement the Singleton pattern.
    Use with care
    """
    _objects = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._objects:
            cls._objects[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._objects[cls]