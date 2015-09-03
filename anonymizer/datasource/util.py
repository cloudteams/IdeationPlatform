__author__ = 'dipap'

import json
import sys
import os


class Configuration:
    """
    The Configuration class contains the parsed info of the test_config.json file
    """
    def __init__(self, from_file='', from_str=''):
        if from_file:
            from_str = open(from_file).read()
        self.data = json.loads(from_str)

    def get_connection_info(self):
        return self.data['sites'][0]['connections']




