
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, base_dir, filename, when="midnight", interval=1, backupCount=7,*args, **kwargs):
        self.base_dir = Path(base_dir)
        self.filename = filename
        super().__init__(self.base_dir / filename, when, interval, backupCount, *args, **kwargs)

    def _rotate_file(self, source, dest):
        dest.parent.mkdir(parents=True, exist_ok=True)  # Ensure folder exists
        source.rename(dest)

    def doRollover(self):
        date_folder = datetime.now().strftime("%d-%m-%Y")
        new_log_folder = self.base_dir / f"{date_folder}_Logs"
        new_log_file = new_log_folder / f"debug_{date_folder}.log"
        if self.stream:
            self.stream.close()
            self.stream = None
        self._rotate_file(Path(self.baseFilename), new_log_file)

        # Ensure old logs are rotated properly
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                Path(s).unlink(missing_ok=True)

        self.mode = 'a'
        self.stream = self._open()
