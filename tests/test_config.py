import os
import logging

from config import setup_logger


def test_setup_logger_creates_log_file(tmp_path, monkeypatch):
    import config as cfg

    # redirige le log file vers un dossier temporaire
    monkeypatch.setattr(cfg, "LOG_DIR", str(tmp_path))
    os.makedirs(cfg.LOG_DIR, exist_ok=True)
    monkeypatch.setattr(cfg, "LOG_FILE", os.path.join(cfg.LOG_DIR, "app.log"))

    logger = setup_logger("test_logger")

    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.DEBUG

    # log
    logger.info("test log message")


    for h in logger.handlers:
        try:
            h.flush()
        except Exception:
            pass

    # le fichier doit exister 
    assert os.path.exists(cfg.LOG_FILE)
