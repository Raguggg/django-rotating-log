from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path
import time


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        base_dir,
        filename,
        when="midnight",
        interval=1,
        backupCount=7,
        *args,
        **kwargs,
    ):
        self.base_dir = Path(base_dir)
        self.filename = filename
        super().__init__(
            self.base_dir / filename, when, interval, backupCount, *args, **kwargs
        )

    def _rotate_file(self, source, dest):
        dest.parent.mkdir(parents=True, exist_ok=True)  # Ensure folder exists
        source.rename(dest)

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        date_folder = (datetime.now() - timedelta(1)).strftime("%d-%m-%Y")

        new_log_folder = self.base_dir / date_folder

        new_log_folder.mkdir(parents=True, exist_ok=True)
        new_log_file = new_log_folder / "debug.log"

        dfn = self.rotation_filename(str(new_log_file))
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:
            self.delete_old_folders()
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == "MIDNIGHT" or self.when.startswith("W")) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if (
                    not dstNow
                ):  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def delete_old_folders(self):
        """
        Deletes folders in base_dir that are older than retention_days.

        Args:
            base_dir (Path): The base directory containing date-based folders.
            retention_days (int): Number of days to keep folders.
        """
        today = datetime.now()
        cutoff_date = today - timedelta(days=self.backupCount)

        # Iterate through all items in base_dir
        for folder in self.base_dir.iterdir():
            if folder.is_dir():  # Check if it's a folder
                try:
                    # Attempt to parse the folder name as a date in the format %d-%m-%Y
                    folder_date = datetime.strptime(folder.name, "%d-%m-%Y")
                    # Check if the folder date is older than the cutoff date
                    if folder_date < cutoff_date:
                        print(f"Deleting folder: {folder}")
                        # Recursively delete files and subfolders within the folder
                        self.delete_folder_recursively(folder)
                        folder.rmdir()  # Remove the folder itself
                except ValueError:
                    # Folder name doesn't match the expected date format
                    print(f"Skipping non-date folder: {folder}")

    def delete_folder_recursively(self, folder: Path):
        """
        Recursively deletes all files and subfolders in a folder.

        Args:
            folder (Path): The folder to delete.
        """
        # Iterate through the folder's contents
        for item in folder.iterdir():
            if item.is_dir():
                # Recursively delete subdirectories
                self.delete_folder_recursively(item)
            else:
                # Delete files
                item.unlink()
        folder.rmdir()  # Remove the folder itself after its contents are deleted
