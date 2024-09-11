import pickle

from app.model.calendar import Calendar


class PersistenceService:
    def __init__(self, file_path: str):
        self.file_path: str = file_path

    def save(self, calendar: Calendar):
        with open(self.file_path, mode="wb") as file:
            pickle.dump(calendar, file)

    def load(self) -> Calendar:
        with (open(self.file_path, mode="rb") as file):
            try:
                calendar = pickle.load(file)
            except EOFError:
                calendar = Calendar()
        return calendar
