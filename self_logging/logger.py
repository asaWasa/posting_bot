import logging
import inspect
import os


class Log:
    def __init__(self,
                 logger_name,
                 program_path,
                 file_name,
                 level="INFO"):
        """
        уровень логгирования:
        # DEBUG
        # INFO
        # WARNING
        # ERROR
        # CRITICAL
        """
        self.level = logging.INFO
        self.program_path = program_path
        self.logger_name = logger_name
        self.file_name = file_name
        self.formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.__set_level(level)
        self.file_path = self.__search_path_to_logs()
        self.logger = self.__create_logger()

    def __set_level(self, level):
        if level == 'INFO':
            self.level = logging.INFO
        elif level == 'DEBUG':
            self.level = logging.DEBUG
        elif level == 'WARNING':
            self.level = logging.WARNING
        elif level == 'ERROR':
            self.level = logging.ERROR
        elif level == 'CRITICAL':
            self.level = logging.CRITICAL
        else:
            self.level = logging.INFO

    def __create_logger(self):
        # инициализация
        logger = logging.getLogger(self.logger_name)

        if not logger.handlers:
            logger.setLevel(self.level)

            ch = logging.StreamHandler()
            ch.setLevel(self.level)
            ch.setFormatter(self.formatter)

            fh = logging.FileHandler(self.file_path)
            fh.setLevel(self.level)

            fh.setFormatter(self.formatter)

            logger.addHandler(fh)
            logger.addHandler(ch)

        return logger

    def __search_path_to_logs(self):
        try:
            path = os.path.realpath(self.program_path)
            try:
                while not os.path.exists(path + '/README.md'):
                    path = os.path.dirname(path)
            except:
                path = self.program_path

            try:
                os.mkdir(path + '/logs')
            except:
                pass

            return path + '/logs/' + self.file_name + '.log'
        except:
            return self.program_path + self.file_name + '.log'

    def info(self, message, position='unknown'):
        """Automatically log the current function details."""
        func = inspect.currentframe().f_back.f_code
        self.logger.info("[INFO: %s] - [%s:%s] in [%s:%i]" % (message,
                                                              func.co_name,
                                                              position,
                                                              func.co_filename,
                                                              func.co_firstlineno
                                                              )
                         )

    def debug(self, message, position='unknown'):
        """Automatically log the current function details."""
        func = inspect.currentframe().f_back.f_code
        self.logger.debug("[DEBUG: %s] - [%s:%s] in [%s:%i]" % (message,
                                                                func.co_name,
                                                                position,
                                                                func.co_filename,
                                                                func.co_firstlineno)
                          )

    def error(self, message, position='unknown'):
        """Automatically log the current function details."""
        func = inspect.currentframe().f_back.f_code
        self.logger.error("[ERROR: %s] - [%s:%s] in [%s:%i]" % (message,
                                                                func.co_name,
                                                                position,
                                                                func.co_filename,
                                                                func.co_firstlineno
                                                                )
                          )
