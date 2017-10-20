from __future__ import absolute_import
from __future__ import print_function
import argparse

import os

import sys
import yaml

from aetros import api
from aetros.utils import read_home_config


class InitCommand:
    def __init__(self, logger):
        self.logger = logger
        self.client = None
        self.registered = False
        self.active = True

    def main(self, args):
        import aetros.const

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
            prog=aetros.const.__prog__ + ' run')
        parser.add_argument('name', nargs='?', help="Model/project name")

        home_config = read_home_config()
        parsed_args = parser.parse_args(args)

        if os.path.exists('.aetros.yml'):
            config = yaml.load(open('.aetros.yml', 'r'))
            if isinstance(config, dict) and 'model' in config:
                print("failed: .aetros.yml already exists with a linked model to " + config['model'])
                sys.exit(1)

        name = api.create_model(parsed_args.name or (os.path.basename(os.getcwd())))

        with open('.aetros.yml', 'w') as f:
            f.write('model: ' + name)

        print(".aetros.yml created linked with model " + name + ' in ' + os.getcwd())
        print("Open AETROS Trainer to see the model at https://" + home_config['host'] + '/model/' + name)