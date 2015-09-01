__author__ = 'dipap'

import json
import sys
import os

class Configuration:
    """
    The Configuration class contains the parsed info of the test_config.json file
    """
    def __init__(self):
        if True: #  'test' in sys.argv:
            self.data = json.loads(open(os.path.join('config', 'test_config.json')).read())
        else:
            self.data = json.loads(open(os.path.join('config', 'config.json')).read())

configuration = Configuration()



