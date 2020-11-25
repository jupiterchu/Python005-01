import logging
import os
from datetime import datetime
from pathlib import Path

def log_test():
    now = datetime.strftime(datetime.today(), '%Y-%m-%d')
    filename = f'var/log/python-{now}'
    if not Path(filename).exists():
        os.mkdir(filename)

    logging.basicConfig(filename=filename+'/test.log',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(name)-8s %(levelname)-8s [line: %(lineno)d] %(message)s')

    logging.info("func log_test running")

if __name__ == '__main__':
    log_test()
