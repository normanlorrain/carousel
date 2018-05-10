# Central module for configuration, with command-line and json too.

import argparse
import datetime
import json
import os
import sys
from os.path import dirname, join, realpath

# put our configuration values in this module object, so other modules can see them just by importing.

thismodule = sys.modules[__name__]

class _Config:

    def __init__(self):
        # print('configuration initializing')
        parser = argparse.ArgumentParser(
            description='Carousel'
        )
        # parser.add_argument("root", help="root of document project")
        parser.add_argument("-l", "--log", dest="logLevel", 
                            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                            default='DEBUG',
                            help="Set the logging level")
        args = parser.parse_args()
        # print(f"arguments: {args}")
        setattr(thismodule, 'logLevel', args.logLevel )


    # def loadConfiguration(self):
    #     configName = os.path.join(self.root, "configuration.json")

    #     with open(configName) as json_data:
    #         for key, value in json.load(json_data).items():
    #             setattr(self, key, value)

config = _Config()
