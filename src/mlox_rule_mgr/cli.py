# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 18:18:51 2021

@author: Kaben Nanlohy <kaben.nanlohy@gmail.com>
"""

import argparse
import glob
import logging
import os
import re
import string
import sys

from mlox_rule_mgr import __version__

__author__ = "Kaben Nanlohy"
__copyright__ = "Kaben Nanlohy"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


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


def coalesce_lines(lines):
    text = "".join(lines)
    return text.strip()



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
        usage: merge [-h] base_mlox_file mlox_files [mlox_files ...]
        
        positional arguments:
          base_mlox_file    target file to merge subsequent mlox rule files into
          mlox_files   rule files to merge

        Returns
        -------
        None.

        """
        basefile_name = self.args.base_mlox_file
        rulefile_names = self.args.mlox_files
        _logger.debug(f"base_mlox_file: {basefile_name}, mlox_files: {rulefile_names}")

        sorted_rulefile_names = list()
        for rulefile_name in rulefile_names:
            sorted_rulefile_names.extend(glob.glob(rulefile_name))
        sorted_rulefile_names.sort(key = str.lower)
        
        with open(basefile_name, "w", encoding="utf-8") as out_f:
            for rulefile_name in sorted_rulefile_names:
                _logger.info(f"reading rulefile '{rulefile_name}'")
                with open(rulefile_name, "r", encoding="utf-8") as in_f:
                    lines = in_f.readlines()
                    out_f.write(coalesce_lines(lines))
                    out_f.write(os.linesep)
    
    def split(self):
        """
        usage: split [-h] [-d DIRECTORY] mlox_file

        positional arguments:
          mlox_file              rule file to split
        
        optional arguments:
          -h, --help            show this help message and exit
          -d DIRECTORY, --directory DIRECTORY
                                output directory

        Returns
        -------
        None.

        """
        rulefile_name = os.path.realpath(self.args.mlox_file)
        directory = self.args.directory
        if directory is None:
            directory = os.path.dirname(os.path.realpath(rulefile_name))
        if not os.path.exists(directory):
            _logger.warn(f"specified output directory '{directory}' does not exist")
            return
        
        _logger.debug(f"rulefile: {rulefile_name}")

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
                    #sections[sectionname] = section              
                    section_versions = sections.get(sectionname, list())
                    section_versions.append(section)
                    sections[sectionname] = section_versions
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
            #sections[sectionname] = section              
            section_versions = sections.get(sectionname, list())
            section_versions.append(section)
            sections[sectionname] = section_versions

            _logger.debug(f"output directory: {directory}")
            for name, section_versions in sections.items():
                sectionfile_name = os.path.join(directory, f"{name}.txt")
                with open(sectionfile_name, "w", encoding="utf-8") as out_f:
                    for i, section in enumerate(section_versions):
                        _logger.info(f"saving section '{name}' version {i}")
                        out_f.write(coalesce_lines(section))
                        out_f.write(os.linesep)
            
    def report(self):
        """
        report [-h] [-s] mlox_file
        
        positional arguments:
          mlox_file       rule file to examine
        
        optional arguments:
          -h, --help      show this help message and exit
          -s, --sections  print file sections in the order they appear
          
        Returns
        -------
        None.

        """

    
    def run(self):
        """
        Runs commands specified in args to MloxRuleManager(args).

        Returns
        -------
        None.

        """
        _logger.debug(f"args: {self.args}")
        subcommand = self.args.subcommand
        if hasattr(self, subcommand):
            getattr(self, subcommand)()
        else:
            _logger.info("I don't have that subcommand")


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Mlox rule-file management commands"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="mlox_rule_mgr {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    subparsers = parser.add_subparsers(
        title = "subcommands",
        dest = "subcommand",
        required = True,
    )
    
    merge_cmd = subparsers.add_parser(
        "merge",
        help = "merge mlox rule files"
    )
    merge_cmd.add_argument(
        "base_mlox_file",
        help = "target file to merge subsequent mlox rule files into"
    )
    merge_cmd.add_argument(
        "mlox_files",
        nargs = "+", help = "rule files to merge"
    )
    
    split_cmd = subparsers.add_parser(
        "split",
        help = "split an mlox rule file"
    )
    split_cmd.add_argument(
        "mlox_file",
        help = "rule file to split"
    )
    split_cmd.add_argument(
        "-d", "--directory",
        help = "output directory"
    )
    
    report_cmd = subparsers.add_parser(
        "report",
        help = "examine and report an mlox rule file"
    )
    report_cmd.add_argument(
        "mlox_file",
        help = "rule file to examine"
    )
    report_cmd.add_argument(
        "-s", "--sections",
        action = 'store_true',
        help = "print file sections in the order they appear"
    )

    args = parser.parse_args()
    return args

def setup_logging(loglevel = None):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """
    Run MloxRuleManager(args) with parsed command-line args.

    Returns
    -------
    None.

    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    mlox_rule_mgr = MloxRuleManager(args)
    mlox_rule_mgr.run()


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()