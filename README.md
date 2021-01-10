=============
mlox_rule_mgr
=============


Tool to make Mlox (Morrowind Load Expert) rule files easier to generate and manage.


Description
===========

Provides the following commands:

- `merge`:  merge all subsequent mlox rule files into the first rule file.

    Flags:
      `--sorted` (default: false) When this flag is false, each new file is appended to the old file. When it is true, sections from the new file are inserted into the old file in alphabetical order. If necessary, the old file will be sorted before merging.
      `--report` (default: false) With this flag, the files are **not** merged. Instead, a report about what the result of the merge _would_ be is printed.
    
    If merging would cause duplicate-named sections to be created, or if it would cause header information from the merged files to be misplaced, merging will not proceed without telling you about possible problems and asking for permission to proceed.

    Useful for:
    1. combining one or many downloaded mlox files with your own mlox_user.txt
    1. combining mlox files into a single file sorted by section / mod name (`--sorted`)
    1. checking whether your combined file will have duplicate sections with the same mod name (`--report`)
    1. checking whether your combined sorted file will leave headers from the original files mixed into your sections (`--report --sorted`)
    
    Merging is the main functionality of the mlox_rule_mgr command line tool.
    
    Note: In the case of duplicate sections or abandoned headers, the selected merge happens only with user approval.- `split`: split Mlox rule file by section into individual files names after each section

- `split`: split Mlox rule file by section into individual files names after each section.

- `report`: look at an mlox-formatted file and give you warnings and stats:
    - (info) whether the file has a header
    - (info) number of mod sections found
    - (info) whether the mod sections are sorted alphabetically
    - (warning) number, names, and line numbers of mod sections with the same name
    
    If the `--sections` option is specified, the sections in the file will be printed in the order they appear.

    Useful for:
    1. debugging mlox_rule_mgr's parsing
    1. checking an mlox file before distribution
    1. checking an mlox file you have downloaded
    
    It is relatively advanced functionality; we do not expect that most users will bother.
    
    (Future expansion could include syntax checking, but that is currently neither **in scope** nor **spec'd**.)


Dev Setup
========

- Install Anaconda
- Create dev environment: `conda create -n mlox_rule_mgr python=3.8.5 anaconda`
- Activate dev environment: `conda activate mlox_rule_mgr`
- Install Git command: `conda install git`
- Git-clone this project: `git clone https://github.com/kaben/mlox_rule_mgr.git`
- Install in in-place dev mode: `cd mlox_rule_mgr; pip install -e .`
- Run Mlox Rule Manager: `mlox_rule_mgr --help`

Testing:

- Install pytest: `conda install pytest`
- Install pytest-cov: `conda install pytest-cov`
- Run tests: `pytest`


Note
====

This project has been set up using PyScaffold 3.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
