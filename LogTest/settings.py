from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = "django-insecure-g_lfml)j1wdnr(-znn!=hy_76((mf!wdbnsg&5upll+bnxb7nf"


DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "LogTest.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LogTest.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =================== LOGGING  CustomTimedRotatingFileHandler =================== #
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


# Define the log rotation and file handling configuration
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

# =================== LOGGING  CustomTimedRotatingFileHandler END =================== #