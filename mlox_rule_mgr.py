# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 17:45:55 2021

@author: Morrowind
"""

import argparse, glob, logging, os, re, string, sys

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


def get_safe_filename(name):
    """
    Converts a name to a safe filename.

    Parameters
    ----------
    name : string
        name to convert to safe filename.

    Returns
    -------
    filename : string
        safe filename.

    """
    safechars = string.ascii_lowercase + string.ascii_uppercase + string.digits + '.-'
    filename = ''.join([c for c in name if c in safechars])
    return filename


class MloxRuleManager(object):
    def __init__(self, args):
        """
        MLOX rule-management commands

        Parameters
        ----------
        args : ArgumentParser.Namespace
            rule-management command-line arguments.

        """
        self.args = args

    def merge(self):
        """
        usage: merge [-h] basefile rulefiles [rulefiles ...]
        
        positional arguments:
          basefile    target file to merge subsequent mlox rule files into
          rulefiles   rule files to merge

        Returns
        -------
        None.

        """
        basefile_name = self.args.basefile
        rulefile_names = self.args.rulefiles
        logger.debug(f"basefile: {basefile_name}, rulefiles: {rulefile_names}")

        sorted_rulefile_names = list()
        for rulefile_name in rulefile_names:
            sorted_rulefile_names.extend(glob.glob(rulefile_name))
        sorted_rulefile_names.sort(key = str.lower)
        
        with open(basefile_name, "w", encoding="utf-8") as out_f:
            for rulefile_name in sorted_rulefile_names:
                logger.info(f"reading rulefile '{rulefile_name}'")
                with open(rulefile_name, "r", encoding="utf-8") as in_f:
                    lines = in_f.readlines()
                    text = "".join(lines)
                    out_f.write(text.strip())
                    out_f.write(os.linesep)
    
    def split(self):
        """
        usage: split [-h] [-d DIRECTORY] rulefile

        positional arguments:
          rulefile              rule file to split
        
        optional arguments:
          -h, --help            show this help message and exit
          -d DIRECTORY, --directory DIRECTORY
                                output directory

        Returns
        -------
        None.

        """
        rulefile_name = os.path.realpath(self.args.rulefile)
        directory = self.args.directory
        if directory is None:
            directory = os.path.dirname(os.path.realpath(rulefile_name))
        if not os.path.exists(directory):
            logger.warn(f"specified output directory '{directory}' does not exist")
            return
        
        logger.debug(f"rulefile: {rulefile_name}")

        self.comment_regex = re.compile(r"\s*;+\s*")
        self.sectionname_regex = re.compile(r"\s*;+\s*@(.*)")

        # Try to read rulefile.
        with open(rulefile_name, "r", encoding="utf-8") as in_f:
            # TODO: Instead of collecting sections into dictionary, save to disk.
            sections = dict()

            # Create first "header" section.
            sectionname = "_header"
            section = list()
            comments = list()

            for line_num, line in enumerate(in_f.readlines()):
                sectionname_match = self.sectionname_regex.match(line)
                comment_match = self.comment_regex.match(line)
                if sectionname_match:
                    #logger.debug(f"{line_num}: {sectionname_match}")
                    #logger.debug(sectionname_match.groups())
                    # Save existing section.
                    sections[sectionname] = section
                    # TODO: Instead of collecting sections into dictionary,
                    # save to disk at this point.
                    # Create new section.
                    sectionname = get_safe_filename(sectionname_match.group(1))
                    # Add existing comment lines to start of section.
                    section = comments
                    comments = list()
                    # Add section name to start of section.
                    section.append(line)
                elif comment_match:
                    #logger.debug(f"{line_num}: {comment_match}")
                    # Collect comment line, but don't add to section yet.
                    comments.append(line)
                else:
                    # Add any comment lines to current section.
                    section.extend(comments)
                    comments = list()
                    # Add current line to section.
                    section.append(line)

            # Save final section.
            if comments:
                section.extend(comments)
            sections[sectionname] = section
                
            logger.debug(f"output directory: {directory}")
            for name, section in sections.items():
                logger.info(f"saving section '{name}'")
                sectionfile_name = os.path.join(directory, f"{name}.txt")
                with open(sectionfile_name, "w", encoding="utf-8") as out_f:
                    out_f.writelines(section)
                

    
    def run(self):
        """
        Runs commands specified in args to MloxRuleManager(args).

        Returns
        -------
        None.

        """
        logger.debug(f"args: {self.args}")
        command = self.args.command
        if hasattr(self, command):
            getattr(self, command)()
        else:
            logger.info("I don't have that command")


def parse_args():
    """
    Setup command-line argument parsing.

    Returns
    -------
    args :  ArgumentParser.Namespace
            rule-management command-line arguments.

    """
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
    """
    Run MloxRuleManager(args) with parsed command-line args.

    Returns
    -------
    None.

    """
    args = parse_args()
    mlox_rule_mgr = MloxRuleManager(args)
    mlox_rule_mgr.run()


if __name__ == "__main__":
    sys.exit(main())