import logging
import os
import sys
from pathlib import Path

class CreateLogger(object):
    def __init__(self, namef):
        self.create_logger(namef)

    def create_logger(self, namef):
        # /home/user/.../current_proyect_name/C3
        # Crea folder segun rama del proyecto
        folder = ""
        if sys.platform == "linux":
            #folder = os.path.join("/var/log/C3", current_proyect_name)
            folder = "/var/log/C3"/Path(os.getcwd().split("/")[-2])
        elif sys.platform == "win32":
            folder = "d:\\" / Path(os.getcwd().split("\\")[-1])
        if not os.path.exists(folder):
            os.mkdir(folder)
        pathfile = os.path.join(folder, '{0}.log'.format(namef))
        logger = logging.getLogger(namef)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr = logging.FileHandler(pathfile)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def __del__(self):
        if self.logger:
            for hdlr in self.logger.handlers:
                self.logger.removeHandler(hdlr)
                hdlr.flush()
                hdlr.close()

if __name__ == "__main__":
    errors = CreateLogger("errors")
    errors.logger.exception(KeyError)

    infos = CreateLogger("querys")
    infos.logger.info("Pacto")
