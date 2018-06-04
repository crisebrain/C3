import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

if __name__ == "__main__":
    logerrors = setup_logger("errors", "errors.log")
    logerrors.error("ZeroDivisionError")

    logquerys = setup_logger("querys", "querys.log")
    logquerys.error("KeyError")
