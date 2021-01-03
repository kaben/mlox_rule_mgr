# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 17:45:55 2021

@author: Morrowind
"""

import argparse, logging, sys

# Create logger named after this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not logger.hasHandlers():
    # Create logging handler for console output
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # Create formatter to display time
    formatter = logging.Formatter('%(name)s:%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class MloxRuleManager(object):
    def __init__(self, args):
        self.args = args
        
    def merge(self):
        basefile = self.args.basefile
        rulefiles = self.args.rulefiles
        logger.debug(f"basefile: {basefile}, rulefiles: {rulefiles}")
    
    def split(self):
        rulefile = self.args.rulefile
        logger.debug(f"rulefile: {rulefile}")
    
    def run(self):
        logger.debug(f"args: {self.args}")
        command = self.args.command
        if hasattr(self, command):
            getattr(self, command)()
        else:
            logger.info("I don't have that command")


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = "command")
    
    merge_cmd = subparsers.add_parser("merge", help = "merge mlox rule files")
    merge_cmd.add_argument("basefile", help = "target file to merge subsequent mlox rule files into")
    merge_cmd.add_argument("rulefiles", nargs = "+", help = "rule files to merge")
    
    split_cmd = subparsers.add_parser("split", help = "split an mlox rule file")
    split_cmd.add_argument("rulefile", help = "rule file to split")
    split_cmd.add_argument("-d", "--directory", help = "output directory")
    
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    mlox_rule_mgr = MloxRuleManager(args)
    mlox_rule_mgr.run()


if __name__ == "__main__":
    sys.exit(main())