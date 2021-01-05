# Test cases : **`merge`** #

The `merge` is useful for:

1. combining one or many downloaded mlox files with your own mlox_user.txt
1. combining mlox files into a single file sorted by section / mod name (`-sorted`)
1. checking whether your combined file will have duplicate sections with the same mod name (`-report`)
1. checking whether your combined sorted file will leave headers from the original files mixed into your sections (`-report -sorted`)

Merging is the main functionality of the mlox_rule_mgr command line tool.

Note: In the case of duplicate sections or abandoned headers, the selected merge happens only with user approval.

Behavior specification:

## No file given, any options ##

`> mlox_rule_mgr merge`
`> mlox_rule_mgr merge -sorted`
`> mlox_rule_mgr merge -report`
`> mlox_rule_mgr merge -sorted -report`

Expected output:

```
Usage: mlox_rule_mgr merge [-sorted] [-report] mlox_base_file mlox_file1 mlox_file2...

The merge command will merge all subsequent mlox rule files into the first rule file.

Flags:
  -sorted (default: false) When this flag is false, each new file is appended to the old file. When it is true, sections from the new file are inserted into the old file in alphabetical order. If necessary, the old file will be sorted before merging.
  -report (default: false) With this flag, the files are **not** merged. Instead, a report about what the result of the merge _would_ be is printed.

If merging would cause duplicate-named sections to be created, or if it would cause header information from the merged files to be misplaced, merging will not proceed without telling you about possible problems and asking for permission to proceed.
```

Note: specs do not care whether -sorted and -report are strictly ordered or not, but the usage documentation should reflect whatever decision is made.

## One file given, any options ##

`> mlox_rule_mgr merge unsorted_base_file.txt`
`> mlox_rule_mgr merge -sorted unsorted_base_file.txt`
`> mlox_rule_mgr merge -report unsorted_base_file.txt`
`> mlox_rule_mgr merge -sorted -report unsorted_base_file.txt`

Expected output:

```
You must merge at least two files.
```

## Two files given, no flags ##

### No duplicate section names ###

### Duplicate section names across files ###

### Duplicate section names within a file ###


## Two files given, `-sorted` ##

### Both files already sorted, no headers ###

### Both files already sorted, only base has header ###

### Both files already sorted, only merged-in file has header ###

### Both files already sorted, both files have headers ###

### Base file sorted, merged-in file unsorted ###

### Base file unsorted, merged-in file sorted ###

### Both files unsorted ###


## Two files given, `-report` ##

### No duplicate section names ###

### Duplicate section names across files ###

### Duplicate section names within a file ###


## Two files given, `-sorted -report` ##

### Both files already sorted, no headers, no duplicate sections ###

### Both files already sorted, no headers, duplicate sections across files ###

### Both files already sorted, no headers, duplicate sections within files ###

### Both files already sorted, only merged-in file has header, no duplicate sections ###

### Both files already sorted, only merged-in file has header, duplicate sections across files ###

### Both files already sorted, only merged-in file has header, duplicate sections within files ###

### Both files unsorted, only merged-in file has header, duplicate sections across files ###

## More than two files given, no options ##

## More than two files given, `-sorted` ##

## More than two files given, `-report` ##

## More than two files given, `-sorted -report` ##
