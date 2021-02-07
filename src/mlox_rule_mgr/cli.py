# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 18:18:51 2021

@author: Kaben Nanlohy <kaben.nanlohy@gmail.com>
"""

import argparse
import contextlib
import json
import glob
import logging
import os
import re
import string
import sys

from mlox_rule_mgr import __version__

__author__ = "Kaben Nanlohy"
__copyright__ = "Kaben Nanlohy"

_logger = logging.getLogger(__name__)


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


@contextlib.contextmanager
def textfile_reader_factory(filename, encoding = "utf-8"):
    f = open(filename, 'r', encoding = encoding)
    try:
        yield f
    finally:
        f.close()


@contextlib.contextmanager
def textfile_writer_factory(filename, encoding = "utf-8"):
    f = open(filename, 'w', encoding = encoding)
    try:
        yield f
    finally:
        f.close()


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
        self.reader_factory = textfile_reader_factory
        self.writer_factory = textfile_writer_factory
        self.comment_regex = re.compile(r"\s*;+\s*")
        self.sectionname_regex = re.compile(r"\s*;+\s*@(.*)")
        self.section_name_regex_2 = re.compile(r"\s*;+\s*@(?P<mod_name>.*?)\s*(?: \[(?P<author>.*)\])")


    def parse_rulefile_1(self, reader):
        # TODO: Instead of collecting sections into dictionary, save to disk.
        sections = dict()

        # Create first "header" section.
        sectionname = "_header"
        section = list()
        comments = list()

        for line_num, line in enumerate(reader.readlines()):
            sectionname_match = self.sectionname_regex.match(line)
            comment_match = self.comment_regex.match(line)
            if sectionname_match:
                _logger.debug(f"{line_num}: sectionname: {sectionname_match}")
                _logger.debug(sectionname_match.groups())
                # Save existing section.
                #sections[sectionname] = section              
                section_versions = sections.get(sectionname, list())
                section_versions.append(section)
                sections[sectionname] = section_versions
                # TODO: Instead of collecting sections into dictionary,
                # save to disk at this point.
                # Create new section.
                sectionname = get_safe_filename(sectionname_match.group(1))
                _logger.debug(f"{line_num}: safe_sectionname: {sectionname}")
                # Add existing comment lines to start of section.
                section = comments
                comments = list()
                # Add section name to start of section.
                section.append(line)
            elif comment_match:
                _logger.debug(f"{line_num}: comment: {comment_match}")
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
        section_versions = sections.get(sectionname, list())
        section_versions.append(section)
        sections[sectionname] = section_versions
        
        return sections
        


    def parse_rulefile_2(self, reader):
        # TODO: Instead of collecting sections into dictionary, save to disk.
        section_dict = dict()

        # Create first "header" section.
        section_info = dict()
        section_info["line_number"] = 1
        section_info["mod_name"] = "_header"
        section_info["author"] = ""
        section_name = "_header"
        section_lines = list()
        comment_lines = list()

        for line_num, line in enumerate(reader.readlines()):
            # Since enumerations used zero-based indexing,
            # But file line numbers use one-based indexing,
            # we add 1 to line_num.
            #line_num += 1
            
            section_name_match = self.section_name_regex_2.match(line)
            comment_match = self.comment_regex.match(line)
            if section_name_match:
                # Save existing section.
                section_info["lines"] = section_lines
                section_versions = section_dict.get(section_name, list())
                section_versions.append(section_info)
                section_dict[section_name] = section_versions

                # TODO: Instead of collecting sections into dictionary,
                # save to disk at this point.
                # Create new section.
                _logger.debug("NEW SECTION")
                _logger.debug(f"{line_num}: section_name_match: {section_name_match}")
                section_info = dict()
                section_info["line_number"] = line_num

                section_name_groupdict = section_name_match.groupdict()
                _logger.debug(f"{line_num}: section_name_groupdict: {section_name_groupdict}")

                mod_name = section_name_groupdict["mod_name"]
                author = section_name_groupdict["author"]
                section_info["mod_name"] = mod_name
                section_info["author"] = author
                section_name = f"{mod_name} [{author}]"
                _logger.debug(f"{line_num}: mod_name: {mod_name}")
                _logger.debug(f"{line_num}: author: {author}")
                _logger.debug(f"{line_num}: section_name: {section_name}")

                # Add existing comment lines to start of new section.
                section_lines = comment_lines
                comment_lines = list()
                
                # Also add section name line to start of new section.
                section_lines.append(line)
                
            elif comment_match:
                _logger.debug(f"{line_num}: comment_match: {comment_match}")
                # Comment line might or might not be part of a new section,
                # but we need to read more lines to know which is the case,
                # so collect comment line, but don't add to section yet.
                comment_lines.append(line)
            else:
                # At this point we know we're not in a new section, so if
                # there are any stored comment lines, we can add them to the
                # the current section.
                section_lines.extend(comment_lines)
                comment_lines = list()
                # Add current line to section.
                section_lines.append(line)

        # Save final section.
        if comment_lines:
            section_lines.extend(comment_lines)
        section_info["lines"] = section_lines
        section_versions = section_dict.get(section_name, list())
        section_versions.append(section_info)
        section_dict[section_name] = section_versions
        
        return section_dict
        
    
    def parse_rulefile(self, reader):
        return self.parse_rulefile_2(reader)
        

    def merge_1(self):
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
    
    def split_1(self):
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

        # Try to read rulefile.
        with open(rulefile_name, "r", encoding="utf-8") as in_f:
            sections = self.parse_rulefile_1(in_f)

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
        rulefile_name = os.path.realpath(self.args.mlox_file)
        with self.reader_factory(rulefile_name, encoding="utf-8") as in_f:
            section_dict = self.parse_rulefile(in_f)
            header_versions = section_dict.pop("_header", None)
            header_content = "".join(["".join(version["lines"]) for version in header_versions])
                        
            if (not header_content) and (len(section_dict) == 0):
                print(f"{self.args.mlox_file} is empty.")
                return

            num_sections = 0
            duplicate_sections = dict()
            section_line_nums = []
            for name, versions in section_dict.items():
                num_versions = len(versions)
                num_sections += num_versions
                if num_versions > 1:
                    duplicate_sections[name] = versions
                for version in versions:
                    section_line_nums.append((name, version["line_number"]))

            print(f"{self.args.mlox_file} report:")
            print("\tHeader: ", end='')
            print(header_content and 'Yes' or 'No')
            print(f"\t{num_sections} Mod Section", end='')
            print((num_sections != 1) and 's' or '')
            
            if (num_sections == 0):
                return            
            
            section_line_nums_sorted_by_name = section_line_nums.copy()
            section_line_nums_sorted_by_line = section_line_nums.copy()
            section_line_nums_sorted_by_name.sort(key = lambda entry: entry[0])
            section_line_nums_sorted_by_line.sort(key = lambda entry: entry[1])
            sections_sorted_by_name = [entry[0] for entry in section_line_nums_sorted_by_name]
            sections_sorted_by_line = [entry[0] for entry in section_line_nums_sorted_by_line]
            print("\tSections Sorted: ", end='')
            print((sections_sorted_by_name == sections_sorted_by_line) and 'Yes' or 'No')

            num_dup_sections = len(duplicate_sections)
            if (num_dup_sections == 0):
                print("\t0 Duplicate Section Names")
            else:
                if (num_dup_sections == 1):
                    print("\t1 Duplicate Section Name:")
                else:
                    print(f"\t{num_dup_sections} Duplicate Section Names:")
                for name, versions in duplicate_sections.items():
                    _logger.debug(f"report: duplicate_section: name {name}, versions {versions}")
                    line_number_list = ", ".join(f"line {version['line_number']}" for version in versions)
                    print(f"\t\t{name}: {line_number_list}")

            if self.args.sections:
                print()
                print("\tSections found:")
                for entry in sections_sorted_by_line:
                    print(f"\t\t{entry}")

    
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
        help = "merge mlox rule files",
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
        help = "examine and report an mlox rule file",
        description = """
The report command will look at an mlox-formatted file and give you warnings and stats:

- (info) whether the file has a header
- (info) number of mod sections found
- (info) whether the mod sections are sorted alphabetically
- (warning) number, names, and line numbers of mod sections with the same name

If the --sections option is specified, the sections in the file will be printed in the order they appear.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
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

    args = parser.parse_args(args)
    return args

def setup_logging(loglevel = None):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    if loglevel is None:
        loglevel = logging.INFO
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
    rule_mgr = MloxRuleManager(args)
    rule_mgr.run()


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
