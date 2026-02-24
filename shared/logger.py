import logging
import sys


def get_logger(name: str, level: str = "INFO"):
    logger = logging.getLogger(name)

    # מונע כפילויות אם הלוגר כבר קיים
    if not logger.handlers:
        logger.setLevel(level)

        # הגדרת פורמט: זמן | שם השירות | רמה | הודעה
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )

        # יציאה למסך (Console)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
