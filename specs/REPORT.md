# Test cases: `report` #

The `report` command is useful for:

1. debugging mlox_rule_mgr's parsing
1. checking an mlox file before distribution
1. checking an mlox file you have downloaded

It is relatively advanced functionality; we do not expect that most users will bother.

(Future expansion could include syntax checking, but that is currently neither **in scope** nor **spec'd**.)

Behavior Specification:

## No file given ##

`> mlox_rule_mgr report`

Expected output:

```
Usage: mlox_rule_mgr report [-sections] mlox_file

The report command will look at an mlox-formatted file and give you warnings and stats:
- (info) whether the file has a header
- (info) number of mod sections found
- (info) whether the mod sections are sorted alphabetically
- (warning) number, names, and line numbers of mod sections with the same name

If the -sections option is specified, the sections in the file will be printed in the order they appear.
```

## Empty file ##

`> mlox_rule_mgr report empty.txt`

Expected output:

```
<filename> is empty.
```

## Empty file with `-sections` ##

`> mlox_rule_mgr report -sections empty.txt`

Expected output:

```
<filename> is empty.
```

## File without sections :( ##

`> mlox_rule_mgr report loose_rules.txt`

Expected output:

```
<filename> report:
	Header: Yes
	0 Mod Sections
```
	
## File without sections, `-sections` ##
(see file without sections)

## File with one section, no header ##

`> mlox_rule_mgr report single_section.txt`

Expected output:

```
<filename> report:
	Header: No
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names
```
	
## File with 1 section, no header, `-sections` ##

`> mlox_rule_mgr report -sections single_section.txt`

Expected output:

```
<filename> report:
	Header: No
	1 Mod Section
	Sections Sorted: Yes
	0 Sections for the same Plugin
	
	Sections found:
		mod1 [author1]
```
		
## File with header and 1 section ##

`> mlox_rule_mgr report single_section_with_header.txt`

Expected output:

```
<filename> report:
	Header: Yes
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names
```
	
## File with header and 1 section, `-sections` ##

`> mlox_rule_mgr report -sections single_section_with_header.txt`

Expected output:

```
<filename> report:
	Header: Yes
	1 Mod Section
	Sections Sorted: Yes
	0 Duplicate Section Names
	
	Sections found:
		mod1 [author1]
```
		
## File with header and 1 section (with rules in it) ##

`> mlox_rule_mgr report single_section_with_ruleheader.txt`

Expected output: same as header without rules
	
## File with header and 1 section (with rules in it), `-sections` ##

`> mlox_rule_mgr report -sections single_section_with_ruleheader.txt`

Expected output: same as header without rules

## File with multiple (unique) sections, unsorted ##

`> mlox_rule_mgr report unique_unsorted_sections.txt`

Expected output:

```
<filename> report:
	Header: No
	2 Mod Sections
	Sections Sorted: No
	0 Duplicate Section Names
```
	
## File with multiple (unique) sections, unsorted, `-sections` ##

`> mlox_rule_mgr report -sections unique_unsorted_sections.txt`

Expected output:

```
<filename> report:
	Header: No
	2 Mod Sections
	Sections Sorted: No
	0 Duplicate Section Names

	Sections found:
		mod1 [author1]
		abc_mod [author2]
```

## File with multiple (unique) sections, sorted ##

`> mlox_rule_mgr report unique_sorted_sections.txt`

Expected output:

```
<filename> report:
	Header: No
	2 Mod Sections
	Sections Sorted: Yes
	0 Duplicate Section Names
```
	
## File with multiple (unique) sections, sorted, `-sections` ##

`> mlox_rule_mgr report -sections unique_sorted_sections.txt`

Expected output:

```
<filename> report:
	Header: No
	2 Mod Sections
	Sections Sorted: Yes
	0 Duplicate Section Names
	
	Sections found:
		abc_mod [author2]
		mod1 [author1]
```
		
## File with duplicate section-names ##

`> mlox_rule_mgr report duplicate_sections.txt`

Expected output:

```
<filename> report:
	Header: No
	2 Mod Sections
	Sections Sorted: Yes
	1 Duplicate Section Name:
		mod2 [author2]: line 1, line 9
```
		
## File with duplicate section-names, `-sections` ##

`> mlox_rule_mgr report -sections duplicate_sections.txt`

Expected output:

```
<filename> report:
	Header: No
	2 Mod Sections
	Sections Sorted: Yes
	1 Duplicate Section Name:
		mod2 [author2]: line 1, line 9
		
	Sections found:
		mod2 [author2]
		mod2 [author2]
```
		
## Combined test case ##

`> mlox_rule_mgr report -sections report_tester.txt`

Expected output:

```
<filename> report:
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
```


## SCOPE EXPANSION: `-modlist` ##
This scope expansion is not fully spec'd out.

### No file given ###

`> mlox_rule_mgr report`

Expected output: As originally specified, with this addition:

```If the -modlist option is specified, it will also print a full list of the plugin names it has found.```

### No file given -modlist ###
As originally specified.

### File without sections -modlist ###

`> mlox_rule_mgr -modlist loose_rules.txt`

Expected Output:

```
<filename> report:
	Header: Yes
	0 Mod Sections

	.esp files:
		mod1.esp
		mod2.esp
		mod3.esp
```
		
Note: spec does not care if .esp files are alpha-sorted or just in the order they're encountered.
