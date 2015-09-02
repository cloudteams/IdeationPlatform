__author__ = 'dipap'

import json
import sys
import os


class Configuration:
    """
    The Configuration class contains the parsed info of the test_config.json file
    """
    def __init__(self, filename):
        self.data = json.loads(open(filename).read())

    def get_connection_info(self):
        return self.data['sites'][0]['connections']




