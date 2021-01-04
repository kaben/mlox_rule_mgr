# Definitions #

## Header ##
`Comments` and `rules` at the beginning of the file.

**Starts:** start of file

**Ends:** when the first `section` starts

Note: In the future we may wish to define this only as the initial `comments`, but for now it includes loose `rules`, with or without `comments`.

## Comment ##
Any line starting with a semicolon (but please see MLOX parser for certainty).

## Section ##
A convention for grouping rules about the same plugin; see MLOX rule submission guidelines or the header of mlox_base.txt.

**Starts:** two lines of this format:

1. comment characters only
2. comment characters, optional whitespace, @ symbol, text

**Ends:** when the next `section` start is detected, alas.

Sections may contain any combination of `comments`, whitespace, and `rules`.

## Rule ##
See MLOX parser. However, since some rule types (ORDER) do not accept info lines, it may be useful for us to recognize both "strict rules", i.e.

```
[RULE]
rulestuff
```

and "commented rules", i.e.
```
;rulecomment with no empty lines after it
[RULE]
rulestuff
```

