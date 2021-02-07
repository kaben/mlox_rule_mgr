# -*- coding: utf-8 -*-

import json, os, sys

import pytest

from mlox_rule_mgr import cli

__author__ = "Kaben Nanlohy"
__copyright__ = "Kaben Nanlohy"


this_dir = os.path.dirname(os.path.realpath(__file__))
testfile_dir = os.path.abspath(os.path.join(this_dir, '..', 'specs', 'testfiles'))


def test_MloxRuleManager_parse_rulefile_1():
    args = []
    rule_mgr = cli.MloxRuleManager(args)

    report_tester_fnam = os.path.join(testfile_dir, "report_tester.txt")
    with open(report_tester_fnam, 'r', encoding = 'utf-8') as report_tester_f:
        sections = rule_mgr.parse_rulefile_1(report_tester_f)
    
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



def test_MloxRuleManager_parse_rulefile():
    args = []
    rule_mgr = cli.MloxRuleManager(args)

    report_tester_fnam = os.path.join(testfile_dir, "report_tester.txt")
    with open(report_tester_fnam, 'r', encoding = 'utf-8') as report_tester_f:
        section_dict = rule_mgr.parse_rulefile(report_tester_f)
    
    #print(json.dumps(section_dict, indent = 4))
    expected_section_dict = {
        "_header": [
            {
                "line_number": 1,
                "mod_name": "_header",
                "author": "",
                "lines": [
                    ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n",
                    "; Oops I am unorganized\n",
                    ";;;;;;;;;\n",
                    "\n",
                    "[NearFirst]\n",
                    "\tEverything should overwrite this but I can't be bothered to put it in the right section.\n",
                    "abc_mod.esp\n",
                    "\n"
                ]
            }
        ],
        "mod2 [author2]": [
            {
                "line_number": 9,
                "mod_name": "mod2",
                "author": "author2",
                "lines": [
                    ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n",
                    "; @mod2 [author2]\n",
                    "\n",
                    "[CONFLICT]\n",
                    "\tOnly use one.\n",
                    "abc_mod.esp\n",
                    "mod2.esp\n",
                    "\n"
                ]
            },
            {
                "line_number": 49,
                "mod_name": "mod2",
                "author": "author2",
                "lines": [
                    ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n",
                    ";; @mod2   [author2]\n",
                    "\n",
                    "[ORDER]\n",
                    "mod2.esp\n",
                    "mod1.esp\n",
                    "\n"
                ]
            }
        ],
        "abc_mod [author1]": [
            {
                "line_number": 17,
                "mod_name": "abc_mod",
                "author": "author1",
                "lines": [
                    ";;;;;;;;;;;;;;;\n",
                    ";; @abc_mod [author1]\n",
                    "\n",
                    "[Order]\n",
                    "abc_mod.esp\n",
                    "mod3.esp\n",
                    "\n",
                    "[Patch]\n",
                    "abc_mod.esp\n",
                    "abc_mod_v2_patch.esp\n",
                    "\n"
                ]
            },
            {
                "line_number": 28,
                "mod_name": "abc_mod",
                "author": "author1",
                "lines": [
                    ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n",
                    ";;@abc_mod [author1]\n",
                    "\n",
                    "; I guess I copypasted this from somewhere and didn't merge properly\n",
                    "[Order]\n",
                    "abc_mod.esp\n",
                    "cool_new_mod.esp\n",
                    "\n"
                ]
            }
        ],
        "unique_mod [author3]": [
            {
                "line_number": 36,
                "mod_name": "unique_mod",
                "author": "author3",
                "lines": [
                    ";;;;;;;;;;;;;;;;;;;;\n",
                    ";;; @unique_mod [author3]\n",
                    "\n",
                    "[Order]\n",
                    "fun_mod.esp\n",
                    "unique_mod.esp\n",
                    "\n",
                    "[Requires]\n",
                    "unique_fun_mod.esp\n",
                    "[ALL fun_mod.esp\n",
                    "     unique_mod.esp]\n",
                    "\t \n",
                    "\n"
                ]
            }
        ],
        "mod2 [otherauthor]": [
            {
                "line_number": 56,
                "mod_name": "mod2",
                "author": "otherauthor",
                "lines": [
                    ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n",
                    ";; @mod2 [otherauthor]\n",
                    "\n",
                    "[Order]\n",
                    "unique_mod.esp\n",
                    "otherauthor's mod2.esp\n"
                ]
            }
        ]
    }
    
    assert section_dict == expected_section_dict


def test_MloxRuleManager_report_emptyFile(capsys):
    testfile_path = os.path.join(testfile_dir, "empty.txt")
    cli.main(args = ["report", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} is empty.
""".strip()


def test_MloxRuleManager_report_emptyFile_withSectionsFlag(capsys):
    testfile_path = os.path.join(testfile_dir, "empty.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    captured = capsys.readouterr()
    assert captured.out.strip() == f"""
{testfile_path} is empty.
""".strip()


def test_MloxRuleManager_report_withoutSections(capsys):
    testfile_path = os.path.join(testfile_dir, "loose_rules.txt")
    cli.main(args = ["report", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: Yes
	0 Mod Sections
""".strip()


def test_MloxRuleManager_report_withoutSections_withSectionsFlag(capsys):
    testfile_path = os.path.join(testfile_dir, "loose_rules.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: Yes
	0 Mod Sections
""".strip()


def test_MloxRuleManager_report_singleSection_noHeader(capsys):
    testfile_path = os.path.join(testfile_dir, "single_section.txt")
    cli.main(args = ["report", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: No
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names
""".strip()


def test_MloxRuleManager_report_singleSection_noHeader_withSectionsFlag(capsys):
    testfile_path = os.path.join(testfile_dir, "single_section.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: No
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names

	Sections found:
		mod1 [author1]
""".strip()


def test_MloxRuleManager_report_header_singleSection(capsys):
    testfile_path = os.path.join(testfile_dir, "single_section_with_header.txt")
    cli.main(args = ["report", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: Yes
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names
""".strip()


def test_MloxRuleManager_report_header_singleSection_withSectionsFlag(capsys):
    testfile_path = os.path.join(testfile_dir, "single_section_with_header.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: Yes
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names

	Sections found:
		mod1 [author1]
""".strip()


def test_MloxRuleManager_report_ruleHeader_singleSection(capsys):
    testfile_path = os.path.join(testfile_dir, "single_section_with_ruleheader.txt")
    cli.main(args = ["report", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: Yes
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names
""".strip()


def test_MloxRuleManager_report_ruleHeader_singleSection_withSectionsFlag(capsys):
    testfile_path = os.path.join(testfile_dir, "single_section_with_ruleheader.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: Yes
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names

	Sections found:
		mod1 [author1]
""".strip()


def test_MloxRuleManager_report_multipleUniqueSections_unsorted(capsys):
    testfile_path = os.path.join(testfile_dir, "unique_unsorted_sections.txt")
    cli.main(args = ["report", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: No
	2 Mod Sections
	Sections Sorted: No
	0 Duplicate Section Names
""".strip()


def test_MloxRuleManager_report_multipleUniqueSections_unsorted_withSectionsFlag(capsys):
    testfile_path = os.path.join(testfile_dir, "unique_unsorted_sections.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: No
	2 Mod Sections
	Sections Sorted: No
	0 Duplicate Section Names

	Sections found:
		mod1 [author1]
		abc_mod [author2]
""".strip()


def test_MloxRuleManager_report_multipleUniqueSections_sorted(capsys):
    testfile_path = os.path.join(testfile_dir, "unique_sorted_sections.txt")
    cli.main(args = ["report", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: No
	2 Mod Sections
	Sections Sorted: Yes
	0 Duplicate Section Names
""".strip()


def test_MloxRuleManager_report_multipleUniqueSections_sorted_withSectionsFlag(capsys):
    testfile_path = os.path.join(testfile_dir, "unique_sorted_sections.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: No
	2 Mod Sections
	Sections Sorted: Yes
	0 Duplicate Section Names

	Sections found:
		abc_mod [author2]
		mod1 [author1]
""".strip()


def test_MloxRuleManager_report_duplicateSectionNames(capsys):
    testfile_path = os.path.join(testfile_dir, "duplicate_sections.txt")
    cli.main(args = ["report", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: No
	2 Mod Sections
	Sections Sorted: Yes
	1 Duplicate Section Name:
		mod2 [author2]: line 1, line 9
""".strip()


def test_MloxRuleManager_report_duplicateSectionNames_withSectionsFlag(capsys):
    testfile_path = os.path.join(testfile_dir, "duplicate_sections.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: No
	2 Mod Sections
	Sections Sorted: Yes
	1 Duplicate Section Name:
		mod2 [author2]: line 1, line 9

	Sections found:
		mod2 [author2]
		mod2 [author2]
""".strip()


def test_MloxRuleManager_report_combined(capsys):
    testfile_path = os.path.join(testfile_dir, "report_tester.txt")
    cli.main(args = ["report", "--sections", testfile_path])
    assert capsys.readouterr().out.strip() == f"""
{testfile_path} report:
	Header: Yes
	6 Mod Sections
	Sections Sorted: No
	2 Duplicate Section Names:
		mod2 [author2]: line 9, line 49
		abc_mod [author1]: line 17, line 28

	Sections found:
		mod2 [author2]
		abc_mod [author1]
		abc_mod [author1]
		unique_mod [author3]
		mod2 [author2]
		mod2 [otherauthor]
""".strip()
