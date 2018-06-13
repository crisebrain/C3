import logging

class CreateLogger(object):
    def __init__(self, i):
        self.create_logger(i)

    def create_logger(self, i):
        i = str(i)
        pathfile = '/var/log/C3/{0}.log'.format(i)
        logger = logging.getLogger(i)
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
