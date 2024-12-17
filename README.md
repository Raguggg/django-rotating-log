# Django Rotating Logs 🔄📜

This project was born out of frustration with `TimedRotatingFileHandler`, as it didn’t quite create logs the way I needed. So, I decided to create a custom `CustomTimedRotatingFileHandler` logger with my own format. Let's dive in!

---

### Installation 🛠️

1. **Copy the `logger_config.py` file** from the `LogTest` directory into your project.
2. **Add the following logging configuration** to your Django settings file.

---

### Example Output 📂

The folder structure will look something like this:

```
Project_DIR
|
|_ DEBUG_LOGS
    |
    ├── Today_Logs
    │   └── debug_Today_Logs.log
    └── dd-mm-yyyy
        └── debug.log
```

---

### Steps to Setup 🔧

#### 1. **Copy the File** 📄

Simply copy the `logger_config.py` file to your project’s `LogTest` directory.

#### 2. **Create the `LOGGING` variable** 📝

Add this configuration to your settings file to set up logging.

```python
def get_log_file_path():
    file_path = BASE_DIR / "DEBUG_LOGS" / "Today_Logs"
    file_path.mkdir(parents=True, exist_ok=True)
    
    # Create .gitignore file to prevent logs from being committed
    gitignore = """
    # Automatically created by CustomTimedRotatingFileHandler.
    *
    """
    with open(BASE_DIR / "DEBUG_LOGS" / ".gitignore", "w") as f:
        f.write(gitignore)
        
    # Define the path for today's log file
    APP_LOG_FILENAME = file_path / "debug_Today_Logs.log"
    return APP_LOG_FILENAME
```

This function will create the log folder and file for today’s logs.

#### 3. **Add the Logging Configuration** 📋

Now, configure your logging by adding the following to the `LOGGING` dictionary in your Django settings:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(asctime)-8s %(name)-8s %(levelname)-8s %(message)s"},
        "file": {"format": "%(asctime)-8s %(levelname)-8s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        
        "timed_rotating_file": {
            "level": "INFO",
            "class": "LogTest.logger_config.CustomTimedRotatingFileHandler",  # Update this based on your project
            "formatter": "file",
            "base_dir": BASE_DIR / "DEBUG_LOGS",
            "filename": get_log_file_path(),
            "when": "midnight",  # Rotate every midnight
            "interval": 1,  # Every day
            "backupCount": 7,  # Keep the last 7 days of logs, set to 0 to avoid auto-deletion
            "encoding": "utf-8",
            "utc": False,  # Use local time for rotation
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": [
                "console",
                "timed_rotating_file",
            ],
        },
    },
}
```

#### 4. **Configure the `CustomTimedRotatingFileHandler`** 🔧

The handler configuration should point to:

- **Class**: `LogTest.logger_config.CustomTimedRotatingFileHandler`
- **Base Directory**: `BASE_DIR / "DEBUG_LOGS"`
- **Filename**: `get_log_file_path()`
- **Backup Count**: Set it to `0` if you don’t want to delete logs automatically (set a higher number for auto-deletion).

---

### Key Parameters 📑

- **`class`**: Path to the custom log handler class (update to reflect your project).
- **`base_dir`**: Directory where logs will be stored (e.g., `BASE_DIR / "DEBUG_LOGS"`).
- **`filename`**: Use the function `get_log_file_path()` to determine the file name for today’s logs.
- **`when`**: Rotation period (set to `"midnight"` for daily rotation).
- **`interval`**: Number of days between rotations (set to `1` for daily).
- **`backupCount`**: The number of backups to keep (set to `0` to disable auto-deletion).
- **`utc`**: Use local time for rotation (`False` for local time).

---

### Summary 📝

1. **Copy the config file** to your project.
2. **Create the `LOGGING` variable** in your settings.
3. **Configure the `CustomTimedRotatingFileHandler`** as described.

Now, your logs will rotate daily, and you will have a clean, organized log structure for your project. 📅
