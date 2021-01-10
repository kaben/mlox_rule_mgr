# -*- coding: utf-8 -*-

import json, os, sys

import pytest

from mlox_rule_mgr import cli

__author__ = "Kaben Nanlohy"
__copyright__ = "Kaben Nanlohy"


this_dir = os.path.dirname(os.path.realpath(__file__))
testfile_dir = os.path.abspath(os.path.join(this_dir, '..', 'specs', 'testfiles'))


def dump_sections(sections):
    section_keys = list(sections.keys())
    print('expected_section_names = [')
    for key in section_keys:
        print(f"    {json.dumps(key)},")
    print("]")

    section_values = list(sections.values())
    coalesced_sections = [["".join(lines) for lines in entry] for entry in section_values]
    print('expected_sections = [')
    for section in coalesced_sections:
        print("    [")
        for entry in section:
            print(f"        {json.dumps(entry)},")
        print("    ],")
    print("]")


def test_MloxRuleManager_parse():
    args = ["report", ""]
    rule_mgr = cli.MloxRuleManager(args)

    report_test_fnam = os.path.join(testfile_dir, "report_tester.txt")
    with open(report_test_fnam, 'r', encoding = 'utf-8') as report_test_f:
        sections = rule_mgr.parse_rulefile(report_test_f)
    
    dump_sections(sections)
    #assert False
    
    expected_section_names = [
        "_header",
        "mod2author2",
        "abcmodauthor1",
        "uniquemodauthor3",
        "mod2otherauthor",
    ]
    expected_sections = [
        [
            ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n; Oops I am unorganized\n;;;;;;;;;\n\n[NearFirst]\n\tEverything should overwrite this but I can't be bothered to put it in the right section.\nabc_mod.esp\n\n",
        ],
        [
            ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n; @mod2 [author2]\n\n[CONFLICT]\n\tOnly use one.\nabc_mod.esp\nmod2.esp\n\n",
            ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n;; @mod2   [author2]\n\n[ORDER]\nmod2.esp\nmod1.esp\n\n",
        ],
        [
            ";;;;;;;;;;;;;;;\n;; @abc_mod [author1]\n\n[Order]\nabc_mod.esp\nmod3.esp\n\n[Patch]\nabc_mod.esp\nabc_mod_v2_patch.esp\n\n",
            ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n;;@abc_mod [author1]\n\n; I guess I copypasted this from somewhere and didn't merge properly\n[Order]\nabc_mod.esp\ncool_new_mod.esp\n\n",
        ],
        [
            ";;;;;;;;;;;;;;;;;;;;\n;;; @unique_mod [author3]\n\n[Order]\nfun_mod.esp\nunique_mod.esp\n\n[Requires]\nunique_fun_mod.esp\n[ALL fun_mod.esp\n     unique_mod.esp]\n\t \n\n",
        ],
        [
            ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n;; @mod2 [otherauthor]\n\n[Order]\nunique_mod.esp\notherauthor's mod2.esp\n",
        ],
    ]

    section_names = list(sections.keys())
    section_values = list(sections.values())
    coalesced_sections = [["".join(lines) for lines in entry] for entry in section_values]
    
    assert section_names == expected_section_names
    assert coalesced_sections == expected_sections
