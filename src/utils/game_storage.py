import json

from src.game_engines.game_brief import GameBrief

_GAME_BRIEF_FILE = "game_brief.storage"

class GameBriefStorage:

    def __init__(self):
        self._file = None
        self.game_brief = GameBrief()

    def file_open(self):
        self._file = open(_GAME_BRIEF_FILE, "w+")

    def load_brief(self):
        if self._file is None or self._file.closed:
            self.file_open()
        content = self._file.read()
        if content.strip() == "":
            content = "{}"
        brief_data:dict = json.loads(content)
        self.game_brief.global_points = brief_data.get('global_points',0)
        self.game_brief.global_points = brief_data.get('tries',0)
        self._file.close()

    def save_brief(self):
        if self._file is None or self._file.closed:
            self.file_open()

        brief_data = {
            "global_points": self.game_brief.global_points,
            "tries": self.game_brief.tries
        }
        data_dump = json.dumps(brief_data)
        self._file.write(data_dump)
        self._file.close()

    def close(self):
        self._file.close()
