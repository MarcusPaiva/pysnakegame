class GameBrief:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameBrief, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._global_points = 0
        self._tries = 0

    @classmethod
    def reset_instance(cls):
        cls._instance = None

    def add_global_points(self, value:int):
        """
        Increment global player points.
        :param value: Value to increment.
        """
        self._global_points += value

    @property
    def global_points(self) -> int:
        """
        Retrieve global points.
        :return: Number as global points.
        """
        return self._global_points

    @global_points.setter
    def global_points(self, value:int):
        """
        Global points setter.
        :param value: Global value to set.
        """
        self._global_points = value

    def increment_tries(self,):
        """
        Increment player tries.
        """
        self._tries += 1

    @property
    def tries(self) -> int:
        """
        Retrieve player tries.
        :return: Number as player tries.
        """
        return self._tries

    @tries.setter
    def tries(self, value: int):
        """
        player tries setter.
        :param value: Player tries value to set.
        """
        self._tries = value