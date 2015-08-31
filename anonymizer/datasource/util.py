__author__ = 'dipap'

import json
import sys


class Configuration:
    """
    The Configuration class contains the parsed info of the test_config.json file
    """
    def __init__(self):
        if 'test' in sys.argv:
            self.data = json.loads(open('config\\test_config.json').read())
        else:
            self.data = json.loads(open('config\\config.json').read())

configuration = Configuration()



